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
device_dir = g_config.get('device_dir')  # 电源/电池机目录


class RemoteCameraRecord(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass
            # self.alarm_type_selector = 'ReoTitle'  # 报警录像计划>报警类型 选项
            # self.ReoIcon_Draw = '//*[@resource-id="ReoIcon-Draw"]'  # 报警录像计划主页底部涂画按钮
            # self.ReoIcon_Erase = '//*[@resource-id="ReoIcon-Erase"]'  # 报警录像计划主页底部擦除按钮

        elif self.platform == 'ios':
            pass

    def turn_on_camera_recording(self):
        """
        判断摄像机录像按钮开关状态，如果为关，则点击打开
        :return:
        """
        try:
            is_on = self.find_element_by_xpath_recursively(start_xpath_prefix='//*[@resource-id="record_switch"]',
                                                           target_id='ReoSwitch:1')
            if is_on:
                logger.info('摄像机录像按钮已处于开启状态')
                return True
            else:
                logger.info('摄像机录像按钮处于关闭状态，正在尝试打开')
                self.scroll_click_right_btn(text_to_find='摄像机录像',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(5)
        except Exception as e:
            pytest.fail(f'摄像机录像按钮开关状态判断函数执行失败，失败原因{e}')

    def check_camera_record_main_text(self, camera_record_config):
        """
        验证摄像机录像主页文案
        :param camera_record_config: 摄像机录像yaml配置
        :return:
        """
        supported_modes = []
        supported_cn_name = []
        # 模式名称映射
        mode_name_mapping = {
            'alarm_recording_plan': '报警录像计划',
            'auto_extended_recording': '自动延长录像',
            'record_delay_duration': '录像延时时长',
            'pre_record': '预录像',
            'timed_recording_plan': '定时录像计划',
            'smart_power_saving_mode': '智能省电模式'
        }
        # 电源机模式解释文案
        mode_texts_mapping = {
            'alarm_recording_plan': '配置报警录像（检测到报警事件时触发录像）的触发类型和时间计划。',
            'auto_extended_recording': '通过AI辅助延长录像持续到事件结束，最长120秒。',
            'record_delay_duration': '触发事件停止后延后录制的时长',
            'pre_record': '触发报警前开始录像',
            'timed_recording_plan': '配置持续录像的时间计划，启用的时间段会持续不间断录像。',
            'smart_power_saving_mode': '不同电量下摄像机会以不同的设置进行定时录像，以延长使用时间。'
        }
        # 电池机模式解释文案
        b_mode_texts_mapping = {
            'alarm_recording_plan': '配置报警录像（检测到报警事件时触发录像）的触发类型和时间计划。',
            'auto_extended_recording': '通过AI辅助延长录像持续到事件结束，最长120秒。',
            'record_delay_duration': '触发事件停止后延后录制的时长。延时越长，能耗越大。',
            'pre_record': '触发报警前开始录像',
            'timed_recording_plan': '配置持续录像的时间计划，启用的时间段会持续不间断录像。',
            'smart_power_saving_mode': '不同电量下摄像机会以不同的设置进行定时录像，以延长使用时间。'
        }

        # def check_text(mode_type):
        #     if device_dir.startswith('power'):
        #         if mode_type in mode_texts_mapping:
        #             RemoteSetting().scroll_check_funcs2(texts=mode_texts_mapping[mode_type],
        #                                                 back2top=False)
        #         else:
        #             logger.error(f"未识别的模式 ==> {mode_type}")
        #     else:
        #         if mode_type in b_mode_texts_mapping:
        #             RemoteSetting().scroll_check_funcs2(texts=b_mode_texts_mapping[mode_type],
        #                                                 back2top=False)
        #         else:
        #             logger.error(f"未识别的模式 ==> {mode_type}")

        def check_text(mode_type):
            # 定义映射字典的获取方式
            texts_mapping = b_mode_texts_mapping if not device_dir.startswith('power') else mode_texts_mapping

            # 检查模式类型是否在映射字典中
            if mode_type in texts_mapping:
                RemoteSetting().scroll_check_funcs2(texts=texts_mapping[mode_type], back2top=False)
            else:
                logger.error(f"未识别的模式 ==> {mode_type}")

        def check_modes():
            # 检查每个模式
            for mode in camera_record_config:
                if camera_record_config[mode]:
                    # 构建支持的模式列表
                    supported_modes.append(mode)

                    # 转换键名为对应的模式名称，构建名称列表
                    mode_name = mode_name_mapping.get(mode, mode)
                    supported_cn_name.append(mode_name)

        try:
            # 打开摄像机录像开关
            self.turn_on_camera_recording()
            # 统计该设备的模式
            check_modes()
            # 验证全局文案
            for i in supported_modes:
                check_text(mode_type=i)
            # 验证选项文案
            RemoteSetting().scroll_check_funcs2(texts=supported_cn_name, selector='ReoTitle')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_camera_timed_recording_page_text(self, texts_list):
        """
        验证 摄像机主页>定时录像 文案内容
        :param texts_list: 需要验证的文案列表
        :return:
        """
        try:
            self.turn_on_camera_recording()
            self.scroll_and_click_by_text(text_to_find='定时录像')
            camera_recording_page_text_status = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            return camera_recording_page_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_alarm_recording_plan(self, supported_alarm_type, options_text):
        """
        点击并测试 报警录像>报警录像计划 并验证文案内容
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param options_text: 报警类型筛选页面的可勾选选项
        :return:
        """
        # common_texts这里有个疑问，顶部标题到底是使用【报警录像计划】还是【计划】
        common_texts = ['取消', '计划', '保存',
                        '配置报警录像（检测到报警事件时触发录像）的触发类型和时间计划。', ]

        def handle_alarm_type():
            """处理报警型页面的遍历和保存操作"""
            detect_options = options_text['options']  # 报警类型选项文案
            detect_text = ['保存', '全选', '报警类型'] + detect_options  # 拼接报警类型全局文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='报警类型')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text)  # 验证报警类型全局文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=alarm_type_selector)  # 验证报警类型选项文案
            self.scroll_and_click_by_text('保存')

        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='报警录像计划')  # 点击报警录像计划

            # 验证报警录像计划文案
            RemoteSetting().scroll_check_funcs2(texts=common_texts, back2top=False)
            # 验证底部涂抹按钮文案：涂画
            self.click_by_xpath(xpath_expression=_ReoIcon_Draw)
            RemoteSetting().scroll_check_funcs2(texts=draw_text, scroll_or_not=False, back2top=False)
            # 验证底部涂抹按钮文案：擦除
            self.click_by_xpath(xpath_expression=_ReoIcon_Erase)
            RemoteSetting().scroll_check_funcs2(texts=erase_text, scroll_or_not=False, back2top=False)

            # 如果支持选择报警类型：
            if supported_alarm_type:
                handle_alarm_type()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def auto_extended_record(self):
        """
        测试自动延长录像
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find='自动延长录像',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')
            time.sleep(3)

            self.scroll_click_right_btn(text_to_find='自动延长录像',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_timed_recording_plan(self, supported_alarm_type, options_text):
        """
        点击并测试 定时录像>定时录像计划 并验证文案内容
        :param supported_alarm_type: 是否支持报警类型筛选，bool
        :param options_text: 报警类型筛选页面的可勾选选项
        """
        common_texts = ['取消', '定时录像计划', '保存',
                        '配置持续录像的时间计划，启用的时间段会持续不间断地录像。']

        def handle_alarm_type():
            """处理报警型页面的遍历和保存操作"""
            detect_options = options_text['options']  # 报警类型选项文案
            detect_text = ['报警类型', '保存', '全选'] + detect_options  # 报警类型全局文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='报警类型')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text)  # 验证报警类型全局文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=alarm_type_selector)  # 验证报警类型选项文案
            self.scroll_and_click_by_text('保存')

        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='定时录像计划')  # 点击定时录像计划

            # 验证定时录像计划文案
            RemoteSetting().scroll_check_funcs2(texts=common_texts)
            # 验证底部涂抹按钮文案：涂画
            self.click_by_xpath(xpath_expression=_ReoIcon_Draw)
            RemoteSetting().scroll_check_funcs2(texts=draw_text, scroll_or_not=False, back2top=False)
            # 验证底部涂抹按钮文案：擦除
            self.click_by_xpath(xpath_expression=_ReoIcon_Erase)
            RemoteSetting().scroll_check_funcs2(texts=erase_text, scroll_or_not=False, back2top=False)

            # 如果支持选择报警类型：
            if supported_alarm_type:
                handle_alarm_type()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_record_delay_duration(self, options):
        """
        验证录像延时时长文案内容,验证完毕后返回上一页。
        :param options: 遍历操作选项列表
        :return:
        """
        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='录像延时时长')  # 点击录像延时时长
            # 验证标题
            RemoteSetting().scroll_check_funcs2(texts='录像延时时长', back2top=False)

            # 遍历操作选项
            self.iterate_and_click_popup_text(option_text_list=options, menu_text='录像延时时长')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_overwrite_record(self):
        """
        点击两次覆盖录像的开关按钮
        :return:
        """
        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_click_right_btn(text_to_find='覆盖录像')
            self.scroll_click_right_btn(text_to_find='覆盖录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_test_pre_recording(self):
        """
        点击两次预录像的开关按钮
        :return:
        """
        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_click_right_btn(text_to_find='预录像',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup'
                                        )
            time.sleep(3)
            self.scroll_click_right_btn(text_to_find='预录像',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup'
                                        )
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

    def verify_smart_power_saving_mode(self, support_frame_rate, options, fps_options):
        """
        点击并测试智能省电模式
        :param support_frame_rate: 是否支持帧率
        :param options: 智能省电模式主页ReoTitle选项列表
        :param fps_options: 帧率ReoTitle选项列表
        :return:
        """
        texts_list = ['智能省电模式', '不同电量下摄像机会以不同的设置进行定时录像，以延长使用时间。',
                      '0%', '100%']
        fps_texts_list = ['帧率(fps)', '低帧率续航更长，高帧率观看体验更佳']

        def turn_on_smart_power_saving_mode():
            """
            判断智能省电模式开关是否处于开启状态，未开启则点击开启
            :return:
            """
            if self.is_element_exists(element_value='ReoSwitch:1', selector_type='id'):
                logger.info('智能省电模式开关已处于开启状态')
                return True
            else:
                logger.info('智能省电模式开关未处于开启状态，正在尝试开启')
                self.scroll_click_right_btn(text_to_find='智能省电模式',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(5)

        try:
            self.turn_on_camera_recording()  # 打开摄像机录像开关
            self.scroll_and_click_by_text(text_to_find='智能省电模式')  # 点击智能省电模式

            # 开启智能省电模式
            turn_on_smart_power_saving_mode()
            # 验证智能省电模式主页文案
            RemoteSetting().scroll_check_funcs2(texts=texts_list)
            # 验证智能省电模式的菜单选项
            RemoteSetting().scroll_check_funcs2(texts=options,
                                                selector='ReoTitle',
                                                scroll_or_not=False,
                                                back2top=False)

            # 如果支持帧率：
            if support_frame_rate:
                # 点击帧率
                self.scroll_and_click_by_text(text_to_find='帧率(fps)')
                # 验证帧率主页文案
                RemoteSetting().scroll_check_funcs2(texts=fps_texts_list)
                # 返回上一级
                self.back_previous_page_by_xpath()
                # 开始点击帧率并遍历选项
                self.iterate_and_click_popup_text(option_text_list=fps_options,
                                                  menu_text='帧率(fps)')

            # 关闭智能省电模式，验证关闭后的文案
            self.scroll_click_right_btn(text_to_find='智能省电模式')  # 关闭
            time.sleep(5)
            # 验证智能省电模式关闭后的文案
            off_texts = ['智能省电模式关闭后，电量低于10%会停用定时录像',
                         '不同电量下摄像机会以不同的设置进行定时录像，以延长使用时间。',
                         ]
            reotitle_text = ['智能省电模式']
            RemoteSetting().scroll_check_funcs2(texts=off_texts)
            RemoteSetting().scroll_check_funcs2(texts=reotitle_text,
                                                selector='ReoTitle',
                                                scroll_or_not=False,
                                                back2top=False)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
