# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
status_light_texts = g_config.get("status_light_texts")  # 状态灯>配置页状态灯的全局文案
status_light_reotitle = g_config.get("status_light_reotitle")  # 状态灯>配置页状态灯的reotitle
infrared_light_texts = g_config.get("infrared_light_texts")  # 红外灯>配置页红外灯的全局文案
infrared_light_reotitle = g_config.get("infrared_light_reotitle")  # 红外灯>配置页红外灯的reotitle
doorbell_button_light_texts = g_config.get("doorbell_button_light_texts")  # 门铃按钮灯>配置页门铃按钮灯的全局文案
doorbell_button_light_reotitle = g_config.get("doorbell_button_light_reotitle")  # 门铃按钮灯>配置页门铃按钮灯的reotitle
header_little_tips = g_config.get("header_little_tips")  # 白光灯>顶部导航栏解释文案
close_tips = g_config.get("close_tips")  # 白光灯关闭模式>解释文案
auto_tips = g_config.get("auto_tips")  # 白光灯自动模式>解释文案
night_tips = g_config.get("night_tips")  # 白光灯夜视常亮模式>解释文案
time_tips = g_config.get("time_tips")  # 白光灯定时模式>解释文案
smart_tips = g_config.get("smart_tips")  # 白光灯智能模式>解释文案
smart_night_tips = g_config.get("smart_night_tips")  # 白光灯夜间智能模式>解释文案
preview_auto_tips = g_config.get("preview_auto_tips")  # 白光灯预览自动开启模式>解释文案
common_detect_texts = g_config.get("common_detect_texts")  # 白光灯>侦测通用文案


class RemoteLight(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 定时模式：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 定时模式：分钟
            self.base_left_button = '//*[@resource-id="PageHeaderLeft"]'  # 左上角返回上一页按钮
            self.detect_selector = ''  # 侦测类型的定位参数

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
        light_texts_mapping = {
            '状态灯': ['位于镜头附近的一个表示摄像机连接状态的灯。'],
            '指示灯': ['位于镜头附近的一个表示摄像机连接状态的灯。'],
            '红外灯': ['红外补光灯，能让你在夜晚或光线较暗时拍出更清晰的影像。'],
            '白光灯': ['夜晚时开启照明灯画面呈现彩色模式，拍摄效果更佳。'],
            '按钮灯': ['按钮周围一圈表示门铃状态的灯']
        }

        def check_light_text(light_type):
            if light_type in light_texts_mapping:
                RemoteSetting().scroll_check_funcs2(texts=light_texts_mapping[light_type],
                                                    scroll_or_not=False,
                                                    back2top=False)
            else:
                logger.error(f"未识别的灯类型 ==> {light_type}")

        try:
            if lights_num:
                if not self.loop_detect_element_exist(element_value='//*[@text="灯"]',
                                                      selector_type='xpath',
                                                      loop_times=2,
                                                      scroll_or_not=False):
                    pytest.fail(f"灯页面缺失headerTitle ==> ‘灯’")

                RemoteSetting().scroll_check_funcs2(texts=texts, selector='ReoTitle')

                for text in texts:
                    check_light_text(text)

            else:
                if len(texts) == 1:
                    light_type = texts[0]
                    if light_type == '白光灯':
                        logger.info(f"该设备仅存在一个白光灯，相关内容验证由test_floodlight_light函数完成！")
                    else:
                        check_light_text(light_type)
                else:
                    logger.error(f"灯类型列表不符合预期，应为单个灯类型 ==> {texts}")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_floodlight_main_text(self, lights_num, floodlight_config):
        """
        验证白光灯主页文案
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param floodlight_config: yaml配置文件中的白光灯模式配置
        :return:
        """
        supported_modes = []
        supported_cn_name = []
        # 模式名称映射
        mode_name_mapping = {
            'night_vision_steady_light': '夜视常亮模式',
            'preview_opens_auto': '预览自动开启',
            'brightness': '亮度',
            'light_off_mode': '关闭',
            'timer_mode': '定时模式',
            'auto_mode': '自动模式',
            'smart_mode': '智能模式',
            'night_smart_mode': '夜间智能模式'
        }
        # 模式解释文案
        mode_texts_mapping = {
            'light_off_mode': close_tips,
            'auto_mode': auto_tips,
            'night_vision_steady_light': night_tips,
            'timer_mode': time_tips,
            'smart_mode': smart_tips,
            'night_smart_mode': smart_night_tips,
            'preview_opens_auto': preview_auto_tips,
            'brightness': '亮度'

        }

        def check_light_text(mode_type):
            if mode_type in mode_texts_mapping:
                RemoteSetting().scroll_check_funcs2(texts=mode_texts_mapping[mode_type],
                                                    back2top=False)
            else:
                logger.error(f"未识别的白光灯模式 ==> {mode_type}")

        def check_floodlight_modes():
            # 检查floodlight内容中的每个模式
            for mode in floodlight_config:
                if floodlight_config[mode]:
                    # 构建支持的模式列表
                    supported_modes.append(mode)

                    # 转换键名为对应的模式名称，构建名称列表
                    mode_name = mode_name_mapping.get(mode, mode)
                    supported_cn_name.append(mode_name)

        def validate_floodlight_texts():
            """验证白光灯主页ReoTitle选项"""
            RemoteSetting().scroll_check_funcs2(texts=supported_cn_name, selector='ReoTitle')

        try:
            if lights_num:
                # 先点击进入白光灯主页
                self.scroll_and_click_by_text(text_to_find='白光灯')
                # 检查设备的白光灯所支持的模式
                check_floodlight_modes()
                # 根据白光灯所支持的模式supported_modes列表，检查对应模式的解释文案
                for i in supported_modes:
                    check_light_text(mode_type=i)
                # 验证白光灯主页的ReoTitle选项
                validate_floodlight_texts()
            else:
                # 根据白光灯所支持的模式supported_modes列表，检查对应模式的解释文案
                for i in supported_modes:
                    check_light_text(mode_type=i)
                validate_floodlight_texts()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_button_light_main_text(self, lights_num):
        """
        验证按钮灯主页文案
        :param lights_num: 布尔值，灯的数量大于1: True,  等于1：False
        """
        try:
            def validate_button_light_texts():
                """验证按钮灯主页文案"""
                RemoteSetting().scroll_check_funcs2(texts=doorbell_button_light_texts)
                RemoteSetting().scroll_check_funcs2(texts=doorbell_button_light_reotitle,
                                                    selector='ReoTitle',
                                                    scroll_or_not=False,
                                                    back2top=False)

            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                validate_button_light_texts()
            else:
                validate_button_light_texts()

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
            pytest.fail(f"判断灯的数量函数执行出错: {str(e)}")

    def verify_and_test_infrared_light(self, lights_num, options_text):
        """
        点击进入红外灯的配置页并测试红外灯的选项配置
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param options_text: 红外灯 配置页操作项, 仅亮度
        :return:
        """
        def drag_brightness_slider(slider_mode='id'):  # 拖动亮度条
            element_obj = 'RNE__Slider_Thumb'
            time.sleep(2)
            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=8)

        # 定义一个函数来处理每个选项
        def handle_option(options, is_back):
            # 操作红外灯配置
            self.scroll_and_click_by_text(text_to_find=options)
            if is_back:
                # 返回上一页
                self.back_previous_page_by_xpath()
                # 断言回显
                if not self.scroll_and_click_by_text(text_to_find=options):
                    pytest.fail(f"红外灯选择【{options}】后，未检查到回显！")

        def verify_texts():
            # 验证红外灯主页文案
            RemoteSetting().scroll_check_funcs2(texts=infrared_light_texts,
                                                scroll_or_not=False,
                                                back2top=False)
            # 验证ReoTitle选项
            RemoteSetting().scroll_check_funcs2(texts=new_options, selector='ReoTitle',
                                                scroll_or_not=True, back2top=False)

            # 如果亮度条存在，则拖动亮度条
            if '亮度' in options_text:
                drag_brightness_slider()

        try:
            # 拼接ReoTitle选项
            new_options = infrared_light_texts + options_text
            # 如果是多个灯，则点击红外灯
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='红外灯')

                # 验证红外灯主页文案、ReoTitle选项
                verify_texts()

                # 遍历操作选项
                for option in infrared_light_texts:
                    handle_option(option, True)

            else:
                # 验证红外灯主页文案、ReoTitle选项
                verify_texts()

                # 遍历操作选项
                for option in infrared_light_texts:
                    handle_option(option, False)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_floodlight_night_smart_mode(self, lights_num, supported_detect_type, options_text):
        """
        点击并测试白光灯的夜间智能模式，（没有验证侦测页的文案）
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param supported_detect_type: 是否支持 侦测
        :param options_text: 配置页操作项
        :return:
        """

        # TODO: 验证侦测类型选项文案需要写id
        def handle_detect_type():
            """处理侦测类型页面的遍历和保存操作"""
            detect_options = options_text['detect_type']['option_text']  # 侦测类型选项文案
            detect_text = detect_options + common_detect_texts  # 侦测类型全局文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='侦测')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text)  # 验证侦测类型全局文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=self.detect_selector)  # 验证侦测类型选项文案
            self.scroll_and_click_by_text('保存')

        try:
            # 如果是多个灯，则先点击白光灯
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')

                self.scroll_and_click_by_text(text_to_find='夜间智能模式')  # 点击夜间智能模式

                if supported_detect_type:  # 如果支持侦测类型，处理侦测类型
                    handle_detect_type()

                self.back_previous_page_by_xpath()  # 返回灯主页并验证模式回显
                if not RemoteSetting().scroll_check_funcs2(texts='夜间智能模式'):
                    pytest.fail("白光灯选择【夜间智能模式】后，未检查到回显！")

            else:
                # 单灯情况：直接点击夜间智能模式
                self.scroll_and_click_by_text(text_to_find='夜间智能模式')
                if supported_detect_type:
                    handle_detect_type()

        except Exception as e:
            pytest.fail(f"verify_floodlight_night_smart_mode 执行出错: {e}")

    def verify_floodlight_smart_mode(self, lights_num, supported_detect_type, options_text):
        """
        点击并测试白光灯的智能模式（没有验证侦测页的文案）
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :param supported_detect_type: 是否支持 侦测
        :param options_text: 侦测类型配置页操作项
        :return:
        """

        def handle_detect_type():
            """处理侦测类型页面的遍历和保存操作"""
            detect_options = options_text['detect_type']['option_text']  # 侦测类型选项文案
            detect_text = detect_options + common_detect_texts  # 侦测类型全局文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='侦测')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text)  # 验证侦测类型全局文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=self.detect_selector)  # 验证侦测类型选项文案
            self.scroll_and_click_by_text('保存')

        def set_timer():
            """设置开始和结束时间"""
            # 点击开始时间
            self.scroll_and_click_by_text(text_to_find='开始时间')
            self.time_selector(iteration=1)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')

            # 点击结束时间
            self.scroll_and_click_by_text(text_to_find='结束时间')
            self.time_selector(iteration=2)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')

        try:
            # 如果是多个灯，则点击白光灯》智能模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_and_click_by_text(text_to_find='智能模式')

                # 如果支持侦测类型，则点击侦测类型：
                if supported_detect_type:
                    handle_detect_type()

                # 分别选择智能模式的开始时间、结束时间
                set_timer()

                # 返回灯主页，验证白光灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='智能模式'):
                    pytest.fail(f"白光灯选择【智能模式】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='智能模式')

                # 如果支持侦测类型，则点击侦测类型：
                if supported_detect_type:
                    handle_detect_type()

                # 分别选择智能模式的开始时间、结束时间
                set_timer()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_floodlight_timer_mode(self, lights_num):
        """
        点击并测试白光灯的定时模式
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :return:
        """

        def set_timer():
            """设置开始和结束时间"""
            # 点击开始时间
            self.scroll_and_click_by_text(text_to_find='开始时间')
            self.time_selector(iteration=1)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')

            # 点击结束时间
            self.scroll_and_click_by_text(text_to_find='结束时间')
            self.time_selector(iteration=2)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')

        try:
            # 如果是多个灯，点击白光灯后进入定时模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_and_click_by_text(text_to_find='定时模式')
                set_timer()

                # 返回灯聚合页，验证定时模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='定时模式'):
                    pytest.fail("白光灯选择【定时模式】后，未检查到回显！")
            else:
                # 单个灯直接进入定时模式并设置定时
                self.scroll_and_click_by_text(text_to_find='定时模式')
                set_timer()

        except Exception as e:
            pytest.fail(f"verify_floodlight_timer_mode 执行出错: {e}")

    def verify_floodlight_night_vision_steady_light_mode(self, lights_num):
        """
        点击测试白光灯/泛光灯的夜视常亮模式
        :return:
        """
        try:
            # 如果是多个灯，则点击白光灯》夜视常亮 模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_and_click_by_text(text_to_find='夜视常亮')

                # 返回灯聚合页，验证夜视常亮 模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='夜视常亮'):
                    pytest.fail("白光灯选择【夜视常亮】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='夜视常亮')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_preview_opens_auto(self, lights_num):
        """
        点击测试 白光灯>预览自动开启 的switch切换按钮
        :return:
        """
        try:
            # 如果是多个灯，则点击白光灯》预览自动开启
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_click_right_btn(text_to_find='预览自动开启',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup'
                                            )

                # 返回灯聚合页，验证预览自动开启回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='预览自动开启'):
                    pytest.fail(f"白光灯选择【预览自动开启】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_click_right_btn(text_to_find='预览自动开启',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup'
                                            )

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_light_off_mode(self, lights_num):
        """
        点击测试白光灯的关闭模式
        :return:
        """
        try:
            # 如果是多个灯，则点击白光灯》关闭模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_and_click_by_text(text_to_find='关闭')

                # 返回灯聚合页，验证白光灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                    pytest.fail(f"白光灯选择【关闭模式】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='关闭')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_light_auto_mode(self, lights_num):
        """
        点击测试白光灯>自动模式
        :param lights_num:
        :return:
        """
        try:
            # 如果是多个灯，则点击白光灯》自动模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')
                self.scroll_and_click_by_text(text_to_find='自动模式')

                # 返回灯聚合页，验证白光灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动模式'):
                    pytest.fail(f"白光灯选择【关闭模式】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='自动模式')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_status_lights_off(self, lights_num):
        """
        点击测试状态灯》关闭模式
        :param lights_num:
        :param status_lights_texts:
        :param options: ReoTitle操作选项
        :return:
        """
        try:
            def verify_texts(texts):
                RemoteSetting().scroll_check_funcs2(texts=texts, scroll_or_not=False, back2top=False)

            # 根据灯的数量选择不同的点击路径
            if lights_num:
                self.loop_detect_element_and_click(element_value='状态灯')
                self.loop_detect_element_and_click(element_value='关闭')
            else:
                self.loop_detect_element_and_click(element_value='关闭')

            # 验证状态灯主页全局文案
            verify_texts(status_light_texts)
            # 验证状态灯主页选项文案
            verify_texts(status_light_reotitle)

            # 返回灯聚合页，验证状态灯模式回显
            self.back_previous_page_by_xpath()
            if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                pytest.fail("状态灯选择【关闭】后，未检查到回显！")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_status_lights_on(self, lights_num):
        """
        点击测试状态灯》开启模式
        :param lights_num:
        :param status_lights_texts:
        :param options: ReoTitle操作选项
        :return:
        """
        try:
            def verify_texts(texts):
                RemoteSetting().scroll_check_funcs2(texts=texts, scroll_or_not=False, back2top=False)

            # 根据灯的数量选择不同的点击路径
            if lights_num > 1:
                self.loop_detect_element_and_click(element_value='状态灯')
                self.loop_detect_element_and_click(element_value='开启')
            else:
                self.loop_detect_element_and_click(element_value='开启')

            # 验证状态灯主页文案
            verify_texts(status_light_texts)
            verify_texts(status_light_reotitle)

            # 返回灯聚合页，验证状态灯模式回显
            self.back_previous_page_by_xpath()
            if not RemoteSetting().scroll_check_funcs2(texts='开启'):
                pytest.fail("状态灯选择【开启】后，未检查到回显！")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_doorbell_button_light_off(self, lights_num):
        """
        点击测试门铃按钮灯》关闭模式
        :param lights_num: 灯的数量大于1:True,  等于1：False
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》开启模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='关闭')

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='关闭'):
                    pytest.fail(f"状态灯选择【关闭】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='关闭')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_doorbell_button_light_auto(self, lights_num):
        """
        点击测试门铃按钮灯》自动模式
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》自动模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='自动')

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动'):
                    pytest.fail(f"状态灯选择【自动】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='自动')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_doorbell_button_light_auto_on_night(self, lights_num):
        """
        点击测试门铃按钮灯》自动且夜间常亮 模式
        :param lights_num: 布尔值，灯的数量大于1:True,  等于1：False
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》自动且夜间常亮模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='自动且夜间常亮')

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='自动且夜间常亮'):
                    pytest.fail(f"状态灯选择【自动且夜间常亮】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='自动且夜间常亮')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_doorbell_button_light_always_on(self, lights_num):
        """
        点击测试门铃按钮灯》常亮 模式
        :param lights_num:
        :return:
        """
        try:
            # 如果是多个灯，则点击按钮灯》常亮模式
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='按钮灯')
                self.scroll_and_click_by_text(text_to_find='常亮')

                # 返回灯聚合页，验证按钮灯模式回显
                self.back_previous_page_by_xpath()
                if not RemoteSetting().scroll_check_funcs2(texts='常亮'):
                    pytest.fail(f"状态灯选择【常亮】后，未检查到回显！")

            else:
                self.scroll_and_click_by_text(text_to_find='常亮')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def floodlight_drag_brightness_slider(self, lights_num, slider_mode='id'):  # 拖动亮度条
        try:
            element_obj = 'RNE__Slider_Thumb'
            # 多个灯
            if lights_num:
                self.scroll_and_click_by_text(text_to_find='白光灯')

                time.sleep(2)

                # 往右拖动15次
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=element_obj,
                                     direction='right',
                                     iteration=5)

                # 往左拖动25次
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=element_obj,
                                     direction='left',
                                     iteration=10)

                # 往右拖动5次
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=element_obj,
                                     direction='right',
                                     iteration=8)

            else:
                logger.info(f'单个灯，正在拖动亮度条')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
