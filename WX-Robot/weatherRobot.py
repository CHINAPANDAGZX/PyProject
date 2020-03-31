#!/usr/bin/python
# -*- coding: UTF-8 -*-

#该程序为爬取最近7天的天气预报代码

from datetime import datetime,date
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# from wxpy import *

sendMsg =""

def handleDayWeatherData( i,now_day,position ):
    '''
        用于处理7天天气预报的数据
    :return:None
    '''
    global sendMsg
    # print(i.get_attribute('class'))
    # 打印所在的节点 class 名称
    # print("====================================")
    # print(i.text)
    # 打印所在的节点里的文本内容
    # print("====================================")
    day = i.find_element_by_tag_name('h1').text #从标签获得日期
    day = day.split("（")[0]  #截取日期
    # day = day[0:3] #只截取日期作为参数
    dayNum = day.split("日")[0]  #截取日期的纯数字
    inputDay = str(now_day)[-2:]
    k = int(dayNum)
    j = int(inputDay)
    if(k==j):
        print("========================================================================")
        # sendMsg = sendMsg + "========================================================================" +'\n'
        dayList = str(now_day).split("-")
        # print("日期：" + day)
        day = str("公元" + dayList[0] + "年" + dayList[1] + "月" + dayList[2] + "日")
        print("日期：" + day)
        sendMsg = sendMsg + "日期：" + day
        # print("====================================")
        print("位置：" + position)
        sendMsg = sendMsg + '\n' + "位置：" + position
        # print("====================================")
        weather = i.find_element_by_class_name("wea").text #获取天气情况
        print("天气：" + weather)
        sendMsg = sendMsg + '\n' + "天气：" + weather
        # print("====================================")
        temperature = i.find_element_by_class_name("tem").text #获取气温
        print("气温：" + temperature)
        sendMsg = sendMsg + '\n' + "气温：" + temperature
        # print("====================================")
        wind = i.find_element_by_class_name("win") #获取风力所在节点
        wind_force = wind.find_element_by_tag_name("i").text #获取风力等级
        wind_direction = wind.find_element_by_tag_name("em").find_element_by_tag_name("span").get_attribute('title') #获取风向
        print("风力等级：" + wind_force)
        print("风向：" + wind_direction)
        sendMsg = sendMsg + '\n' +"风力等级：" + wind_force
        sendMsg = sendMsg + '\n' +"风向：" + wind_direction
        # sendMsg = sendMsg + '\n' +"========================================================================"
        print("========================================================================")

if __name__ == "__main__":
    now_day = date.today()
    now_time = time.strftime("%H:%M:%S")
    now_longTime = datetime.now()
    print(str(now_day))  # 打印当前日期
    print(str(now_time))  # 打印当前时间
    print(str(now_longTime))  # 打印当前日期时间

    nowTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #获得当前时间
    print("当前时间为：" + nowTime)
    browser = webdriver.Chrome()
    try:
        browser.get('http://www.weather.com.cn/weather/101230201.shtml')
        wait = WebDriverWait(browser, 10)  # 等待条件为浏览器，最大等待时间为10秒
        # 成功匹配等待条件后立即向下执行，否则超过最大等待时长则抛出异常

        css1 = browser.find_element(By.ID, "7d")  # 定位到天气预报的7天范围
        # print(css1)
        css2 = css1.find_elements_by_class_name("clearfix")
        # print(css2)
        css3 = css2[0].find_elements(By.CLASS_NAME, "sky")

        cityNode = browser.find_element(By.CLASS_NAME, "today")
        cityNode2 = cityNode.find_element_by_class_name("crumbs")
        node = cityNode2.find_elements_by_tag_name("a")
        nodeSpan = cityNode2.find_elements_by_tag_name("span")
        province = node[0].text  # 获取省份名称
        city = node[1].text  # 获取城市名称
        area = nodeSpan[2].text  # 获取地区名称
        position = province+">"+city+">"+area
        print(position)
        for i in css3:
            handleDayWeatherData(i,now_day,position);
    finally:
        browser.close()
        # # 初始化机器人，扫码登陆
        # bot = Bot(cache_path=True)  # 启用缓存保存自己的登录状态
        # bot.enable_puid()  # 启用puid属性，不同于其他 ID 属性，puid 可始终被获取到，且具有稳定的唯一性，但不可跨机器人使用
        # my_group1 = bot.groups().search()
        # my_group2 = bot.groups().search("西")[0]
        # my_group2.send("自制微信天气预报助手")
        # my_group2.send(sendMsg)
        # bot.logout()
        print("程序结束")

