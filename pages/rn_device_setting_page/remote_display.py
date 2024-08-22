# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteDisplay(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def access_in_stream(self, text_list, option_text='码流'):
        """
        进入并测试码流页面
        :param text_list: 文本
        :param option_text: 菜单功能项，该方法默认进入【码流】
        :return:
        """
        # 进入码流页面
        self.scroll_and_click_by_text(text_to_find=option_text)

        # 检查码流页面文案
        page_fun_list = RemoteSetting().scroll_check_funcs(text_list)

        # 断言
        assert page_fun_list is True
