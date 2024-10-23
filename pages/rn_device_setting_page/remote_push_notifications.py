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

    def click_test_button(self):
        """
        点击测试按钮
        :return:
        """
        try:
            self.click_by_text('测试')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_push_on(self):
        """
        判断手机推送按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            if not RemoteSetting().scroll_check_funcs2(texts='测试'):  # 可能需要修改判断逻辑，不是所有设备开启后都要测试按钮
                self.scroll_click_right_btn(text_to_find='手机推送')
                time.sleep(6)
                if self.is_element_exists(element_value='确定', scroll_or_not=False):
                    self.click_by_text('确定')
                self.click_by_text('测试')  # 点击测试按钮
                time.sleep(4)

            else:
                if self.is_element_exists(element_value='测试'):
                    self.click_by_text('测试')  # 点击测试按钮
                    time.sleep(3)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_push_main_text(self, main_text):
        """
        验证摄像机录像主页文案
        :param main_text: 待验证的push主页文案列表
        :return:
        """
        try:
            self.is_push_on()
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            return main_text_res
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

    def click_test_push_alarm_type(self, texts_list, supported_alarm_type, option_text_list):
        """
        点击手机推送的报警类型，验证文案内容
        :param texts_list: 需要验证的文案列表
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param option_text_list: 报警类型操作文案
        :return:
        """
        try:
            alarm_type_text_res = True
            if supported_alarm_type:
                self.scroll_and_click_by_text(text_to_find='报警类型')
                alarm_type_text_res = RemoteSetting().scroll_check_funcs2(texts=texts_list)
                self.click_checkbox_by_text(option_text_list=option_text_list, menu_text='报警类型')
                self.back_previous_page()  # 返回到计划主页
                self.back_previous_page()  # 返回到推送主页
            return alarm_type_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_push_interval(self, texts_list, option_text_list):
        """
        点击并遍历推送间隔
        :param texts_list: 推送间隔主页文案
        :param option_text_list: 推送间隔选项
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='推送间隔')
            push_interval_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='推送间隔')

            return push_interval_text_status
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
