# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteCloudRecord(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.slider_stop_pre_record_battery = ''
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 编辑分段灵敏度，开始时间设置：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 编辑分段灵敏度，开始时间设置：分钟

        elif self.platform == 'ios':
            pass

    def turn_on_cloud_recording(self):
        """
        打开云录像开关。
        ①如果为关，则点击打开；
        ②如果为开，则进行功能项校验。
        :return:
        """
        try:
            # 如果是关，则点击打开：
            self.loop_detect_element_and_click(element_value='测试')
            time.sleep(6)  # 等待loading
            if self.loop_detect_element_exist(element_value='未开启云录像功能'):
                self.loop_detect_element_and_click(element_value='确定')
                self.scroll_click_right_btn(text_to_find='云录像')  # 开启云录像

            elif self.loop_detect_element_exist(element_value='测试成功'):
                self.loop_detect_element_and_click(element_value='确定')

            time.sleep(1)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_cloud_recording_main_text(self, main_text):
        """
        验证云录像主页文案
        :param main_text: 待验证的文案列表
        :return:
        """
        try:
            self.turn_on_cloud_recording()  # 开启云录像
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=main_text)
            return main_text_res, illegal_funcs_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_recording_resolution_text(self, main_text, option_text_list):
        """
        验证录像清晰度主页文案
        :param main_text: 待验证的文案列表
        :param option_text_list: 待遍历的选项
        :return:
        """
        try:
            # 文案验证
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=main_text)

            # 清晰度选项遍历
            self.iterate_and_click_popup_text(option_text_list=option_text_list,
                                              menu_text='录像清晰度')

            return main_text_res, illegal_funcs_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
