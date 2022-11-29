# -*- coding: UTF-8 -*-
# 对应PMS的设备表实体类
# 时间：2022年11月25日09:24:28

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JwInstrument(Base):
    __tablename__ = "jw_instrument"

    # ID
    id = Column(String(32), primary_key=True)
    name = Column(String(64), unique=True)
    # 删除标注位 1 是删除
    del_flag = Column(String(6), unique=True)

    def __init__(self, name):
        self.name = name
