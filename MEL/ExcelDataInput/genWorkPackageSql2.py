# -*- coding: UTF-8 -*-
# 用于将嘉庚号助理系统数据表中的数据转换为工作包表sql语句
# 时间：2022年11月24日16:59:28

import xlrd
import xlwt
import uuid
import time

from urllib.parse import quote_plus as urlquote

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from MEL.ExcelDataInput.entity.JwInstrument import JwInstrument

from MEL.ExcelDataInput.entity.JwInstrumentItem import JwInstrumentItem
from MEL.ExcelDataInput.entity.JwInstrumentPackage import JwInstrumentPackage
from MEL.ExcelDataInput.entity.JwWorkItem import JwWorkItem
from MEL.ExcelDataInput.entity.SysRole import SysRole


class WorkPackage:
    """工作包类"""

    def __init__(self, name):
        self.id = str(uuid.uuid1()).replace('-', '')  # 保养包ID
        self.name = name  # 5——保养包名称
        self.device_name = ''  # 7、6——设备名称
        self.code = ''  # 0——保养包编码
        self.cycle = ''  # 11、12——保养包周期
        self.cycle_type = 0  # 周期计算方式 0-时间周期 1-计数周期
        self.pro_class = ''  # 10——项目分类（项目类别）
        self.bus_class = ''  # 1——业务类别
        self.opr_class = ''  # 2——作业类别
        self.responsible_role = ''  # 4——责任岗位
        self.is_cms = '0'  # 是否CMS相关 0-否；1-是(是否循环检验（CMS）)
        self.is_pms = '0'  # 是否PMS相关 0-否；1-是(是否船级相关PMS)
        self.is_commision = ''  # 是否委托 0-否；1-是(是否委托)
        self.front_tolerance = ''  # 13——前允差
        self.back_tolerance = ''  # 14——后允差
        self.work_des = ''  # 15——工作描述
        self.eng_des = ''  # 16——英文描述
        self.is_replace_spare = ''  # 17——是否更换备件 0-否；1-是
        self.risk_rank = ''  # 风险等级 1-低风险；2-中风险；3-高风险
        self.risk_des = ''  # 18——风险描述及措施
        self.create_by = 1  # 创建者
        self.create_time = ''  # 创建时间
        self.update_by = 1  # 更新者
        self.update_time = ''  # 更新时间
        self.del_flag = 0  # 删除标志位
        self.is_sent = 0  # 是否需要通讯 0 不用 1需要
        self.sent_status = 0  # 发送状态 0未发送 1已发送 2未发送数据处理报错
        self.sent_target = ''  # 发送目标
        self.is_wfpass = ''  # 审核流是否通过 true false
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

        # 暂存数据字段
        self.device_id = ''  # 设备ID
        self.role_id = ''  # 责任岗位角色ID


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
    # 用于存储设备信息
    package_instrument_Set = set()
    for j in range(1, nrows):
        work_page = WorkPackage(table.cell_value(j, 5))
        # 生成保养编码的规则,使用表中原始数据
        work_page.code = table.cell_value(j, 0)

        work_page.device_name = replaceDeviceName(table.cell_value(j, 6), table.cell_value(j, 7))
        # 周期处理
        work_page.cycle_type = 0
        cycle = 0
        if "小时" in table.cell_value(j, 11):
            work_page.cycle_type = 1
            cycle = int(table.cell_value(j, 12))
            work_page.front_tolerance = int(0 if table.cell_value(j, 13) == '' else table.cell_value(j, 13))
            work_page.back_tolerance = int(0 if table.cell_value(j, 14) == '' else table.cell_value(j, 14))
        elif "月" in table.cell_value(j, 11):
            cycle = int(float(str(table.cell_value(j, 12)).replace("月", "")) * 31)
            work_page.front_tolerance = int(0 if table.cell_value(j, 13) == '' else table.cell_value(j, 13) * 31)
            work_page.back_tolerance = int(0 if table.cell_value(j, 14) == '' else table.cell_value(j, 14) * 31)
        elif "年" in table.cell_value(j, 11):
            cycle = int(table.cell_value(j, 12)) * 366
            work_page.front_tolerance = int(0 if table.cell_value(j, 13) == '' else table.cell_value(j, 13) * 366)
            work_page.back_tolerance = int(0 if table.cell_value(j, 14) == '' else table.cell_value(j, 14) * 366)
        work_page.cycle = cycle

        work_page.pro_class = table.cell_value(j, 10)
        work_page.bus_class = table.cell_value(j, 1)
        work_page.opr_class = table.cell_value(j, 2)
        work_page.responsible_role = table.cell_value(j, 4)

        work_page.work_des = table.cell_value(j, 15)
        work_page.eng_des = table.cell_value(j, 16)
        work_page.is_replace_spare = 1 if table.cell_value(j, 17).strip() == "是" else 0
        work_page.risk_des = table.cell_value(j, 18)
        work_page.remark = table.cell_value(j, 19)

        work_package_list.append(work_page)
        responsible_role_Set.add(work_page.responsible_role)
        package_instrument_Set.add(work_page.device_name)
    return work_package_list, responsible_role_Set, package_instrument_Set


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


def gen_sql(work_package_list, work_item_list, instrument_package_list, instrument_item_list):
    """
    将保养工作包转换成新增sql语句写入文件
    """
    f = open("insert.sql", "w", encoding='utf-8')
    # 创建工作包sql
    for wp in work_package_list:
        #  处理周期
        sql = "INSERT INTO `jw_work_package`" \
              "(`id`, `name`, `code`, `cycle`, `cycle_unit`, `remark`, `pro_class`, `bus_class`, `opr_class`, `responsible_role`, `is_CMS`, `is_PMS`, " \
              "`is_commission`, `front_tolerance`, `back_tolerance`, `work_des`, `eng_des`, `is_replace_spare`, `risk_rank`, `risk_des`, " \
              "`create_by`, `create_time`, `update_by`, `update_time`, `del_flag`, `is_sent`, `sent_status`, `sent_target`, `is_wfpass`, `is_valid`, `cycle_type`, `ship_id`, `operation_type`) VALUES " \
              "({}, {}, {}, {}, '0', '', {}, {}, {}, {}, {}, {}," \
              " {}, {}, {}, {}, {}, {}, {}, {}, " \
              "'1', {}, '1', {}, '0', '0', '0', '', '', '0', '1', '102', '3');\n" \
            .format("'" + wp.id + "'", "'" + wp.name + "'", "'" + wp.code + "'",  "'" + str(wp.cycle) + "'", "'" + wp.pro_class + "'",
                    "'" + str(wp.bus_class) + "'",  "'" + str(wp.opr_class) + "'", "'" + str(wp.role_id) + "'",
                    "'" + wp.is_cms + "'", "'" + wp.is_pms + "'",
                    "'" + trans_01(wp.is_commision) + "'", "'" + str(wp.front_tolerance) + "'", "'" + str(wp.back_tolerance) + "'",
                    "\"" + wp.work_des + "\"", "\"" + wp.eng_des + "\"", "'" + str(wp.is_replace_spare) + "'",
                    "'" + wp.risk_rank + "'", "'" + wp.risk_des + "'",
                    "'" + time.strftime("%F %T") + "'", "'" + time.strftime("%F %T") + "'")
        print(wp)
        f.write(sql)
    # 创建工作明细sql
    for wi in work_item_list:
        sql = "INSERT INTO `jw_work_item` (`id`, `code`, `name`, `description`, `eng_description`," \
              " `is_replace_spare`, `is_key_work`, `PSC_defect_type`," \
              "`PSC_defect_class`, `PSC_defect_code`, `PMS_code`, `CMS_code`," \
              " `defect_property`, `remark`, `create_by`, `create_time`, `update_by`," \
              " `update_time`, `del_flag`) VALUES" \
              "({}, {}, {}, {}, {}," \
              "{},{},{}," \
              "{},{},{},{}," \
              "{},{},{},{},{}" \
              ",{},{});\n" \
            .format("'" + wi.id + "'", "'" + wi.code + "'", "'" + wi.name + "'", "'" + wi.description + "'",
                    "'" + wi.eng_description + "'",
                    "'" + wi.is_replace_spare + "'", "'" + wi.is_key_work + "'", "'" + wi.PSC_defect_type + "'",
                    "'" + wi.PSC_defect_class + "'", "'" + wi.PSC_defect_code + "'", "'" + wi.PMS_code + "'",
                    "'" + wi.CMS_code + "'",
                    "'" + wi.defect_property + "'", "'" + wi.remark + "'", "'" + wi.create_by + "'",
                    "'" + wi.create_time + "'", "'" + wi.update_by + "'",
                    "'" + wi.update_time + "'", "'" + wi.del_flag + "'", )
        print(wi)
        f.write(sql)
    # 创建设备保养包关联表sql
    for ip in instrument_package_list:
        sql = "INSERT INTO `jw_instrument_package` (`id`, `instrument_id`, `package_id`," \
              " `cycle_type`, `last_maintenance_time`, `last_time_num`," \
              " `create_by`, `create_time`, `update_by`," \
              " `update_time`, `del_flag`, `is_sent`," \
              " `sent_status`, `sent_target`, `is_wfpass`, `remark`) " \
              "VALUES({},{},{}," \
              "{},{},{}," \
              "{},{},{}," \
              "{},{},{}," \
              "{},{},{},{});\n" \
            .format("'" + ip.id + "'", "'" + ip.instrument_id + "'", "'" + ip.package_id + "'",
                    ip.cycle_type, ('null' if ip.last_maintenance_time == '' else ip.last_maintenance_time), ip.last_time_num,
                    "'" + ip.create_by + "'", "'" + ip.create_time + "'", "'" + ip.update_by + "'",
                    "'" + ip.update_time + "'", "'" + ip.del_flag + "'", "'" + ip.is_sent + "'",
                    "'" + ip.sent_status + "'", "'" + ip.sent_target + "'", "'" + ip.is_wfpass + "'",
                    "'" + ip.remark + "'")
        print(ip)
        f.write(sql)
    # 创建设备工作明细关联表sql
    for ii in instrument_item_list:
        sql = "INSERT INTO `jw_instrument_item` (`id`, `instrument_id`, `item_id`," \
              "`create_by`, `create_time`, `update_by`," \
              "`update_time`, `del_flag`, `is_sent`," \
              "`sent_status`, `sent_target`, `is_wfpass`, `remark`) VALUES " \
              "({},{},{}," \
              "{},{},{}," \
              "{},{},{}," \
              "{},{},{},{});\n" \
            .format("'" + ii.id + "'", "'" + ii.instrument_id + "'", "'" + ii.item_id + "'",
                    "'" + ii.create_by + "'", "'" + ii.create_time + "'", "'" + ii.update_by + "'",
                    "'" + ii.update_time + "'", "'" + ii.del_flag + "'", "'" + ii.is_sent + "'",
                    "'" + ii.sent_status + "'", "'" + ii.sent_target + "'", "'" + ii.is_wfpass + "'",
                    "'" + ii.remark + "'")
        print(ii)
        f.write(sql)
    f.close()


def delete_sql(work_package_list, work_item_list, instrument_package_list, instrument_item_list):
    """
    将保养工作包转换成删除sql语句写入文件
    """
    if len(work_package_list) > 0:
        f = open("rollback.sql", "w", encoding='utf-8')
        for wp in work_package_list:
            #  处理周期
            sql = "DELETE FROM `jw_work_package` WHERE id = {};\n".format("'" + wp.id + "'")
            f.write(sql)
        for wp in work_item_list:
            #  处理周期
            sql = "DELETE FROM `jw_work_item` WHERE id = {};\n".format("'" + wp.id + "'")
            f.write(sql)
        for wp in instrument_package_list:
            #  处理周期
            sql = "DELETE FROM `jw_instrument_package` WHERE id = {};\n".format("'" + wp.id + "'")
            f.write(sql)
        for wp in instrument_item_list:
            #  处理周期
            sql = "DELETE FROM `jw_instrument_item` WHERE id = {};\n".format("'" + wp.id + "'")
            f.write(sql)
        f.close()
    else:
        print("数据为空")


# def trans_cycle(cycle):
#     """
#     将保养周期转换为数据库格式
#     """
#     if cycle == "1(年)":
#         return 365
#     elif cycle == "4(年)":
#         return 365 * 4
#     elif cycle == "3(月)":
#         return 30 * 3


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


def transWorkPackageDeviceAndRole(work_package_list, responsible_role_Set, package_instrument_Set):
    """
    将工作包中的设备和责任岗位的ID进行替换
    work_package_list : 待处理的工作包
    responsible_role_Set : 工作包涉及到的责任岗位名称集合
    package_instrument_Set : 工作包涉及到的设备名称集合
    """
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
    sys_roles = session.query(SysRole).filter(SysRole.role_name.in_(responsible_role_Set)).all()

    # 查询相关设备ID
    relate_instrument_Set = set()
    for instrument_name in package_instrument_Set:
        instrument_name = instrument_name.replace("主", "")
        # 以#号分隔设备名称查询
        instrument_name_list = instrument_name.split("#")
        if len(instrument_name_list) == 2:
            # words = ['%' + instrument_name_list[0] + '%', '%'+instrument_name_list[1]+'%']
            words = ['%.' + instrument_name_list[0] + instrument_name_list[1] + '%']
        else:
            words = ['%' + instrument_name_list[0] + '%']
        rule = and_(*[JwInstrument.name.like(w) for w in words])
        instrument_list = session.query(JwInstrument).filter(rule).all()
        for instrument in instrument_list:
            relate_instrument_Set.add(instrument)

    # 将工作包数据列表中的责任岗位ID和设备ID进行替换
    for work_package in work_package_list:

        # 替换设备ID
        for relate_instrument in relate_instrument_Set:
            if (work_package.device_name == "1#主空压机") & (relate_instrument.name == "NO.1空压机"):
                print("ok")
            device_name_list = work_package.device_name.split("#")
            if relate_instrument.name.startswith("NO.") & (
                    device_name_list[0] in relate_instrument.name) & (
                    device_name_list[1].replace("主", "") in relate_instrument.name):
                work_package.device_id = relate_instrument.id
                break
        # 替换责任岗位ID
        for sys_role in sys_roles:
            if work_package.responsible_role == sys_role.role_name:
                work_package.role_id = sys_role.role_id

    return work_package_list, sys_roles, list(relate_instrument_Set)


def write_data_to_excel(work_package_list, sys_roles, package_instrument_list, opr_class_dict, bus_class_dict):
    """
    将工作包数据输出到中间表中方便检查
    work_package_list : 待处理的工作包
    responsible_role_Set : 工作包涉及到的责任岗位名称集合
    package_instrument_Set : 工作包涉及到的设备名称集合
    opr_class_dict : 作业类别字典
    bus_class_dict : 业务类别字典
    """

    # 创建一个Workbook对象，即创建一个Excel工作簿
    f = xlwt.Workbook()
    # 创建工作包信息表
    # sheet1表示Excel文件中的一个表
    # 创建一个sheet对象，命名为“工作包”，cell_overwrite_ok表示是否可以覆盖单元格，是Worksheet实例化的一个参数，默认值是False
    sheet1 = f.add_sheet(u'工作包', cell_overwrite_ok=True)
    sheet2 = f.add_sheet(u'关联设备', cell_overwrite_ok=True)
    sheet3 = f.add_sheet(u'责任岗位', cell_overwrite_ok=True)
    # 标题信息行集合
    sheet1RowTitle = [u'保养项目代码', u'业务类别', u'作业类别', u'业务部门', u'项目负责岗位', u'负责角色ID', u'保养项目名称', u'设备名称',
                      u'设备ID', u'周期单位', u'工作周期', u'前允差', u'后允差', u'工作描述', u'英文描述', u'是否更换备件', u'风险描述及措施', u'备注']
    sheet2RowTitle = [u'设备ID', u'设备名称']
    sheet3RowTitle = [u'角色ID', u'角色名称']
    # 保养明细表
    sheet4RowTitle = [u'角色ID', u'角色名称']
    # 设备保养包关联表
    sheet4RowTitle = [u'角色ID', u'角色名称']
    # 设备保养明细关联表
    sheet4RowTitle = [u'角色ID', u'角色名称']

    # 输出保养包数据
    # 遍历向表格写入标题行信息
    for i in range(0, len(sheet1RowTitle)):
        # 其中的'0'表示行, 'i'表示列，0和i指定了表中的单元格，'sheet1RowTitle[i]'是向该单元格写入的内容
        sheet1.write(0, i, sheet1RowTitle[i])
    # 遍历向表格写入工作项目信息
    for k in range(0, len(work_package_list)):  # 先遍历外层的集合，即每行数据
        sheet1.write(k + 1, 0, work_package_list[k].code)
        sheet1.write(k + 1, 1, bus_class_dict[work_package_list[k].bus_class])
        sheet1.write(k + 1, 2, opr_class_dict[work_package_list[k].opr_class])
        sheet1.write(k + 1, 3, "")
        sheet1.write(k + 1, 4, work_package_list[k].responsible_role)
        sheet1.write(k + 1, 5, work_package_list[k].role_id)
        sheet1.write(k + 1, 6, work_package_list[k].name)
        sheet1.write(k + 1, 7, work_package_list[k].device_name)
        sheet1.write(k + 1, 8, work_package_list[k].device_id)
        sheet1.write(k + 1, 9, work_package_list[k].cycle_type)
        sheet1.write(k + 1, 10, work_package_list[k].cycle)
        sheet1.write(k + 1, 11, work_package_list[k].front_tolerance)
        sheet1.write(k + 1, 12, work_package_list[k].back_tolerance)
        sheet1.write(k + 1, 13, work_package_list[k].work_des)
        sheet1.write(k + 1, 14, work_package_list[k].eng_des)
        sheet1.write(k + 1, 15, work_package_list[k].is_replace_spare)
        sheet1.write(k + 1, 16, work_package_list[k].risk_des)
        sheet1.write(k + 1, 17, work_package_list[k].remark)
    # 输出设备数据
    for i in range(0, len(sheet2RowTitle)):
        sheet2.write(0, i, sheet2RowTitle[i])
    for k in range(0, len(package_instrument_list)):  # 先遍历外层的集合，即每行数据
        sheet2.write(k + 1, 0, package_instrument_list[k].id)
        sheet2.write(k + 1, 1, package_instrument_list[k].name)
    # 输出角色数据
    for i in range(0, len(sheet3RowTitle)):
        sheet3.write(0, i, sheet3RowTitle[i])
    for k in range(0, len(sys_roles)):  # 先遍历外层的集合，即每行数据
        sheet3.write(k + 1, 0, sys_roles[k].role_id)
        sheet3.write(k + 1, 1, sys_roles[k].role_name)
    # 保存文件的路径及命名
    f.save('C:/Users/admin/Desktop/2022年11月24日导入工作包/数据校对.xls')


if __name__ == '__main__':
    # 从Excel中读取数据
    work_package_list, responsible_role_Set, package_instrument_Set = copy_data_to_object(
        'C:/Users/admin/Desktop/2022年11月24日导入工作包/嘉庚号助力系统基础数据.xlsx')
    # 将工作包的设备和责任岗位进行处理
    work_package_list, sys_roles, package_instrument_list = transWorkPackageDeviceAndRole(work_package_list,
                                                                                          responsible_role_Set,
                                                                                          package_instrument_Set)
    # 作业类别字典
    opr_class_dict = {'全面检查': '1', '目视检查': '2', '功能测试': '3'}
    bus_class_dict = {'法定和船级检验': '1', '外部审核': '2', '周期维护': '3'}

    # 生成各种关联表数据
    # 1、生成保养明细表数据
    work_item_list = []
    instrument_package_list = []
    instrument_item_list = []
    for i in range(0, len(work_package_list)):
        if "。" in work_package_list[i].work_des:
            work_des_list = work_package_list[i].work_des.split("。")
            for j in range(0, len(work_des_list)):
                print(work_package_list[i].name)
                code = "BY100" + str(618 + len(work_item_list)).zfill(7)
                work_des = work_des_list[j]
                work_item = JwWorkItem(work_package_list[i].name, code, work_des_list[j], work_package_list[i].eng_des,
                                       work_package_list[i].is_replace_spare)
                work_item_list.append(work_item)
                instrumentItem = JwInstrumentItem()
                instrumentItem.instrument_id = work_package_list[i].device_id
                instrumentItem.item_id = work_item.id
                instrument_item_list.append(instrumentItem)
        instrument_package = JwInstrumentPackage()
        instrument_package.instrument_id = work_package_list[i].device_id
        instrument_package.package_id = work_package_list[i].id
        instrument_package.cycle_type = work_package_list[i].cycle_type
        instrument_package_list.append(instrument_package)

    # 输出中间表检查数据
    write_data_to_excel(work_package_list, sys_roles, package_instrument_list, opr_class_dict, bus_class_dict)

    # 生成创建SQL语句

    # 生成回滚删除SQL语句

    gen_sql(work_package_list, work_item_list, instrument_package_list, instrument_item_list)
    delete_sql(work_package_list, work_item_list, instrument_package_list, instrument_item_list)
    print("ok")
