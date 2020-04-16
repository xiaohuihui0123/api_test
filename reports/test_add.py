"""
北京-漠雪殇-27
"""

import unittest
from common.handle_excel import Excel_Hande
from common.heandle_path import DATA_DIR
from common.handle_config import conf
import os
from library.myddt import ddt,data
from requests import request
import jsonpath
from common.handle_mysql import HandleMysql
from common.handle_logging import log
from common.handel_replace import EnvData,replace_data



@ddt
class AddTest(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'add')
    case = excel.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls):
        # 准备登录用的数据
        url = conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')

        }
        headers = eval(conf.get('env','headers'))
        respons = request(method='post',url=url,json=data,headers=headers)
        re = respons.json()
        member_id = str(jsonpath.jsonpath(re,'$..id')[0])
        token = "Bearer" + " " + jsonpath.jsonpath(re,'$..token')[0]
        setattr(EnvData,'member_id',member_id)
        setattr(EnvData,'token',token)

    @data(*case)
    def test_add(self,cas):
        # 准备用例数据
        url = conf.get('env','url') + cas['url']
        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1
        # 请求之前查询用户标的数量
        if cas['check_sql']:
            sql = replace_data(cas['check_sql'])
            st = self.bb.find_count(sql)
            print('请求之前的标数：',st)



        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()

        print('预期结果：',expected)
        print('实际结果：',res)
        # 请求后查询用户标的数量
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                end = self.bb.find_count(sql)
                print('请求之后标数', end)
                self.assertEqual(1,end-st)
        except AssertionError as e:
            log.error('用例--{}--未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}：'.format(res))
            log.exception(e)
            self.excel.write(row=row,column=8,value='不通过')

            raise e
        else:
            log.info('用例--{}--通过'.format(cas['title']))
            self.excel.write(row=row,column=8,value='通过')



