# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteLight(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 定时模式：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 定时模式：分钟

        elif self.platform == 'ios':
            self.time_selector_hour = ''
            self.time_selector_min = ''

    def click_light_off(self):
        """
        点击关闭
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='关闭')

    def click_timer_mode(self):
        """
        点击定时模式
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='定时模式')

    def click_night_smart_mode(self):
        """
        点击夜间智能模式
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='夜间智能模式')

    def click_infrared_light(self):
        """
        点击进入红外灯的配置页
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='红外灯')

    def click_floodlight(self):
        """
        点击进入照明灯的配置页
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='照明灯')

    def time_selector(self, direction='up', iteration=1):
        """
        时间选择器
        :param direction: slider的定位方式，支持id或者xpath
        :param iteration:
        :return:
        """
        # 手指向上滑动选择小时
        self.scroll_selector(id_or_xpath=self.time_selector_hour,
                             direction=direction,
                             times=iteration)

        # 手指向上滑动选择分钟
        self.scroll_selector(id_or_xpath=self.time_selector_min,
                             direction=direction,
                             times=iteration)
