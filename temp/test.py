# -*- coding:utf-8 -*-
# @author: 软件测试凡哥

from appium import webdriver
from log.logging_test import logger


def android_driver():
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "10",
        "deviceName": "PCT_AL10",
        "appPackage": "com.ss.android.article.news",
        "appActivity": ".activity.MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True,
    }
    logger.info("启动今日头条APP...")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    return driver


def login_opera(driver):
    """登录今日头条操作"""
    logger.info("开始登陆今日头条APP...")
    try:
        driver.find_element_by_id("com.ss.android.article.news:id/cji").click()  # 点击【我知道了】
        driver.find_element_by_id("android:id/button1").click()  # 点击权限管理-确定按钮
        driver.find_element_by_xpath(
            "//android.widget.TabWidget/android.widget.RelativeLayout[@index=3]").click()  # 点击未登录
        driver.find_element_by_id("com.ss.android.article.news:id/a10").click()  # 未登录页点击登录按钮
        driver.find_element_by_id("com.ss.android.article.news:id/bgh").click()  # 登录页点击“。。。”
        driver.find_element_by_xpath("//android.widget.LinearLayout[@index=4]").click()  # 选择密码登录
        driver.find_element_by_id("com.ss.android.article.news:id/bu").send_keys("18768124236")  # 输入账号
        driver.find_element_by_id("com.ss.android.article.news:id/c5").send_keys("xiaoqq3915172")  # 输入密码
        driver.find_element_by_id("com.ss.android.article.news:id/a2o").click()  # 点击登录
    except Exception as e:
        logger.error("登录错误，原因为：{}".format(e))
    else:
        logger.info("登陆成功...")


driver = android_driver()
login_opera(driver)