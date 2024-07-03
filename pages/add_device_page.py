# -*- coding: utf-8 -*-
from pages.base_page import BasePage


class AddDevicePage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.manual_input_button = '//*[@resource-id="com.mcu.reolink:id/tv_input_uid_ip"]'  # 按钮：手动输入
            self.manual_input_uid = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'  # UID选项的输入框

            self.manual_ip ='//*[@resource-id="com.mcu.reolink:id/tv_ip"]'  # IP选项
            self.manual_input_ip = '(//*[@resource-id="com.mcu.reolink:id/edit_text"])[1]'  # IP选项的输入框

            self.btn_next_step = '//*[@resource-id="com.mcu.reolink:id/btn_next"]'  # 下一步
        elif self.platform == 'ios':
            self.manual_input_button = ''
            self.manual_input_uid = ''
            self.btn_next_step = ''

    def input_by_uid(self, uid):
        """
        设备列表添加设备：输入设备uid并点击下一步
        uid: 你要添加的设备UID
        """
        self.click_by_xpath(self.manual_input_uid)
        self.input_text(uid)
        self.click_by_xpath(self.btn_next_step)

    def input_by_id(self, ip):
        """
        设备列表添加设备：输入设备ip并点击下一步
        :param ip: 设备ip
        :return:
        """
        # TODO: 待完成
        self.click_by_xpath(self.)

    def click_manual_input(self, method, identifier):
        """点击手动输入按钮,并选择以何种方式添加设备"""
        if method.lower() == "uid":
            self.input_by_uid(identifier)
        return self.click_by_xpath(self.manual_input_button)