"""
北京-漠雪殇-27
"""
import unittest
from common.handle_excel import Excel_Hande
from library.myddt import ddt,data
from common.heandle_path import DATA_DIR
from common.handle_config import conf
from common.handle_logging import log
from common.handle_mysql import HandleMysql
from requests import request
import jsonpath
import os
from common.handel_replace import EnvData,replace_data

@ddt
class AuditTest(unittest.TestCase):
    excel = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'Sheet1')
    case = excel.read_excel()
    bb = HandleMysql()

    @classmethod
    def setUpClass(cls):
        # 普通用户登录
        # 准备数据
        url = conf.get('env','url') + '/member/login'
        user_data = {
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')

        }
        headers = eval(conf.get('env','headers'))
        respons = request(method='post',url=url,json=user_data,headers=headers)
        re = respons.json()
        user_member_id = str(jsonpath.jsonpath(re,'$..id')[0])
        user_token = 'Bearer' + ' ' + jsonpath.jsonpath(re,'$..token')[0]
        setattr(EnvData,'user_member_id',user_member_id)
        setattr(EnvData,'user_token',user_token)
        # 管理员登录
        data = {
            'mobile_phone': conf.get('test_data', 'admin_phone'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        resp = request(method='post',url=url,json=data,headers=headers)
        es = resp.json()
        admin_token = 'Bearer' + ' ' + jsonpath.jsonpath(es,'$..token')[0]
        setattr(EnvData,'admin_token',admin_token)

# 加标
    def setUp(self) -> None:
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData,'user_token')
        data = {"member_id": getattr(EnvData,'user_member_id'),
                "title": "木森借钱买飞机",
                "amount": 2000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_date_type": 1,
                "bidding_days": 5}
        # 发送请求，添加项目
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        # 获取标id
        loan_id = str(jsonpath.jsonpath(res, "$..id")[0])
        setattr(EnvData,'loan_id',loan_id)

    @data(*case)
    def test_audit(self,cas):
        # 准备数据
        url = conf.get('env','url') + cas['url']
        # 判断是否需要替换为审核通过的标id
        if "#pass_loan_id#" in cas['data']:
            cas['data'] = replace_data(cas['data'])

        cas['data'] = replace_data(cas['data'])
        data = eval(cas['data'])
        method = cas['method']
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(EnvData,'admin_token')
        expected = eval(cas['expected'])
        row = cas['case_id'] + 1
        # 获取实际结果
        response = request(url=url,method=method,json=data,headers=headers)
        rese = response.json()
        print('预期结果：',expected)
        print('实际结果：',rese)
        # 判断是否是审核通过的用例，并且审核成功
        if cas['title'] =='审核通过' and rese['msg'] == 'OK':
            setattr(EnvData,'pass_loan_id',str(data['loan_id']))



        try:
            self.assertEqual(expected['code'],rese['code'])
            self.assertEqual(expected['msg'],rese['msg'])
            if cas['check_sql']:
                sql = replace_data(cas['check_sql'])
                status = self.bb.find_one(sql)['status']
                self.assertEqual(expected['status'],status)
                print(status,type(status))
        except AssertionError as e:
            log.error('用例--{}--未通过'.format(cas['title']))
            log.debug('预期结果{}'.format(expected))
            log.debug('实际结果{}：'.format(rese))
            log.exception(e)
            self.excel.write(row=row,column=8,value='不通过')

            raise e
        else:
            log.info('用例--{}--通过'.format(cas['title']))
            self.excel.write(row=row,column=8,value='通过')
