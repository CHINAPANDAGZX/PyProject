# -*- coding: UTF-8 -*-
# 对应PMS的系统角色表实体类
# 时间：2022年11月24日16:59:28


from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SysRole(Base):
    __tablename__ = "sys_role"

    # ID
    role_id = Column(BigInteger, primary_key=True)
    role_name = Column(String(64), unique=True)

    def __init__(self, name, email):
        self.name = name
