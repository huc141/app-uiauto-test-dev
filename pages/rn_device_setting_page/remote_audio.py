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
            self.device_sound_xpath = '//*[@resource-id="RNE__Slider_Thumb"]'  # 设备音量拖动条
            self.adjust_noise_reduction_xpath = ''  # 降噪强度拖动条
            self.start_record_sound = '//*[@resource-id="RecordSwitch:0"]'  # 开始录音按钮
            self.stop_record_sound = '//*[@resource-id="RecordSwitch:1"]'  # 停止录音按钮
            self.next_step = '//*[@resource-id="RecordNext-ReoButton"]'  # 录音完成后【下一步】按钮
            self.retry_record_sound = '//*[@resource-id="RecordRetry-ReoButton"]'  # 重试按钮

        elif self.platform == 'ios':
            self.device_sound_xpath = ''
            self.adjust_noise_reduction_xpath = ''
            self.start_record_sound = ''
            self.stop_record_sound = ''
            self.next_step = ''
            self.retry_record_sound = ''

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
        打开【音频降噪】，并调节降噪强度.
        :return:
        """
        def adjust_noise_reduction(slider_mode):
            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=self.adjust_noise_reduction_xpath,
                                 direction='right',
                                 iteration=5)

            # 往左拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=self.adjust_noise_reduction_xpath,
                                 direction='left',
                                 iteration=5)

            # 往右拖动2次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=self.adjust_noise_reduction_xpath,
                                 direction='right',
                                 iteration=2)

        if self.is_element_exists(element_value='降噪强度'):
            logger.info('音频降噪已开启')

        else:
            logger.info('音频降噪未开启，正在尝试开启')
            self.scroll_click_right_btn(text_to_find='音频降噪')
            if self.is_element_exists(element_value='降噪强度'):
                logger.info('音频降噪已开启')
                adjust_noise_reduction(slider_mode='xpath')

    def click_auto_reply(self):
        """
        点击【自动回复】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='自动回复')

    def click_record_auto_reply(self):
        """
        点击【录制自动回复】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='录制自动回复')

    def click_start_record_sound(self, mode=1):
        """
        点击【开始录音】
        :param mode: TODO:1：录音5s后点击停止；命名录音
                    TODO:2：录音10s后自动停止录音；命名录音
                    TODO:3：录音10s后点击重录并重新录制10s，命名录音
                    TODO:4：录音5s后点击停止，命名录音、重命名录音、删除录音
        :return:
        """
        if mode == 1:
            # 点击开始录音按钮
            self.scroll_and_click_by_text(text_to_find=self.start_record_sound, el_type='xpath')
            time.sleep(5)
            # 点击关闭录音按钮
            self.scroll_and_click_by_text(text_to_find=self.stop_record_sound, el_type='xpath')
            # 点击下一步并命名录音
            self.scroll_and_click_by_text(text_to_find=self.next_step, el_type='xpath')
            # TODO:定位命名输入框并输入“auto_test_record_xxxx”，点击保存，验证保存是否成功

        if mode == 2:
            # 点击开始录音按钮
            self.scroll_and_click_by_text(text_to_find=self.start_record_sound, el_type='xpath')
            time.sleep(12)
            # 点击下一步并命名录音
            self.scroll_and_click_by_text(text_to_find=self.next_step, el_type='xpath')
            # TODO:录音命名

        if mode == 3:
            # 点击开始录音按钮
            self.scroll_and_click_by_text(text_to_find=self.start_record_sound, el_type='xpath')
            time.sleep(12)
            # 点击重新录制
            self.scroll_and_click_by_text(text_to_find=self.retry_record_sound, el_type='xpath')

        if mode == 4:
            # 点击开始录音按钮
            self.scroll_and_click_by_text(text_to_find=self.start_record_sound, el_type='xpath')
            time.sleep(5)
            # 点击关闭录音按钮
            self.scroll_and_click_by_text(text_to_find=self.stop_record_sound, el_type='xpath')
            # 点击下一步并命名录音
            self.scroll_and_click_by_text(text_to_find=self.next_step, el_type='xpath')
            # TODO:录音命名

    def click_waiting_time(self, option_text_list):
        """
        点击【等待时长】，并遍历选项
        :param option_text_list:
        :return:
        """
        self.iterate_and_click_popup_text(option_text_list=option_text_list, menu_text='等待时长')

    def click_edit(self):
        """
        点击【编辑】按钮
        :return:
        """
        self.scroll_and_click_by_text(text_to_find='编辑')

    def auto_reply_rename(self):
        pass

    def auto_reply_delete(self):
        pass

