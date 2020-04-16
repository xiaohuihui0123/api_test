"""
北京-漠雪殇-27
"""
import unittest
from BeautifulReport import BeautifulReport
from common.heandle_path import CASE_DIR,REPORTS_DIR
from common.handel_email import sm



suit = unittest.TestSuite()
load = unittest.TestLoader()
suit.addTest(load.discover(CASE_DIR))

bf = BeautifulReport(suit)
bf.report('注册接口',filename='bur.html',report_dir=REPORTS_DIR)

# sm.email()

