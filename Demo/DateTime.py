#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    本例使用datetime库获取时间的相关信息
"""

import datetime


nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #获得当前时间
print("当前时间为：" + nowTime)

today = datetime.date.today()
print(today)
tomorrow = today + datetime.timedelta(days=0)
print(tomorrow)