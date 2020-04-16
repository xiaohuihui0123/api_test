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
class Audit(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'audit')
    case = exce.read_excel()
    bb = HandleMysql()
    #普通用户登录
    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get('env','url') + '/member/login'
        user_data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')
        }
        headers = eval(conf.get('env','headers'))
        respones = request(url=url,method='post',json=user_data,headers=headers)
        res = respones.json()
        user_token = 'Bearer' + ' ' + jsonpath.jsonpath(res,'$..token')[0]
        user_member_id = str(jsonpath.jsonpath(res,'$..id')[0])
        setattr(EnvData,'user_token',user_token)
        setattr(EnvData,'user_member_id',user_member_id)

        #管理员登录
        admin_data = {
            'mobile_phone':conf.get('test_data','admin_phone'),
            'pwd':conf.get('test_data','admin_pwd')
        }
        q = request(url=url,method='post',json=admin_data,headers=headers)
        f = q.json()
        admin_token = 'Bearer' + ' ' + jsonpath.jsonpath(f,'$..token')[0]
        admin_member_id = str(jsonpath.jsonpath(f, '$..id')[0])
        setattr(EnvData, 'admin_token', admin_token)
        setattr(EnvData, 'admin_member_id', admin_member_id)

    #每条用例执行前，添加一个标
    def setUp(self) -> None:
        url = conf.get('env','url') + '/loan/add'
        data = {
             "member_id":getattr(EnvData,'user_member_id'),
             "title":"借钱娶媳妇",
             "amount":2000,
             "loan_rate":12.0,
             "loan_term":3,
             "loan_date_type":1,
             "bidding_days":5

             }
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'user_token')
        pn = request(url=url,method='post',json=data,headers=headers)
        ss = pn.json()
        loan_id = str(jsonpath.jsonpath(ss,'$..id')[0])
        setattr(EnvData,'loan_id',loan_id)

    @data(*case)
    def test_audit(self,cas):

        url = conf.get('env','url') + cas['url']
        method = cas['method']
        data =eval(replace_data(cas['data']))
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'admin_token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1

        respones1 = request(url=url,method=method,json=data,headers=headers)
        res1 = respones1.json()

        if cas['title'] =='审核通过' and res1['msg'] == 'OK':
            setattr(EnvData,'pass_loan_id',str(data['loan_id']))
        print('预期结果：',expected)
        print('实际结果：',res1)

        try:
            self.assertEqual(expected['code'],res1['code'])
            self.assertEqual(expected['msg'],res1['msg'])
            #判断审核状态是否符合预期的结果
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                status = self.bb.find_one(sql)['status']
                self.assertEqual(expected['status'],status)
        except AssertionError as e:
            log.error('这条用例{}没有通过'.format(cas['title']))
            log.exception(e)
            self.exce.write(row=row,column=8,value='不通过')
            raise e
        else:
            log.info('这条用例{}执行通过'.format(cas['title']))
            self.exce.write(row=row,column=8,value='通过')