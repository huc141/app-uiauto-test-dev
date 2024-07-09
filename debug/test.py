# -*- coding: utf-8 -*-
import time

import pytest
import wda
import yaml
import os
import uiautomator2 as u2
from pages.base_page import BasePage
from common_tools.logger import logger

driver = u2.connect_usb("28131FDH2000K1")

driver(resourceId='com.mcu.reolink:id/add_device_button').click()  # 点击添加按钮
driver(text='手动输入').click()  # 点击手动输入
driver.xpath('//*[@resource-id="com.mcu.reolink:id/tv_ip"]').click()
time.sleep(1)
driver.xpath('//*[@text="9000"]').click()
driver.clear_text()
time.sleep(1)
driver.xpath('(//*[@resource-id="com.mcu.reolink:id/edit_text"])[2]').set_text("564186156")

print("--------------------------------")

# ios_driver = wda.Client('http://localhost:8100')
# element = ios_driver(xpath="(//XCUIElementTypeButton)[2]")  # 定位添加按钮
# element.click()  # 点击添加按钮
#
# element = ios_driver(xpath='(//*[@label="手动输入"])[2]')  # 定位手动输入
# element.click()  # 点击手动输入
# ios_driver(xpath='(//XCUIElementTypeTextField)').set_text("564186156")  # 定位输入框，赋值给ee
