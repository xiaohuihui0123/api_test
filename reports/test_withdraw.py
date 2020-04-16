"""
北京-漠雪殇-27
"""
import unittest

from common.handle_excel import Excel_Hande
from common.handle_config import conf
from common.heandle_path import DATA_DIR
import os
from library.myddt import ddt, data
from requests import request
import jsonpath
from common.handle_mysql import HandleMysql
import decimal
from common.handle_logging import log

@ddt
class Withdraw(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'withdraw')
    case = excel.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls):
        # 准备的登录的数据
        url = conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone': conf.get('test_data', 'phone'),
            'pwd': conf.get('test_data', 'pwd')

        }
        headers = eval(conf.get('env','headers'))
        respons = request(url=url,method='post',json=data,headers=headers)
        re = respons.json()
        cls.member_id = jsonpath.jsonpath(re,'$..id')[0]
        cls.token = "Bearer" + " " + jsonpath.jsonpath(re,'$..token')[0]


    @data(*case)
    def test_withdraw(self,cas):

        # 准备用例数据
        url = conf.get('env','url') + cas['url']
        cas['data'] = cas['data'].replace('#member_id#',str(self.member_id))
        data = eval(cas['data'])

        method = cas['method']
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = self.token
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1


        # 查询取现之前的余额
        if cas['check_sql']:
            sql = cas['check_sql'].format(self.member_id)
            start_money = self.bb.find_one(sql)['leave_amount']
            print('取现前：',start_money)
        # 发送请求
        response1 = request(method=method,url=url,headers=headers,json=data)
        res = response1.json()
        print('实际结果：',res)
        print('预期结果：', expected)
        # 断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            # 查询请求之后的账户余额
            if cas['check_sql']:
                sql = cas['check_sql'].format(self.member_id)
                end_money = self.bb.find_one(sql)['leave_amount']
                print('取现后：',end_money)
                # 用例数据中data，amount的数值类型转换
                my_data = decimal.Decimal(str(data['amount']))


                self.assertEqual(my_data,start_money-end_money)
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
