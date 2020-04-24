"""
北京-漠雪殇-27
"""
from requests import request
from common.heandle_path import DATA_DIR
from common.handle_config import conf
import jsonpath
import unittest
from common.handle_mysql import HandleMysql


        # --------------------------------------------------------------------------------

urr = 'http://api.lemonban.com/futureloan/member/register'
da = {
    'mobile_phone':281,
    'reg_name':"asd"
}
headers = {'X-Lemonban-Media-Type':'lemonban.v2'}




