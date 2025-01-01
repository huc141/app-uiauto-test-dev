# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config_back = read_yaml.get_data(key="back", source="global_data")  # 读取全局配置
g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
_ReoIcon_Draw = g_config.get('ReoIcon_Draw')  # 计划主页底部涂画按钮
_ReoIcon_Erase = g_config.get('ReoIcon_Erase')  # 计划主页底部擦除按钮
draw_text = g_config.get('draw_text')  # 选择涂抹按钮后显示的文案
erase_text = g_config.get('erase_text')  # 选择擦除按钮后显示的文案
erase_all_btn = g_config.get('erase_all_btn')  # 计划表【全部清除】按钮二次确认弹窗内容


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

    def check_pir_main_text(self, pir_config):
        """
        验证PIR主页的文案
        :param pir_config: PIR的 yaml配置
        :return:
        """
        supported_modes = []
        supported_cn_name = []
        # 模式名称映射
        mode_name_mapping = {
            'pir': 'PIR传感器',
            'plan': '计划',
            'sensitivity': '探测精度',
            'alarm_time_limit': '报警时限',
            'trigger_interval': '触发间隔'
        }
        # 模式解释文案
        mode_texts_mapping = {
            'alarm_time_limit': ['触发报警后，设备将在达到设置时限后停止报警。'],
            'trigger_interval': ['结束报警后，PIR传感器在设定的时间内不会再被触发。']
        }

        def check_pir_text(mode_type):
            """检查pir每个模式的解释文案"""
            if mode_type in mode_texts_mapping:
                RemoteSetting().scroll_check_funcs2(texts=mode_texts_mapping[mode_type],
                                                    back2top=False)
            else:
                logger.error(f"未识别的pir模式 ==> {mode_type}")

        def check_pir_modes():
            # 统计pir内容中的每个模式
            for mode in pir_config:
                if pir_config[mode]:
                    # 构建支持的模式列表
                    supported_modes.append(mode)

                    # 转换键名为对应的模式名称，构建名称列表
                    mode_name = mode_name_mapping.get(mode, mode)
                    supported_cn_name.append(mode_name)

        def is_pir_tips_exist():
            """pir关闭后，远程配置首页是否显示tip提示"""
            if self.loop_detect_element_exist(element_value='//*[@text="PIR已关闭，设备将无法检测报警事件。"]',
                                              selector_type='xpath'):
                return True
            else:
                return False

        def is_there_speaker():
            """判断设备是否有扬声器"""
            yes_speaker = ['摄像机检测到画面内有物体移动时会触发报警，并通过手机推送、声音报警、邮件通知用户。']
            no_speaker = ['摄像机检测到画面内有物体移动时会触发报警，并通过手机推送、邮件通知用户。']

            if pir_config['is_there_speaker']:
                RemoteSetting().scroll_check_funcs2(texts=yes_speaker, back2top=False)
            else:
                RemoteSetting().scroll_check_funcs2(texts=no_speaker, back2top=False)

        def toggle_pir_switch(expected_state):
            """
            切换PIR开关并验证状态
            :param expected_state: 预期开关状态 (True: 开启, False: 关闭)
            """
            for _ in range(3):
                if self.is_pir_on() == expected_state:
                    logger.info(f'PIR开关已处于{"开启" if expected_state else "关闭"}状态')
                    is_there_speaker()
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
        try:
            # TODO: 关闭pir开关的二次弹窗处理
            if self.is_pir_on():  # PIR开关处于开启状态
                # 检查pir支持的模式
                check_pir_modes()

                # 根据构建的supported_cn_name列表，检查ReoTitle选项
                RemoteSetting().scroll_check_funcs2(texts=supported_cn_name,
                                                    selector='ReoTitle')

                # 根据所支持的模式supported_modes列表，检查对应模式的解释文案
                for i in supported_modes:
                    check_pir_text(mode_type=i)

                self.click_by_xpath(xpath_expression=g_config_back)
                validate_remote_setting_home_tip(expected_visible=False)

                self.loop_detect_element_and_click(element_value='PIR 传感器')
                toggle_pir_switch(expected_state=False)

            else:  # PIR开关处于关闭状态
                self.click_by_xpath(xpath_expression=g_config_back)
                validate_remote_setting_home_tip(expected_visible=True)

                self.loop_detect_element_and_click(element_value='PIR 传感器')
                toggle_pir_switch(expected_state=True)
                is_there_speaker()

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

    def verify_pir_sensitivity(self):
        """
        验证PIR灵敏度功能
        :return:
        """
        text1 = ['探测精度', '减少误报',
                 '如果监控范围内不时有物体晃动（如树叶摆动），请打开此功能以减少误报',
                 '灵敏度',
                 '灵敏度高，检测到细微的物体移动就报警，不放过任何风吹草动，如细小的蚊虫、较远的人等。',
                 '0',
                 '100'
                 ]
        text2 = ['减少误报', '灵敏度']
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
            self.common_drag_slider_seek_bar(start_xpath_prefix='//*[@resource-id="RNE__Slider_Container"]', )

        except Exception as e:
            pytest.fail(f'PIR灵敏度功能函数执行失败，失败原因{e}')

    def verify_pir_alarm_time_limit(self, options):
        """
        验证PIR报警时间限制功能
        :param options: 页面功能项文案
        :return:
        """
        # 拼接全局文案列表
        texts = ['报警时限'] + options
        try:
            # 点击报警时限进入报警时限页面
            self.click_by_text(text='报警时限')

            # 报警时限页面加载成功后，验证页面文案
            if self.loop_detect_element_exist(element_value='不限制'):
                RemoteSetting().scroll_check_funcs2(texts=texts, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=options,
                                                    selector='ReoTitle',
                                                    back2top=False)

                # 返回上一页
                self.click_by_xpath(xpath_expression=g_config_back)

                # 开始遍历验证报警时限选项
                self.iterate_and_click_popup_text(option_text_list=options,
                                                  menu_text='报警时限')

            else:
                pytest.fail('报警时限页面加载失败！')

        except Exception as e:
            pytest.fail(f'PIR报警时限功能函数执行失败，失败原因{e}')

    def verify_pir_trigger_interval(self, options):
        """
        验证PIR触发间隔功能
        :param options: 页面功能项文案
        :return:
        """
        # 拼接全局文案列表
        texts = ['触发间隔'] + options
        try:
            # 点击触发间隔进入触发间隔页面
            self.click_by_text(text='触发间隔')

            # 触发间隔页面加载成功后，验证页面文案
            if self.loop_detect_element_exist(element_value='不限制'):
                RemoteSetting().scroll_check_funcs2(texts=texts, back2top=False)
                RemoteSetting().scroll_check_funcs2(texts=options, selector='ReoTitle', back2top=False)

                # 返回上一页
                self.click_by_xpath(xpath_expression=g_config_back)

                # 开始遍历验证报警时限选项
                self.iterate_and_click_popup_text(option_text_list=options, menu_text='触发间隔')

            else:
                pytest.fail('报警时限页面加载失败！')

        except Exception as e:
            pytest.fail(f'PIR报警时限功能函数执行失败，失败原因{e}')

    def verify_pir_plan(self):
        """
        测试 计划
        :return:
        """
        try:
            # 验证计划主页通用内容
            common_plan_texts = ['取消', '计划', '保存', '00', '02', '04', '06', '08', '10', '12', '14', '16', '18',
                                 '20', '22', '24', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
            RemoteSetting().scroll_check_funcs2(texts=common_plan_texts, scroll_or_not=False, back2top=False)

            # 验证底部涂抹按钮文案：擦除
            self.click_by_xpath(xpath_expression=_ReoIcon_Erase)
            RemoteSetting().scroll_check_funcs2(texts=erase_text, scroll_or_not=False, back2top=False)
            self.click_by_text('全部清除')  # 点击右下角全部清除按钮
            RemoteSetting().scroll_check_funcs2(texts=erase_all_btn, scroll_or_not=False, back2top=False)  # 验证二次弹窗内容
            self.click_by_text('全部清除')  # 点击二次弹窗中的全部清除按钮
            # 验证底部涂抹按钮文案：涂画
            self.click_by_xpath(xpath_expression=_ReoIcon_Draw)
            RemoteSetting().scroll_check_funcs2(texts=draw_text, scroll_or_not=False, back2top=False)
            self.click_by_text('全选')  # 点击右下角全选按钮

        except Exception as e:
            pytest.fail(f'PIR计划功能函数执行失败，失败原因{e}')











