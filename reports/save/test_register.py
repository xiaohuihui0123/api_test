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
import random
from requests import request
from common.handle_logging import log

@ddt
class Register(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'register')
    case = exce.read_excel()
    my = HandleMysql()

    @data(*case)
    def test_register(self,cas):
        url = cas['url']
        method = cas['method']

        if '#phone#' in cas['data']:
            phon = self.phone_replace()
            setattr(EnvData,'mobile_phone',phon)
            cas['data'] = replace_data(cas['data'])

        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=method,json=data,headers=headers)
        res = respones.json()


        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                f = self.my.find_count(sql)
                self.assertEqual(1,f)
        except AssertionError as e:
            log.error('这条用例{}报错'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row, column=8, value='不通过')
            raise e
        else:
            log.info('这条用例{}通过了'.format(cas['title']))
            self.exce.write(row=row, column=8, value='通过')


    @classmethod
    def phone_replace(cls):
        while True:
            phone = '135'
            for i in range(8):
                re = random.randint(0,9)
                phone += str(re)
            sql = 'select * from futureloan.member where mobile_phone={}'.format(phone)
            d = cls.my.find_count(sql)
            if d == 0:
                return phone
