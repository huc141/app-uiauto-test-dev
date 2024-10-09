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

    def check_wifi_main_text(self, texts):
        """
        验证Wi-Fi主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            wifi_main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            return wifi_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_band_preference(self, text_list, option_text_list):
        """
        进入并测试wifi频段偏好页面，验证文案和遍历操作选项
        :param text_list: wifi频段偏好 文案
        :param option_text_list: 操作选项
        :return:
        """
        try:
            time.sleep(2)
            # 默认进入【Wi-Fi 频段偏好】
            self.scroll_and_click_by_text(text_to_find='Wi-Fi 频段偏好')

            # 检查wifi频段偏好页面文案
            wifi_band_preference_text = RemoteSetting().scroll_check_funcs2(texts=text_list)

            # 遍历操作选项
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='Wi-Fi 频段偏好')

            # 遍历文本，执行点击操作
            # for i in text_list:
            #     self.scroll_and_click_by_text(text_to_find='Wi-Fi 频段偏好')
            #     time.sleep(0.5)
            #     logger.info('点击 ' + i)
            #     self.click_by_text(i)
            #     time.sleep(1)
            #     page_options = RemoteSetting().scroll_check_funcs(i)  # 断言
            #     if i != '取消':
            #         assert page_options is True
            #     elif i == '取消':
            #         assert page_options is False

            return wifi_band_preference_text

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_test(self, text_list):
        """
        进入wifi测速页面，验证文本内容存在,点击开始测速
        :return:
        """
        try:
            time.sleep(2)
            # 点击Wi-Fi测速功能项
            self.scroll_and_click_by_text(text_to_find='Wi-Fi测速')

            # 检查Wi-Fi测速页面文案
            wifi_test_speed_text = RemoteSetting().scroll_check_funcs2(texts=text_list)

            # 遍历文本，检查当前页面的文本内容
            # for i in text_list:
            #     page_element_status = self.is_element_exists(element_value=i)
            #     if page_element_status:
            #         logger.info('元素 ' + i + '存在')
            #         assert True
            #     else:
            #         logger.info('元素 ' + i + '缺失')
            #         assert False

            # 点击开始测速
            self.scroll_and_click_by_text(text_to_find='开始测速')
            # 验证测速页面是否打开
            time.sleep(10)
            google_speed_page = RemoteSetting().scroll_check_funcs2(texts='How fast are you going?')
            self.back_previous_page()  # 返回Wi-Fi测速页

            # 返回Wi-Fi主页，有可能失败
            self.back_previous_page()

            return wifi_test_speed_text, google_speed_page

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_add_network(self, text_list, wifi_name=None, wifi_passw=None):
        """
        进入添加其他网络页面
        :return:
        """
        try:
            time.sleep(2)
            # 点击进入添加其他网络页面
            self.scroll_and_click_by_text(text_to_find='添加其他网络')

            # 检查添加其他网络页面文案
            add_network_text = RemoteSetting().scroll_check_funcs2(texts=text_list)

            # 遍历文本，检查当前页面的文本内容
            # for i in text_list:
            #     page_element_status = self.is_element_exists(element_value=i)
            #     if page_element_status:
            #         logger.info('元素 ' + i + '存在')
            #         assert True
            #     else:
            #         logger.info('元素 ' + i + '缺失')
            #         assert False

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

            return add_network_text

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

