# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteLight(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 定时模式：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 定时模式：分钟
            self.base_left_button = '//*[@resource-id="com.mcu.reolink:id/base_left_button"]'  # 左上角返回上一页按钮

        elif self.platform == 'ios':
            self.time_selector_hour = ''
            self.time_selector_min = ''
            self.base_left_button = ''

    def check_lights_main_text(self, lights_num, texts):
        """
        验证灯主页文案
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            # 如果是多个灯，则点击红外灯
            if lights_num:
                lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts)
                return lights_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_lights_list_length(self, texts):
        """
        计算列表长度, 判断灯的数量
        :param texts: 传入一个列表，计算列表长度
        :return:
        """
        try:
            if isinstance(texts, list):
                if len(texts) > 1:
                    return True
                elif len(texts) == 1:
                    return False
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_light_off(self):
        """
        点击关闭
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='关闭')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_timer_mode(self):
        """
        点击定时模式
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='定时模式')

    def click_night_smart_mode(self):
        """
        点击夜间智能模式
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='夜间智能模式')

    def click_and_test_infrared_light(self, lights_num, infrared_light_texts, options_text):
        """
        点击进入红外灯的配置页并测试红外灯的选项配置
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param infrared_light_texts: 红外灯 配置页文案
        :param options_text: 红外灯 配置页操作项
        :return:
        """
        try:
            # 如果是多个灯，则点击红外灯
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='红外灯')
                # 验证红外灯主页文案
                infrared_main_text_res = RemoteSetting().scroll_check_funcs2(texts=infrared_light_texts)
                # 遍历操作
                for i in options_text:
                    # 操作红外灯配置
                    self.scroll_and_click_by_text(text_to_find=i)
                    # 返回上一页
                    self.back_previous_page_by_xpath(xpath_expression=self.base_left_button)
                    # 断言
                    if not self.scroll_and_click_by_text(text_to_find=i):
                        pytest.fail(f"红外灯选择【{i}】后，未检查到回显！")

                return infrared_main_text_res

            else:
                # 验证红外灯主页文案
                infrared_main_text_res = RemoteSetting().scroll_check_funcs2(texts=infrared_light_texts)
                # 遍历操作
                for i in options_text:
                    # 操作红外灯配置
                    self.scroll_and_click_by_text(text_to_find=i)

                return infrared_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_floodlight_night_smart_mode(self, lights_num, infrared_light_texts, options_text):
        """
        点击并测试照明灯的夜间智能模式
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param infrared_light_texts: 配置页文案
        :param options_text: 配置页操作项
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='夜间智能模式')
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=infrared_light_texts)
                # 遍历操作
                for i in options_text:
                    # 操作照明灯配置
                    self.scroll_and_click_by_text(text_to_find=i)
                    # 返回上一页
                    self.back_previous_page_by_xpath(xpath_expression=self.base_left_button)
                    # 断言
                    if not self.scroll_and_click_by_text(text_to_find=i):
                        pytest.fail(f"照明灯选择【{i}】后，未检查到回显！")

                return floodlight_main_text_res

            else:
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=infrared_light_texts)
                # 遍历操作
                for i in options_text:
                    # 操作照明灯配置
                    self.scroll_and_click_by_text(text_to_find=i)

                return floodlight_main_text_res

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def time_selector(self, direction='up', iteration=1):
        """
        时间选择器
        :param direction: slider的定位方式，支持id或者xpath
        :param iteration:
        :return:
        """
        # 手指向上滑动选择小时
        self.scroll_selector(id_or_xpath=self.time_selector_hour,
                             direction=direction,
                             times=iteration)

        # 手指向上滑动选择分钟
        self.scroll_selector(id_or_xpath=self.time_selector_min,
                             direction=direction,
                             times=iteration)
