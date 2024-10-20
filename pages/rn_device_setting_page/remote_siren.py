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
            self.siren_start_record = ''  # 添加自定义声音的开始录制按钮
            self.siren_stop_record = ''  # 添加自定义声音的停止录制按钮
            self.edit_custom_sound_button = ''  # 自定义声音的编辑按钮
            self.clear_custom_sound_button = ''  # 清空自定义声音的 按钮
            self.rerecord_custom_sound = ''  # 重录按钮
            self.play_sound_button = ''  # 录制声音页面的播放按钮

        elif self.platform == 'ios':
            self.siren_start_record = ''
            self.siren_stop_record = ''
            self.edit_custom_sound_button = ''
            self.clear_custom_sound_button = ''
            self.rerecord_custom_sound = ''
            self.play_sound_button = ''

    @staticmethod
    def check_siren_alerts_main_text(texts):
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

    def clear_custom_sound(self):
        """
        点击编辑自定义声音按钮，重录自定义声音、清空自定义声音文件
        :return:
        """
        try:
            self.is_siren_alert_on()
            if RemoteSetting().scroll_check_funcs2('自定义声音'):
                # 点击自定义声音的编辑按钮
                self.scroll_and_click_by_text(text_to_find=self.edit_custom_sound_button, el_type='xpath')

                # 点击重录按钮
                self.scroll_and_click_by_text(text_to_find=self.rerecord_custom_sound, el_type='xpath')
                # 点击开始录制按钮
                self.scroll_and_click_by_text(text_to_find=self.siren_start_record, el_type='xpath')
                time.sleep(3)  # 等待录制3秒

                # 点击停止录制按钮
                self.scroll_and_click_by_text(text_to_find=self.siren_stop_record, el_type='xpath')

                # 点击清空按钮
                self.scroll_and_click_by_text(text_to_find=self.clear_custom_sound_button, el_type='xpath')
                # 点击取消
                self.scroll_and_click_by_text(text_to_find='取消')
                # 点击清空按钮
                self.scroll_and_click_by_text(text_to_find=self.clear_custom_sound_button, el_type='xpath')
                # 点击确认
                self.scroll_and_click_by_text(text_to_find='确认')

                # 验证清空成功后回到鸣笛主页
                siren_main_res = RemoteSetting().scroll_check_funcs2('鸣笛')

                return siren_main_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_test_custom_sound(self):
        """
        点击并测试默认声音、添加自定义声音
        :return:
        """
        try:
            before_record_sound_text_list = ['取消', '录制声音', '保存']
            after_record_sound_text_list = ['取消', '录制声音', '保存', '重录', '清空']

            self.scroll_and_click_by_text('添加自定义声音')
            # 验证录制前的页面文案
            bf_res = RemoteSetting().scroll_check_funcs2(texts=before_record_sound_text_list)

            # 点击开始录制按钮
            self.scroll_and_click_by_text(text_to_find=self.siren_start_record, el_type='xpath')
            time.sleep(6)  # 等待录制6秒自动完成录制

            # 验证录制后的页面文案
            af_res = RemoteSetting().scroll_check_funcs2(texts=after_record_sound_text_list)

            # 点击播放按钮
            self.scroll_and_click_by_text(text_to_find=self.play_sound_button, el_type='xpath')
            time.sleep(6)

            # 保存录音
            self.scroll_and_click_by_text(text_to_find='保存')

            return bf_res, af_res

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
