# -*- coding: utf-8 -*-
from pages.base_page import BasePage


class AddDevicePage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.manual_input_button = '//*[@resource-id="com.mcu.reolink:id/tv_input_uid_ip"]'  # 按钮：手动输入
            self.manual_input_uid = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'  # UID选项的输入框

            self.manual_ip = '//*[@resource-id="com.mcu.reolink:id/tv_ip"]'  # IP选项
            self.manual_input_ip = '(//*[@resource-id="com.mcu.reolink:id/edit_text"])[1]'  # IP选项的输入框

            self.manual_authlink = '//*[@resource-id="com.mcu.reolink:id/tv_link"]'  # 授权链接选项
            self.manual_input_authlink = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'  # 授权链接的输入框

            self.btn_next_step = '//*[@resource-id="com.mcu.reolink:id/btn_next"]'  # 按钮：下一步

            self.device_usage_method = '//*[@resource-id="com.mcu.reolink:id/tvTitle"]'  # 页面标题：选择设备的使用方式
            self.device_network_access_Method = ''  # 页面标题：选择设备接入网络的方式

        elif self.platform == 'ios':
            self.manual_input_button = ''
            self.manual_input_uid = ''
            self.btn_next_step = ''

    def input_by_uid(self, uid):
        """
        设备列表-添加设备：输入设备uid并点击下一步
        uid: 你要添加的设备UID
        """
        self.click_by_xpath(self.manual_input_uid)
        self.input_text(uid)
        self.click_by_xpath(self.btn_next_step)

    def input_by_ip(self, ip):
        """
        设备列表-添加设备：输入设备ip并点击下一步
        :param ip: 设备ip
        :return:
        """
        self.click_by_xpath(self.manual_ip)
        self.click_by_xpath(self.manual_input_ip)
        self.input_text(ip)
        self.click_by_xpath(self.btn_next_step)

    def input_by_authlink(self, authlink):
        """
        设备列表-添加设备：输入设备授权链接并点击下一步
        :param authlink: 设备的授权链接
        :return:
        """
        self.click_by_xpath(self.manual_authlink)
        self.click_by_xpath(self.manual_input_authlink)
        self.input_text(authlink)
        self.click_by_xpath(self.btn_next_step)

    def identify_page_type(self):
        """
        判断页面是【选择设备的使用方式】 or 【选择网络接入方式】
        :return: bool
        """
        # TODO: 待确定要不要专门写一个方法来判断是不是这两个页面，还是直接调用is_element_exists()
        return self.is_element_exists("xpath", self.device_usage_method)

    def click_manual_input(self, method='uid', identifier=None):
        """点击手动输入按钮,并选择以何种方式添加设备，并自动输入uid/ip/授权链接，然后点击下一步"""
        if method.lower() == "uid":
            self.input_by_uid(identifier)
        elif method.lower() == "ip":
            self.input_by_ip(identifier)
        elif method.lower() == 'authlink':
            self.input_by_authlink(identifier)

        # return self.click_by_xpath(self.manual_input_button)
