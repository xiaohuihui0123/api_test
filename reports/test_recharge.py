"""
北京-漠雪殇-27
"""
import unittest
from ddt import ddt,data
from common.handle_excel import Excel_Hande
from common.heandle_path import DATA_DIR
import os
from common.handle_config import conf
from requests import request
import jsonpath
from common.handle_mysql import HandleMysql
import decimal
from common.handle_logging import log



fms = os.path.join(DATA_DIR,'apicases.xlsx')
@ddt
class Recharge_Case(unittest.TestCase):
    excel = Excel_Hande(fms,'recharge')
    case_data = excel.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls):
        url = conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')
        }
        headers = eval(conf.get('env','headers'))
        resp = request(method='post',url=url,json=data,headers=headers)
        qw = resp.json()
        cls.member_id = str(jsonpath.jsonpath(qw,"$..id")[0])
        cls.token = "Bearer" + " " + jsonpath.jsonpath(qw,'$..token')[0]
        print('用户id',cls.member_id)
        print('token值',cls.token)
    @data(*case_data)
    def test_recharge(self,cas):

        # 准备数据
        url = conf.get('env','url') + cas['url']
        cas['data'] = cas['data'].replace('#member_id#',self.member_id)
        data = eval(cas['data'])
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = self.token
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        if cas['check_sql']:
            sql = cas['check_sql'].format(self.member_id)
            money_data = self.bb.find_one(sql)['leave_amount']
            print("充值之前的钱：",money_data)

        # 发送请求获取实际结果
        repans = request(url=url,method=method,json=data,headers=headers)
        res = repans.json()

        if cas['check_sql']:
            sql = cas['check_sql'].format(self.member_id)
            money_data2 = self.bb.find_one(sql)['leave_amount']
            print("充值之后的钱:",money_data2)

        print('预期结果:',expected)
        print('实际结果：',res)
        # 断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if cas['check_sql']:
                # 将准备的data数据中的amount数值类型转换为decimal
                my_data = decimal.Decimal(str(data['amount']))
                self.assertEqual(my_data,money_data2-money_data)

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
