# -*- coding: UTF-8 -*-
# 用于将表格中的数据提炼出工作包数据

import xlrd
import xlwt
import uuid

import entity
import replaceDeviceName


class WorkItem:
    """工作项目类"""

    def __init__(self, name):
        self.id = str(uuid.uuid1()).replace('-', '')  # 保养项目ID
        self.code = None  # 保养编码
        self.name = name  # 保养项目名称
        self.device_name = None  # 设备名称，用于切分excel表格中的多个设备
        self.description = None  # 中文描述
        self.eng_description = None  # 英文描述
        self.is_replace_spare = None  # 是否更换备件 0-否；1-是
        self.is_key_work = None  # 是否为关键工作 0-否；1-是
        self.PSC_defect_type = None  # PSC缺陷类型
        self.PSC_defect_class = None  # PSC缺陷细分类
        self.PSC_defect_code = None  # PMS缺陷代码
        self.PMS_code = None  # PMS编码
        self.CMS_code = None  # CMS编码
        self.defect_property = None  # 缺陷性质
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
        self.item_type = 0  # 工作类型 0-新增;1-PMS;2-CMS;3-PSC;4-附属工作内容
        self.pid = None  # 附属工作内容所属的项目id
        self.CMS_type = None  # CMS类型





def trans_excel_data_to_work_item_list(filename, code):
    """
    将Excel表格中的数据转换为工作项目对象列表
    filename 文件路径
    code 当前数据表中的最大编码
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("基数数据-工作项目(必填)")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 返回由该行中所有的单元格对象组成的列表,这与tabel.raw()方法并没有区别。
    ncols = table.ncols
    # 获取数据
    work_item_list = []  # 空列表
    for j in range(1, nrows):
        work_item = WorkItem(table.cell_value(j, 1))
        code += 1
        work_item.code = 'BY' + str(code)
        work_item.description = table.cell_value(j, 3)
        work_item.eng_description = table.cell_value(j, 4)
        work_item.device_name = table.cell_value(j, 5)
        work_item.is_key_work = table.cell_value(j, 7)
        work_item.remark = table.cell_value(j, 8)
        work_item.device_name = replaceDeviceName.replaceDeviceName(table.cell_value(j, 5))
        work_item_list.append(work_item)
    return work_item_list


def trans_excel_data_to_package_item_list(filename):
    """
    将Excel表格中的数据转换为工作包关联工作项目对象列表
    filename 文件路径
    """
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("基础数据-所属关系（尽量填）")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 返回由该行中所有的单元格对象组成的列表,这与tabel.raw()方法并没有区别。
    ncols = table.ncols
    # 获取数据
    work_package_item_list = []  # 空列表
    for j in range(1, nrows):
        work_package_item = entity.WorkPackageItem('', table.cell_value(j, 1), '', table.cell_value(j, 3))
        work_package_item_list.append(work_package_item)
    return work_package_item_list


def trans_excel_data_to_item_instrument_list(work_item_list):
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


def trans_instrument_list(item_instrument_list):
    """
    从工作项目列表中提取项目设备关联列表
    work_item_list 工作项目
    """
    instrument_list = []
    for item_instrument in item_instrument_list:
        instrument_list.append(item_instrument.device_name)
    # 去重
    instrument_list = set(instrument_list)
    instrument_list = list(instrument_list)
    instrument_list.sort()
    return instrument_list


def copy_data_to_object(filename):
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("基数数据-工作项目(必填)")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 返回由该行中所有的单元格对象组成的列表,这与tabel.raw()方法并没有区别。
    ncols = table.ncols
    # 获取数据
    work_item_list = []  # 空列表
    for j in range(1, nrows):
        work_item = WorkItem(table.cell_value(j, 1))
        work_item.description = table.cell_value(j, 3)
        work_item.eng_description = table.cell_value(j, 4)
        work_item.device_name = table.cell_value(j, 5)
        work_item.is_key_work = table.cell_value(j, 7)
        work_item.remark = table.cell_value(j, 8)
        work_item.device_name = table.cell_value(j, 5).replace("瓶位、", "瓶位").replace("瓶位、", "瓶位").replace(" ", "")
        work_item_device_list = work_item.device_name.split("、")
        if len(work_item_device_list) > 1:
            for device in work_item_device_list:
                work_item_children = WorkItem(table.cell_value(j, 1))
                work_item_children.description = table.cell_value(j, 3)
                work_item_children.eng_description = table.cell_value(j, 4)
                work_item_children.device_name = table.cell_value(j, 5)
                work_item_children.is_key_work = table.cell_value(j, 7)
                work_item_children.remark = table.cell_value(j, 8)
                work_item_children.device_name = table.cell_value(j, 5)
                work_item_children.device_name = device.replace("\n", "")
                work_item_list.append(work_item_children)
                print(work_item_children.__dict__)
        else:
            work_item_list.append(work_item)
            print(work_item.__dict__)
    print("完成啦！")
    for work_item in work_item_list:
        print(work_item.__dict__)
    write_data_to_excel(work_item_list)


def write_data_to_excel(work_item_list):
    # 创建一个Workbook对象，即创建一个Excel工作簿
    f = xlwt.Workbook()
    # 创建工作包信息表
    # sheet1表示Excel文件中的一个表
    # 创建一个sheet对象，命名为“工作包”，cell_overwrite_ok表示是否可以覆盖单元格，是Worksheet实例化的一个参数，默认值是False
    sheet1 = f.add_sheet(u'工作包', cell_overwrite_ok=True)
    sheet2 = f.add_sheet(u'关联设备名称', cell_overwrite_ok=True)
    # 标题信息行集合
    rowTitle = [u'保养项目代码', u'保养项目名称', u'项目中文描述', u'项目英文描述', u'设备名称', u'设备ID', u'是否关键工作',u'备注']
    sheet2RowTitle = [u'设备ID', u'设备名称']
    work_item_device_list = []
    # 遍历向表格写入标题行信息
    for i in range(0, len(rowTitle)):
        # 其中的'0'表示行, 'i'表示列，0和i指定了表中的单元格，'rowTitle[i]'是向该单元格写入的内容
        sheet1.write(0, i, rowTitle[i])
    # 遍历向表格写入工作项目信息
    for k in range(0, len(work_item_list)):  # 先遍历外层的集合，即每行数据
            sheet1.write(k + 1, 0, "保养项目代码")
            sheet1.write(k + 1, 1, work_item_list[k].name)
            sheet1.write(k + 1, 2, work_item_list[k].description)
            sheet1.write(k + 1, 3, work_item_list[k].eng_description)
            sheet1.write(k + 1, 4, work_item_list[k].device_name)
            sheet1.write(k + 1, 5, "设备ID")
            sheet1.write(k + 1, 6, work_item_list[k].is_key_work)
            sheet1.write(k + 1, 7, work_item_list[k].remark)
            work_item_device_list.append(work_item_list[k].device_name)

    work_item_device_list = set(work_item_device_list)
    work_item_device_list = list(work_item_device_list)
    for i in range(0, len(sheet2RowTitle)):
        sheet2.write(0, i, sheet2RowTitle[i])
        # 遍历向表格写入学生信息
    for k in range(0, len(work_item_device_list)):  # 先遍历外层的集合，即每行数据
        sheet2.write(k + 1, 0, "设备ID")
        sheet2.write(k + 1, 1, work_item_device_list[k])
    # 保存文件的路径及命名
    f.save('C:/Users/admin/Desktop/数据校对/transWorkItem.xls')


if __name__ == '__main__':
    copy_data_to_object('C:/Users/admin/Desktop/数据校对/维修保养基础数据-水文气象组设备-20210714(1)(1).xlsx')

