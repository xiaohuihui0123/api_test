"""
北京-漠雪殇-27
"""
import pymysql
from common.handle_config import conf


class HandleMysql():
    def __init__(self):
        # 连接数据库
        self.con = pymysql.connect(host=conf.get('mysql','host'),
                             port=conf.getint('mysql','port'),
                             user=conf.get('mysql','user'),
                             password=conf.get('mysql','password'),
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        # 创建游标对象
        self.cu = self.con.cursor()

    def find_one(self,sql):
        """

        :param sql: 查询的sql语句
        :return: 返回查询到的第一条数据
        """
        self.con.commit()
        self.cu.execute(sql)
        return self.cu.fetchone()

    def find_all(self,sql):
        """

        :param sql: 查询的sql语句
        :return: 返回所有查询到的数据
        """
        self.con.commit()
        self.cu.execute(sql)
        return self.cu.fetchall()
    def find_count(self,sql):
        self.con.commit()
        s = self.cu.execute(sql)
        return s
    def update(self,sql):
        """

        :param sql: 增删改的sql的语句
        :return:
        """
        self.cu.execute(sql)
        self.con.commit()

    def close(self):
        self.cu.close()
        self.con.close()

if __name__ == '__main__':
    dd = HandleMysql()
    re = dd.find_count('select * from futureloan.member limit 2')
    print(re)

