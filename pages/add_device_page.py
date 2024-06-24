# -*- coding: utf-8 -*-
from pages.base_page import BasePage


class AddDevicePage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.manual_input_button = '//*[@resource-id="com.mcu.reolink:id/tv_input_uid_ip"]'
            self.manual_input_uid = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'
            self.btn_next_step = '//*[@resource-id="com.mcu.reolink:id/btn_next"]'
        elif self.platform == 'ios':
            self.manual_input_button = ''
            self.manual_input_uid = ''
            self.btn_next_step = ''

    def click_manual_input(self):
        """点击手动输入按钮"""
        return self.click_by_xpath(self.manual_input_button)

    def input_by_uid(self, uid):
        """
        设备列表：输入设备uid并点击下一步
        uid: 你要添加的设备UID
        """
        self.click_by_xpath(self.manual_input_uid)
        self.input_text(uid)
        self.click_by_xpath(self.btn_next_step)
