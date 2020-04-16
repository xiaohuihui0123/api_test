"""
北京-漠雪殇-27
"""
import unittest
from requests import request
from common.handle_config import conf
from common.heandle_path import DATA_DIR
from common.handle_excel import Excel_Hande
import jsonpath
from common.handle_logging import log
from library.myddt import ddt,data
from common.handle_mysql import HandleMysql
import os

@ddt
class UpdateCase(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'nickname')
    case = excel.read_excel()
    bb = HandleMysql()


    @classmethod
    def setUpClass(cls):
        # 登录
        url = conf.get('env', 'url') + '/member/login'
        data = {
            'mobile_phone': '13367899876',
            'pwd': 'lemonban'

        }
        headers = eval(conf.get('env', 'headers'))

        r = request(url=url, method='post', json=data, headers=headers)
        re = r.json()
        cls.token = 'Bearer' + ' ' + jsonpath.jsonpath(re, '$..token')[0]
        cls.member_id = jsonpath.jsonpath(re, '$..id')[0]
        cls.reg_name = jsonpath.jsonpath(re, '$..reg_name')[0]
        print('登陆时的昵称',cls.reg_name)

    @data(*case)
    def test_update(self,cas):
        url = conf.get('env', 'url') + cas['url']
        cas['data'] = cas['data'].replace('#member_id#',str(self.member_id))
        data = eval(cas['data'])
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = self.token
        method = cas['method']
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        response = request(method=method,url=url,json=data,headers=headers)
        res = response.json()

        print('预期结果：',expected)
        print('实际结果：',res)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if cas['check_sql']:
                sql = cas['check_sql'].replace('#member_id#',str(self.member_id))
                q = self.bb.find_one(sql)['reg_name']
                print('更新后昵称',q)
                self.assertEqual(q,expected['reg_name'])

        except AssertionError as e:
            log.error('用例--{}--未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}：'.format(res))
            log.exception(e)
            self.excel.write(row=row, column=8, value='不通过')

            raise e
        else:
            log.info('用例--{}--通过'.format(cas['title']))
            self.excel.write(row=row, column=8, value='通过')





