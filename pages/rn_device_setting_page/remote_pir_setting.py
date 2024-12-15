# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config_back = read_yaml.get_data(key="back", source="global_data")  # 读取全局配置


class RemotePirSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def click_switch(self, text_to_find):
        """
        点击switch开关
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find=text_to_find,
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')
        except Exception as e:
            pytest.fail(f'开关点击函数执行失败，失败原因{e}')

    def is_pir_on(self):
        """
        判断PIR开关是否处于开启状态
        :return:
        """
        try:
            if self.is_element_exists(element_value='ReoSwitch:1', selector_type='id', scroll_or_not=False):
                logger.info('PIR开关处于开启状态')
                return True
            else:
                return False
        except Exception as e:
            pytest.fail(f'PIR开关状态判断函数执行失败，失败原因{e}')

    def click_pir_switch(self):
        """
        点击PIR开关
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find='PIR 传感器',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')
        except Exception as e:
            pytest.fail(f'PIR开关点击函数执行失败，失败原因{e}')

    def check_pir_main_text(self, text1, text2):
        """
        验证PIR主页的文案
        :param text1: 页面所有文案
        :param text2: 页面功能项文案
        :return:
        """
        try:
            # 定义一个PIR开关处于关闭状态的文案列表
            pir_off_text = [
                'PIR 传感器',
                '摄像机检测到画面内有物体移动时会触发报警，并通过手机推送、声音报警、邮件通知用户。'
            ]

            def is_pir_tips_exist():
                if self.loop_detect_element_exist(element_value='ReoIcon-InfoLine', selector_type='xpath', scroll_or_not=False):
                    return True
                else:
                    return False

            # TODO: 关闭pir开关的二次弹窗处理

            def toggle_pir_switch(expected_state, validation_texts):
                """
                切换PIR开关并验证状态
                :param expected_state: 预期开关状态 (True: 开启, False: 关闭)
                :param validation_texts: 对应状态的文案列表
                """
                for _ in range(3):
                    if self.is_pir_on() == expected_state:
                        logger.info(f'PIR开关已处于{"开启" if expected_state else "关闭"}状态')
                        RemoteSetting().scroll_check_funcs2(
                            texts=validation_texts, scroll_or_not=False, back2top=False)
                        return True
                    self.click_pir_switch()
                    time.sleep(6)

                pytest.fail(f"PIR开关未正常{'开启' if expected_state else '关闭'}，状态验证失败！")

            def validate_remote_setting_home_tip(expected_visible):
                """
                验证远程设置主页的提示文案显示情况
                :param expected_visible: 提示文案是否应可见 (True: 显示, False: 隐藏)
                """
                if is_pir_tips_exist() != expected_visible:
                    state = '显示' if expected_visible else '隐藏'
                    pytest.fail(f"PIR开关状态与远程设置主页提示文案显示情况不符，应{state}但未{state}！")

            if self.is_pir_on():
                # PIR开关处于开启状态
                RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False,
                                                    back2top=False)

                self.click_by_xpath(xpath_expression=g_config_back)
                validate_remote_setting_home_tip(expected_visible=False)

                self.loop_detect_element_and_click(element_value='PIR 传感器')
                toggle_pir_switch(expected_state=False, validation_texts=pir_off_text)

            else:
                # PIR开关处于关闭状态
                RemoteSetting().scroll_check_funcs2(texts=pir_off_text, scroll_or_not=False, back2top=False)

                self.click_by_xpath(xpath_expression=g_config_back)
                validate_remote_setting_home_tip(expected_visible=True)

                self.loop_detect_element_and_click(element_value='PIR 传感器')
                toggle_pir_switch(expected_state=True, validation_texts=text1)
                RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False,
                                                    back2top=False)

            # if self.is_pir_on():
            #     # 验证pir开关处于开启状态的页面文案
            #     RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
            #     RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False, back2top=False)
            #
            #     # 返回上一页远程设置主页，验证主页的开关状态文案提示
            #     self.click_by_xpath(xpath_expression=g_config_back)
            #
            #     if is_pir_tips_exist():
            #         pytest.fail('PIR开关处于开启状态，但远程设置主页PIR已关闭的提示文案却仍然显示！')
            #
            #     else:
            #         logger.info('PIR开关处于开启状态，远程设置主页PIR已关闭的提示文案已隐藏！')
            #         # 再次点击PIR传感器进入PIR传感器主页
            #         self.loop_detect_element_and_click(element_value='PIR 传感器')
            #         # 点击PIR开关，关闭pir
            #         self.click_pir_switch()
            #         time.sleep(6)
            #         for i in range(3):
            #             if not self.is_pir_on():
            #                 logger.info('PIR开关关闭成功！')
            #                 # 验证关闭后的文案
            #                 RemoteSetting().scroll_check_funcs2(texts=pir_off_text, scroll_or_not=False, back2top=False)
            #                 break
            #             elif self.is_pir_on():
            #                 self.click_pir_switch()
            #                 time.sleep(6)
            #                 continue
            #             else:
            #                 time.sleep(6)
            #                 continue
            # else:
            #     # 验证pir开关处于关闭状态的页面文案
            #     RemoteSetting().scroll_check_funcs2(texts=pir_off_text, scroll_or_not=False, back2top=False)
            #
            #     # 返回上一页远程设置主页，验证主页的开关状态文案提示
            #     self.click_by_xpath(xpath_expression=g_config_back)
            #
            #     if is_pir_tips_exist():
            #         logger.info('PIR开关处于关闭状态，远程设置主页PIR已关闭的提示文案已显示！')
            #         # 再次点击PIR传感器进入PIR传感器主页
            #         self.loop_detect_element_and_click(element_value='PIR 传感器')
            #         # 点击PIR开关，开启pir
            #         self.click_pir_switch()
            #         time.sleep(6)
            #         # 验证开关是否开启，若成功开启，则验证开启后的文案
            #         for i in range(3):
            #             if self.is_pir_on():
            #                 logger.info('PIR开关开启成功！')
            #                 # 验证开启后的文案
            #                 RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
            #                 RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False, back2top=False)
            #                 break
            #             elif not self.is_pir_on():
            #                 self.click_pir_switch()
            #                 time.sleep(6)
            #                 continue
            #             else:
            #                 time.sleep(6)
            #                 continue
            #
            #     else:
            #         pytest.fail('PIR开关处于关闭状态，远程设置主页PIR已关闭的提示文案未显示！')

        except Exception as e:
            pytest.fail(f'PIR主页文案函数执行失败，失败原因{e}')

    def click_reduce_misstatement(self, expected_state):
        """
        点击减少误报switch按钮
        :param expected_state: 预期开关状态 (True: 开启, False: 关闭)
        :return:
        """
        for _ in range(3):
            if self.is_pir_on() == expected_state:
                logger.info(f'减少误报的开关已处于{"开启" if expected_state else "关闭"}状态')
                return True
            self.click_switch(text_to_find='减少误报')
            time.sleep(6)

        pytest.fail(f"PIR开关未正常{'开启' if expected_state else '关闭'}，状态验证失败！")

    def verify_pir_sensitivity(self, text1, text2):
        """
        验证PIR灵敏度功能
        :param text1: 页面所有文案
        :param text2: 页面功能项文案
        :return:
        """
        try:
            # 点击探测精度进入探测精度页面
            self.click_by_text(text='探测精度')
            # 灵敏度页面加载成功后，验证页面文案
            if self.loop_detect_element_exist(element_value='减少误报', scroll_or_not=False):
                RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', scroll_or_not=False,
                                                    back2top=False)
            else:
                pytest.fail('PIR灵敏度页面加载失败！')

            # 点击减少误报switch按钮，验证开关状态
            self.click_reduce_misstatement(expected_state=True)
            self.click_reduce_misstatement(expected_state=False)
            self.click_reduce_misstatement(expected_state=True)

            # 拖动灵敏度的滑动条
            self.common_drag_slider_seek_bar(start_xpath_prefix='//*[@resource-id="RNE__Slider_Container"]',)

        except Exception as e:
            pytest.fail(f'PIR灵敏度功能函数执行失败，失败原因{e}')

    def verify_pir_alarm_time_limit(self, text1, text2):
        """
        验证PIR报警时间限制功能
        :param text1: 页面所有文案
        :param text2: 页面功能项文案
        :return:
        """
        try:
            # 点击报警时限进入报警时限页面
            self.click_by_text(text='报警时限')

            # 报警时限页面加载成功后，验证页面文案
            if self.loop_detect_element_exist(element_value='不限制'):
                RemoteSetting().scroll_check_funcs2(texts=text1, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', back2top=False)

                # 返回上一页
                self.click_by_xpath(xpath_expression=g_config_back)

                # 开始遍历验证报警时限选项
                self.iterate_and_click_popup_text(option_text_list=text2, menu_text='报警时限')

            else:
                pytest.fail('报警时限页面加载失败！')

        except Exception as e:
            pytest.fail(f'PIR报警时限功能函数执行失败，失败原因{e}')

    def verify_pir_trigger_interval(self, text1, text2):
        """
        验证PIR触发间隔功能
        :param text1: 页面所有文案
        :param text2: 页面功能项文案
        :return:
        """
        try:
            # 点击触发间隔进入触发间隔页面
            self.click_by_text(text='触发间隔')

            # 触发间隔页面加载成功后，验证页面文案
            if self.loop_detect_element_exist(element_value='不限制'):
                RemoteSetting().scroll_check_funcs2(texts=text1, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle', back2top=False)

                # 返回上一页
                self.click_by_xpath(xpath_expression=g_config_back)

                # 开始遍历验证报警时限选项
                self.iterate_and_click_popup_text(option_text_list=text2, menu_text='触发间隔')

            else:
                pytest.fail('报警时限页面加载失败！')

        except Exception as e:
            pytest.fail(f'PIR报警时限功能函数执行失败，失败原因{e}')

    def verify_pir_plan(self, text1, text2):
        """
        验证PIR计划功能
        :param text1: 页面所有文案
        :param text2: 页面功能项文案
        :return:
        """
        # TODO: PIR计划功能待实现，交互上没看见，不确定是否保留计划功能
        pass

