# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemotePush(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def is_push_on(self):
        """
        判断手机推送按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            if not RemoteSetting().scroll_check_funcs2(texts='测试'):
                self.scroll_click_right_btn(text_to_find='手机推送')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_visitor_phone_remind_on(self):
        """
        判断访客电话提醒按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.is_push_on()
            if not RemoteSetting().scroll_check_funcs2(texts='访客铃声'):
                self.scroll_click_right_btn(text_to_find='访客电话提醒')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_device_notify_ringtone_on(self):
        """
        判断设备通知铃声按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.is_push_on()
            if not RemoteSetting().scroll_check_funcs2(texts='报警铃声'):
                self.scroll_click_right_btn(text_to_find='设备通知铃声')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_delay_notifications_on(self):
        """
        判断延时通知按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.is_push_on()
            if not RemoteSetting().scroll_check_funcs2(texts='延迟时间'):
                self.scroll_click_right_btn(text_to_find='延时通知')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_visitor_phone_remind(self, texts):
        """
        点击并测试访客电话提醒
        :return:
        """
        try:
            visitor_phone_remind_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            self.scroll_click_right_btn(text_to_find='访客电话提醒')
            self.scroll_click_right_btn(text_to_find='访客电话提醒')
            return visitor_phone_remind_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_device_notify_ringtone(self, option_text_list):
        """
        点击并测试设备通知铃声
        :param option_text_list: 需要遍历的报警铃声列表
        :return:
        """
        try:
            self.is_device_notify_ringtone_on()
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='报警铃声')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_plan_text(self, texts_list):
        """
        验证手机推送主页的 计划 文案
        :return:
        """
        try:
            push_plan_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return push_plan_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_push_plan(self, texts_list):
        """
        点击计划并验证文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='计划')
            plan_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return plan_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_push_alarm_type(self, texts_list):
        """
        点击手机推送的报警类型，验证文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警类型')
            alarm_type_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            self.back_previous_page()
            self.back_previous_page()
            return alarm_type_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_push_interval_text(self, texts_list):
        """
        验证推送间隔文案
        :return:
        """
        try:
            push_interval_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return push_interval_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_push_interval(self, option_text_list):
        """
        点击并遍历推送间隔
        :return:
        """
        try:
            self.is_device_notify_ringtone_on()
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='推送间隔')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_delay_notifications(self, option_text_list):
        """
        点击并测试延时通知
        :param option_text_list: 需要遍历的延迟时间列表
        :return:
        """
        try:
            self.is_delay_notifications_on()
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='延迟时间')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_button(self):
        """
        点击测试按钮
        :return:
        """
        try:
            self.is_push_on()
            self.scroll_and_click_by_text('测试')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
