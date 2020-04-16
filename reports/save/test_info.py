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
from common.handel_replace import replace_data,EnvData
from common.handle_mysql import HandleMysql
import jsonpath


@ddt
class Loans(unittest.TestCase):
    execl = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'info')
    case = execl.read_excel()

    @classmethod
    def setUpClass(cls) -> None:
        #普通用户登录
        url = conf.get('env','url') + '/member/login'
        data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')
        }

        headers = eval(conf.get('env','headers'))
        r = request(url=url,method='post',json=data,headers=headers)
        res = r.json()
        token = 'Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
        member_id = str(jsonpath.jsonpath(res,'$..id')[0])
        setattr(EnvData,'token',token)
        setattr(EnvData,'member_id',member_id)

    @data(*case)
    def test_loans(self,cas):
        cas['url'] = replace_data(cas['url'])
        url = conf.get('env','url') + cas['url']
        headers = eval(conf.get('env','headers'))
        headers["Authorization"] = getattr(EnvData, "token")
        method = cas['method']
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=method,headers=headers)
        res = respones.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
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
