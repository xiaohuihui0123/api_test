"""
北京-漠雪殇-27
"""
import unittest
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.handle_config import conf
from common.heandle_path import DATA_DIR
import os

from requests import request
from common.handle_logging import log

@ddt
class Login(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'login')
    case = exce.read_excel()

    @data(*case)
    def test_login(self,cas):
        url = cas['url']
        menthod = cas['method']
        headers = eval(conf.get('env','headers'))
        data = eval(cas['data'])
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=menthod,json=data,headers=headers)
        res = respones.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            log.error('该用例{}报错'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('这个用例{}通过'.format(cas['title']))
            self.exce.write(row=row,column=8,value='通过')