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
class Recharge(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'recharge')
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
        reepons = request(url=url,method='post',json=data,headers=headers)
        res = reepons.json()
        token ='Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
        member_id = str(jsonpath.jsonpath(res,'$..id')[0])
        setattr(EnvData,'token',token)
        setattr(EnvData,'member_id',member_id)

    @data(*case)
    def test_recharge(self,cas):
        url = conf.get('env','url') + cas['url']
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1
        #替换用例中的数据
        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        #查询充值之前的账户金额
        if cas['check_sql']:
            sql = replace_data(cas['check_sql'])
            money_start = self.bb.find_one(sql)['leave_amount']

        response = request(url=url,method=method,json=data,headers=headers)
        res1 = response.json()

        try:
            self.assertEqual(expected['code'],res1['code'])
            self.assertEqual(expected['msg'],res1['msg'])
            #查询充值后的账户金额
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                money_end = self.bb.find_one(sql)['leave_amount']
                #将用例数据中的金额值类型转换，因为数据库中的数据类型是decimal
                s = decimal.Decimal(str(data['amount']))
                self.assertEqual(s,money_end-money_start)
        except AssertionError as e:
            log.error('这条用例{}没有通过'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('这条用例{}执行通过'.format(cas['title']))
            self.exce.write(row=row,column=8,value='通过')

