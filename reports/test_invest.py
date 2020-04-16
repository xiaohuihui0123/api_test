"""
北京-漠雪殇-27
"""
import unittest
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.heandle_path import DATA_DIR
from common.handle_config import conf
import os
from common.handel_replace import EnvData,replace_data
from requests import request
import jsonpath
from common.handle_logging import log

@ddt
class Invest(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'invest')
    case = excel.read_excel()

    @data(*case)
    def test_invest(self,cas):
        url = conf.get('env','url') + cas['url']
        data = eval(replace_data(cas['data']))
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        if cas['interface'] != 'login':
            #不是登录的接口，则需要给他添加token
            headers['Authorization'] = getattr(EnvData,'token')

        repons = request(url=url,method=method,json=data,headers=headers)
        res = repons.json()

        if cas['interface'] == 'login':
            #如果是登录的接口，我们需要提取他的id和token
            token = 'Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
            member_id = str(jsonpath.jsonpath(res,'$..id')[0])
            setattr(EnvData,'token',token)
            setattr(EnvData,'member_id',member_id)

        if cas['interface'] == 'add':
            #如果是添加项目接口，我们要提取标id
            loan_id = str(jsonpath.jsonpath(res,'$..id')[0])
            setattr(EnvData,'loan_id',loan_id)

        print('预期结果：',expected)
        print('实际结果：',res)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            log.error('这是{}用例未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}'.format(res))
            log.exception(e)
            self.excel.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('用例{}通过'.format(cas['title']))
            self.excel.write(row=row,column=8,value='通过')


