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
            self.time_selector_hour = '//*[@resource-id="com.mcu.reolink:id/options1"]'  # 编辑分段灵敏度，开始时间设置：小时
            self.time_selector_min = '//*[@resource-id="com.mcu.reolink:id/options2"]'  # 编辑分段灵敏度，开始时间设置：分钟

        elif self.platform == 'ios':
            self.non_detection_area = ''
            self.non_detection_area_fullscreen_button = ''
            self.time_selector_hour = ''
            self.time_selector_min = ''

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

    def click_smart_detect(self):
        """
        点击智能侦测
        :return:
        """
        self.scroll_and_click_by_text('智能侦测')

    def click_add_multi_time_sensitivity_motion(self):
        """
        点击添加分段灵敏度
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='添加分段灵敏度')

    def click_start_time(self):
        """
        点击开始时间，针对时间选择器
        :return:
        """
        self.scroll_and_click_by_text('开始时间')

    def click_end_time(self):
        """
        点击结束时间，针对时间选择器
        :return:
        """
        self.scroll_and_click_by_text('结束时间')

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

    def delete_multi_time_sensitivity_motion(self):
        """
        删除灵敏度分段
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='高 灵敏度(50)')
        self.scroll_and_click_by_text(text_to_find='删除该分段')

    def click_alarm_delay(self):
        """
        点击延时报警
        :return:
        """
        self.scroll_and_click_by_text('延时报警')

    def drag_alarm_delay_slider_person(self):
        """
        拖动延时报警：人
        :return:
        """
        # TODO: 待rn提测
        pass

    def drag_alarm_delay_slider_car(self):
        """
        拖动延时报警：车
        :return:
        """
        # TODO: 待rn提测
        pass

    def drag_alarm_delay_slider_animal(self):
        """
        拖动延时报警：动物
        :return:
        """
        # TODO: 待rn提测
        pass

    def click_and_test_object_size(self, object_list):
        """
        点击并测试目标尺寸.
        测试策略：
        进入目标尺寸页面后，遍历检测目标类型，并点击最小目标、最大目标。
        :param object_list: 检测目标类型，如人车动物包裹等。列表
        :return:
        """
        self.scroll_and_click_by_text('目标尺寸')

