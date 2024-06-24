# -*- coding: utf-8 -*-
from pages.base_page import BasePage


class DeviceListPage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.add_device_button = '//*[@resource-id="com.mcu.reolink:id/add_device_button"]'
        elif self.platform == 'ios':
            self.add_device_button = '(//XCUIElementTypeButton)[1]'

    def click_add_device_button(self):
        """
        点击设备列表的添加按钮
        """
        return self.click_by_xpath(self.add_device_button)
