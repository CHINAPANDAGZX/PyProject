# -*- coding: UTF-8 -*-
# 对应PMS的保养包对应设备关联表实体类
# 时间：2022年11月28日09:45:30

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

import uuid

# Base = declarative_base()


class JwWorkItemNew:
    # __tablename__ = "jw_work_item"

    def __init__(self):
        self.id = str(uuid.uuid1()).replace('-', '')  # ID
        self.code = None  # 对应设备ID
        self.name = None  # 对应设备ID
        self.description = None  # 对应设备ID
        self.eng_description = None  # 对应设备ID
        self.is_replace_spare = None  # 对应设备ID

        self.remark = None  # 备注
        self.create_by = 1  # 创建者
        self.create_time = None  # 创建时间
        self.update_by = 1  # 更新者
        self.update_time = None  # 更新时间
        self.del_flag = 0  # 删除标志位
        self.is_sent = 0  # 是否需要通讯 0 不用 1需要
        self.sent_status = 0  # 发送状态 0未发送 1已发送 2未发送数据处理报错
        self.sent_target = ''  # 发送目标
        self.is_wfpass = 'false'  # 审核流是否通过 true false
