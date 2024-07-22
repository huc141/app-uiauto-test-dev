# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteWiFi(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.ivSelectChannelButton = '//*[@resource-id="com.mcu.reolink:id/ivSelectChannelButton"]'  # nvr的通道按钮

        elif self.platform == 'ios':
            self.ivSelectChannelButton = '(//XCUIElementTypeButton)[2]'

    def access_in_remote_wifi(self, device_name, sub_name, access_mode):
        """
        进入指定设备的远程配置的wifi页面.
        接入hub、nvr的设备名称在命名时不能过长导致省略隐藏。
        :param device_name: 单机设备、hub、nvr的昵称(不是接入hub、nvr下的设备昵称)。
        :param sub_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param access_mode: 设备接入方式，支持single、in_hub、in_nvr。明确设备是单机还是接入NVR下、接入hub下。
        :return:
        """
        # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
        self.access_in_remote_setting(device_name)

        # 如果设备是单机：
        if access_mode == 'single':
            time.sleep(2)
            # 进入wifi主页
            self.scroll_and_click_by_text('Wi-Fi')

        # 如果设备接入了nvr：
        elif access_mode == 'in_nvr' and sub_name is not None:
            time.sleep(2)
            self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
            # 选择通道并点击(但是设备接入nvr后不会显示wifi的远程配置)
            self.scroll_and_click_by_text(sub_name)
            logger.info("设备接入了nvr，页面不显示WiFi功能")

        # 如果设备接入了hub：
        elif access_mode == 'in_hub' and sub_name is not None:
            time.sleep(2)
            # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
            self.scroll_and_click_by_text(sub_name)
            # 进入wifi主页
            self.scroll_and_click_by_text('Wi-Fi')

    def check_remote_wifi_text(self, expected_text, exclude_texts,
                               xml_az_parse_conditions, xml_ios_parse_conditions):
        """
        根据设备名，检查对应设备的远程配置功能是否和预期一致
        :param xml_az_parse_conditions: 安卓的远程配置页面解析条件，用于排除无关文本，筛选出页面功能
        :param xml_ios_parse_conditions: iOS的远程配置页面解析条件，用于排除无关文本，筛选出页面功能
        :param expected_text: 需要检查的预期文本
        :param exclude_texts: 需要排除的文本(额外添加需要排除的文本)
        :return:
        """
        return self.verify_page_text(expected_text=expected_text,
                                     exclude_texts=exclude_texts,
                                     xml_az_parse_conditions=xml_az_parse_conditions,
                                     xml_ios_parse_conditions=xml_ios_parse_conditions
                                     )

    def access_in_wifi_band_preference(self):
        """
        进入wifi频段偏好页面
        :return:
        """
        pass

    def access_in_wifi_test(self):
        """
        进入wifi测试页面
        :return:
        """
        pass

    def access_in_add_network(self):
        """
        进入添加其他网络页面
        :return:
        """
        pass

