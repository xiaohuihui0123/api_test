"""
北京-漠雪殇-27
"""
import pymysql
# 链接数据库

cu = pymysql.connect(host='120.78.128.25',
                     port=3306,
                     user='future',
                     password='123456',
                     charset='utf8',
                     cursorclass=pymysql.cursors.DictCursor)

# 创建游标
con = cu.cursor()
sql = 'select * from futureloan.member limit 3'
# 执行sql
con.execute(sql)
# 获取结果
# re = con.fetchone()
# print(re)
re = con.fetchall()
print(re)
'''
增删改操作需要提交事务

连接对象.commit



'''