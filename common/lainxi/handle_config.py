"""
北京-漠雪殇-27
"""

from configparser import ConfigParser
class ConfigHandle(ConfigParser):
    def __init__(self,filename):
        super().__init__()
        self.read(filename,encoding='utf8')

conf = ConfigHandle(r'E:\pycharm_new\api_test\conf\confing.ini')
re = conf.get('log','fh_level')
print(re)


# con = ConfigParser()
# con.read('confing.ini',encoding='utf8')
 # res = con.get('level','fh_level')
# print(res)

