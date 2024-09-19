# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteAudio(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.device_sound_xpath = ''  # 设备音量拖动条

        elif self.platform == 'ios':
            self.device_sound_xpath = ''

    def click_twice_record_sound(self, text_to_find):
        """
        点击【录制声音】switch开关，点击两次
        :param text_to_find: 要查找的文本
        :return:
        """
        self.scroll_click_right_btn(text_to_find=text_to_find)

    def click_twice_doorbell_button_sound(self, text_to_find):
        """
        点击【门铃按钮的声音】switch开关，点击两次
        :param text_to_find: 要查找的文本
        :return:
        """
        self.scroll_click_right_btn(text_to_find=text_to_find)

    def drag_slider_device_volume(self, slider_mode, iteration=20):
        """
        对【设备音量】拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id或者xpath
        :param id_or_xpath: id或者xpath的定位参数
        :param direction: 方向，支持"left", "right", "up", "down"方向
        :param iteration: 拖动次数，若是ios，则此处为移动“步数”，不支持定义拖动次数，
        :return:
        """
        # 往右拖动20次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.device_sound_xpath,
                             direction='right',
                             iteration=iteration)

        # 往左拖动30次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.device_sound_xpath,
                             direction='left',
                             iteration=30)

        # 往右拖动10次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.device_sound_xpath,
                             direction='right',
                             iteration=10)

    def click_sound_test(self, text_to_find):
        """
        点击【试听】播放开关
        :param text_to_find: 要查找的文本
        :return:
        """
        self.scroll_click_right_btn(text_to_find=text_to_find)

    def turn_on_noise_reduction(self):
        """
        TODO:
        :return:
        """
        pass