# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteWiFi(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def access_in_wifi_band_preference(self, text_list, option_text='Wi-Fi 频段偏好'):
        """
        进入并测试wifi频段偏好页面
        :param text_list: 文本
        :param option_text: 菜单功能项，该方法默认进入【Wi-Fi 频段偏好】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

        # 检查wifi频段偏好页面文案
        page_fun_list = RemoteSetting().scroll_check_funcs(text_list)

        # 断言
        assert page_fun_list is True

        # 关闭弹窗，返回Wi-Fi页
        self.click_by_text('取消')

        # 遍历文本，执行点击操作
        for i in text_list:
            self.scroll_and_click_by_text(text_to_find=option_text)
            time.sleep(0.5)
            logger.info('点击 ' + i)
            self.click_by_text(i)
            time.sleep(0.5)
            page_options = RemoteSetting().scroll_check_funcs(i)  # 断言
            if i != '取消':
                assert page_options is True
            elif i == '取消':
                assert page_options is False

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

