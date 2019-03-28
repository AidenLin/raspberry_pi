# -*- coding: UTF-8 -*-

#import MySQLdb
import pymysql.cursors
import time
import sys
import datetime

#打开数据库连接
#conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='rapberry',port=3306)
conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='rapberry',port=3306)

#使用cursor()方法获取操作游标
cur=conn.cursor()

#SQL插入语句
#sql = "insert into person values(%s, %s) " % (name, current_time)
#sql = "select * from person"

'''
#使用字典传递
sql = "INSERT INTO person(name, time) VALUES (%(n)s, %(t)s)"
value = {"n":name,"t":curren_time}
'''

'''
user_id = "test123"
password = "password"

con.execute('insert into Login values("%s", "%s")' % \
             (user_id, password))
'''

#获取当前时间
username = "test111"
#current_time= time.asctime(time.localtime(time.time()))
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
#sql_insert="insert into person(name,time) values(%s,str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" %(name,time.strftime("%Y-%m-%d %H:%M:%S"))

#str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s')
try:
    #执行sql语句
    #cur.execute("insert into person(name,time) values(%s,%s)" %(name,time.strftime("%Y-%m-%d %H:%M:%S")))
    #cur.execute('insert into person(name,time) values(%s, %s)' %(name,str_to_date(current_time)))
    #cur.execute('insert into test1(name) values(%s)'%name)
    cur.execute("insert into person values('%s','%s')"%(username, dt))
    #cur.execute(sql, value)
    '''
    # 获取所有记录列表
    results = cur.fetchall()
    for row in results:
        name = row[0]
        time = row[1]
        # 打印结果
        print "name=%s,time=%s" % (name, time)
    '''
    cur.close()
    #提交到数据库执行
    conn.commit()
    print("插入成功")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
except:
    #发生错误时回滚
    conn.rollback()
    print("插入失败")
finally:
    #关闭数据库链接
    conn.close()




