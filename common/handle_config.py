"""
北京-漠雪殇-27
"""
from configparser import RawConfigParser
import os
from common.heandle_path import CONF_DIR

class HandeConfig(RawConfigParser):
    def __init__(self,filename):
        super().__init__()
        self.read(filename,encoding='utf8')

conf = HandeConfig(os.path.join(CONF_DIR,'confing.ini'))






