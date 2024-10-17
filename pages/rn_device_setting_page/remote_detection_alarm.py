# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
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
            self.object_size_drawable_range = ''  # 目标尺寸-可以绘制的屏幕区域范围
            self.min_object = ''  # 目标尺寸-最小目标
            self.max_object = ''  # 目标尺寸-最大目标
            self.fullscreen_object = ''  # 目标尺寸-横屏按钮
            self.landscape_fullscreen_object = ''  # 目标尺寸-恢复竖屏按钮
            self.set_maximum_left_turn_angle = ''  # 水平追踪范围-设置最大左转角度
            self.set_maximum_right_turn_angle = ''  # 水平追踪范围-设置最大右转角度
            self.smart_detection_slider = ''  # 智能侦测拖动条
            self.alarm_delay_slider = ''  # 延时报警拖动条
            self.draw_button = ''  # 非侦测区域的绘制按钮
            self.erasure_button = ''  # 非侦测区域的擦除按钮

        elif self.platform == 'ios':
            self.non_detection_area = ''
            self.non_detection_area_fullscreen_button = ''
            self.landscape_bar_portrait_button = ''
            self.time_selector_hour = ''
            self.time_selector_min = ''
            self.object_size_drawable_range = ''
            self.min_object = ''
            self.max_object = ''
            self.fullscreen_object = ''
            self.landscape_fullscreen_object = ''
            self.set_maximum_left_turn_angle = ''
            self.set_maximum_right_turn_angle = ''
            self.smart_detection_slider = ''
            self.alarm_delay_slider = ''
            self.draw_button = ''
            self.erasure_button = ''

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

    def time_selector(self, direction='up', iteration=1):
        """
        时间选择器
        :param direction: slider的定位方式，支持id或者xpath
        :param iteration:
        :return:
        """
        try:
            # 手指向上滑动选择小时
            self.scroll_selector(id_or_xpath=self.time_selector_hour,
                                 direction=direction,
                                 times=iteration)

            # 手指向上滑动选择分钟
            self.scroll_selector(id_or_xpath=self.time_selector_min,
                                 direction=direction,
                                 times=iteration)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_add_multi_time_sensitivity_motion(self, main_texts):
        """
        点击添加分段灵敏度
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='添加分段灵敏度')

            # 验证添加灵敏度分段主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)
            if not main_texts_res:
                pytest.fail(f"添加分段灵敏度主页文案存在错误，需查录屏!")

            self.click_start_time()  # 点击开始时间
            self.time_selector()  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')  # 点击确定

            self.click_end_time()  # 点击结束时间
            self.time_selector(iteration=2)  # 选择时、分
            self.scroll_and_click_by_text(text_to_find='确定')  # 点击确定

            self.scroll_and_click_by_text(text_to_find='保存')  # 保存分段

            if not RemoteSetting().scroll_check_funcs2('编辑'):  # 验证页面存在“编辑”文案，否则标记失败
                pytest.fail(f"添加分段灵敏度点击保存后，可能未成功，需查录屏!")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

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

    def delete_multi_time_sensitivity_motion(self):
        """
        删除灵敏度分段
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='高 灵敏度(50)')
        self.scroll_and_click_by_text(text_to_find='删除该分段')

# --------------------------------------------------------------
    def check_detection_alarm_main_text(self, main_text, smart_tracking):
        """
        验证侦测报警主页文案
        :param smart_tracking: 是否支持智能追踪
        :param main_text: 待验证的文案列表
        :return:
        """
        try:
            # 开启智能追踪按钮
            if smart_tracking:
                is_auto_tracking_on = RemoteSetting().scroll_check_funcs2(texts='追踪类型')
                if not is_auto_tracking_on:
                    self.scroll_click_right_btn('智能追踪')

            # 侦测报警主页文案验证
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)

            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def draw_portrait_non_detection_area(self, mode='xpath', draw_area='左上'):
        """
        竖屏：绘制非侦测区域，这里的策略是：首先点击全部绘制，然后点击全部擦除，然后点击绘制并在屏幕上绘制一部分内容，最后再点击擦除并对刚刚绘制的区域进行擦除操作
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='全部绘制')
        self.scroll_and_click_by_text(text_to_find=self.erasure_button, el_type='xpath')  # 点击切换【擦除】按钮
        self.scroll_and_click_by_text(text_to_find='全部擦除')

        self.scroll_and_click_by_text(text_to_find=self.draw_button, el_type='xpath')  # 点击切换【绘制】按钮
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)
        self.scroll_and_click_by_text(text_to_find=self.erasure_button, el_type='xpath')  # 点击切换【擦除】按钮
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)

    def draw_landscape_non_detection_area(self, mode='xpath', draw_area='左上'):
        """
        横屏：绘制非侦测区域，这里的策略是：首先点击全部绘制，然后点击全部擦除，然后点击绘制并在屏幕上绘制一部分内容，最后再点击擦除并对刚刚绘制的区域进行擦除操作
        :return:
        """
        # 点击横屏按钮
        self.scroll_and_click_by_text(text_to_find=self.non_detection_area_fullscreen_button, el_type='xpath')

        self.scroll_and_click_by_text(text_to_find='全部绘制')
        self.scroll_and_click_by_text(text_to_find=self.erasure_button, el_type='xpath')  # 点击切换【擦除】按钮
        self.scroll_and_click_by_text(text_to_find='全部擦除')

        self.scroll_and_click_by_text(text_to_find=self.draw_button, el_type='xpath')  # 点击切换【绘制】按钮
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)
        self.scroll_and_click_by_text(text_to_find=self.erasure_button, el_type='xpath')  # 点击切换【擦除】按钮
        self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.non_detection_area, draw_area=draw_area)

        # 点击左上角按钮恢复竖屏
        self.scroll_and_click_by_text(text_to_find=self.landscape_bar_portrait_button, el_type='xpath')

        # 点击保存
        # self.scroll_and_click_by_text(text_to_find='保存')

    def click_test_both_object_size(self):
        """
        点击并测试目标尺寸.适用左、右摄像头
        测试策略：
        分别点击和绘制最小目标、最大目标。横屏
        :return:
        """
        try:
            # 进入目标尺寸页面
            # self.scroll_and_click_by_text("目标尺寸")
            time.sleep(1)

            # 定义通用操作：点击摄像机、绘制最小/最大目标
            def click_camera_and_draw(camera_name):
                self.scroll_and_click_by_text(text_to_find=camera_name, el_type='xpath')  # 点击左/右摄像机
                self.get_coordinates_and_draw(mode='xpath',
                                              id_or_xpath=self.object_size_drawable_range,
                                              draw_area='左上')  # 绘制最小目标
                self.get_coordinates_and_draw(mode='xpath',
                                              id_or_xpath=self.object_size_drawable_range,
                                              draw_area='全屏')  # 绘制最大目标

            # 对左、右摄像机执行操作
            for camera in ["左摄像机", "右摄像机"]:
                click_camera_and_draw(camera)

            # 点击取消后重新进入目标尺寸页面
            self.scroll_and_click_by_text('取消')
            self.scroll_and_click_by_text("目标尺寸")

            # 再次对左、右摄像机执行相同操作
            for camera in ["左摄像机", "右摄像机"]:
                click_camera_and_draw(camera)

            # 点击横屏按钮
            self.scroll_and_click_by_text(text_to_find=self.fullscreen_object, el_type='xpath')
            # 点击返回竖屏按钮
            self.scroll_and_click_by_text(text_to_find=self.landscape_fullscreen_object, el_type='xpath')

            # 点击保存
            self.scroll_and_click_by_text('保存')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_test_single_object_size(self):
        """
        点击并测试目标尺寸.适用单摄像头
        测试策略：
        分别点击和绘制最小目标、最大目标。横屏
        :return:
        :return:
        """
        try:
            # 进入目标尺寸页面
            # self.scroll_and_click_by_text("目标尺寸")
            time.sleep(1)

            # 定义通用操作：绘制最小/最大目标
            def click_camera_and_draw():
                self.get_coordinates_and_draw(mode='xpath',
                                              id_or_xpath=self.object_size_drawable_range,
                                              draw_area='左上')  # 绘制最小目标
                self.get_coordinates_and_draw(mode='xpath',
                                              id_or_xpath=self.object_size_drawable_range,
                                              draw_area='全屏')  # 绘制最大目标

            # 对摄像机执行操作
            click_camera_and_draw()

            # 点击取消后重新进入目标尺寸页面
            self.scroll_and_click_by_text('取消')
            self.scroll_and_click_by_text("目标尺寸")

            # 再次对摄像机执行相同操作
            click_camera_and_draw()

            # 点击横屏按钮
            self.scroll_and_click_by_text(text_to_find=self.fullscreen_object, el_type='xpath')
            # 点击返回竖屏按钮
            self.scroll_and_click_by_text(text_to_find=self.landscape_fullscreen_object, el_type='xpath')

            # 点击保存
            self.scroll_and_click_by_text('保存')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_person_object_size(self, main_texts, texts, is_both):
        """
        点击并测试人——目标尺寸
        :param main_texts: 人主页文案
        :param texts: 目标尺寸页的文案内容
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='人')
            # 验证人主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            self.scroll_and_click_by_text('目标尺寸')
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            if not is_both:
                self.clk_test_single_object_size()
            else:
                self.click_test_both_object_size()

            return main_texts_res, texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_person_smart_detection(self):
        """
        点击测试人-智能侦测
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='人')
            # 向右拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath=self.smart_detection_slider,
                                 direction='right',
                                 iteration=20)
            # 向左拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath=self.smart_detection_slider,
                                 direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看智能侦测
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='人')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_person_alarm_delay(self):
        """
        点击测试人-延时报警
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='人')
            # 向右拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='right', iteration=20)
            # 向左拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='left', iteration=20)

            # 返回上一页，再点击进入查看延时报警
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='人')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_car_object_size(self, main_texts, texts, is_both):
        """
        点击并测试车——目标尺寸
        :param main_texts: 车主页文案
        :param texts: 目标尺寸页的文案内容
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='车')
            # 验证车主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            self.scroll_and_click_by_text('目标尺寸')
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            if not is_both:
                self.clk_test_single_object_size()
            else:
                self.click_test_both_object_size()

            return main_texts_res, texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_car_smart_detection(self):
        """
        点击测试车-智能侦测
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='车')
            # 向右拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='right',
                                 iteration=20)
            # 向左拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看智能侦测
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='车')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_car_alarm_delay(self):
        """
        点击测试车-延时报警
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='车')
            # 向右拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='right',
                                 iteration=20)
            # 向左拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看延时报警
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='车')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_animal_object_size(self, main_texts, texts, is_both):
        """
        点击并测试动物——目标尺寸
        :param main_texts: 动物主页文案
        :param texts: 目标尺寸页的文案内容
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='动物')
            # 验证动物主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            self.scroll_and_click_by_text('目标尺寸')
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            if not is_both:
                self.clk_test_single_object_size()
            else:
                self.click_test_both_object_size()

            return main_texts_res, texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_animal_smart_detection(self):
        """
        点击测试动物-智能侦测
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='动物')
            # 向右拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='right',
                                 iteration=20)
            # 向左拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看智能侦测
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='动物')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_animal_alarm_delay(self):
        """
        点击测试动物-延时报警
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='动物')
            # 向右拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='right',
                                 iteration=20)
            # 向左拖动延时报警
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看延时报警
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find='动物')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_package_object_size(self, main_texts, texts, is_both):
        """
        点击并测试包裹——目标尺寸
        :param main_texts: 包裹主页文案
        :param texts: 目标尺寸页的文案内容
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='包裹')
            # 验证包裹主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            self.scroll_and_click_by_text('目标尺寸')
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            if not is_both:
                self.clk_test_single_object_size()
            else:
                self.click_test_both_object_size()

            return main_texts_res, texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_test_ai_non_detect_area(self, non_detect_type, edit_texts, is_both):
        """
        点击并测试某某非侦测选项——>非侦测区域
        :param non_detect_type: 非侦测选项的入口：人、车、动物、包裹
        :param edit_texts: 非侦测区域编辑页文案
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find=non_detect_type)  # 点击需要测试的非非侦测选项的入口
            self.scroll_and_click_by_text(text_to_find='非侦测区域')
            # 验证非侦测区域编辑页文案
            edit_texts_res = RemoteSetting().scroll_check_funcs2(texts=edit_texts)
            if not is_both:
                # 测试竖屏绘制非侦测区域
                self.draw_portrait_non_detection_area()
                # 测试横屏绘制非侦测区域
                self.draw_landscape_non_detection_area()
            else:
                # 测试竖屏绘制非侦测区域
                self.scroll_and_click_by_text('左摄像机')
                self.draw_portrait_non_detection_area()
                self.scroll_and_click_by_text('右摄像机')
                self.draw_portrait_non_detection_area()
                # 测试横屏绘制非侦测区域
                self.scroll_and_click_by_text('左摄像机')
                self.draw_landscape_non_detection_area()
                self.scroll_and_click_by_text('右摄像机')
                self.draw_landscape_non_detection_area()

            return edit_texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_draw_sensitivity(self, non_detect_type):
        """
        点击并测试侦测报警主页>某某选项——>灵敏度
        :param non_detect_type: 侦测报警主页选项的入口：人、车、动物、包裹
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find=non_detect_type)  # 点击需要测试的选项入口
            # 向右拖动灵敏度
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='right',
                                 iteration=20)
            # 向左拖动灵敏度
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.alarm_delay_slider, direction='left',
                                 iteration=20)

            # 返回上一页，再点击进入查看灵敏度
            self.back_previous_page()
            self.scroll_and_click_by_text(text_to_find=non_detect_type)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def clk_test_main_non_detect_area(self, edit_texts, is_both):
        """
        点击并测试侦测报警主页——>非侦测区域
        :param edit_texts: 非侦测区域编辑页文案
        :param is_both: 是否双摄像头
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='非侦测区域')  # 点击侦测报警主页》非侦测区域
            # 验证非侦测区域编辑页文案
            edit_texts_res = RemoteSetting().scroll_check_funcs2(texts=edit_texts)

            if not is_both:
                # 测试竖屏绘制非侦测区域
                self.draw_portrait_non_detection_area()
                # 测试横屏绘制非侦测区域
                self.draw_landscape_non_detection_area()
            else:
                # 测试竖屏绘制非侦测区域
                self.scroll_and_click_by_text('左摄像机')
                self.draw_portrait_non_detection_area()
                self.scroll_and_click_by_text('右摄像机')
                self.draw_portrait_non_detection_area()
                # 测试横屏绘制非侦测区域
                self.scroll_and_click_by_text('左摄像机')
                self.draw_landscape_non_detection_area()
                self.scroll_and_click_by_text('右摄像机')
                self.draw_landscape_non_detection_area()
                # 点击保存
                self.scroll_and_click_by_text(text_to_find='保存')

            return edit_texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_motion_detect(self, main_texts, add_multi_time_texts):
        """
        点击测试【MD/其他】（原移动侦测）
        :return:
        """
        try:
            # 点击MD/其他
            self.scroll_and_click_by_text('MD/其他')
            # 验证MD/其他主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 点击添加灵敏度分段
            self.click_add_multi_time_sensitivity_motion(add_multi_time_texts)

            return main_texts_res is True

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_smart_tracking(self, options):
        """
        点击并测试智能追踪.
        :param options: 包含所有参数的字典
            - tracking_type_list: 需要遍历勾选的 追踪类型 文本列表
            - tracking_method_list: 需要遍历勾选的 追踪方式 文本列表
            - plan_text_list: 计划表需要验证的文本列表
            - object_stops_list: 目标静止多久后结束追踪的时间，列表
            - object_disappears_list: 目标消失多久后结束追踪的时间，列表
            - menu_text: 需要点击进入多选页面的菜单功能项
            - text_to_find: 保底需要勾选的文本
        :return:
        """
        try:
            # 判断页面是否存在“追踪类型”字段。没有则点击按钮开启智能追踪
            is_auto_tracking_on = RemoteSetting().scroll_check_funcs2(texts='追踪类型')
            if not is_auto_tracking_on:
                self.scroll_click_right_btn('智能追踪')

            # 点击并遍历追踪类型
            self.click_checkbox_by_text(option_text_list=options['tracking_type']['option_text'], menu_text='追踪类型')
            self.scroll_and_click_by_text(text_to_find=options['tracking_type']['option_text'][0])
            self.scroll_and_click_by_text(text_to_find='保存')

            # 验证追踪方式页面文案
            smart_tracking_texts_res = RemoteSetting().scroll_check_funcs2(texts=options['tracking_mode']['text'])
            # 点击并遍历追踪方式
            self.iterate_and_click_popup_text(option_text_list=options['tracking_mode']['option_text'], menu_text='追踪方式')

            # 点击并测试水平追踪范围
            self.scroll_and_click_by_text(text_to_find='水平追踪范围')
            # 验证水平追踪范围主页文案
            hril_tracking_range_texts_res = RemoteSetting().scroll_check_funcs2(texts=options['horizontal_tracking_range']['text'])
            self.scroll_and_click_by_text(text_to_find='设置')
            # TODO: 设置左、右侧
            # 验证左侧页面文案
            left_texts_res = RemoteSetting().scroll_check_funcs2(texts=options['horizontal_tracking_range']['left_side_text'])
            self.long_click_by(text_to_find=self.set_maximum_left_turn_angle, el_type='xpath')  # 长按左侧
            self.scroll_and_click_by_text('下一步')
            # 验证右侧页面文案
            right_texts_res = RemoteSetting().scroll_check_funcs2(texts=options['horizontal_tracking_range']['right_side_text'])
            self.long_click_by(text_to_find=self.set_maximum_right_turn_angle, el_type='xpath')  # 长按右侧
            self.long_click_by(text_to_find=self.set_maximum_right_turn_angle, el_type='xpath')  # 再长按一次
            self.scroll_and_click_by_text('保存')
            # 点击清空
            self.scroll_and_click_by_text('清空')
            self.scroll_and_click_by_text('取消')  # 点击取消
            # 点击清空
            self.scroll_and_click_by_text('清空')
            self.scroll_and_click_by_text('清空')
            # 返回上一页
            self.back_previous_page()

            # 点击并测试计划表
            self.scroll_and_click_by_text(text_to_find='计划')
            plan_text_res = RemoteSetting().scroll_check_funcs2(texts=options['time_plan']['text'])

            # 点击并遍历目标静止、目标消失（没有验证文案）
            self.iterate_and_click_popup_text(option_text_list=options['object_stops']['option_text'],
                                              menu_text='目标静止')
            self.iterate_and_click_popup_text(option_text_list=options['object_disappears']['option_text'],
                                              menu_text='目标消失')

            result = {
                'smart_tracking': smart_tracking_texts_res,
                'hril_tracking_range': hril_tracking_range_texts_res,
                'left_texts': left_texts_res,
                'right_texts': right_texts_res,
                'plan_text': plan_text_res
            }
            return result

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
# --------------------------------------------------------------






































