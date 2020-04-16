"""
北京-漠雪殇-27
"""
import logging
from common.handle_config import conf
import os
from common.heandle_path import LOGS_DIR


file_path = os.path.join(LOGS_DIR,conf.get('log','filename'))
class LoggingHandle:

    @staticmethod
    def logging_log():
        # 创建日志收集器
        log = logging.getLogger('小明')
        # 设置收集器的收集等级
        log.setLevel(conf.get('log','level'))
        # 设置输出渠道和输出等级
        fh = logging.FileHandler(file_path,encoding='utf8')
        fh.setLevel(conf.get('log','fh_level'))
        log.addHandler(fh)

        #创建一个输出格式对象
        form = logging.Formatter(conf.get('log','formats'))
        #将输出格式对象添加到输出渠道
        fh.setFormatter(form)

        return log

log = LoggingHandle.logging_log()



