#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    本例使用读写处理文件的测试
"""
# 导入时间库
import datetime
# 导入系统库

# 格式化输出
# 192.168.0.100:8888
print("{}:{}".format('192.168.0.100', 8888))

with open('test.txt', 'a', encoding="utf8") as f:
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获得当前时间
    f.write("\n" + "#" * 20 + "\n")
    f.write(nowTime + "\n")
    f.write("#" * 20 + "\n")
    f.write('Hello, world!\n')
    # 刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。
    f.flush()

# # 将当前目录改为"/home/newdir"
# os.chdir("/home/newdir")
# # 创建目录test
# os.mkdir("test")
# # 给出当前的目录
# print(os.getcwd())
# # 删除”/tmp/test”目录
# os.rmdir( "/tmp/test"  )



