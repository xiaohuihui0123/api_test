"""
北京-漠雪殇-27
"""
import unittest
import os
from common.handle_excel import Excel_Hande
from ddt import ddt,data
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.heandle_path import DATA_DIR
from common.handle_mysql import HandleMysql
import random


filename = os.path.join(DATA_DIR,'apicases.xlsx')
@ddt
class RegisterTestcase(unittest.TestCase):
    excel = Excel_Hande(filename,'register')
    case_data = excel.read_excel()
    bb = HandleMysql()

    @data(*case_data)
    def test_register(self,cas):

        expected = eval(cas['expected'])
        method = cas['method']
        # 用生成的随机手机号码替换#phon#
        if '#phon#' in cas['data']:
            phones = self.readom_phon()
            cas['data'] = cas['data'].replace('#phon#',phones)
        data = eval(cas['data'])
        url = cas['url']
        headers = eval(conf.get('env','headers'))
        row = cas['case_id'] + 1
        respons = request(method=method,url=url,json=data,headers=headers)
        res = respons.json()
        print('预期结果：',expected)
        print('实际结果：',res)

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])

            if cas['sql']:
                qy = cas['sql'].replace('#phon#',data['mobile_phone'])
                re = self.bb.find_one(qy)
                self.assertTrue(re)


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

    @classmethod
    def readom_phon(cls):
        while True:
            phon = '155'
            for i in range(8):
                re = random.randint(0, 9)
                phon += str(re)
            mysql = 'select * from futureloan.member where mobile_phone={}'.format(phon)
            sq = cls.bb.find_count(mysql)
            if sq == 0:
                return phon
