"""
北京-漠雪殇-27
"""

import smtplib
from common.handle_config import conf
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.heandle_path import REPORTS_DIR
import os
from email.mime.text import MIMEText

class Email_smtp:

    @staticmethod
    def email():

        # 连接smtp服务
        smtp = smtplib.SMTP_SSL(host='smtp.qq.com',port=465)
        # 登录
        smtp.login(user=conf.get('smtp','user'),password=conf.get('smtp','password'))

        # 创建多组件套件
        msg = MIMEMultipart()
        msg['subject'] = '我给你的邮件'
        msg['To'] = '1948232996@qq.com'
        msg['From'] = '1948232996@qq.com'

        # 获取报告内容
        q = os.path.join(REPORTS_DIR,'bur.html')
        with open(q,'rb') as f:
            count = f.read()
        # 创建一个邮件附件，将读取的内容加到附件
        report = MIMEApplication(count)
        #设置附件显示的名称
        report.add_header('content-disposition', 'attachment', filename='python.html')
        msg.attach(report)

        #构建一个邮件文本内容
        text = MIMEText('嘿嘿嘿嘿嘿',_charset='utf8')
        msg.attach(text)

        # 发送邮件

        smtp.send_message(msg,from_addr='1948232996@qq.com',to_addrs='1948232996@qq.com')

sm = Email_smtp()