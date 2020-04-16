"""
北京-漠雪殇-27
"""
import os

# 项目目录绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例模块所在的目录路径
CASE_DIR = os.path.join(BASE_DIR,'testcase')

# 用例数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR,'data')

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR,'conf')

# 测试报告所在的目录路径
REPORTS_DIR = os.path.join(BASE_DIR,'reports')

# 日志文件的目录路径
LOGS_DIR = os.path.join(BASE_DIR,'logs')
