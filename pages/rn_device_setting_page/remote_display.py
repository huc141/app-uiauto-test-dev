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
            self.shelter_player = '//*[@resource-id="com.mcu.reolink:id/shelter_player"]'  # 隐私遮盖可画框区域
            self.slider_brightness_xpath = ''  # 亮度条定位xpath

        elif self.platform == 'ios':
            self.shelter_player = ''
            self.slider_brightness_xpath = ''

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

    def click_anti_flicker(self, option_text='抗闪烁'):
        """
        :param option_text: 菜单功能项，该方法默认点击【抗闪烁】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_day_and_night(self, option_text='白天和黑夜'):
        """
        :param option_text: 菜单功能项，该方法默认点击【白天和黑夜】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def drag_slider_brightness(self, slider_mode, iteration=20):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id或者xpath
        :param id_or_xpath: id或者xpath的定位参数
        :param direction: 方向，支持"left", "right", "up", "down"方向
        :param iteration: 拖动次数，若是ios，则此处为移动“步数”，不支持定义拖动次数，
        :return:
        """
        # 往右拖动20次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.slider_brightness_xpath,
                             direction='right',
                             iteration=iteration)

        # 往左拖动30次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.slider_brightness_xpath,
                             direction='left',
                             iteration=30)

        # 往右拖动10次
        self.slider_seek_bar(slider_mode=slider_mode,
                             id_or_xpath=self.slider_brightness_xpath,
                             direction='right',
                             iteration=10)

    def click_device_name(self, option_text='设备名称'):
        """
        :param option_text: 菜单功能项，该方法默认点击【设备名称】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def access_in_privacy_mask(self, option_text='遮盖区域'):
        """
        :param option_text: 菜单功能项，该方法默认点击【遮盖区域】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)
        if self.is_element_exists(element_value='清空并继续'):
            logger.info(f'弹出了遮盖区域提示，正在尝试点击【清空并继续】...')
            self.click_by_text(text='清空并继续')
            logger.info('已点击【清空并继续】')

    def draw_privacy_mask(self, mode, draw_area='左上'):
        """
        画隐私遮盖区域
        :param mode: 定位方式，支持id或者xpath
        :param id_or_xpath: 可遮盖区域的id或者xpath的定位参数
        :param draw_area: 需要遮盖的区域，支持[左上]、[左下]、[右上]、[右下]的1/4屏，以及[全屏]遮盖，默认左上。
        :param num: 画框数量，默认为0，为0时需要指定遮盖区域draw_area，若不指定，则默认左上遮盖
        :return:
        """
        try:

            if not self.is_element_exists(element_value='广角画面'):
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=9)

            if self.is_element_exists(element_value='广角画面'):
                self.click_by_text('广角画面')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

            if self.is_element_exists(element_value='长焦画面'):
                self.click_by_text('长焦画面')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

        except Exception as err:
            logger.info(f"可能发生了错误: {err}")
            return False

