# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteCameraRecord(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def is_camera_recording_on(self):
        """
        判断摄像机录像按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            if not RemoteSetting().scroll_check_funcs2(texts='报警类型'):
                self.scroll_click_right_btn(text_to_find='摄像机录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_camera_record_main_text(self, main_text, record_type):
        """
        验证摄像机录像主页文案
        :param record_type: 支持的录像类型：报警录像，定时录像
        :param main_text: 待验证的文案列表
        :return:
        """
        try:
            self.is_camera_recording_on()
            self.scroll_and_click_by_text(text_to_find=record_type)
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_camera_timed_recording_page_text(self, texts_list):
        """
        验证 摄像机主页>定时录像 文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.is_camera_recording_on()
            self.scroll_and_click_by_text(text_to_find='定时录像')
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return camera_recording_page_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_alarm_recording_plan(self, texts_list, supported_alarm_type, alarm_type_text, option_text):
        """
        点击并测试 报警录像>报警录像计划 并验证文案内容
        :param texts_list: 需要验证的文案列表
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param alarm_type_text: 报警类型筛选页面的文案
        :param option_text: 报警类型筛选页面的可勾选选项
        :return:
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='报警录像')  # 点击报警录像
            self.scroll_and_click_by_text(text_to_find='报警录像计划')  # 点击报警录像计划

            # 验证报警录像计划文案
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)

            alarm_type_text_res = True
            # 如果支持选择报警类型：
            if supported_alarm_type:
                self.click_checkbox_by_text(option_text_list=option_text, menu_text='报警类型')
                alarm_type_text_res = RemoteSetting().scroll_check_funcs2(texts=alarm_type_text)
                self.scroll_and_click_by_text(text_to_find=option_text[0])  # 保底选项，防止下一步无法点击保存
                self.scroll_and_click_by_text('保存')

            return camera_recording_page_text_status, alarm_type_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_timed_recording_plan(self, texts_list, supported_alarm_type, alarm_type_text, option_text):
        """
        点击并测试 定时录像>定时录像计划 并验证文案内容
        :param texts_list: 需要验证的文案列表
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param alarm_type_text: 报警类型筛选页面的文案
        :param option_text: 报警类型筛选页面的可勾选选项
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='定时录像')  # 点击定时录像
            self.scroll_and_click_by_text(text_to_find='定时录像计划')  # 点击定时录像计划

            # 验证定时录像计划文案
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)

            alarm_type_text_res = True
            # 如果支持选择报警类型：
            if supported_alarm_type:
                self.click_checkbox_by_text(option_text_list=option_text, menu_text='报警类型')
                alarm_type_text_res = RemoteSetting().scroll_check_funcs2(texts=alarm_type_text)
                self.scroll_and_click_by_text(text_to_find=option_text[0])  # 保底选项，防止下一步无法点击保存
                self.scroll_and_click_by_text('保存')

            return camera_recording_page_text_status, alarm_type_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_record_delay_duration(self, texts_list, option_text_list):
        """
        验证录像延时时长文案内容,验证完毕后返回上一页。
        :param texts_list: 需要验证的文案列表
        :param option_text_list: 遍历操作选项列表
        :return:
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='报警录像')  # 点击报警录像
            self.scroll_and_click_by_text(text_to_find='录像延时时长')
            # 验证录像延时时长主页文案
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            # 遍历操作选项
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='录像延时时长')

            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_overwrite_record(self):
        """
        点击两次覆盖录像的开关按钮
        :return:
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_click_right_btn(text_to_find='覆盖录像')
            self.scroll_click_right_btn(text_to_find='覆盖录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_pre_recording(self):
        """
        点击两次预录像的开关按钮
        :return:
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_click_right_btn(text_to_find='预录像')
            self.scroll_click_right_btn(text_to_find='预录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_test_frame_rate(self, texts, option_text):
        """
        遍历智能省电模式的帧率
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='帧率(fps)')
            # 验证popup文案
            popup_text_res = RemoteSetting().scroll_check_funcs2(texts=texts)

            # 遍历popup选项
            self.iterate_and_click_popup_text(option_text_list=option_text, menu_text='帧率(fps)')

            return popup_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_smart_power_saving_mode(self, texts_list, frame_rate_texts, option_text):
        """
        点击并测试智能省电模式
        :param texts_list:
        :param frame_rate_texts:
        :param option_text:
        :return:
        """
        try:
            self.is_camera_recording_on()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='定时录像')  # 点击定时录像
            self.scroll_and_click_by_text(text_to_find='智能省电模式')  # 点击智能省电模式

            main_text_res = None
            # 点击开启/关闭智能省电模式
            if not RemoteSetting().scroll_check_funcs2(texts='电量'):
                self.scroll_click_right_btn(text_to_find='智能省电模式')  # 开启
                # 验证智能省电模式主页文案
                main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts_list)
                # 遍历popup选项
                self.clk_test_frame_rate(texts=frame_rate_texts, option_text=option_text)

                self.scroll_click_right_btn(text_to_find='智能省电模式')  # 关闭
            else:
                # 遍历popup选项
                self.clk_test_frame_rate(texts=frame_rate_texts, option_text=option_text)
                self.scroll_click_right_btn(text_to_find='智能省电模式')  # 关闭

            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
