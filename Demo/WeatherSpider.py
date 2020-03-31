#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    本Demo中使用selenium操控浏览器访问中国天气网，
    并对页面元素数据进行抓取后，保存到Mysql数据库中
"""

# 导入时间库
import datetime

# 该程序为爬取最近7天的天气预报代码
# 导入mysql库
import pymysql
# 其他库
# from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def handleDayWeatherData(i, cursor, k):
    '''
        用于处理7天天气预报的数据,并保存到数据库
    :return:None
    '''
    print("========================================================================")
    # print(i.get_attribute('class'))
    # 打印所在的节点 class 名称
    # print("====================================")
    # print(i.text)
    # 打印所在的节点里的文本内容
    # print("====================================")
    day = i.find_element_by_tag_name('h1').text #从标签获得日期
    day = day[0:3] #只截取日期作为参数
    print("日期：" + day)
    # print("====================================")
    weather = i.find_element_by_class_name("wea").text #获取天气情况
    print("天气：" + weather)
    # print("====================================")
    temperature = i.find_element_by_class_name("tem").text #获取气温
    print("气温：" + temperature)
    # print("====================================")
    wind = i.find_element_by_class_name("win") #获取风力所在节点
    wind_force = wind.find_element_by_tag_name("i").text #获取风力等级
    wind_direction = wind.find_element_by_tag_name("em").find_element_by_tag_name("span").get_attribute('title') #获取风向
    print("风力等级：" + wind_force)
    print("风向：" + wind_direction)
    print("========================================================================")
    # 查询当前天气表的最大ID
    maxID = 0

    sql = "SELECT MAX(id) FROM tb_weather"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            maxID = row[0]
            if maxID is None :
                maxID = 0
            else :
                maxID = int(maxID) + 1
            # maxID = str(maxID)
            print("当前最大ID为=%s" % \
            (maxID))
    except:
        print("查询出现错误！")
    today = datetime.date.today()
    day = today + datetime.timedelta(days=k)

    # SQL 插入语句
    sql = """INSERT INTO tb_weather(id, days, weather, temperature, wind_force, wind_direction)
             VALUES (%s, '%s', '%s', '%s', '%s', '%s')""" % (maxID, str(day), str(weather), str(temperature), str(wind_force), str(wind_direction))
    try:
        # 执行SQL语句
        cursor.execute(sql)
        db.commit()
    except  Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()



if __name__ == "__main__":
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #获得当前时间
    print("当前时间为：" + nowTime)
    browser = webdriver.Chrome()
    try:
        browser.get('http://www.weather.com.cn/weather/101230201.shtml')
        wait = WebDriverWait(browser, 10)  # 等待条件为浏览器，最大等待时间为10秒
        # 成功匹配等待条件后立即向下执行，否则超过最大等待时长则抛出异常

        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "root", "test1")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # input = browser.find_element_by_id('kw')
        # input.send_keys('Python')
        # input.send_keys(Keys.ENTER)

        # wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        # print(browser.current_url)
        # print(browser.get_cookies())
        # print(browser.page_source)
        html = browser.page_source #保存网页数据
        with open('test.txt', 'a', encoding="utf8") as f:
            f.write(html)
            f.flush()
        # print(html)
        # doc = pq(html)
        # items = doc('li')
        # print("items" + items)
        # print(items.html())
        # print(items.text())
        # print(type(items.text()))

        css1 = browser.find_element(By.ID, "7d")  # 定位到天气预报的7天范围
        # print(css1)
        css2 = css1.find_elements_by_class_name("clearfix")
        # print(css2)
        css3 = css2[0].find_elements(By.CLASS_NAME, "sky")
        k = 0
        for i in css3:
            handleDayWeatherData(i, cursor, k)
            k = k + 1
    finally:
        print("关闭浏览器")
        browser.close()
        print("关闭数据库连接")
        db.close()
        print("程序结束")




