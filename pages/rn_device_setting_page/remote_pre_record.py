# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemotePreRecord(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.slider_stop_pre_record_battery = ''

        elif self.platform == 'ios':
            pass

    def turn_on_precording(self):
        """
        打开预录模式开关。
        ①如果为关，则点击打开；
        ②如果为开，则进行功能项校验。
        :return:
        """
        try:
            # 如果是关，则点击打开：
            if not self.loop_detect_element_exist(element_value='停止预录电量', scroll_or_not=False):
                self.scroll_click_right_btn(text_to_find='预录模式',
                                            resourceId_1='com.mcu.reolink:id/tv_title',
                                            className_2='android.view.View')  # 点击预录模式
                time.sleep(1)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_precording_main_text(self, main_text):
        """
        验证预录模式主页文案
        :param main_text: 待验证的文案列表
        :return:
        """
        try:
            self.turn_on_precording()  # 开启预录模式
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def set_stop_pre_recording_power(self):
        """
        设置停止预录电量
        :return:
        """
        try:
            # 向右拖动
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath=self.slider_stop_pre_record_battery,
                                 direction='right',
                                 iteration=20)

            # 向左拖动
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath=self.slider_stop_pre_record_battery,
                                 direction='left',
                                 iteration=20)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_fps(self, texts, option_text_list):
        """
        点击帧率(fps)验证页面文案，并遍历帧率选项
        :param texts: 帧率(fps)页面文案
        :param option_text_list: 帧率(fps)页面选项
        :return:
        """
        try:
            # 进入帧率主页
            self.loop_detect_element_and_click(element_value='帧率(fps)')
            # 验证帧率主页文案
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            # 模拟右滑返回上一页
            self.back_previous_page()
            # 遍历帧率选项
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='帧率(fps)')

            return texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_precording_plan(self):
        pass










