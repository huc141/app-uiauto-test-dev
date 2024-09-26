# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteDetectionAlarm(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.non_detection_area = '//*[@resource-id="com.mcu.reolink:id/ziv"]'  # 非侦测区域屏幕
            self.non_detection_area_fullscreen_button = '//*[@resource-id="com.mcu.reolink:id/player_fullscreen_button"]'  # 非侦测区域横屏按钮
            self.landscape_bar_portrait_button = '//*[@resource-id="com.mcu.reolink:id/landscape_bar_portrait"]'  # 非侦测区域横屏左上角按钮恢复竖屏按钮

        elif self.platform == 'ios':
            self.non_detection_area = ''
            self.non_detection_area_fullscreen_button = ''

    def click_non_detection_area(self):
        """
        点击进入非侦测区域
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='非侦测区域')

    def draw_portrait_non_detection_area(self, mode='xpath', draw_area='左上'):
        """
        竖屏：绘制非侦测区域，这里的策略是：首先点击全部绘制，然后点击全部擦除，然后点击绘制并在屏幕上绘制一部分内容，最后再点击擦除并对刚刚绘制的区域进行擦除操作
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='全部绘制')

        self.scroll_and_click_by_text(text_to_find='全部擦除')

        self.scroll_and_click_by_text(text_to_find='绘制')
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)
        self.scroll_and_click_by_text(text_to_find='擦除')
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)

    def draw_landscape_non_detection_area(self, mode='xpath', draw_area='左上'):
        """
        横屏：绘制非侦测区域，这里的策略是：首先点击全部绘制，然后点击全部擦除，然后点击绘制并在屏幕上绘制一部分内容，最后再点击擦除并对刚刚绘制的区域进行擦除操作
        :return:
        """
        # 点击横屏按钮
        self.scroll_and_click_by_text(text_to_find=self.non_detection_area_fullscreen_button, el_type='xpath')

        self.scroll_and_click_by_text(text_to_find='全部绘制')
        self.scroll_and_click_by_text(text_to_find='全部擦除')

        self.scroll_and_click_by_text(text_to_find='绘制')
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)
        self.scroll_and_click_by_text(text_to_find='擦除')
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)

        # 点击左上角按钮恢复竖屏
        self.scroll_and_click_by_text(text_to_find=self.landscape_bar_portrait_button, el_type='xpath')

    def click_motion_mark_switch(self):
        """
        点击移动标记Switch按钮，点击两次
        :return:
        """
        self.scroll_click_right_btn(text_to_find='移动标记')
        time.sleep(1.5)
        self.scroll_click_right_btn(text_to_find='移动标记')

    def click_sensitivity_motion(self):
        """
        点击灵敏度
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='灵敏度')

    def click_motion_detect(self):
        """
        点击移动侦测
        :return:
        """
        # 点击移动侦测
        self.scroll_and_click_by_text('移动侦测')

    def click_add_multi_time_sensitivity_motion(self):
        """
        点击添加分段灵敏度
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='添加分段灵敏度')
