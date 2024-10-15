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
            self.min_object = ''  # 目标尺寸-最小目标
            self.max_object = ''  # 目标尺寸-最大目标
            self.set_maximum_left_turn_angle = ''  # 水平追踪范围-设置最大左转角度
            self.set_maximum_right_turn_angle = ''  # 水平追踪范围-设置最大右转角度
            self.smart_detection_slider = ''  # 智能侦测拖动条
            self.alarm_delay_slider = ''  # 延时报警拖动条

        elif self.platform == 'ios':
            self.non_detection_area = ''
            self.non_detection_area_fullscreen_button = ''
            self.time_selector_hour = ''
            self.time_selector_min = ''
            self.min_object = ''
            self.max_object = ''
            self.set_maximum_left_turn_angle = ''
            self.set_maximum_right_turn_angle = ''
            self.smart_detection_slider = ''
            self.alarm_delay_slider = ''

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
                self.scroll_click_right_btn(text_to_find='智能追踪')

            # 侦测报警主页文案验证
            main_text_res = RemoteSetting().scroll_check_funcs2(texts=main_text)

            return main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_object_size(self):
        """
        点击并测试目标尺寸.
        测试策略：
        分别点击和绘制最小目标、最大目标。
        :return:
        """
        try:
            self.scroll_and_click_by_text("目标尺寸")
            time.sleep(1)

            # 点击 最大目标
            self.scroll_and_click_by_text(text_to_find=self.max_object, el_type='xpath')
            # TODO：绘制最大目标

            # 点击 最小目标
            self.scroll_and_click_by_text(text_to_find=self.min_object, el_type='xpath')
            # TODO：绘制最小目标

            # 点击 取消
            self.scroll_and_click_by_text('取消')

            self.scroll_and_click_by_text("目标尺寸")

            # 点击 最大目标
            self.scroll_and_click_by_text(text_to_find=self.max_object, el_type='xpath')
            # TODO：绘制最大目标
            # TODO：删除最大目标

            # 点击 最小目标
            self.scroll_and_click_by_text(text_to_find=self.min_object, el_type='xpath')
            # TODO：绘制最小目标
            # TODO：删除最小目标

            # TODO：点击横屏按钮
            # TODO：绘制最大目标
            # TODO：绘制最小目标

            # TODO: 点击左上角返回竖屏按钮

            # TODO：点击保存

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_test_person_object_size(self, main_texts, texts):
        """
        点击并测试人——目标尺寸
        :param main_texts: 人主页文案
        :param texts: 目标尺寸页的文案内容
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='人')
            # 验证人主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            self.click_and_test_object_size()

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
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='right', iteration=20)
            # 向左拖动智能侦测
            self.slider_seek_bar(slider_mode='xpath', id_or_xpath=self.smart_detection_slider, direction='left', iteration=20)

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

    def click_test_car_object_size(self, main_texts, texts):
        """
        点击并测试车——目标尺寸
        :param main_texts: 车主页文案
        :param texts: 目标尺寸页的文案内容
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='车')
            # 验证车主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            self.click_and_test_object_size()

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

    def click_test_animal_object_size(self, main_texts, texts):
        """
        点击并测试动物——目标尺寸
        :param main_texts: 动物主页文案
        :param texts: 目标尺寸页的文案内容
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='动物')
            # 验证动物主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            self.click_and_test_object_size()

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

    def click_test_package_object_size(self, main_texts, texts):
        """
        点击并测试包裹——目标尺寸
        :param main_texts: 包裹主页文案
        :param texts: 目标尺寸页的文案内容
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='包裹')
            # 验证包裹主页文案
            main_texts_res = RemoteSetting().scroll_check_funcs2(texts=main_texts)

            # 验证目标尺寸文案
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)
            self.click_and_test_object_size()

            return main_texts_res, texts_res
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

# --------------------------------------------------------------

    def click_and_test_auto_tracking(self, tracking_type_list, tracking_method_list, plan_text_list, object_stops_list, object_disappears_list, text_to_find, mode):
        """
        点击并测试智能追踪.
        :param tracking_type_list: 需要遍历勾选的 追踪类型 文本列表
        :param tracking_method_list: 需要遍历勾选的 追踪方式 文本列表
        :param plan_text_list: 计划表需要验证的文本列表
        :param object_stops_list: 目标静止多久后结束追踪的时间，列表
        :param object_disappears_list: 目标消失多久后结束追踪的时间，列表
        :param menu_text: 需要点击进入多选页面的菜单功能项
        :param text_to_find: 保底需要勾选的文本
        :param mode: 1：根据文本直接多选；2：根据文本点击右边按钮多选
        :return:
        """
        try:
            # 判断页面是否存在“追踪类型”字段。没有则点击按钮开启智能追踪
            is_auto_tracking_on = RemoteSetting().scroll_check_funcs2(texts='追踪类型')
            if not is_auto_tracking_on:
                self.scroll_click_right_btn('智能追踪')

            # 点击并遍历追踪类型
            self.click_checkbox_by_text(option_text_list=tracking_type_list, menu_text='追踪类型')
            self.scroll_and_click_by_text(text_to_find=text_to_find)
            self.scroll_and_click_by_text(text_to_find='保存')

            # 点击并遍历追踪方式
            self.iterate_and_click_popup_text(option_text_list=tracking_method_list, menu_text='追踪方式')

            # 点击并测试水平追踪范围
            self.scroll_and_click_by_text(text_to_find='水平追踪范围')
            self.scroll_and_click_by_text(text_to_find='设置')
            # TODO: 设置左、右侧
            self.scroll_and_click_by_text(text_to_find=self.set_maximum_left_turn_angle, el_type='xpath')
            self.scroll_and_click_by_text('下一步')
            self.scroll_and_click_by_text(text_to_find=self.set_maximum_right_turn_angle, el_type='xpath')
            self.scroll_and_click_by_text('保存')

            # 点击并测试计划表
            self.scroll_and_click_by_text(text_to_find='计划')
            plan_text_result = RemoteSetting().scroll_check_funcs2(texts=plan_text_list)

            # 点击并遍历目标静止、目标消失
            self.iterate_and_click_popup_text(option_text_list=object_stops_list, menu_text='目标静止')
            self.iterate_and_click_popup_text(option_text_list=object_disappears_list, menu_text='目标消失')

            return plan_text_result

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")




































