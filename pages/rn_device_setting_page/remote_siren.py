# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteSirenAlerts(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def check_siren_alerts_main_text(self, texts):
        """
        验证鸣笛主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            siren_alerts_main_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            return siren_alerts_main_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_siren_alert_on(self):
        """
        判断鸣笛通知按钮开关状态：
            ①如果为关，则点击打开；
            ②如果为开，则不做其他操作。
        :return:
        """
        try:
            # 如果是关：
            if not RemoteSetting().scroll_check_funcs2(texts='鸣笛声音'):
                self.scroll_click_right_btn(text_to_find='鸣笛')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_siren_alarm_type(self, texts_list):
        """
        点击鸣笛>计划>报警类型，验证文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警类型')
            email_alarm_type_text_status = RemoteSetting().click_checkbox_by_text(option_text_list=texts_list, menu_text='报警类型')
            return email_alarm_type_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_plan(self, plan_main_text, alarm_type_text, alarm_type_option_text):
        """
        测试 计划
        :param plan_main_text: 计划主页 文案
        :param alarm_type_text: 报警类型 子页文案
        :param alarm_type_option_text: 报警类型子页操作列表
        :return:
        """
        try:
            self.scroll_and_click_by_text('计划')
            # 验证计划主页 文案内容
            plan_main_text_status = RemoteSetting().scroll_check_funcs2(texts=plan_main_text)

            # 验证报警类型 子页文案
            alarm_type_text_status = RemoteSetting().scroll_check_funcs2(texts=alarm_type_text)

            # 遍历报警类型子页操作列表
            self.click_and_test_siren_alarm_type(texts_list=alarm_type_option_text)

            return plan_main_text_status, alarm_type_text_status

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
