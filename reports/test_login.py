"""
北京-漠雪殇-27
"""

import unittest
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.heandle_path import DATA_DIR
from common.handle_config import conf
import os
from requests import request
from common.handle_logging import log

@ddt
class Login(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'login')
    case = excel.read_excel()

    @data(*case)
    def test_login(self,cas):
        url = cas['url']
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        data = eval(cas['data'])
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respons = request(url=url,method=method,json=data,headers=headers)
        res = respons.json()
        print('实际结果：',res)
        print('预期结果：',expected)


        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            log.error('用例{}没有通过，错误等级为error'.format(cas['title']))
            log.debug('预期结果{}'.format(cas['expected']))
            log.debug('实际结果{}'.format(res))
            log.exception(e)
            self.excel.write(row=row,column=8,value='未通过')
            raise e
        else:
            log.info('用例{}执行通过'.format(cas['title']))
            self.excel.write(row=row,column=8,value='通过')