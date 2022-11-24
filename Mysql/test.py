#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Python sqlalchemy 数据库操作例程
参考网址：
https://www.cnblogs.com/ybjourney/p/11832045.html
https://blog.csdn.net/cynthrial/article/details/88725612
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
初始化创建了Engine，Engine内部维护了一个Pool（连接池）和Dialect（方言），方言来识别具体连接数据库种类
echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
pool_recycle: 设置时间以限制数据库多久没连接自动断开
"""
engine = create_engine("mysql://root:root@192.168.136.128/python-test?charset=utf8", echo=True, pool_size=8, pool_recycle=60 * 30)

"""
declarative_base()是sqlalchemy内部封装的一个方法，通过其构造一个基类，这个基类和它的子类，可以将Python类和数据库表关联映射起来
数据库表模型类通过__tablename__和表关联起来，Column表示数据表的列
"""
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(64))

    def __init__(self, name, email):
        self.name = name
        self.email = email

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
新增记录
session.add()将会把Model加入当前session维护的持久空间(可以从session.dirty看到)中，直到commit时提交到数据库
"""
add_user = Users("test2", "test123@qq.com")
session.add(add_user)
session.commit()
"""
查询记录
通常我们通过以上查询模式获取数据，需要注意的是，通过session.query()我们查询返回了一个Query对象，此时还没有去具体的数据库中查询，只有当执行具体的.all()，.first()等函数时才会真的去操作数据库。
"""
users = session.query(Users).filter_by(id=1).all()
for item in users:
    print(item.name)
"""
修改记录
更新数据有两种方法，一种是使用query中的update方法
另一种是操作对应的表模型
"""
session.query(Users).filter_by(id=1).update({'name': "Jack"})

users = session.query(Users).filter_by(name="Jack").first()
users.name = "test"
session.add(users)
