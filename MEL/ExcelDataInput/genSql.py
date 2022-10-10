# -*- coding: UTF-8 -*-
# 用于总体控制，将表格中的数据提炼为sql语句
import genWorkPackageSql
import readMiddleTable
import transWorkItem
import xlwt

source_excel_path = 'C:/Users/admin/Desktop/数据校对/维修保养基础数据-水文气象组设备-20210714(1)(1).xlsx'
output_excel_path = 'C:/Users/admin/Desktop/数据校对/中间表.xls'


def write_data_to_excel(work_package_list, work_package_item_list, work_item_list, item_instrument_list, instrument_package_list, instrument_list):
    """
    将所有数据输出到Excel做成中间表
    work_package_list 工作包列表
    work_item_list 工作项目列表
    instrument_list 设备列表
    """
    # 创建一个Workbook对象，即创建一个Excel工作簿
    f = xlwt.Workbook()
    # sheet1表示Excel文件中的一个表
    # 创建sheet对象，cell_overwrite_ok表示是否可以覆盖单元格，是Worksheet实例化的一个参数，默认值是False
    work_package_sheet = f.add_sheet(u'工作包', cell_overwrite_ok=True)
    work_package_item_sheet = f.add_sheet(u'工作包-工作项目-关联表', cell_overwrite_ok=True)
    work_item_sheet = f.add_sheet(u'工作项目', cell_overwrite_ok=True)
    work_item_instrument_sheet = f.add_sheet(u'工作项目-设备-关联表', cell_overwrite_ok=True)
    work_instrument_package_sheet = f.add_sheet(u'工作包-设备-关联表', cell_overwrite_ok=True)
    work_instrument_sheet = f.add_sheet(u'设备', cell_overwrite_ok=True)
    # 创建各表标题信息
    work_package_title = [u'工作包编码', u'工作包名称', u'项目类别', u'业务类别', u'作业类别',
                          u'项目负责岗位', u'是否循环检验(CMS)', u'是否船级相关PMS', u'是否委托',
                          u'周期单位', u'工作周期', u'前允差', u'后允差', u'工作描述', u'英文描述',
                          u'需换新备件', u'风险等级', u'风险描述及措施', u'备注']
    work_package_item_title = [u'工作包编码', u'工作包名称 ', u'保养项目代码', u'保养项目名称']
    work_item_title = [u'保养项目ID', u'保养项目代码', u'保养项目名称', u'项目中文描述', u'项目英文描述', u'是否关键工作', u'备注']
    work_item_instrument_title = [u'保养项目代码', u'保养项目名称', u'项目中文描述', u'项目英文描述', u'设备名称', u'设备ID', u'是否关键工作', u'备注']
    work_instrument_package_title = [u'保养包ID', u'保养包名称', u'设备ID', u'设备名称']
    work_instrument_sheet_title = [u'设备ID', u'设备名称']
    # 写入各表标题行
    for i in range(0, len(work_package_title)):
        # 其中的'0'表示行, 'i'表示列，0和i指定了表中的单元格，'rowTitle[i]'是向该单元格写入的内容
        work_package_sheet.write(0, i, work_package_title[i])
    for i in range(0, len(work_package_item_title)):
        work_package_item_sheet.write(0, i, work_package_item_title[i])
    for i in range(0, len(work_item_title)):
        work_item_sheet.write(0, i, work_item_title[i])
    for i in range(0, len(work_item_instrument_title)):
        work_item_instrument_sheet.write(0, i, work_item_instrument_title[i])
    for i in range(0, len(work_instrument_package_title)):
        work_instrument_package_sheet.write(0, i, work_instrument_package_title[i])
    for i in range(0, len(work_instrument_sheet_title)):
        work_instrument_sheet.write(0, i, work_instrument_sheet_title[i])
    # 工作包表
    for k in range(0, len(work_package_list)):  # 先遍历外层的集合，即每行数据
        work_package_sheet.write(k + 1, 0, work_package_list[k].id)
        work_package_sheet.write(k + 1, 1, work_package_list[k].name)
        work_package_sheet.write(k + 1, 2, work_package_list[k].pro_class)
        work_package_sheet.write(k + 1, 3, work_package_list[k].bus_class)
        work_package_sheet.write(k + 1, 4, work_package_list[k].opr_class)
        work_package_sheet.write(k + 1, 5, work_package_list[k].responsible_role)
        work_package_sheet.write(k + 1, 6, work_package_list[k].is_cms)
        work_package_sheet.write(k + 1, 7, work_package_list[k].is_pms)
        work_package_sheet.write(k + 1, 8, work_package_list[k].is_commision)
        work_package_sheet.write(k + 1, 10, work_package_list[k].cycle)
        work_package_sheet.write(k + 1, 11, work_package_list[k].front_tolerance)
        work_package_sheet.write(k + 1, 12, work_package_list[k].back_tolerance)
        work_package_sheet.write(k + 1, 13, work_package_list[k].work_des)
        work_package_sheet.write(k + 1, 14, work_package_list[k].eng_des)
        work_package_sheet.write(k + 1, 15, work_package_list[k].is_replace_spare)
        work_package_sheet.write(k + 1, 16, work_package_list[k].risk_rank)
        work_package_sheet.write(k + 1, 17, work_package_list[k].risk_des)
    # 工作包关联工作项目表
    for k in range(0, len(work_package_item_list)):
        work_package_item_sheet.write(k + 1, 1, work_package_item_list[k].package_name)
        work_package_item_sheet.write(k + 1, 3, work_package_item_list[k].item_name)
    # 工作项目表
    for k in range(0, len(work_item_list)):
        work_item_sheet.write(k + 1, 0, work_item_list[k].id)
        work_item_sheet.write(k + 1, 1, work_item_list[k].code)
        work_item_sheet.write(k + 1, 2, work_item_list[k].name)
        work_item_sheet.write(k + 1, 3, work_item_list[k].description)
        work_item_sheet.write(k + 1, 4, work_item_list[k].eng_description)
        work_item_sheet.write(k + 1, 5, work_item_list[k].is_key_work)
        work_item_sheet.write(k + 1, 6, work_item_list[k].remark)
    # 工作项目关联设备表
    for k in range(0, len(item_instrument_list)):
        work_item_instrument_sheet.write(k + 1, 0, item_instrument_list[k].code)
        work_item_instrument_sheet.write(k + 1, 1, item_instrument_list[k].name)
        work_item_instrument_sheet.write(k + 1, 2, item_instrument_list[k].description)
        work_item_instrument_sheet.write(k + 1, 3, item_instrument_list[k].eng_description)
        work_item_instrument_sheet.write(k + 1, 4, item_instrument_list[k].device_name)
        work_item_instrument_sheet.write(k + 1, 5, "")
        work_item_instrument_sheet.write(k + 1, 6, item_instrument_list[k].is_key_work)
        work_item_instrument_sheet.write(k + 1, 7, item_instrument_list[k].remark)
    # 工作包关联设备表
    for k in range(0, len(instrument_package_list)):
        work_instrument_package_sheet.write(k + 1, 0, instrument_package_list[k].package_id)
        work_instrument_package_sheet.write(k + 1, 1, instrument_package_list[k].package_name)
        work_instrument_package_sheet.write(k + 1, 2, instrument_package_list[k].device_id)
        work_instrument_package_sheet.write(k + 1, 3, instrument_package_list[k].device_name)
    # 设备表
    for k in range(0, len(instrument_list)):
        work_instrument_sheet.write(k + 1, 0, "")
        work_instrument_sheet.write(k + 1, 1, instrument_list[k])

    # 保存文件的路径及命名
    f.save(output_excel_path)


def genEcxel():
    """
    根据Excel表格，整理数据，并重新生成xcel中间表输出
    """
    # 获取工作包
    work_package_list = genWorkPackageSql.copy_data_to_object(source_excel_path)
    # 获取工作包设备关联表
    instrument_package_list = genWorkPackageSql.trans_excel_data_to_instrument_package_list(work_package_list)
    # 获取工作包项目关联表
    work_package_item_list = transWorkItem.trans_excel_data_to_package_item_list(source_excel_path)
    # 获取工作项目
    work_item_list = transWorkItem.trans_excel_data_to_work_item_list(source_excel_path, 1020000597)
    # 项目设备关联列表
    item_instrument_list = transWorkItem.trans_excel_data_to_item_instrument_list(work_item_list)
    # 设备列表
    instrument_list = transWorkItem.trans_instrument_list(item_instrument_list)

    # 将中间数据全部写入到Excel表中
    write_data_to_excel(work_package_list, work_package_item_list, work_item_list, item_instrument_list,instrument_package_list, instrument_list)


if __name__ == '__main__':
    # genEcxel()
    # 读取工作包列表
    work_package_list, work_package_dict = readMiddleTable.copy_work_package_by_middle_table(output_excel_path)
    # 读取工作项目列表
    work_item_list, work_item_dict = readMiddleTable.copy_work_item_by_middle_table(output_excel_path)
    # 读取设备列表
    instrument_list, instrument = readMiddleTable.copy_instrument_by_middle_table(output_excel_path)
    # 读取并拼凑出工作包和工作项目关联列表
    work_package_list = readMiddleTable.copy_package_item_by_middle_table(output_excel_path, work_package_dict, work_item_dict)
    # 读取并拼凑出工作项目和设备关联列表

    for wp in work_package_list:
        print(wp.__dict__)

    # genWorkPackageSql.gen_sql(work_package_list)
    # genWorkPackageSql.delete_sql(work_package_list)