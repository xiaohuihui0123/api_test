"""
北京-漠雪殇-27
"""
import re
from common.handle_config import conf

class EnvData:
    pass


def replace_data(data):

    while re.search('#(.*?)#',data):
        f = re.search('#(.*?)#',data)
        key = f.group()
        value = f.group(1)
        try:
            d = conf.get('test_data',value)
        except:
            d = getattr(EnvData,value)
        data = data.replace(key,d)
    return data





