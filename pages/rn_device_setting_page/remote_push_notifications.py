# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
_ReoIcon_Draw = g_config.get('ReoIcon_Draw')  # 计划主页底部涂画按钮
_ReoIcon_Erase = g_config.get('ReoIcon_Erase')  # 计划主页底部擦除按钮
draw_text = g_config.get('draw_text')  # 选择涂抹按钮后显示的文案
erase_text = g_config.get('erase_text')  # 选择擦除按钮后显示的文案
alarm_type_selector = g_config.get('alarm_type_selector')  # 计划>报警类型 选项
push_checkbox_agree_icon = g_config.get('push_checkbox_agree_icon')  # 首次打开推送隐私条款弹窗勾选框勾选图标
push_popup_content = g_config.get('push_popup_content')  # 推送隐私条款弹窗内容


class RemotePush(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass
            # self.alarm_type_selector = 'ReoTitle'  # 计划>报警类型 选项
            # self.ReoIcon_Draw = '//*[@resource-id="ReoIcon-Draw"]'  # 计划主页底部涂画按钮
            # self.ReoIcon_Erase = '//*[@resource-id="ReoIcon-Erase"]'  # 计划主页底部擦除按钮

        elif self.platform == 'ios':
            pass

    def click_test_button(self):
        """
        点击测试按钮
        :return:
        """
        try:
            def check_tips():
                if not self.loop_detect_element_exist(element_value='正在发送测试推送', time_interval=1, scroll_or_not=False):
                    pytest.fail('测试按钮点击后，未出现正在发送测试推送提示')
                else:
                    logger.info('测试按钮点击后，已出现正在发送测试推送提示')

                if self.loop_detect_element_exist(element_value='确定', time_interval=2, scroll_or_not=False):
                    pytest.fail('测试按钮点击后，出现测试失败提示！')

            self.click_by_text('测试')
            check_tips()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def turn_on_push(self):
        """
        判断手机推送按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            is_on = self.find_element_by_xpath_recursively(start_xpath_prefix='//*[@resource-id="ReoCell"]',
                                                           target_id='ReoSwitch:1')
            if is_on:
                logger.info('手机推送按钮已处于开启状态')
                return True
            else:
                logger.info('手机推送按钮处于关闭状态，正在尝试打开')
                self.scroll_click_right_btn(text_to_find='手机推送',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                # 如果检测到声明与条款弹窗则勾选并点击同意
                if self.loop_detect_element_exist(element_value='声明与条款', time_interval=2, scroll_or_not=False):
                    logger.info('检测到声明与条款弹窗，正在尝试勾选并点击同意')
                    # 验证弹窗内容
                    RemoteSetting().scroll_check_funcs2(texts=push_popup_content,
                                                        scroll_or_not=False,
                                                        back2top=False)
                    self.click_by_xpath(xpath_expression=push_checkbox_agree_icon)
                    self.click_by_text('同意')

            time.sleep(5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_push_main_text(self, other_switch):
        """
        验证摄像机录像主页文案
        :param other_switch: 是否其他Switch开关，支持则开启
        :return:
        """
        try:
            self.turn_on_push()  # 打开手机推送

            if BasePage().is_key_in_yaml(other_switch, 'visitor_phone_remind'):
                self.turn_on_visitor_phone_remind()

            if BasePage().is_key_in_yaml(other_switch, 'schedule'):
                RemoteSetting().scroll_check_funcs2(texts='可筛选报警类型或时间进行规划。')  # 验证解释文案

            if BasePage().is_key_in_yaml(other_switch, 'push_interval'):
                RemoteSetting().scroll_check_funcs2(texts='推送间隔')  # 验证推送间隔功能是否存在

            if BasePage().is_key_in_yaml(other_switch, 'device_notify_ringtone'):
                self.turn_on_device_notify_ringtone()
                RemoteSetting().scroll_check_funcs2(texts='开启后，可为设备单独设置通知铃声。')  # 验证解释文案

            if BasePage().is_key_in_yaml(other_switch, 'delay_notifications'):
                self.turn_on_delay_notifications()
                RemoteSetting().scroll_check_funcs2(texts='延迟时间')  # 验证延迟时间功能是否存在

            if BasePage().is_key_in_yaml(other_switch, 'supported_test'):
                self.click_test_button()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def turn_on_visitor_phone_remind(self):
        """
        判断访客电话提醒按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.turn_on_push()

            is_on = self.find_element_by_xpath_recursively(start_xpath_prefix='//*[@text="访客电话提醒"]',
                                                           target_id='ReoSwitch:1')
            if is_on:
                logger.info('访客电话提醒按钮已处于开启状态')
                return True
            else:
                logger.info('访客电话提醒按钮处于关闭状态，正在尝试打开')
                self.scroll_click_right_btn(text_to_find='访客电话提醒',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def turn_on_device_notify_ringtone(self):
        """
        判断设备通知铃声按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.turn_on_push()

            is_on = self.find_element_by_xpath_recursively(start_xpath_prefix='//*[@text="设备通知铃声"]',
                                                           target_id='ReoSwitch:1')
            if is_on:
                logger.info('设备通知铃声已处于开启状态')
                return True
            else:
                logger.info('设备通知铃声处于关闭状态，正在尝试打开')
                self.scroll_click_right_btn(text_to_find='设备通知铃声',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def turn_on_delay_notifications(self):
        """
        判断延时通知按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            self.turn_on_push()

            is_on = self.find_element_by_xpath_recursively(start_xpath_prefix='//*[@text="延时通知"]',
                                                           target_id='ReoSwitch:1')
            if is_on:
                logger.info('延时通知已处于开启状态')
                return True
            else:
                logger.info('延时通知处于关闭状态，正在尝试打开')
                self.scroll_click_right_btn(text_to_find='延时通知',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_device_notify_ringtone(self):
        """
        点击并测试设备通知铃声
        :param text: 需要验证的全局文案
        :param options: 需要遍历的报警铃声列表
        :return:
        """
        text = ['报警铃声', '强烈通知', '重要通知', '一般通知']
        options = ['强烈通知', '重要通知', '一般通知']
        try:
            self.turn_on_device_notify_ringtone()
            time.sleep(1)
            self.click_by_text(text='设备通知铃声')

            RemoteSetting().scroll_check_funcs2(texts=text)
            RemoteSetting().scroll_check_funcs2(texts=options,
                                                selector='ReoTitle')

            self.back_previous_page_by_xpath()

            self.iterate_and_click_popup_text(option_text_list=options, menu_text='报警铃声')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_push_plan(self, texts_list, supported_alarm_type, options_text):
        """
        点击并测试 计划 验证文案内容
        :param texts_list: 需要验证的文案列表
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param options_text: 报警类型筛选页面的可勾选选项
        :return:
        """
        # 计划主页通用内容
        common_plan_texts = ['取消', '计划', '保存', '00', '02', '04', '06', '08', '10', '12', '14', '16', '18',
                             '20', '22', '24', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

        def handle_alarm_type():
            """处理报警型页面的遍历和保存操作"""
            detect_options = options_text['options']  # 报警类型选项文案
            detect_text = ['报警类型', '保存'] + detect_options  # 报警类型全局文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='报警类型')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text)  # 验证报警类型全局文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=alarm_type_selector)  # 验证报警类型选项文案
            self.scroll_and_click_by_text('保存')

        try:
            self.turn_on_push()  # 打开手机推送开关
            self.scroll_and_click_by_text(text_to_find='计划')  # 点击计划

            # 验证计划文案
            RemoteSetting().scroll_check_funcs2(texts=common_plan_texts)
            # 验证底部涂抹按钮文案：涂画
            self.click_by_xpath(xpath_expression=_ReoIcon_Draw)
            RemoteSetting().scroll_check_funcs2(texts=draw_text, scroll_or_not=False, back2top=False)
            # 验证底部涂抹按钮文案：擦除
            self.click_by_xpath(xpath_expression=_ReoIcon_Erase)
            RemoteSetting().scroll_check_funcs2(texts=erase_text, scroll_or_not=False, back2top=False)

            # 如果支持选择报警类型：
            if supported_alarm_type:
                RemoteSetting().scroll_check_funcs2(texts='配置推送的触发类型和时间计划。')  # 验证存在报警类型时上方的解释文案
                handle_alarm_type()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_test_push_interval(self, option_text_list):
        """
        点击并遍历推送间隔
        :param option_text_list: 推送间隔选项
        :return:
        """
        # 拼接全局文案列表
        texts_list = ['推送间隔'] + option_text_list
        try:
            self.turn_on_push()

            if self.loop_detect_element_and_click(element_value='推送间隔', scroll_or_not=True):
                RemoteSetting().scroll_check_funcs2(texts=texts_list)

                self.back_previous_page_by_xpath()

                self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='推送间隔')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_delay_notifications(self, options):
        """
        点击并测试延时通知
        :param text: 延时通知主页全局文案
        :param options: 需要遍历的延迟时间列表
        :return:
        """
        # 拼接全局文案
        text = ['延迟时间'] + options
        try:
            self.turn_on_push()  # 打开手机推送开关
            self.turn_on_delay_notifications()  # 打开延时通知开关
            self.click_by_text(text='延迟时间')  # 点击延迟时间

            # 验证延迟时间主页文案
            RemoteSetting().scroll_check_funcs2(texts=text)
            RemoteSetting().scroll_check_funcs2(texts=options, selector='ReoTitle')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
