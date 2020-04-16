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
class Update(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'update')
    case = exce.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls) -> None:
        url =  conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')
        }
        headers = eval(conf.get('env','headers'))
        respones2 = request(url=url,method='post',json=data,headers=headers)
        res2 = respones2.json()
        token = 'Bearer' ' ' + jsonpath.jsonpath(res2,'$..token')[0]
        member_id = str(jsonpath.jsonpath(res2,'$..id')[0])
        setattr(EnvData,'token',token)
        setattr(EnvData,'member_id',member_id)


    @data(*case)
    def test_update(self,cas):

        url = conf.get('env','url') + cas['url']
        method = cas['method']
        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=method,json=data,headers=headers)
        res = respones.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            #判断数据库中是否更新昵称
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                s = self.bb.find_one(sql)['reg_name']
                self.assertEqual(data['reg_name'],s)

        except AssertionError as e:
            log.error('该用例{}报错'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('该用例{}通过'.format(cas['title']))
            self.exce.write(row=row, column=8, value='通过')
