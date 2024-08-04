# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteWiFi(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def access_in_wifi_band_preference(self, option_text='Wi-Fi 频段偏好'):
        """
        进入wifi频段偏好页面
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

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

