# -*- coding: utf-8 -*-
import os
import time
from os.path import exists

from common_tools.app_driver import driver
from common_tools.logger import logger
from pages.device_list_page import DeviceListPage


class TestAddDevice:
    def test_add_device_by_uid(self):
        driver.start()
        device_list_page = DeviceListPage()  # 初始化设备列表对像
        time.sleep(3)
        device_list_page.click_by_xpath('//*[@resource-id="com.mcu.reolink:id/nav_menu_button"]')
        device_list_page.click_by_xpath('//*[@resource-id="com.mcu.reolink:id/id_text_view"]')
        time.sleep(6)
        device_list_page.click_by_xpath('//android.widget.TextView[@text=""]')
        time.sleep(3)
        device_list_page.click_by_xpath('//android.widget.EditText')
        time.sleep(3)
        device_list_page.click_by_xpath('//android.widget.EditText[1]')
        time.sleep(3)
        device_list_page.input_text('1111')

