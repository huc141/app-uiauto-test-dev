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

    def check_camera_alarm_recording_page_text(self, texts_list):
        """
        验证 摄像机主页>报警录像 文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警录像')
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return camera_recording_page_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_camera_timed_recording_page_text(self, texts_list):
        """
        验证 摄像机主页>定时录像 文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='定时录像')
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return camera_recording_page_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_alarm_recording_plan(self, texts_list):
        """
        点击报警录像计划并验证文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警录像')
            self.scroll_and_click_by_text(text_to_find='报警录像计划')
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return camera_recording_page_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_alarm_type(self, texts_list):
        """
        点击报警类型，验证文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警类型')
            alarm_type_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return alarm_type_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_timed_recording_text(self, texts_list):
        """验证定时录像计划文案内容"""
        try:
            self.scroll_and_click_by_text(text_to_find='定时录像计划')
            timed_recording_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return timed_recording_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错：{str(e)}")

    def check_record_delay_duration_text(self, texts_list):
        """
        验证录像延时时长文案内容,验证完毕后返回上一页。
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='录像延时时长')
            alarm_type_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            self.back_previous_page()
            return alarm_type_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_record_delay_duration(self, option_text_list):
        """
        点击录像延时时长，遍历点击延时时长选项
        :param option_text_list: 需要遍历的列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='录像延时时长')
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='录像延时时长')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_overwrite_record(self):
        """
        点击两次覆盖录像的开关按钮
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find='覆盖录像')
            self.scroll_click_right_btn(text_to_find='覆盖录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")




















