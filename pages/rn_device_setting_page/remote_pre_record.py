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
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 编辑分段灵敏度，开始时间设置：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 编辑分段灵敏度，开始时间设置：分钟

        elif self.platform == 'ios':
            pass

    def time_selector(self, direction='up', iteration=1):
        """
        时间选择器
        :param direction: slider的定位方式，支持id或者xpath
        :param iteration:
        :return:
        """
        try:
            # 手指向上滑动选择小时
            self.scroll_selector(id_or_xpath=self.time_selector_hour,
                                 direction=direction,
                                 times=iteration)

            # 手指向上滑动选择分钟
            self.scroll_selector(id_or_xpath=self.time_selector_min,
                                 direction=direction,
                                 times=iteration)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

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
            illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=main_text)

            return main_text_res, illegal_funcs_res
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

    def verify_precording_plan(self, plan_texts, new_plan_texts):
        try:
            # 点击计划，进入计划页面
            self.loop_detect_element_and_click(element_value='计划')
            time.sleep(2)

            # 点击自定义
            self.loop_detect_element_and_click(element_value='自定义')

            # 验证页面文案
            plan_texts_res = RemoteSetting().scroll_check_funcs2(texts=plan_texts)
            plan_illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=plan_texts)

            # 点击新增计划，进入新增计划页面
            self.loop_detect_element_and_click(element_value='//*[@resource-id="com.mcu.reolink:id/ivCreate"]',
                                               selector_type='xpath',
                                               scroll_or_not=False)

            # 在新增计划下选择点击每周，并验证当前页面文案
            self.loop_detect_element_and_click(element_value='每周')
            new_plan_texts_res = RemoteSetting().scroll_check_funcs2(texts=new_plan_texts)
            new_plan_illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=new_plan_texts)

            # 点击并选择开始时间、结束时间
            self.scroll_and_click_by_text('开始时间')  # 点击开始时间
            self.time_selector()  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')  # 点击确定

            self.scroll_and_click_by_text('结束时间')  # 点击结束时间
            self.time_selector(iteration=2)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')  # 点击确定

            # 取消周日、周六、周三
            self.scroll_and_click_by_text('周日')
            self.scroll_and_click_by_text('周六')
            self.scroll_and_click_by_text('周三')

            # 点击完成按钮，新增当前计划
            self.scroll_and_click_by_text('完成')
            custom_plan_res = RemoteSetting().scroll_check_funcs2(texts=['周一,周二,周四,周五'])

            # 点击保存按钮，保存当前计划
            self.scroll_and_click_by_text('保存')

            result = {
                'plan_texts_res': plan_texts_res,
                'plan_illegal_funcs_res': plan_illegal_funcs_res,
                'new_plan_texts_res': new_plan_texts_res,
                'new_plan_illegal_funcs_res': new_plan_illegal_funcs_res,
                'custom_plan_res': custom_plan_res
            }

            return result
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
