# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteDisplay(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def access_in_stream(self, option_text='码流'):
        """
        进入并测试码流页面
        :param option_text: 菜单功能项，该方法默认进入【码流】
        :return:
        """
        # 进入码流页面
        self.scroll_and_click_by_text(text_to_find=option_text)

    def access_in_clear(self, option_text='清晰'):
        """
        进入码流>清晰页面
        :param option_text: 菜单功能项，该方法默认进入【码流>清晰】
        :return:
        """
        # 进入码流>清晰页面
        self.scroll_and_click_by_text(text_to_find=option_text)

    def access_in_fluent(self, option_text='流畅'):
        """
        进入码流>流畅页面
        :param option_text: 菜单功能项，该方法默认进入【码流>流畅】
        :return:
        """

    def click_resolution(self, option_text='分辨率'):
        """
        :param option_text: 菜单功能项，该方法默认点击【分辨率】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_frame_rate(self, option_text='帧率(fps)'):
        """
        :param option_text: 菜单功能项，该方法默认点击【帧率(fps)】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_max_bit_rate(self, option_text='最大码率(kbps)'):
        """
        :param option_text: 菜单功能项，该方法默认点击【最大码率(kbps)】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_frame_rate_mode(self, option_text='帧率控制'):
        """
        :param option_text: 菜单功能项，该方法默认点击【帧率控制】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def draw_privacy_mask(self, mode, id_or_xpath):
        """
        隐私遮盖区域，目前的操作策略是画1/4屏，然后画全屏
        :param mode:
        :param id_or_xpath:
        :return:
        """
