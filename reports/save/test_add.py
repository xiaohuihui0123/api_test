"""
北京-漠雪殇-27
"""
import unittest
from library.myddt import ddt,data
from common.handle_excel import Excel_Hande
from common.heandle_path import DATA_DIR
import os
from common.handle_config import conf
from requests import request
import jsonpath
from common.handle_mysql import HandleMysql
from common.handle_logging import log
from common.handel_replace import replace_data,EnvData

@ddt
class Add(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'add')
    case = exce.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')

        }
        headers = eval(conf.get('env','headers'))
        respones = request(url=url,method='post',json=data,headers=headers)
        res = respones.json()
        token = 'Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
        member_id = str(jsonpath.jsonpath(res,'$..id')[0])
        setattr(EnvData,'token',token)
        setattr(EnvData,'member_id',member_id)


    @data(*case)
    def test_add(self,cas):
        url = conf.get('env','url') + cas['url']
        method = cas['method']
        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        #查询添加项目之前的标的数量
        if cas['check_sql']:
            sql = replace_data(cas['check_sql'])
            f = self.bb.find_count(sql)

        respones = request(url=url,method=method,json=data,headers=headers)
        res = respones.json()
        print('预期结果：',expected)
        print('实际结果：',res)

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            #查询加标后标的数量
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                q = self.bb.find_count(sql)
                self.assertEqual(1,q-f)

        except AssertionError as e:
            log.error('该用例{}错误'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('该用例{}通过'.format('通过'))
            self.exce.write(row=row,column=8,value='通过')