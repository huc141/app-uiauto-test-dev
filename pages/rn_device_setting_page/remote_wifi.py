# -*- coding: utf-8 -*-
import time
import pytest
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
            self.base_left_button = '//*[@resource-id="com.mcu.reolink:id/base_left_button"]'

        elif self.platform == 'ios':
            pass

    @staticmethod
    def check_wifi_main_text(text1, text2):
        """
        验证Wi-Fi主页文案
        :param text1: 待验证的文案列表
        :param text2: ReoTitle验证的文案列表
        :return:
        """
        try:
            RemoteSetting().scroll_check_funcs2(texts=text1)
            RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_band_preference(self, text1, text2):
        """
        进入并测试wifi频段偏好页面，验证文案和遍历操作选项
        :param text1: wifi频段偏好 文案
        :param text2: 操作选项列表
        :return:
        """
        try:
            time.sleep(2)
            # 默认进入【Wi-Fi 频段偏好】
            self.loop_detect_element_and_click(element_value='Wi-Fi 频段偏好')

            # 检查wifi频段偏好页面文案
            RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False, back2top=False)

            # 遍历操作选项
            self.iterate_and_click_popup_text(option_text_list=text2, menu_text='Wi-Fi 频段偏好')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_test(self, text):
        """
        进入wifi测速页面，验证文本内容存在,点击开始测速
        :return:
        """
        try:
            time.sleep(2)
            # 点击Wi-Fi测速功能项
            self.loop_detect_element_and_click(element_value='Wi-Fi测速')

            # 检查Wi-Fi测速页面文案
            RemoteSetting().scroll_check_funcs2(texts=text)

            # 点击开始测速
            self.loop_detect_element_and_click(element_value='开始测速')

            # 验证测速页面是否打开
            time.sleep(2)
            speed_text = 'How fast are you going?'
            if not self.loop_detect_element_exist(element_value=speed_text, scroll_or_not=False):
                pytest.fail('未进入测速页面,或测速页面错误！')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_add_network(self, text_list, wifi_name='test_name', wifi_passw='reolink123'):
        """
        进入添加其他网络页面,输入wifi名称和密码,点击保存和跳过并保存.
        :param text_list: 待验证的文案列表
        :param wifi_name: wifi名称
        :param wifi_passw: wifi密码
        :return:
        """
        try:
            time.sleep(2)
            # 点击进入添加其他网络页面
            self.loop_detect_element_and_click(element_value='添加其他网络')

            # 检查添加其他网络页面文案
            RemoteSetting().scroll_check_funcs2(texts=text_list)

            # 点击输入Wi-Fi名称
            self.loop_detect_element_and_click(element_value='Wi-Fi名称')
            time.sleep(1)
            self.input_text(xpath_exp=self.edit_wifi_name_text, text=wifi_name)

            # 点击输入Wi-Fi密码
            self.loop_detect_element_and_click(element_value='Wi-Fi密码')
            self.input_text(xpath_exp=self.edit_wifi_passw_text, text=wifi_passw)

            # 点击保存
            self.loop_detect_element_and_click(element_value='保存')

            # 点击跳过并保存
            self.loop_detect_element_and_click(element_value='跳过并保存')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

