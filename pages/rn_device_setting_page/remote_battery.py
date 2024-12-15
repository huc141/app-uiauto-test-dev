# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config_back = read_yaml.get_data(key="back", source="global_data")  # 读取全局配置


class RemoteBattery(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.battery_data_off_button = '//*[@resource-id="com.mcu.reolink:id/im_close"]'  # 电池数据关闭按钮

        elif self.platform == 'ios':
            self.battery_data_off_button = ''

    def check_battery_page(self, text, options):
        """
        验证电池主页文案和开关操作
        :param text: 未开启电池统计数据前的页面文案列表
        :param options: 开启电池统计数据后的页面文案列表
        :return:
        """
        try:
            # 定义一个电池WiFi设备的电量使用统计弹窗内容列表
            battery_off_button = ['电量使用统计', '关闭统计，将停止对设备进行记录和统计，并删除相关数据。', '取消', '确定']

            # wifi设备
            def verify_wifi_battery_page():
                logger.info('开始执行wifi设备-电池模块的验证')

                def check_and_click_agree():
                    self.click_by_text(text='同意并继续')
                    time.sleep(2)
                    RemoteSetting().scroll_check_funcs2(texts=options, scroll_or_not=False, back2top=False)

                def check_and_click_close_statistics():
                    self.click_by_xpath(xpath_expression=self.battery_data_off_button)
                    time.sleep(1)
                    self.click_by_text(text='关闭统计')

                def confirm_close_statistics():
                    check_and_click_close_statistics()
                    RemoteSetting().scroll_check_funcs2(texts=battery_off_button, scroll_or_not=False, back2top=False)
                    self.click_by_text(text='取消')
                    check_and_click_close_statistics()
                    self.click_by_text(text='确定')
                    time.sleep(2)
                    RemoteSetting().scroll_check_funcs2(texts=text, scroll_or_not=False, back2top=False)

                if self.loop_detect_element_exist(element_value='同意并继续', loop_times=2, scroll_or_not=False):
                    RemoteSetting().scroll_check_funcs2(texts=text, scroll_or_not=False, back2top=False)
                    check_and_click_agree()
                elif self.loop_detect_element_exist(element_value='最近4周运行时长', loop_times=2, scroll_or_not=False):
                    RemoteSetting().scroll_check_funcs2(texts=options, scroll_or_not=False, back2top=False)
                    confirm_close_statistics()
                else:
                    logger.info('未检测到“同意并继续”和“最近4周运行时长”文案，可能是4G设备，执行4G设备的验证')

            # 4G设备
            def verify_4g_battery_page():
                logger.info('开始执行4G设备-电池模块的验证')
                RemoteSetting().scroll_check_funcs2(texts=text,
                                                    scroll_or_not=False,
                                                    back2top=False)

            # 先检测是电池WiFi设备/电池4G设备
            if self.loop_detect_element_exist(element_value='最近30天的每日剩余电量', loop_times=2, scroll_or_not=False):
                logger.info('检测到“最近30天的每日剩余电量”文案，可能是4G设备，执行4G设备的验证')
                verify_4g_battery_page()
            else:
                logger.info('未检测到“最近30天的每日剩余电量”文案，可能是WiFi设备，执行WiFi设备的验证')
                verify_wifi_battery_page()

        except Exception as e:
            pytest.fail(f'验证失败，错误信息：{e}')



