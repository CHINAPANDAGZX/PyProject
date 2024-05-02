# 将csv文件数据提取出来输出成sql文件
import csv
import mysql.connector

# 输入CSV文件名
input_csv_file = '嘉庚号测试.csv'
# 输出SQL文件名
output_sql_file = 'output.sql'
# 数据库连接配置
config = {
    'user': 'mel',
    'password': 't@2185570#$',
    'host': '10.64.35.127',
    'port': 9909,
    'database': 'z-gzx-bailuzhou-tx-init',
    'raise_on_warnings': True
}


# 定义一个函数来创建REPLACE INTO语句
def create_replace_statement(ins_dict,header, row):
    """
    创建一个REPLACE INTO语句。
    :param header: 一个包含字段名的列表
    :param row: 一个包含行数据的列表
    :return: 一个格式化的REPLACE INTO语句
    """
    row[6] = ins_dict.get(row[6], row[6])
    # 将字段名和值转换为适合SQL语句的格式
    value_placeholders = ', '.join([f"'{value}'" if value else "NULL" for value in row])
    # 创建REPLACE INTO语句
    statement = f"REPLACE INTO jw_work_package ({', '.join(header)}) VALUES ({value_placeholders});"
    return statement


# 读取CSV文件并生成SQL语句
def generate_sql_statements_and_write_to_file(ins_dict,input_file, output_file):
    with open(input_file, 'r', newline='', encoding='gbk') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        # 创建CSV读取器
        reader = csv.reader(infile)

        # 对应的表字段名
        header = ["id","code","name","cycle","front_tolerance","back_tolerance","responsible_role"]

        # 遍历CSV文件中的每一行数据
        for row in reader:
            # 创建REPLACE语句
            sql_statement = create_replace_statement(ins_dict,header, row)
            # 将生成的SQL语句写入输出文件
            outfile.write(sql_statement + '\n')

# 建立数据库连接
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
# 执行SQL查询
query = "SELECT role_id,role_name FROM sys_role;"
cursor.execute(query)
# 获取所有查询结果
results = cursor.fetchall()
# 将查询结果中的两列字段作为键值对
role_dict = {row[1]: row[0] for row in results}
# 关闭游标和连接
cursor.close()
cnx.close()
# 调用函数，生成SQL语句并写入文件
generate_sql_statements_and_write_to_file(role_dict,input_csv_file, output_sql_file)
