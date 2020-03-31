#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
   本例是利用pymysql库对mysql数据库进行增删改查
"""
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "test1")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# ----------------查询数据库版本开始-------------------- #
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
# print("Database version : %s " % data)
# ----------------查询数据库版本结束-------------------- #
# ----------------增删数据库表格开始-------------------- #

# 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("DROP TABLE IF EXISTS tb_weather")
# # 使用预处理语句创建表
# sql = """CREATE TABLE tb_weather (
#          `id` varchar(64) NOT NULL COMMENT '主键',
#          `days` varchar(20) DEFAULT NULL COMMENT '日期',
#          `weather` varchar(30) DEFAULT NULL COMMENT '天气',
#          `temperature` varchar(30) DEFAULT NULL COMMENT '气温',
#          `wind_force` varchar(30) DEFAULT NULL COMMENT '风力等级',
#          `wind_direction` varchar(30) DEFAULT NULL COMMENT '风向',
#          PRIMARY KEY (`id`)
#           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
# # 执行建表语句
# cursor.execute(sql)
# ----------------增删数据库表格结束-------------------- #

# ----------------增删数据库数据开始-------------------- #

# SQL 插入语句
# sql = """INSERT INTO tb_weather(id,
#          days, weather, temperature, wind_force, wind_direction)
#          VALUES ('1','25日', '天气：小雨转多云', '19/15℃', '3-4级转<3级', '北风')"""
# # try:
#     # 执行sql语句
# cursor.execute(sql)
#     # 提交到数据库执行
# db.commit()
# except:
#     # 如果发生错误则回滚
#     db.rollback()
# ----------------增删数据库数据结束-------------------- #

# ----------------查询数据库数据开始-------------------- #
# SQL 查询语句
sql = "SELECT MAX(id) FROM tb_weather"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
       # 打印结果
      print ("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
             (fname, lname, age, sex, income ))
except:
   print ("Error: unable to fetch data")
# ----------------查询数据库数据结束-------------------- #

# 关闭数据库连接
db.close()
