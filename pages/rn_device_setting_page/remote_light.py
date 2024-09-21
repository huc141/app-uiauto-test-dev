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
            pass

        elif self.platform == 'ios':
            pass

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
