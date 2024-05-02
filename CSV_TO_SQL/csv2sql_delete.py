# 将csv文件数据提取出来输出成sql文件
import csv

# 输入CSV文件名
input_csv_file = '嘉庚号测试.csv'
# 输出SQL文件名
output_sql_file = 'delete_statements.sql'


# 定义一个函数来读取CSV文件并生成删除SQL语句
def generate_delete_statements(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='gbk') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        # 创建CSV读取器
        reader = csv.reader(infile)

        # 遍历CSV文件中的每一行
        for row in reader:
            # 确保行中至少有一个值
            if row:
                # 提取第一个值作为id
                id_value = row[0]
                # 构建DELETE语句
                delete_statement = f"DELETE FROM jw_work_package WHERE id = '{id_value}';\n"
                # 将DELETE语句写入输出文件
                outfile.write(delete_statement)


# 调用函数，生成删除SQL语句并写入文件
generate_delete_statements(input_csv_file, output_sql_file)