"""
北京-漠雪殇-27
"""
import logging
class LoggingHandle:
    @staticmethod
    def logging_log():
        log = logging.getLogger()
        log.setLevel('DEBUG')
        fh = logging.FileHandler('HH.log',encoding='utf8')
        fh.setLevel('DEBUG')

        forms = 'formats = %%(asctime)s -- [%%(filename)s-->line:%%(lineno)d] - %%(levelname)s: %%(message)s'
        fo = logging.Formatter(forms)
        fh.setFormatter(fo)

        return log

log = LoggingHandle.logging_log()