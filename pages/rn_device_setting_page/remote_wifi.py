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
            self.edit_wifi_name_text = '//*[@text="Wi-Fi名称"]'
            self.edit_wifi_passw_text = '//*[@text="Wi-Fi密码"]'

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

    def access_in_wifi_test(self, text_list, option_text='Wi-Fi测速'):
        """
        进入wifi测速页面，验证文本内容存在
        :return:
        """
        # 点击Wi-Fi测速功能项
        self.scroll_and_click_by_text(text_to_find=option_text)

        # 遍历文本，检查当前页面的文本内容
        for i in text_list:
            page_element_status = self.is_element_exists(element_value=i)
            if page_element_status:
                logger.info('元素 ' + i + '存在')
                assert True
            else:
                logger.info('元素 ' + i + '缺失')
                assert False

    def access_in_add_network(self, text_list, option_text='添加其他网络', wifi_name=None, wifi_passw=None):
        """
        进入添加其他网络页面
        :return:
        """
        # 点击进入添加其他网络页面
        self.scroll_and_click_by_text(text_to_find=option_text)

        # 遍历文本，检查当前页面的文本内容
        for i in text_list:
            page_element_status = self.is_element_exists(element_value=i)
            if page_element_status:
                logger.info('元素 ' + i + '存在')
                assert True
            else:
                logger.info('元素 ' + i + '缺失')
                assert False

        # 点击输入Wi-Fi名称
        self.scroll_and_click_by_text(text_to_find='Wi-Fi名称')
        self.input_text(xpath_exp=self.edit_wifi_name_text, text=wifi_name)

        # 点击输入Wi-Fi密码
        self.scroll_and_click_by_text(text_to_find='Wi-Fi密码')
        self.input_text(xpath_exp=self.edit_wifi_passw_text, text=wifi_passw)

        # 点击保存
        self.scroll_and_click_by_text(text_to_find='保存')

        # 点击跳过并保存
        self.scroll_and_click_by_text(text_to_find='跳过并保存')
