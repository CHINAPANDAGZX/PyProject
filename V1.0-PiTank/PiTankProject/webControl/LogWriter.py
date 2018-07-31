#!/usr/bin/python
# -*- coding:utf-8 -*
import datetime
import time

def writeLog(msg):
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write('\n' + msg )



now_day = datetime.date.today()
now_time = time.strftime("%H:%M:%S")
now_longTime = datetime.datetime.now()
print(str(now_day)) # 打印当前日期
print(str(now_time)) # 打印当前时间
print(str(now_longTime)) # 打印当前日期时间
writeLog('=' * 50)
writeLog('当前时间： ' + str(now_day) + ' ' + str(now_time))

writeLog('以下是日志文本信息')
writeLog('=' * 50)
