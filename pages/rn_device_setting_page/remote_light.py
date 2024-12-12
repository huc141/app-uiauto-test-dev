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
            self.base_left_button = '//*[@resource-id="PageHeaderLeft"]'  # 左上角返回上一页按钮

        elif self.platform == 'ios':
            self.time_selector_hour = ''
            self.time_selector_min = ''
            self.base_left_button = ''

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

    def check_lights_main_text(self, lights_num, texts):
        """
        验证灯主页文案
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            # 如果是多个灯
            if lights_num:
                if not self.loop_detect_element_exist(element_value='//*[@text="灯"]', selector_type='xpath',
                                                      loop_times=2, scroll_or_not=False):
                    pytest.fail(f"当前页面缺失headerTitle ==> ‘灯’")

                lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts, selector='ReoTitle')

                return lights_main_text_res

            # 如果只有一个灯，则验证该灯的配置页文案
            else:
                light_config_text_res = RemoteSetting().scroll_check_funcs2(texts=texts)

                return light_config_text_res

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    @staticmethod
    def verify_lights_list_length(texts):
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
                    self.back_previous_page_by_xpath()
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

    def click_test_floodlight_night_smart_mode(self, lights_num, supported_detect_type, flood_light_texts,
                                               options_text):
        """
        点击并测试照明灯的夜间智能模式，（没有验证侦测页的文案）
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param supported_detect_type: 是否支持 侦测
        :param flood_light_texts: 配置页文案
        :param options_text: 配置页操作项
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》夜间智能模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='夜间智能模式')
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 如果支持侦测类型，则点击侦测类型，否则返回灯主页：
                if supported_detect_type:
                    # 点击侦测类型，进入侦测页面遍历,遍历完成点击保存，回到灯主页
                    self.click_checkbox_by_text(option_text_list=options_text, menu_text='侦测')
                    self.scroll_and_click_by_text(text_to_find=options_text[0])  # 保底选项，防止下一步无法点击保存
                    self.scroll_and_click_by_text('保存')

                # 返回灯主页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='夜间智能模式'):
                    pytest.fail(f"照明灯选择【夜间智能模式】后，未检查到回显！")

                return floodlight_main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='夜间智能模式')
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                # 如果支持侦测类型，则点击侦测类型，否则返回灯主页：
                if RemoteSetting().scroll_check_funcs2(texts='侦测'):
                    # 点击侦测类型，进入侦测页面遍历,遍历完成点击保存，回到照明灯的配置页
                    self.click_checkbox_by_text(option_text_list=options_text, menu_text='侦测')
                    self.scroll_and_click_by_text(text_to_find=options_text[0])  # 保底选项，防止下一步无法点击保存
                    self.scroll_and_click_by_text('保存')

                return floodlight_main_text_res

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_floodlight_smart_mode(self, lights_num, supported_detect_type, flood_light_texts, options_text):
        """
        点击并测试照明灯的智能模式（没有验证侦测页的文案）
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param supported_detect_type: 是否支持 侦测
        :param flood_light_texts: 配置页文案
        :param options_text: 配置页操作项
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》智能模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='智能模式')
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 如果支持侦测类型，则点击侦测类型，否则返回灯主页：
                if supported_detect_type:
                    # 点击侦测类型，进入侦测页面遍历,遍历完成点击保存，回到灯主页
                    self.click_checkbox_by_text(option_text_list=options_text, menu_text='侦测')
                    self.scroll_and_click_by_text(text_to_find=options_text[0])  # 保底选项，防止下一步无法点击保存
                    self.scroll_and_click_by_text('保存')

                # 分别选择智能模式的开始时间、结束时间
                self.scroll_and_click_by_text(text_to_find='开始时间')  # 点击开始时间
                self.time_selector(iteration=1)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                self.scroll_and_click_by_text(text_to_find='结束时间')  # 点击结束时间
                self.time_selector(iteration=2)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                # 返回灯主页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='智能模式'):
                    pytest.fail(f"照明灯选择【智能模式】后，未检查到回显！")

                return floodlight_main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='智能模式')
                # 验证照明灯主页文案
                floodlight_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                # 如果支持侦测类型，则点击侦测类型，否则返回灯主页：
                if supported_detect_type:
                    # 点击侦测类型，进入侦测页面遍历,遍历完成点击保存，回到照明灯的配置页
                    self.click_checkbox_by_text(option_text_list=options_text, menu_text='侦测')
                    self.scroll_and_click_by_text(text_to_find=options_text[0])  # 保底选项，防止下一步无法点击保存
                    self.scroll_and_click_by_text('保存')

                # 分别选择智能模式的开始时间、结束时间
                self.scroll_and_click_by_text(text_to_find='开始时间')  # 点击开始时间
                self.time_selector(iteration=1)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                self.scroll_and_click_by_text(text_to_find='结束时间')  # 点击结束时间
                self.time_selector(iteration=2)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                return floodlight_main_text_res

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_floodlight_timer_mode(self, lights_num, flood_light_texts):
        """
        点击并测试白光灯的定时模式
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param flood_light_texts: 配置页文案
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》定时模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='定时模式')
                # 验证照明灯主页文案
                timer_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 点击开始时间
                self.scroll_and_click_by_text(text_to_find='开始时间')
                self.time_selector(iteration=1)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                # 点击结束时间
                self.scroll_and_click_by_text(text_to_find='结束时间')
                self.time_selector(iteration=2)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                # 返回灯聚合页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='定时模式'):
                    pytest.fail(f"照明灯选择【定时模式】后，未检查到回显！")

                return timer_main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='定时模式')
                # 验证照明灯主页文案
                timer_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 点击开始时间
                self.scroll_and_click_by_text(text_to_find='开始时间')
                self.time_selector(iteration=1)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                # 点击结束时间
                self.scroll_and_click_by_text(text_to_find='结束时间')
                self.time_selector(iteration=2)  # 选择时、分
                self.scroll_and_click_by_text(text_to_find='确定')

                return timer_main_text_res

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_floodlight_night_vision_steady_light_mode(self, lights_num, flood_light_texts):
        """
        点击测试白光灯/泛光灯的夜视常亮模式
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》夜视常亮 模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='夜视常亮')
                # 验证照明灯主页文案
                light_steady_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                return light_steady_main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='夜视常亮')
                # 验证照明灯主页文案
                light_off_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                return light_off_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_preview_opens_auto(self, lights_num, flood_light_texts):
        """
        点击测试 照明灯>预览自动开启 的switch切换按钮
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》预览自动开启
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_click_right_btn(text_to_find='预览自动开启')
                # 验证照明灯主页文案
                preview_opens_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 返回灯聚合页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='夜视常亮'):
                    pytest.fail(f"照明灯选择【夜视常亮】后，未检查到回显！")

                return preview_opens_text_res

            else:
                self.scroll_click_right_btn(text_to_find='预览自动开启')
                # 验证照明灯主页文案
                preview_opens_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                return preview_opens_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_light_off_mode(self, lights_num, flood_light_texts):
        """
        点击测试白光灯的关闭模式
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》关闭模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='关闭')
                # 验证照明灯主页文案
                light_off_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 返回灯聚合页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                    pytest.fail(f"照明灯选择【关闭模式】后，未检查到回显！")

                return light_off_main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='关闭')
                # 验证照明灯主页文案
                light_off_main_text_res = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                return light_off_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_light_auto_mode(self, lights_num, flood_light_texts):
        """
        点击测试照明灯>自动模式
        :param lights_num:
        :param flood_light_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击照明灯》自动模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='照明灯')
                self.scroll_and_click_by_text(text_to_find='自动模式')
                # 验证照明灯主页文案
                flood_light_texts = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)

                # 返回灯聚合页，验证照明灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动模式'):
                    pytest.fail(f"照明灯选择【关闭模式】后，未检查到回显！")

                return flood_light_texts

            else:
                self.scroll_and_click_by_text(text_to_find='自动模式')
                # 验证照明灯主页文案
                flood_light_texts = RemoteSetting().scroll_check_funcs2(texts=flood_light_texts)
                return flood_light_texts
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_status_lights_off(self, lights_num, status_lights_texts):
        """
        点击测试状态灯》关闭模式
        :param lights_num:
        :param status_lights_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击状态灯》关闭模式
            if lights_num:
                self.loop_detect_element_and_click(element_value='状态灯')
                self.loop_detect_element_and_click(element_value='关闭')
                # 验证状态灯主页文案
                status_lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=status_lights_texts)

                # 返回灯聚合页，验证状态灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                    pytest.fail(f"状态灯选择【关闭】后，未检查到回显！")

                return status_lights_main_text_res

            else:
                self.loop_detect_element_and_click(element_value='关闭')
                # 验证状态灯主页文案
                status_lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=status_lights_texts)

                return status_lights_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_status_lights_on(self, lights_num, status_lights_texts):
        """
        点击测试状态灯》开启模式
        :param lights_num:
        :param status_lights_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击状态灯》开启模式
            if lights_num:
                self.loop_detect_element_and_click(element_value='状态灯')
                self.loop_detect_element_and_click(element_value='开启')
                # 验证状态灯主页文案
                status_lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=status_lights_texts)

                # 返回灯聚合页，验证状态灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='开启'):
                    pytest.fail(f"状态灯选择【开启】后，未检查到回显！")

                return status_lights_main_text_res

            else:
                self.loop_detect_element_and_click(element_value='开启')
                # 验证状态灯主页文案
                status_lights_main_text_res = RemoteSetting().scroll_check_funcs2(texts=status_lights_texts)

                return status_lights_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_doorbell_button_light_off(self, lights_num, button_light_texts):
        """
        点击测试门铃按钮灯》关闭模式
        :param lights_num:
        :param button_light_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》开启模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')

                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)

                self.scroll_and_click_by_text(text_to_find='关闭')

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                    pytest.fail(f"状态灯选择【关闭】后，未检查到回显！")

                return button_light__main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='关闭')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)
                return button_light__main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_doorbell_button_light_auto(self, lights_num, button_light_texts):
        """
        点击测试门铃按钮灯》自动模式
        :param lights_num:
        :param button_light_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》自动模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='自动')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动'):
                    pytest.fail(f"状态灯选择【自动】后，未检查到回显！")

                return button_light__main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='自动')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)
                return button_light__main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_doorbell_button_light_auto_on_night(self, lights_num, button_light_texts):
        """
        点击测试门铃按钮灯》自动且夜间常亮 模式
        :param lights_num:
        :param button_light_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》自动且夜间常亮模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='自动且夜间常亮')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动且夜间常亮'):
                    pytest.fail(f"状态灯选择【自动且夜间常亮】后，未检查到回显！")

                return button_light__main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='自动且夜间常亮')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)
                return button_light__main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_doorbell_button_light_always_on(self, lights_num, button_light_texts):
        """
        点击测试门铃按钮灯》常亮 模式
        :param lights_num:
        :param button_light_texts:
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》常亮模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='常亮')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='常亮'):
                    pytest.fail(f"状态灯选择【常亮】后，未检查到回显！")

                return button_light__main_text_res

            else:
                self.scroll_and_click_by_text(text_to_find='常亮')
                # 验证按钮灯主页文案
                button_light__main_text_res = RemoteSetting().scroll_check_funcs2(texts=button_light_texts)
                return button_light__main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
