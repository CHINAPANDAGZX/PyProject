"""
    学习Python字典的用法
"""

MyCon = {12: 'big', 0: 'white', 354: 'gentle', 1: 'good'}
# 访问键为 12 的字典值
# 'big'
print(MyCon[12])

dict = {'Name': 'Fiona', 'Age': 10, 'Class': 'Three'}

# len() 方法计算字典元素个数（键的总个数）
len(dict)

# str() 方法输出字典中可以打印的字符串标识
str(dict)

# type() 方法返回输入的变量类型，如果变量是字典就返回字典类型
type(dict)

# 浅拷贝: 引用对象  赋值
dict2 = dict
# 拷贝
dict3 = dict.copy()
# 赋值会随父对象的修改而修改，拷贝不会随父对象的修改而修改

# 删除键是'Name'的条目
del dict['Name']

# 清空字典所有条目
dict.clear()

# 删除整个字典元素
del dict

# dict.fromkeys(seq[, value])
seq = ('name', 'age', 'class')

# 不指定值
dict = dict.fromkeys(seq)
print("新的字典为 : %s" % str(dict))

# 赋值 10
dict = dict.fromkeys(seq, 10)
print("新的字典为 : %s" % str(dict))

# 　赋值一个元组
dict = dict.fromkeys(seq, ('zs', 8, 'Two'))
print("新的字典为 : %s" % str(dict))

# 以上输出结果
# 新的字典为 : {'name': None, 'age': None, 'class': None}
# 新的字典为 : {'name': 10, 'age': 10, 'class': 10}
# 新的字典为 : {'name': ('zs', 8, 'Two'), 'age': ('zs', 8, 'Two'), 'class': ('zs', 8, 'Two')}
