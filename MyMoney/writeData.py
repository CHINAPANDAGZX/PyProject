#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
本代码作用在于将数据写入数据库中
"""
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
初始化创建了Engine，Engine内部维护了一个Pool（连接池）和Dialect（方言），方言来识别具体连接数据库种类
echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
pool_recycle: 设置时间以限制数据库多久没连接自动断开
"""
engine = create_engine("mysql://root:123456@127.0.0.1:3306/gzx?charset=utf8", echo=True, pool_size=8, pool_recycle=60 * 30)

"""
declarative_base()是sqlalchemy内部封装的一个方法，通过其构造一个基类，这个基类和它的子类，可以将Python类和数据库表关联映射起来
数据库表模型类通过__tablename__和表关联起来，Column表示数据表的列
"""
Base = declarative_base()


"""
创建数据表实体类
"""

class MyBudget(Base):
    __tablename__ = "my_budget"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    number = Column(Float)
    type = Column(String(64))
    date = Column(DateTime)
    remark = Column(Text)
    source = Column(String(64))
    source_id = Column(String(64))

    def __init__(self, id, name, number, type, date, remark, source, source_id):
        self.id = id
        self.name = name
        self.number = number
        self.type = type
        self.date = date
        self.remark = remark
        self.source = source
        self.source_id = source_id



"""
创建表，如果存在则忽略，执行以上代码，就会发现在db中创建了users表
"""
Base.metadata.create_all(engine)
"""
sqlalchemy中使用session用于创建程序和数据库之间的会话，所有对象的载入和保存都需要通过session对象
通过sessionmaker调用创建一个工厂，并关联Engine以确保每个session都可以使用该Engine连接资源
"""
# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()

"""
查询记录
通常我们通过以上查询模式获取数据，需要注意的是，通过session.query()我们查询返回了一个Query对象，此时还没有去具体的数据库中查询，只有当执行具体的.all()，.first()等函数时才会真的去操作数据库。
"""
users = session.query(MyBudget).filter_by(id=1).all()
for item in users:
    print(item.name)

# """
# 新增记录
# session.add()将会把Model加入当前session维护的持久空间(可以从session.dirty看到)中，直到commit时提交到数据库
# """
# add_user = Users("test2", "test123@qq.com")
# session.add(add_user)
# session.commit()