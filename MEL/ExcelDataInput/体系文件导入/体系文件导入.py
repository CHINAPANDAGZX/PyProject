import uuid
import pandas as pd

# 加载Excel文件
file_path = '副本要更新的体系文件RX.xlsx'  # 替换为实际文件路径
xls = pd.ExcelFile(file_path)

# 读取第一个Sheet（根据实际情况选择Sheet）
df = pd.read_excel(xls, sheet_name=0)

# 定义角色对应关系（键和值都是字符串）
role_mapping = {
    '系统管理员': '1',
    '普通角色': '2',
    '船长': '100',
    '大副': '101',
    '二副': '102',
    '三副': '103',
    '水手长': '104',
    '水手': '105',
    '大厨': '106',
    '二厨': '107',
    '服务员': '108',
    '轮机长': '109',
    '大管轮': '110',
    '二管轮': '111',
    '三管轮': '112',
    '电机员': '113',
    '机工长': '114',
    '机工': '115',
    '船管中心普通员工': '116',
    '部门主管': '117',
    '探测员': '118',
    '探测长': '119',
    '财务管理员': '120',
    '资产管理员': '121',
    '档案管理员': '122',
    '行政主管': '123',
    '中心主任': '124',
    '国贸-机务经理': '125',
    '机务主办': '126',
    '国贸-总经理': '127',
    '采购确认角色': '128',
    '探测部-水文气象组': '129',
    '探测部-甲板支撑组': '130',
    '探测部-地球物理组': '131',
    '探测部-信息网络组': '132',
    '探测部-设备管理员': '133',
    '实验室设备管理员': '135',
    '采购状态跟踪设置': '136',
    '国贸协调员': '137',
    '国贸-海务经办人': '138',
    '国贸-运营总监': '139',
    '出海统一录入角色': '140',
    '岸端体系DP': '301',
    '岸端体系海务': '302',
    '岸端体系机务': '303',
    '岸端体系综合': '304'
}

# 定义SQL模板
insert_sql_template = """
INSERT INTO `tx_sms_file` (
    `id`, `file_no`, `file_name`, `read_level`, `trigger_condition`, 
    `report_cycle`, `report_cycle_unit`, `report_role`, `land_dept`, 
    `is_enable`, `is_sure`, `remark`, `operating_mode`
) VALUES (
    '{id}', '{file_no}', '{file_name}', '{read_level}', '{trigger_condition}', 
    {report_cycle}, {report_cycle_unit}, '{report_role}', '{land_dept}', 
    '{is_enable}', '{is_sure}', {remark}, '{operating_mode}'
);
"""

update_sql_template = """
UPDATE `tx_sms_file`
SET 
    `file_no` = '{file_no}',
    `read_level` = '{read_level}',
    `trigger_condition` = '{trigger_condition}',
    `report_cycle` = {report_cycle},
    `report_cycle_unit` = {report_cycle_unit},
    `report_role` = '{report_role}',
    `land_dept` = '{land_dept}',
    `is_enable` = '{is_enable}',
    `is_sure` = '{is_sure}',
    `remark` = {remark},
    `operating_mode` = '{operating_mode}'
WHERE `id` = '{id}';
"""

# 初始化SQL语句列表
insert_sql_statements = []
update_sql_statements = []

# 格式化字段值，确保合法
def format_value(value):
    if pd.isna(value):
        return None
    elif isinstance(value, str):
        return value.replace("'", "''") # 替换单引号为双单引号
    else:
        return value


# 遍历DataFrame，生成SQL语句
for index, row in df.iterrows():
    # 提取数据
    id = row.get('id', None)
    file_no = row.get('file_name', '').split(' ')[0]  # 假设文件编号是文件名的第一部分
    file_name = row.get('file_name', '')
    read_level = row.get('文件类型 0体系文件 2运作表格', '')
    trigger_condition = row.get('触发方式（0 时间周期 1 手动触发）', 0)
    report_cycle = row.get('上报周期', 1)
    report_cycle_unit = row.get('上报周期单位 0年 1月', 0)
    report_role_ids = row.get('上报岗位', '')
    land_dept = row.get('岸端部门 0DP 1海务 2机务 3综合', '')
    is_enable = row.get('是否回签', 1)
    is_sure = row.get('是否回签 0否 1是', '')  # 获取原始值
    remark = row.get('备注', '')
    operating_mode = row.get('运作逻辑 1自动生成文件 2自动生成接续文件', '')



    # 替换角色名称为角色ID
    if pd.notna(report_role_ids):  # 检查是否为非空值
        report_role_ids = str(report_role_ids)  # 确保是字符串
        report_role_list = []
        for role_name in report_role_ids.split(','):
            role_name = role_name.strip()  # 去除可能的空格
            role_id = role_mapping.get(role_name, None)  # 获取角色ID，如果找不到则为None
            if role_id is not None:
                report_role_list.append(role_id)
        if report_role_list:  # 如果有匹配的角色ID
            report_role = ','.join(report_role_list)
        else:  # 如果没有匹配的角色ID，设置为NULL
            report_role = None
    else:
        report_role = None  # 如果为空，则设置为NULL

    # 格式化字段值
    file_no = format_value(file_no)
    file_name = format_value(file_name)
    read_level = format_value(read_level)
    trigger_condition = format_value(trigger_condition)
    report_cycle = format_value(report_cycle)
    report_cycle_unit = format_value(report_cycle_unit)
    report_role = format_value(report_role)
    land_dept = format_value(land_dept)
    is_enable = format_value(is_enable)
    is_sure = format_value(is_sure)  # 使用format_value确保is_sure为NULL或字符串
    remark = format_value(remark)
    operating_mode = format_value(operating_mode)

    # 确保report_cycle是整数
    if report_cycle == 'NULL':
        report_cycle = 'NULL'
    else:
        try:
            report_cycle = int(report_cycle)
        except (ValueError, TypeError):
            report_cycle = 0  # 如果无法转换为整数，则设置为默认值0

    # 确保report_cycle是整数
    if report_cycle_unit == 'NULL':
        report_cycle_unit = 'NULL'
    else:
        try:
            report_cycle_unit = int(report_cycle_unit)
        except (ValueError, TypeError):
            report_cycle_unit = 0  # 如果无法转换为整数，则设置为默认值0

    # 确保remark字段在没有值时使用NULL
    if remark == 'NULL':
        remark = 'NULL'
    elif remark == '':
        remark = 'NULL'
    else:
        remark = f"'{remark}'"  # 有值时加单引号

    # 调试信息：打印trigger_condition和operating_mode的值
    print(f"ID: {id}, Trigger Condition: {trigger_condition}, Operating Mode: {operating_mode}")

    # 处理is_sure字段
    if pd.notna(is_sure):
        is_sure = str(is_sure).strip()  # 转换为字符串并去除空格
        if is_sure in ['1', '1.0']:  # 如果值为1或1.0，保留为'1'
            is_sure = '1'
        else:  # 其他情况（包括0、0.0、空字符串等），改为'0'
            is_sure = '0'
    else:  # 如果is_sure为空（NaN），也改为'0'
        is_sure = '0'

    # 根据是否存在id，生成对应的SQL语句
    if pd.isna(id):
        # 生成32位UUID
        id = str(uuid.uuid4()).replace('-', '')
        # 生成INSERT语句
        sql = insert_sql_template.format(
            id=id,
            file_no=file_no,
            file_name=file_name,
            read_level=read_level,
            trigger_condition=trigger_condition,
            report_cycle=report_cycle,
            report_cycle_unit=report_cycle_unit,
            report_role=report_role,
            land_dept=land_dept,
            is_enable=is_enable,
            is_sure=is_sure,
            remark=remark,
            operating_mode=operating_mode
        )
        insert_sql_statements.append(sql)
    else:
        # 生成UPDATE语句
        sql = update_sql_template.format(
            id=id,
            file_no=file_no,
            read_level=read_level,
            trigger_condition=trigger_condition,
            report_cycle=report_cycle,
            report_cycle_unit=report_cycle_unit,
            report_role=report_role,
            land_dept=land_dept,
            is_enable=is_enable,
            is_sure=is_sure,
            remark=remark,
            operating_mode=operating_mode
        )
        update_sql_statements.append(sql)

# 将SQL语句保存到文件
with open('insert_sql_statements.sql', 'w', encoding='utf-8') as insert_file:
    insert_file.writelines(insert_sql_statements)

with open('update_sql_statements.sql', 'w', encoding='utf-8') as update_file:
    update_file.writelines(update_sql_statements)

print("SQL语句已生成并保存到当前目录下的 'insert_sql_statements.sql' 和 'update_sql_statements.sql' 文件中。")