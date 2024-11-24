# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.app_driver import driver
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemotePrivacyMode(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def turn_on_privacy_mode(self, text):
        """
        打开隐私模式开关。
        ①如果为关，则点击打开；
        ②如果为开，则验证预览界面是否显示隐私模式。
        :param text: 需要找的文本内容
        :return:
        """
        try:
            def back_to_devices_list():
                # 返回设备列表
                # self.back_previous_page()
                while True:
                    status = self.loop_detect_element_exist(element_value='摄像机', loop_times=1)
                    if status:
                        break
                    self.back_previous_page_by_xpath(xpath_expression='//*[@resource-id="com.mcu.reolink:id/base_left_button"]')

            # 返回设备列表
            back_to_devices_list()

            # 找到设备名称，
            x, y = self.get_text_coordinates_center(text=text)
            # 计算预览窗口的新坐标
            new_x = x
            new_y = y + 100  # 向下移动100个像素点

            # 在新坐标处进行点击操作,进入预览页面
            self.click_by_coordinates(x=new_x, y=new_y)

            # 验证开关状态
            # 如果存在隐私模式文案，判断为开：
            if self.loop_detect_element_exist(element_value='隐私模式', loop_times=1):
                logger.info("预览页面存在【隐私模式】文案，判断为开")
                return True
            else:
                return False
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_privacy_mode(self, device_name):
        """
        :param device_name: 设备名称
        :return:
        """
        try:
            # 如果已经开启了隐私模式，则在预览页点击解除：
            if self.turn_on_privacy_mode(text=device_name):
                self.loop_detect_element_and_click(element_value='解除')
                time.sleep(3)
                self.scroll_click_right_btn(text_to_find='隐私模式')
                time.sleep(10)
                return True

            else:
                # 返回设备列表，
                # self.back_previous_page()
                self.back_previous_page_by_xpath(
                    xpath_expression='//*[@resource-id="com.mcu.reolink:id/fold_button"]')

                return False

            # main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)
            # illegal_funcs_res = self.detect_illegal_functions(legal_funcs_ids=main_text)
            #
            # return main_text_res, illegal_funcs_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_privacy_mode(self, device_name):
        """
        :return:
        """
        try:
            # 检查隐私模式是否启用
            privacy_mode_enabled = self.check_privacy_mode(device_name=device_name)

            # 尝试进入远程配置页
            def access_remote_config():
                BasePage().access_in_remote_setting(text_to_find=device_name)

            # 重启APP并进入远程配置页
            def restart_app_and_access():
                driver.start_app()
                access_remote_config()

            # 尝试切换隐私模式的状态
            def toggle_privacy_mode(expected_state):
                """切换隐私模式并检查状态"""
                on_off_state = self.turn_on_privacy_mode(text=device_name)
                if on_off_state != expected_state:
                    state_text = "关闭" if expected_state else "开启"
                    pytest.fail(f"隐私模式{state_text}失败！")
                logger.info(f"隐私模式已成功{'开启' if expected_state else '关闭'}。")

            if privacy_mode_enabled:
                # 隐私模式已启用，尝试关闭隐私模式
                logger.info("隐私模式已启用，准备关闭隐私模式。")
                restart_app_and_access()
                toggle_privacy_mode(expected_state=False)

            else:
                # 隐私模式未启用，尝试启用隐私模式
                logger.info("隐私模式未启用，尝试启用隐私模式。")
                RemoteSetting().access_in_privacy_mode(device_list_name=device_name)
                time.sleep(2)
                self.scroll_click_right_btn(text_to_find='开启后，摄像机部分功能将停止使用',
                                            className_1='android.widget.TextView',
                                            className_2='android.widget.ImageView')  # 点击启用隐私模式按钮
                time.sleep(10)  # 等待设置生效
                restart_app_and_access()
                toggle_privacy_mode(expected_state=True)

            # 若隐私模式已启用，则在解除之后重启APP
            # if privacy_mode_enabled:
            #     driver.start_app()
            #     # 重启APP后进入远程配置页
            #     RemoteSetting().access_in_privacy_mode(device_list_name=device_name)
            #     on_off_state = self.turn_on_privacy_mode(text=device_name)
            #     if on_off_state:
            #         pytest.fail("隐私模式关闭失败！")
            #     else:
            #         logger.info("隐私模式开启成功！")
            #
            # else:
            #     RemoteSetting().access_in_privacy_mode(device_list_name=device_name)
            #     self.scroll_click_right_btn(text_to_find='隐私模式')  # 尝试启用隐私模式
            #     time.sleep(10)
            #     driver.start_app()
            #     RemoteSetting().access_in_privacy_mode(device_list_name=device_name)
            #     on_off_state = self.turn_on_privacy_mode(text=device_name)
            #     if on_off_state:
            #         pytest.fail("隐私模式开启成功！")
            #     else:
            #         pytest.fail("隐私模式关闭失败！")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
