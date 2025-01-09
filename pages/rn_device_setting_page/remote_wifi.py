# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteWiFi(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.edit_wifi_name_text = '//*[@text="Wi-Fi名称"]'
            self.edit_wifi_passw_text = '//*[@text="Wi-Fi密码"]'
            self.base_left_button = '//*[@resource-id="com.mcu.reolink:id/base_left_button"]'

        elif self.platform == 'ios':
            pass

    def check_wifi_main_text(self, wifi_config):
        """
        验证Wi-Fi主页文案
        :param wifi_config: Wi-Fi的 yaml配置
        :return:
        """
        supported_modes = []
        supported_cn_name = []
        # 模式名称映射
        mode_name_mapping = {
            'wifi_band_preference': 'Wi-Fi 频段偏好',
            'wifi_speed_test': 'Wi-Fi测速',
            'add_other_network': '添加其他网络'

        }
        # 模式解释文案
        mode_texts_mapping = {
            'wifi_band_preference': ['连接同一Wi-Fi的哪种频段'],
            'wifi_speed_test': ['检测局域网设备当前的Wi-Fi信号强度'],
            'add_other_network': ['']

        }

        def check_wifi_text(mode_type):
            if mode_type in mode_texts_mapping:
                RemoteSetting().scroll_check_funcs2(texts=mode_texts_mapping[mode_type],
                                                    back2top=False)
            else:
                logger.error(f"未识别的wifi模式 ==> {mode_type}")

        def check_wifi_modes():
            # 检查wifi内容中的每个模式
            for mode in wifi_config:
                if wifi_config[mode]:
                    # 构建支持的模式key列表
                    supported_modes.append(mode)

                    # 转换键名为对应的模式名称，构建名称列表
                    mode_name = mode_name_mapping.get(mode, mode)
                    supported_cn_name.append(mode_name)

        try:
            # 检查设备的wifi所支持的模式
            check_wifi_modes()

            # 根据wifi所支持的模式supported_modes列表，检查ReoTitle模式
            RemoteSetting().scroll_check_funcs2(texts=supported_cn_name, selector='ReoTitle')

            # 根据wifi所支持的模式supported_cn_name列表，检查对应模式的解释文案
            for i in supported_modes:
                check_wifi_text(mode_type=i)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_band_preference(self, options):
        """
        进入并测试wifi频段偏好页面，验证文案和遍历操作选项
        :param options: 操作选项列表
        :return:
        """
        common_texts = ['Wi-Fi 频段偏好', '连接同一Wi-Fi的哪种频段']
        try:
            time.sleep(2)
            # 默认进入【Wi-Fi 频段偏好】
            self.loop_detect_element_and_click(element_value='Wi-Fi 频段偏好')

            # 拼接全局文案
            text1 = common_texts + options
            # 检查wifi频段偏好全局页面文案
            RemoteSetting().scroll_check_funcs2(texts=text1, scroll_or_not=False, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=options, selector='ReoTitle',
                                                scroll_or_not=False, back2top=False)

            # 遍历操作选项
            self.iterate_and_click_popup_text(option_text_list=options, menu_text='Wi-Fi 频段偏好')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_wifi_test(self):
        """
        进入wifi测速页面，验证文本内容存在,点击开始测速
        :return:
        """
        wifi_speed_texts = ['1. 关闭手机移动数据，将手机与设备连接至同一个网络。',
                            '2. 点击“开始测速”测试Wi-Fi信号强度，并将手机和设备尽量靠近路由器。',
                            '3. 查看Wi-Fi信号强度测试结果，正常情况下，需要保证Wi-Fi信号强度在10Mbps以上（总值100Mbps）。'
                            ]
        try:
            time.sleep(2)
            # 点击Wi-Fi测速功能项
            self.loop_detect_element_and_click(element_value='Wi-Fi测速')

            # 检查Wi-Fi测速页面文案
            RemoteSetting().scroll_check_funcs2(texts=wifi_speed_texts)

            # 点击开始测速
            self.loop_detect_element_and_click(element_value='开始测速')

            # 验证测速页面是否打开
            time.sleep(2)
            speed_text = 'How fast are you going?'
            if not self.loop_detect_element_exist(element_value=speed_text, scroll_or_not=False):
                pytest.fail('未进入测速页面,或测速页面错误！')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_add_network(self, wifi_name='test_name', wifi_passw='reolink123'):
        """
        进入添加其他网络页面,输入wifi名称和密码,点击保存和跳过并保存.
        :param wifi_name: wifi名称
        :param wifi_passw: wifi密码
        :return:
        """
        common_before_add_texts = ['取消', '输入密码', '保存', 'Wi-Fi名称', 'Wi-Fi密码']
        try:
            time.sleep(2)
            # 点击进入添加其他网络页面
            self.loop_detect_element_and_click(element_value='添加其他网络')

            # 检查添加其他网络全局页面文案
            RemoteSetting().scroll_check_funcs2(texts=common_before_add_texts)

            # 点击输入Wi-Fi名称
            self.loop_detect_element_and_click(element_value='Wi-Fi名称')
            time.sleep(1)
            self.input_text(xpath_exp=self.edit_wifi_name_text, text=wifi_name)

            # 点击输入Wi-Fi密码
            self.loop_detect_element_and_click(element_value='Wi-Fi密码')
            self.input_text(xpath_exp=self.edit_wifi_passw_text, text=wifi_passw)

            # 点击取消
            self.loop_detect_element_and_click(element_value='取消')

            # 点击跳过并保存
            # self.loop_detect_element_and_click(element_value='跳过并保存')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

