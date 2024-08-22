# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteDisplay(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def access_in_wifi_band_preference(self, text_list, option_text='Wi-Fi 频段偏好'):
        """
        进入并测试wifi频段偏好页面，验证操作内容存在，并点击
        :param text_list: 文本
        :param option_text: 菜单功能项，该方法默认进入【Wi-Fi 频段偏好】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)