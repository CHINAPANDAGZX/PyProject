# -*- coding: UTF-8 -*-
# 用于将转换的Excel中间表数据读取出来

import xlrd
import genWorkPackageSql
import transWorkItem
import entity


def copy_work_package_by_middle_table(filename):
    """
    从中间表中读取工作包数据
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("工作包")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 获取数据
    work_package_list = []  # 空列表
    work_package_dict = {}
    for j in range(1, nrows):
        work_page = genWorkPackageSql.WorkPackage(table.cell_value(j, 1))
        work_page.id = table.cell_value(j, 0)
        work_page.pro_class = table.cell_value(j, 2)
        work_page.bus_class = table.cell_value(j, 3)
        work_page.opr_class = table.cell_value(j, 4)
        work_page.responsible_role = table.cell_value(j, 5)
        work_page.is_cms = table.cell_value(j, 6)
        work_page.is_pms = table.cell_value(j, 7)
        work_page.is_commision = table.cell_value(j, 8)
        work_page.cycle = table.cell_value(j, 10)
        work_page.front_tolerance = table.cell_value(j, 11)
        work_page.back_tolerance = table.cell_value(j, 12)
        work_page.work_des = table.cell_value(j, 13)
        work_page.eng_des = table.cell_value(j, 14)
        work_page.is_replace_spare = table.cell_value(j, 15)
        work_page.risk_rank = table.cell_value(j, 16)
        work_page.risk_des = table.cell_value(j, 17)
        work_package_list.append(work_page)
        work_package_dict[work_page.name] = work_page.id
    work_package_dict['水文气象设备-自选周期性-1年保养'] = 'c0fab938ffcc8e70917cda79a0f6423f'
    work_package_dict['水文气象设备-自选周期性-6月保养'] = '381553611bdbd03d36ca0f5cf73925f0'
    work_package_dict['水文气象设备-自选周期性-1天保养'] = '0548a7abc5e454a0c467748fee21d0a4'
    return work_package_list, work_package_dict


def copy_work_item_by_middle_table(filename):
    """
    从中间表中读取工作项目数据
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("工作项目")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 获取数据
    work_item_list = []  # 空列表
    work_item_dict = {}
    for j in range(1, nrows):
        work_item = transWorkItem.WorkItem(table.cell_value(j, 2))
        work_item.id = table.cell_value(j, 0)
        work_item.code = table.cell_value(j, 1)
        work_item.description = table.cell_value(j, 3)
        work_item.eng_description = table.cell_value(j, 4)
        work_item.is_key_work = table.cell_value(j, 5)
        work_item.remark = table.cell_value(j, 6)
        work_item_list.append(work_item)
        work_item_dict[work_item.name] = work_item.id
    return work_item_list, work_item_dict


def copy_instrument_by_middle_table(filename):
    """
    从中间表中读取设备数据
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("设备")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 获取数据
    instrument_list = []  # 空列表
    instrument_dict = {}
    for j in range(1, nrows):
        instrument = entity.Instrument(table.cell_value(j, 0), table.cell_value(j, 1))
        instrument_list.append(instrument)
        instrument_dict[instrument.name] = instrument.id
    return instrument_list, instrument_dict


def copy_package_item_by_middle_table(filename, work_package_dict, work_item_dict):
    """
    从中间表中读取设备数据
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("工作包-工作项目-关联表")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 获取数据
    work_package_item_list = []  # 空列表
    for j in range(1, nrows):
        package_name = table.cell_value(j, 1)
        package_id = work_package_dict[package_name]
        item_name = table.cell_value(j, 3)
        item_id = work_item_dict[item_name]
        work_package_item = entity.WorkPackageItem(package_id, package_name, item_id, item_name)
        work_package_item_list.append(work_package_item)
    return work_package_item_list

def copy_item_instrument_by_middle_table(work_item_list):
    """
    从工作项目列表中提取项目设备关联列表
    work_item_list 工作项目
    """
    item_instrument_list = []
    for work_item in work_item_list:
        work_item_device_list = work_item.device_name.replace("瓶位、", "瓶位").split("、")
        if len(work_item_device_list) > 1:
            for device in work_item_device_list:
                item_instrument = WorkItem(work_item.name)
                item_instrument.code = work_item.code
                item_instrument.description = work_item.description
                item_instrument.eng_description = work_item.eng_description
                item_instrument.is_key_work = work_item.is_key_work
                item_instrument.remark = work_item.remark
                item_instrument.device_name = device.replace("\n", "")
                item_instrument_list.append(item_instrument)
        else:
            item_instrument_list.append(work_item)
    return item_instrument_list
