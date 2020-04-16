"""
北京-漠雪殇-27
"""
import unittest
from library.myddt import ddt,data
from common.heandle_path import DATA_DIR
from common.handle_excel import Excel_Hande
from common.handle_config import conf
import os
from common.handel_replace import EnvData,replace_data
import random
from common.handle_mysql import HandleMysql
from requests import request

@ddt
class Register(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'case.xlsx'),'register')
    case = exce.read_excel()
    bb = HandleMysql()



    @data
    def test_register(self,cas):
        url = conf.get('env','url2') + '/user/register/'
        method = cas['method']
        expected = eval(cas['expected'])
        if '#username#' in cas['data']:
            username = self.usernam_data()
            setattr(EnvData,'username',username)
            cas['data'] = replace_data(cas['data'])
        if '#email#' in cas['data']:
            email = self.email_data()
            setattr(EnvData,'email',email)
            cas['data'] = replace_data(cas['data'])

        data = eval(cas['data'])
        respones = request(url=url,method=method,json=data)
        res = respones.json()
        #判断用户名是否注册
        url3 = 'http://api.keyou.site:8000/keyou1/count/'


        try:
            self.assertEqual(res[ ])




    @classmethod
    def usernam_data(cls):
        while True:
            name = 'huihui'
            for i in range(5):
                r = random.randint(0, 9)
                name += str(r)
            sql = 'select * from test.auth_user where username={}'.format(name)
            qs = cls.bb.find_count(sql)
            if qs == 0:
                return name

    @classmethod
    def email_data(cls):
        while True:
            n = '1'
            for i in range(8):
                r = random.randint(0, 9)
                n += str(r)
            sql = 'select * from test.auth_user where email={}@qq.com'.format(n)
            qs = cls.bb.find_count(sql)
            if qs == 0:
                return n