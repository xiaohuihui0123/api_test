"""
北京-漠雪殇-27
"""
import unittest
from library.myddt import ddt,data
from common.handle_excel import Excel_Hande
from common.heandle_path import DATA_DIR
import os
from common.handle_config import conf
from requests import request
import jsonpath
from common.handle_mysql import HandleMysql
from common.handle_logging import log
from common.handel_replace import replace_data,EnvData

@ddt
class Invest(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'invest')
    case = excel.read_excel()
    bb = HandleMysql()


    @data(*case)
    def test_invest(self,cas):
        url = conf.get('env','url') + cas['url']
        method = cas['method']
        data = eval(replace_data(cas['data']))
        headers = eval(conf.get('env','headers'))
        if cas['interface'] != 'login':
            #如果不是登录的接口需要添加token
            headers['Authorization'] = getattr(EnvData,'token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones = request(url=url,method=method,json=data,headers=headers)
        res = respones.json()
        if cas['interface'] == 'login':
            #如果是登录接口，需要提取id和token
            token = 'Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
            member_id = str(jsonpath.jsonpath(res,'$..id')[0])
            setattr(EnvData,'token',token)
            setattr(EnvData,'member_id',member_id)


        if cas['interface'] == 'add':
            #如果是加标接口，需要获取加标后的标id
            loan_id = str(jsonpath.jsonpath(res,'$..id')[0])
            setattr(EnvData,'loan_id',loan_id)

        print('预期结果：', expected)
        print('实际结果：', res)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            log.error('这是{}用例未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}'.format(res))
            log.exception(e)
            self.excel.write(row=row, column=8, value='不通过')
            raise e
        else:
            log.info('用例{}通过'.format(cas['title']))
            self.excel.write(row=row, column=8, value='通过')
