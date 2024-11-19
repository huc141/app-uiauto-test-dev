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

    def iterate_recording_resolution(self, options_text):
        """
        遍历录像清晰度选项
        :param options_text: 清晰度选项，需传入一个列表
        :return:
        """
        try:
            for i in options_text:
                self.loop_detect_element_and_click(element_value='录像清晰度')
                self.scroll_and_click_by_text(text_to_find=i)  # 点击清晰度的选项：清晰、流畅、均衡···

                if i == '清晰' and self.loop_detect_element_exist(element_value='开启前须知'):
                    self.scroll_and_click_by_text(text_to_find='取消')
                    self.scroll_and_click_by_text(text_to_find='清晰')
                    self.scroll_and_click_by_text(text_to_find='启用')

                if not self.loop_detect_element_exist(element_value=i):
                    pytest.fail(f'录像清晰度: {i} 未回显！')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

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

            # 遍历清晰度选项
            self.iterate_recording_resolution(options_text=option_text_list)

            return main_text_res, illegal_funcs_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_storage_duration_text(self):
        """
        验证存储时长主页文案
        :return:
        """
        try:
            self.loop_detect_element_and_click(element_value='存储时长')
            if not self.loop_detect_element_exist(element_value='存储时长'):
                pytest.fail(f'未进入存储时长页面 或 缺失页面标题！')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_email_alarm_type(self, texts_list, option_text):
        """
        点击邮件通知>计划>报警>报警类型，验证文案内容
        :param texts_list: 报警类型页面需要验证的文案列表
        :param option_text: 操作列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警类型')
            plan_alarm_type_text_res = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            RemoteSetting().click_checkbox_by_text(option_text_list=option_text, menu_text='报警类型')
            time.sleep(1)
            self.scroll_and_click_by_text(text_to_find='保存')  # 点击报警类型的保存按钮
            self.scroll_and_click_by_text(text_to_find='保存')  # 保存当前计划
            return plan_alarm_type_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_plan(self, plan_alarm_text, plan_timed_text, alarm_type_text, alarm_type_option_text):
        """
        测试 计划
        :param plan_alarm_text: 计划>报警> 文案
        :param plan_timed_text: 计划>定时 文案
        :param alarm_type_text: 计划>报警>报警类型 文案
        :param alarm_type_option_text: 计划>报警>报警类型 操作选项
        :return:
        """
        try:
            self.scroll_and_click_by_text('计划')
            # 验证计划>报警>文案内容
            self.scroll_and_click_by_text('报警')
            plan_alarm_main_text_res = RemoteSetting().scroll_check_funcs2(texts=plan_alarm_text)

            # 验证计划>定时 文案内容
            self.scroll_and_click_by_text('定时')
            plan_timed_main_text_res = RemoteSetting().scroll_check_funcs2(texts=plan_timed_text)

            # 点击报警>报警类型
            self.scroll_and_click_by_text('报警')
            plan_alarm_type_text_res = self.click_and_test_email_alarm_type(texts_list=alarm_type_text,
                                                                            option_text=alarm_type_option_text)

            result = {
                'plan_alarm_main_text': plan_alarm_main_text_res,
                'plan_timed_main_text': plan_timed_main_text_res,
                'plan_alarm_type_text': plan_alarm_type_text_res
            }

            return result

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")