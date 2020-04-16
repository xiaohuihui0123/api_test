"""
北京-漠雪殇-27
"""
import unittest
from common.handle_config import conf
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.heandle_path import DATA_DIR
import os
from requests import request
from common.handle_logging import log



@ddt
class Loans(unittest.TestCase):
    execl = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'loans')
    case = execl.read_excel()


    @data(*case)
    def test_loans(self,cas):
        url = conf.get('env','url') + cas['url']
        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        method = cas['method']
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=method,params=data,headers=headers)
        res = respones.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            #判断返回的数据条数
            self.assertEqual(expected['len'],len(res['data']))
        except AssertionError as e:
            log.error('用例--{}--未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}：'.format(res))
            log.exception(e)
            self.execl.write(row=row, column=8, value='不通过')

            raise e
        else:
            log.info('用例--{}--通过'.format(cas['title']))
            self.execl.write(row=row, column=8, value='通过')
