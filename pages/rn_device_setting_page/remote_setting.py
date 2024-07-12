# -*- coding: utf-8 -*-
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass
        elif self.platform == 'ios':
            pass

    def check_remote_setting_text(self, text_to_check):
        """
        检查文本
        :param text_to_check: 需要检查的预期文本
        :return:
        """
        self.scroll_and_click_by_text(el_type="text", text_to_find=text_to_check)

    def scroll_click_remote_setting(self, device_name):
        """
        逐一滚动查找设备名称并点击远程设置按钮
        :param device_name: 要查找的设备名称
        :return:
        """
        self.access_in_remote_setting(text_to_find=device_name)
