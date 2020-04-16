"""
北京-漠雪殇-27
"""
import unittest
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.handle_config import conf
from common.heandle_path import DATA_DIR
from common.handel_replace import EnvData,replace_data
import os
from common.handle_mysql import HandleMysql
from requests import request
from common.handle_logging import log
import jsonpath
import decimal

@ddt
class Withdraw(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'withdraw')
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
        re = respones.json()
        token = 'Bearer' + " " + jsonpath.jsonpath(re,'$..token')[0]
        member_id = str(jsonpath.jsonpath(re,'$..id')[0])
        setattr(EnvData,'token',token)
        setattr(EnvData,'member_id',member_id)

    @data(*case)
    def test_withdraw(self,cas):
        url = conf.get('env','url') + cas['url']
        method = cas['method']
        #替换用例中中的#member_id#
        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        #查询取现之前的金额
        if cas['check_sql']:
            sql = replace_data(cas['check_sql'])
            money_start = self.bb.find_one(sql)['leave_amount']

        respons = request(url=url,method=method,json=data,headers=headers)
        res = respons.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            #查询取现之后账户的金额
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                money_end = self.bb.find_one(sql)['leave_amount']
                #将用例数据的金额数值类型转换为decimal
                f = decimal.Decimal(str(data['amount']))
                self.assertEqual(f,money_start-money_end)
        except AssertionError as e:
            log.error('该用例{}未通过'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('该用例{}通过'.format(cas['title']))
            self.exce.write(row=row,column=8,value='不通过')
