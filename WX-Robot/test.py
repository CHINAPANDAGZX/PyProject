#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    验证微信机器人的部分功能
"""

# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)  # 启用缓存保存自己的登录状态
# 终端扫码登录的方式
# bot = Bot(console_qr=True)

# 给机器人自己发送消息
# bot.self.send('Hello World!')
# 给文件传输助手发送消息
bot.file_helper.send('Hello World!')

# 查找昵称为'乙醚。'的好友
my_friend = bot.friends().search("冯琦")
my_friend2 = bot.friends().search()
# <Friend: 乙醚。>
# 发送文本
# my_friend.send('测试文本发送!')
# 发送图片
# my_friend.send_image('my_picture.png')
# 发送视频
# my_friend.send_video('my_video.mov')
# 发送文件
# my_friend.send_file('my_file.zip')
# 以动态的方式发送图片
# my_friend.send('@img@my_picture.png')
my_group = bot.groups().search()
my_group2 = bot.groups().search("西")[0]
my_group2.send("测试消息")

print("测试完毕！")
bot.logout()