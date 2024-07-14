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

    def check_remote_setting_text(self, expected_text, exclude_texts):
        """
        根据设备名，检查对应设备的远程配置功能是否和预期一致
        :param expected_text: 需要检查的预期文本
        :param exclude_texts: 需要排除的文本
        :return:
        """
        self.verify_page_text(expected_text=expected_text, exclude_texts=exclude_texts)

    def scroll_click_remote_setting(self, device_name):
        """
        逐一滚动查找设备名称并点击远程设置按钮
        :param device_name: 要查找的设备名称
        :return:
        """
        self.access_in_remote_setting(text_to_find=device_name)
