# -*- coding: UTF-8 -*-
# 对应PMS的保养明细表实体类
# 时间：2022年11月28日09:45:30
import time
import uuid


class JwWorkItem:
    """工作项目类"""

    def __init__(self, name, code, description, eng_description, is_replace_spare):
        self.id = str(uuid.uuid1()).replace('-', '')  # 保养项目ID
        self.code = code  # 保养编码
        self.name = ''  # 保养项目名称
        self.device_name = ''  # 设备名称，用于切分excel表格中的多个设备
        self.description = ''  # 中文描述
        self.eng_description = ''  # 英文描述
        self.is_replace_spare = '0'  # 是否更换备件 0-否；1-是
        self.is_key_work = '0'  # 是否为关键工作 0-否；1-是
        self.PSC_defect_type = ''  # PSC缺陷类型
        self.PSC_defect_class = ''  # PSC缺陷细分类
        self.PSC_defect_code = ''  # PMS缺陷代码
        self.PMS_code = ''  # PMS编码
        self.CMS_code = ''  # CMS编码
        self.defect_property = ''  # 缺陷性质
        self.remark = ''  # 备注
        self.create_by = '1'  # 创建者
        self.create_time = time.strftime("%F %T")  # 创建时间
        self.update_by = '1'  # 更新者
        self.update_time = time.strftime("%F %T")  # 更新时间
        self.del_flag = '0'  # 删除标志位
        self.is_sent = '0'  # 是否需要通讯 0 不用 1需要
        self.sent_status = '0'  # 发送状态 0未发送 1已发送 2未发送数据处理报错
        self.sent_target = ''  # 发送目标
        self.is_wfpass = 'false'  # 审核流是否通过 true false
        self.item_type = '0'  # 工作类型 0-新增;1-PMS;2-CMS;3-PSC;4-附属工作内容
        self.pid = ''  # 附属工作内容所属的项目id
        self.CMS_type = ''  # CMS类型
