"""
北京-漠雪殇-27
"""
from requests import request
from common.heandle_path import DATA_DIR
from common.handle_config import conf
import jsonpath
import unittest
from common.handle_mysql import HandleMysql

class FFF():
    bb = HandleMysql()

    def ss(self):
        url = conf.get('env', 'url') + '/member/login'
        data = {
            'mobile_phone': '13367899876',
            'pwd': 'lemonban'

        }
        headers = eval(conf.get('env', 'headers'))

        r = request(url=url, method='post', json=data, headers=headers)
        re = r.json()
        self.token = jsonpath.jsonpath(re, '$..token')[0]
        self.member_id = jsonpath.jsonpath(re,'$..id')[0]
        self.reg_name = jsonpath.jsonpath(re,'$..reg_name')[0]
        print('登陆时的昵称',self.reg_name)

        # --------------------------------------------------------------------------------

        urr = 'http://api.lemonban.com/futureloan/member/update'
        da = {
            'member_id':281,
            'reg_name':"asd"
        }
        headers = {'X-Lemonban-Media-Type':'lemonban.v2'}
        y_token = 'Bearer' + ' ' + self.token
        headers['Authorization'] = y_token

        re = request(url=urr,method='PATCH',json=da,headers=headers)
        ff = re.json()
        print(ff)
        sql = 'SELECT reg_name FROM  futureloan.member WHERE id={};'.format(self.member_id)
        dd = self.bb.find_one(sql)
        print('数据库查询',dd)
        # q = jsonpath.jsonpath(ff,'$..reg_name')[0]
        # print(q)

a = FFF()
c = a.ss()



