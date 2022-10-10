# -*- coding: UTF-8 -*-
# 用于将表格中的数据提炼出工作包数据

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import xlrd
import xlwt
import uuid


class WorkPackage:
    """工作包类"""
    empCount = 0

    def __init__(self, id, name):
        self.id = str(uuid.uuid1()).replace('-', '')  # 保养包ID
        self.name = name  # 保养包名称——1
        self.code = None  # 保养包编码——0
        self.cycle = None  # 保养包周期——9
        self.pro_class = None  # 项目分类（项目类别）——3
        self.bus_class = None  # 业务类别——4
        self.opr_class = None  # 作业类别——5
        self.is_cms = None  # 是否CMS相关 0-否；1-是(是否循环检验（CMS）)——6
        self.is_pms = None  # 是否PMS相关 0-否；1-是(是否船级相关PMS)——7
        self.is_commision = None  # 是否委托 0-否；1-是(是否委托)——8
        self.front_tolerance = None  # 前允差——11
        self.back_tolerance = None  # 后允差——12
        self.work_des = None  # 工作描述——13
        self.eng_des = None  # 英文描述——14
        self.is_replace_spare = None  # 是否更换备件 0-否；1-是——15
        self.risk_rank = None  # 风险等级 1-低风险；2-中风险；3-高风险——16
        self.risk_des = None  # 风险等级 1-低风险；2-中风险；3-高风险——17
        self.create_by = 1  # 创建者
        self.create_time = None  # 创建时间
        self.update_by = 1  # 更新者
        self.update_time = None  # 更新时间
        self.del_flag = 0  # 删除标志位
        self.is_sent = None  # 是否需要通讯 0 不用 1需要
        self.sent_status = None  # 发送状态 0未发送 1已发送 2未发送数据处理报错
        self.sent_target = None  # 发送目标
        self.is_wfpass = None  # 审核流是否通过 true false
        self.is_valid = None  # 是否生效 0-否；1-是
        self.cycle_type = None  # 周期计算方式 0-时间周期 1-计数周期——10
        self.ship_id = None  # 所属位置
        self.operation_type = None  # 操作方式？
        WorkPackage.empCount += 1

    # def displayCount(self):
    #     print
    #     "Total Employee %d" % Employee.empCount
    #
    # def displayEmployee(self):
    #     print
    #     "Name : ", self.name, ", Salary: ", self.salary


def copy_data_to_object(filename):
    data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
    table = data.sheet_by_name("基础数据-工作包(必填)")  # 通过名称获取
    nrows = table.nrows  # 获取该sheet中的行数，注，这里table.nrows后面不带().
    # 返回由该行中所有的单元格对象组成的列表,这与tabel.raw()方法并没有区别。
    ncols = table.ncols
    # 获取数据
    work_package_list = []  # 空列表
    for j in range(1, nrows):
        work_page = WorkPackage("", table.cell_value(j, 1))
        work_page.code = table.cell_value(j, 0)
        work_page.cycle = table.cell_value(j, 10)
        work_page.cycle_type = table.cell_value(j, 11)
        work_page.pro_class = table.cell_value(j, 2)
        work_page.bus_class = table.cell_value(j, 3)
        work_page.opr_class = table.cell_value(j, 4)
        work_page.is_cms = table.cell_value(j, 7)
        work_page.is_pms = table.cell_value(j, 8)
        work_page.is_commision = table.cell_value(j, 9)
        work_page.front_tolerance = table.cell_value(j, 12)
        work_page.back_tolerance = table.cell_value(j, 13)
        work_page.work_des = table.cell_value(j, 14)
        work_page.eng_des = table.cell_value(j, 15)
        work_page.is_replace_spare = table.cell_value(j, 16)
        work_page.risk_rank = table.cell_value(j, 17)
        work_page.risk_des = table.cell_value(j, 18)
        work_package_list.append(work_page)
    print("完成啦！")
    write_data_to_excel(work_package_list)

def write_data_to_excel(work_package_list):
    # 创建一个Workbook对象，即创建一个Excel工作簿
    f = xlwt.Workbook()
    # 创建工作包信息表
    # sheet1表示Excel文件中的一个表
    # 创建一个sheet对象，命名为“工作包”，cell_overwrite_ok表示是否可以覆盖单元格，是Worksheet实例化的一个参数，默认值是False
    sheet1 = f.add_sheet(u'工作包', cell_overwrite_ok=True)

    # 标题信息行集合
    rowTitle = [u'保养包ID', u'保养包名称', u'保养包周期', u'项目分类', u'业务分类', u'作业类别', u'是否CMS相关',
                u'是否PMS相关', u'是否委托', u'前允差', u'后允差', u'工作描述', u'英文描述', u'是否更换备件', u'风险等级',
                u'周期计算方式']
    # 学生信息行集合
    rowDatas = [[u'10001', u'张三', u'男', u'1998-2-3'], [u'10002', u'李四', u'女', u'1999-12-12'],
                [u'10003', u'王五', u'男', u'1998-7-8']]
    # 遍历向表格写入标题行信息
    for i in range(0, len(rowTitle)):
        # 其中的'0'表示行, 'i'表示列，0和i指定了表中的单元格，'rowTitle[i]'是向该单元格写入的内容
        sheet1.write(0, i, rowTitle[i])
    # 遍历向表格写入学生信息
    for k in range(0, len(work_package_list)):  # 先遍历外层的集合，即每行数据
            sheet1.write(k + 1, 0, work_package_list[k].id)
            sheet1.write(k + 1, 1, work_package_list[k].name)
            sheet1.write(k + 1, 2, work_package_list[k].cycle)
            sheet1.write(k + 1, 3, work_package_list[k].pro_class)
            sheet1.write(k + 1, 4, work_package_list[k].bus_class)
            sheet1.write(k + 1, 5, work_package_list[k].opr_class)
            sheet1.write(k + 1, 6, work_package_list[k].is_cms)
            sheet1.write(k + 1, 7, work_package_list[k].is_pms)
            sheet1.write(k + 1, 8, work_package_list[k].is_commision)
            sheet1.write(k + 1, 9, work_package_list[k].front_tolerance)
            sheet1.write(k + 1, 10, work_package_list[k].back_tolerance)
            sheet1.write(k + 1, 11, work_package_list[k].work_des)
            sheet1.write(k + 1, 12, work_package_list[k].eng_des)
            sheet1.write(k + 1, 13, work_package_list[k].is_replace_spare)
            sheet1.write(k + 1, 14, work_package_list[k].risk_rank)
            sheet1.write(k + 1, 15, work_package_list[k].cycle_type)
    # 保存文件的路径及命名
    f.save('C:/Users/admin/Desktop/数据校对/WriteToExcel.xls')



# def print_hi(filename):
#     data = xlrd.open_workbook(filename)  # 文件名以及路径，如果路径或者文件名有中文给前面加一个 r
#     # table = data.sheets()[0]  # 通过索引顺序获取
#     # table = data.sheet_by_index(sheet_indx)  # 通过索引顺序获取
#     table = data.sheet_by_name("基础数据-工作包(必填)")  # 通过名称获取
#     nrows = table.nrows
#     # 获取该sheet中的行数，注，这里table.nrows后面不带().
#     table.row(0)
#     # 返回由该行中所有的单元格对象组成的列表,这与tabel.raw()方法并没有区别。
#     ncols = table.ncols
#     # 获取数据
#     for j in range(1, nrows):
#         for i in range(0, ncols):
#             value = table.cell_value(j, i)
#             print("第0行" + str(i) + "列值为", value)
#         print('\n')
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {filename}')  # Press Ctrl+F8 to toggle the breakpoint.


# def write_excel():
#     # 创建一个Workbook对象，即创建一个Excel工作簿
#     f = xlwt.Workbook()
#     # 创建学生信息表
#     # sheet1表示Excel文件中的一个表
#     # 创建一个sheet对象，命名为“学生信息”，cell_overwrite_ok表示是否可以覆盖单元格，是Worksheet实例化的一个参数，默认值是False
#     sheet1 = f.add_sheet(u'学生信息', cell_overwrite_ok=True)
#
#     # 标题信息行集合
#     rowTitle = [u'学号', u'姓名', u'性别', u'出生年月']
#     # 学生信息行集合
#     rowDatas = [[u'10001', u'张三', u'男', u'1998-2-3'], [u'10002', u'李四', u'女', u'1999-12-12'],
#                 [u'10003', u'王五', u'男', u'1998-7-8']]
#     # 遍历向表格写入标题行信息
#     for i in range(0, len(rowTitle)):
#         # 其中的'0'表示行, 'i'表示列，0和i指定了表中的单元格，'rowTitle[i]'是向该单元格写入的内容
#         sheet1.write(0, i, rowTitle[i])
#     # 遍历向表格写入学生信息
#     for k in range(0, len(rowDatas)):  # 先遍历外层的集合，即每行数据
#         for j in range(0, len(rowDatas[k])):  # 再遍历内层集合，j表示列数据
#             sheet1.write(k + 1, j, rowDatas[k][j])  # k+1表示先去掉标题行，j表示列数据，rowdatas[k][j] 插入单元格数据
#     # 保存文件的路径及命名
#     f.save('C:/Users/admin/Desktop/WriteToExcel.xls')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    copy_data_to_object('C:/Users/admin/Desktop/数据校对/维修保养基础数据-水文气象组设备-20210714(1)(1).xlsx')
    # write_excel()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
