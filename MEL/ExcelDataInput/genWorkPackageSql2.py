# -*- coding: UTF-8 -*-
# 用于将嘉庚号助理系统数据表中的数据转换为工作包表sql语句
# 时间：2022年11月24日16:59:28

import xlrd
import xlwt
import uuid
import datetime
import time

from urllib.parse import quote_plus as urlquote

from sqlalchemy import create_engine, Column, Integer, String, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from MEL.ExcelDataInput.SysRole import SysRole


class WorkPackage:
    """工作包类"""

    def __init__(self, name):
        self.id = str(uuid.uuid1()).replace('-', '')  # 保养包ID
        self.name = name  # 5——保养包名称
        self.device_name = None  # 7、6——设备名称
        self.code = None  # 0——保养包编码
        self.cycle = None  # 11、12——保养包周期
        self.cycle_type = 0  # 周期计算方式 0-时间周期 1-计数周期
        self.pro_class = None  # 10——项目分类（项目类别）
        self.bus_class = None  # 1——业务类别
        self.opr_class = None  # 2——作业类别
        self.responsible_role = None  # 4——责任岗位
        self.is_cms = None  # 是否CMS相关 0-否；1-是(是否循环检验（CMS）)
        self.is_pms = None  # 是否PMS相关 0-否；1-是(是否船级相关PMS)
        self.is_commision = None  # 是否委托 0-否；1-是(是否委托)
        self.front_tolerance = None  # 13——前允差
        self.back_tolerance = None  # 14——后允差
        self.work_des = None  # 15——工作描述
        self.eng_des = None  # 16——英文描述
        self.is_replace_spare = None  # 17——是否更换备件 0-否；1-是
        self.risk_rank = None  # 风险等级 1-低风险；2-中风险；3-高风险
        self.risk_des = None  # 18——风险描述及措施
        self.create_by = 1  # 创建者
        self.create_time = None  # 创建时间
        self.update_by = 1  # 更新者
        self.update_time = None  # 更新时间
        self.del_flag = 0  # 删除标志位
        self.is_sent = 0  # 是否需要通讯 0 不用 1需要
        self.sent_status = 0  # 发送状态 0未发送 1已发送 2未发送数据处理报错
        self.sent_target = None  # 发送目标
        self.is_wfpass = None  # 审核流是否通过 true false
        self.is_valid = 0  # 是否生效 0-否；1-是
        self.remark = 0  # 19——备注

        self.ship_id = 102  # 所属位置
        # Overhaul O 0
        # Survey S 1
        # Check C 2
        # Maintenance M 3
        # Test T 4
        # Renew R 5
        self.operation_type = 2  # 2——操作方式


class WorkInstrumentPackage:
    """设备关联工作包类"""

    def __init__(self, package_id, package_name, device_id, device_name):
        self.package_id = package_id  # 保养包ID
        self.package_name = package_name  # 保养包名称——1
        self.device_id = device_id  # 设备ID
        self.device_name = device_name  # 设备名称


def copy_data_to_object(filename):
    """
    从Excel中读取数据
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("Sheet1")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 获取数据
    work_package_list = []  # 空列表
    # 用于存储责任岗位信息
    responsible_role_Set = set()
    for j in range(1, nrows):
        work_page = WorkPackage(table.cell_value(j, 5))
        # 生成保养编码的规则？
        work_page.code = table.cell_value(j, 0)

        work_page.device_name = replaceDeviceName(table.cell_value(j, 6), table.cell_value(j, 7))
        work_page.cycle = table.cell_value(j, 12)
        work_page.pro_class = table.cell_value(j, 10)
        work_page.bus_class = table.cell_value(j, 1)
        work_page.opr_class = table.cell_value(j, 2)
        work_page.responsible_role = table.cell_value(j, 4)

        work_page.front_tolerance = table.cell_value(j, 13)
        work_page.back_tolerance = table.cell_value(j, 14)
        work_page.work_des = table.cell_value(j, 15)
        work_page.eng_des = table.cell_value(j, 16)
        work_page.is_replace_spare = table.cell_value(j, 17)
        work_page.risk_des = table.cell_value(j, 18)

        work_package_list.append(work_page)
        responsible_role_Set.add(work_page.responsible_role)
    return work_package_list, responsible_role_Set


def trans_excel_data_to_instrument_package_list(work_package_list):
    """
    从工作包列表中提取工作包设备关联列表
    work_package_list 工作包表
    """
    instrument_package_list = []
    for work_package in work_package_list:
        work_package_device_list = work_package.device_name.split("、")
        if len(work_package_device_list) > 1:
            for device in work_package_device_list:
                item_instrument = WorkInstrumentPackage(work_package.id, work_package.name, '', device)
                instrument_package_list.append(item_instrument)
        else:
            item_instrument = WorkInstrumentPackage(work_package.id, work_package.name, '', work_package.device_name)
            instrument_package_list.append(item_instrument)
    return instrument_package_list


def gen_sql(work_package_list):
    """
    将保养工作包转换成新增sql语句写入文件
    """
    if len(work_package_list) > 0:
        f = open("insert.sql", "w", encoding='utf-8')
        for wp in work_package_list:
            #  处理周期
            sql = "INSERT INTO `jw_work_package`" \
                  "(`id`, `name`, `code`, `cycle`, `cycle_unit`, `remark`, `pro_class`, `bus_class`, `opr_class`, `responsible_role`, `is_CMS`, `is_PMS`, " \
                  "`is_commission`, `front_tolerance`, `back_tolerance`, `work_des`, `eng_des`, `is_replace_spare`, `risk_rank`, `risk_des`, " \
                  "`create_by`, `create_time`, `update_by`, `update_time`, `del_flag`, `is_sent`, `sent_status`, `sent_target`, `is_wfpass`, `is_valid`, `cycle_type`, `ship_id`, `operation_type`) VALUES " \
                  "({}, {}, 'PA1000000001', {}, '0', '', {}, {}, {}, {}, {}, {}," \
                  " {}, {}, {}, {}, {}, {}, {}, {}, " \
                  "'1', {}, '1', {}, '0', '0', '0', '', '', '0', '1', '102', '3');\n" \
                .format("'" + wp.id + "'", "'" + wp.name + "'", trans_cycle(wp.cycle), trans_class(wp.pro_class),
                        trans_class(wp.bus_class), trans_class(wp.opr_class), trans_role(wp.responsible_role),
                        "'" + wp.is_cms + "'", "'" + wp.is_pms + "'",
                        "'" + trans_01(wp.is_commision) + "'", trans_tolerance(wp), trans_tolerance(wp),
                        "'" + wp.work_des + "'", "'" + wp.eng_des + "'", "'" + trans_01(wp.is_replace_spare) + "'",
                        "'" + trans_risk_rank(wp.risk_rank) + "'", "'" + wp.risk_des + "'",
                        "'" + time.strftime("%F %T") + "'", "'" + time.strftime("%F %T") + "'")
            print(wp)
            f.write(sql)
        f.close()
    else:
        print("数据为空")


def delete_sql(work_package_list):
    """
    将保养工作包转换成删除sql语句写入文件
    """
    if len(work_package_list) > 0:
        f = open("rollback.sql", "w", encoding='utf-8')
        for wp in work_package_list:
            #  处理周期
            sql = "DELETE FROM `jw_work_package` WHERE id = {};\n".format("'" + wp.id + "'")
            f.write(sql)
        f.close()
    else:
        print("数据为空")


def trans_cycle(cycle):
    """
    将保养周期转换为数据库格式
    """
    if cycle == "1(年)":
        return 365
    elif cycle == "4(年)":
        return 365 * 4
    elif cycle == "3(月)":
        return 30 * 3


def trans_class(class_str):
    """
    将类别字段截取数字
    """
    return class_str.split('(')[0]


def trans_role(role_str):
    """
    将责任岗位转换为角色ID
    """
    if role_str == "探测部水文气象组":
        return 129


def trans_01(trans_str):
    """
    将是否委托转换为数据库标识
    """
    if trans_str == "是":
        return str(1)
    else:
        return str(0)


def trans_risk_rank(risk_rank_str):
    """
    将风险等级转换为数据库标识
    """
    if risk_rank_str == "高风险":
        return str(3)
    elif risk_rank_str == "中风险":
        return str(2)
    else:
        return str(1)


def trans_tolerance(wp):
    """
    将是否委托转换为数据库标识
    """
    if (wp.front_tolerance == 1) | (wp.front_tolerance == 2) | (wp.front_tolerance == 3):
        if (wp.cycle == "1(年)"):
            return 30
        elif (wp.cycle == "4(年)"):
            return 90
        elif (wp.cycle == "3(月)"):
            return 15
    else:
        return 0


def replaceDeviceName(device_name, device_no):
    """
    将设备名称进行替换
    device_name : 设备名称
    device_no : 设备编号
    """
    device_name = device_no + device_name
    return device_name


if __name__ == '__main__':
    # 从Excel中读取数据
    work_package_list, responsible_role_Set = copy_data_to_object('C:/Users/admin/Desktop/2022年11月24日导入工作包/嘉庚号助力系统基础数据.xlsx')
    # 连接数据库
    # engine = create_engine("mysql+pymysql://mel:t@2185570#$@10.64.35.127:9909/pms-land-tmp-for-lqh?charset=utf8", echo=True, pool_size=8, pool_recycle=60 * 30)
    host = "10.64.35.127"
    port = 9909
    user = "mel"
    password = "t@2185570#$"
    db_name = "pms-land-tmp-for-lqh"
    con_info = f'mysql+pymysql://{user}:{urlquote(password)}@{host}:{port}/{db_name}?charset=utf8'
    engine = create_engine(con_info, echo=True, pool_size=8, pool_recycle=60 * 30)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    # 查询相关责任岗位ID
    sys_roles = session.query(SysRole).filter_by(role_id=1).all()
    for item in sys_roles:
        print(item.role_name)

    # 查询相关设备ID

    # 将工作包数据列表中的责任岗位ID和设备ID进行替换

    # 生成创建SQL语句

    # 生成回滚删除SQL语句

    print("ok")
    # gen_sql(work_package_list)
    # delete_sql(work_package_list)
