# -*- coding: utf-8 -*-
import copy
import time
import pytest
from typing import Literal
from functools import wraps
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.decorators import page_loader_decorator
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config_back = read_yaml.get_data(key="back", source="global_data")
g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
display_device_name_texts = g_config.get("display_device_name_texts")  # 显示>设备名称配置页的所有文案
display_device_name_reotitle = g_config.get("display_device_name_reotitle")  # 设备名称配置页的【设备名称】选项
display_date_texts = g_config.get("display_date_texts")  # 显示>日期配置页的所有文案
display_date_reotitle = g_config.get("display_date_reotitle")  # 日期配置页的【日期】选项
loading_icon = g_config.get("loading_icon")  # 页面加载loading菊花xpath
slider_seek_icon = g_config.get("slider_seek_icon")  # 拖动条定位


class RemoteDisplay(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.shelter_player = '//*[@resource-id="DragMaskOperationArea"]'  # 隐私遮盖可画框区域
            self.user_tips_button = '//*[@resource-id="ReoIcon-Question"]'  # 用户提示按钮
            self.delete_button = '//*[@resource-id="ReoIcon-Delet"]'  # 删除按钮
            self.clear_all_button = '//*[@resource-id="ReoIcon-Retry1x"]'  # 清空所有按钮
            self.fullscreen_switch_button = '//*[@resource-id="ReoIcon-Fullscreen"]'  # 全屏按钮
            self.return_vertical_screen_button = '//*[@resource-id="ReoIcon-Left"]'  # 返回竖屏按钮
            self.layout_expand_button = '//*[@resource-id="ImageLayoutExpand"]'  # 图像布局 > 展开按钮
            self.layout_fisheye_button = '//*[@resource-id="ImageLayoutOriginal"]'  # 图像布局 > 鱼眼按钮
            self.display_mode_type_FLOOR = '//*[@resource-id="FLOOR"]'  # 显示模式 > 桌面
            self.display_mode_type_TOP = '//*[@resource-id="TOP"]'  # 显示模式 > 吸顶
            self.display_mode_type_WALL = '//*[@resource-id="WALL"]'  # 显示模式 > 壁挂
            self.pull_down_element = '//com.horcrux.svg.SvgView'  # 显示页面的上拉元素

        elif self.platform == 'ios':
            self.shelter_player = ''

    # 定义一个判断当前页面是否需要上拉的方法
    def need_pull_down(self, pull_down: bool = True):
        """
        判断当前页面是否需要上拉
        :return:
        """
        try:
            time.sleep(2)
            if RemoteSetting().is_element_exists(element_value=self.pull_down_element, selector_type='xpath',
                                                 scroll_or_not=False) and pull_down:
                self.drag_element(element_xpath=self.pull_down_element,
                                  direction='up', distance=700, duration=1)
            else:
                logger.info('当前页面无需进行上拉操作')
        except Exception as err:
            logger.error(f"上拉页面发生错误: {err}")

    @page_loader_decorator
    def check_display_main_text(self, text1, text2):
        """
        验证显示主页文案
        :param text1: 全局文案列表
        :param text2: ReoTitle的功能项文案列表
        :return:
        """
        try:
            # 先将预览视图往上拉至最小,以便于滚动查找设备名称菜单
            self.need_pull_down()
            # 验证显示主页文案
            RemoteSetting().scroll_check_funcs2(texts=text1)
            RemoteSetting().scroll_check_funcs2(texts=text2, selector='ReoTitle')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_vertical_flip_switch_button(self):
        """
        点击垂直翻转按钮
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find='垂直翻转',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup'
                                        )
        except Exception as err:
            logger.info(f"可能发生了错误: {err}")
            return False

    def click_horizontal_flip_switch_button(self):
        """
        点击水平翻转按钮
        :return:
        """
        try:
            self.scroll_click_right_btn(text_to_find='水平翻转',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup'
                                        )
            time.sleep(3)
        except Exception as err:
            logger.info(f"可能发生了错误: {err}")
            return False

    def access_in_stream(self, option_text='码流'):
        """
        进入并测试码流页面
        :param option_text: 菜单功能项，该方法默认进入【码流】
        :return:
        """
        # 进入码流页面
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_motion_mark(self):
        """点击移动标记"""
        try:
            # 点击两次
            for i in range(2):
                self.scroll_click_right_btn(text_to_find='移动标记',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup'
                                            )
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

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
        # 进入码流>流畅页面
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_resolution(self, option_text='分辨率'):
        """
        :param option_text: 菜单功能项，该方法默认点击【分辨率】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_frame_rate(self, option_text='帧率(FPS)'):
        """
        :param option_text: 菜单功能项，该方法默认点击【帧率(FPS)】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_max_bit_rate(self, option_text='最大码率(Kbps)'):
        """
        :param option_text: 菜单功能项，该方法默认点击【最大码率(Kbps)】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_encoding_format(self, option_text='编码格式'):
        """
        :param option_text: 菜单功能项，该方法默认点击【编码格式】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_i_frame_interval(self, option_text='I 帧间隔'):
        """
        :param option_text: 菜单功能项，该方法默认点击【I 帧间隔】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_frame_rate_mode(self, option_text='帧率控制'):
        """
        :param option_text: 菜单功能项，该方法默认点击【帧率控制】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_rate_mode(self, option_text='码率模式'):
        """
        :param option_text: 菜单功能项，该方法默认点击【码率模式】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_day_and_night(self, option_text='白天和黑夜'):
        """
        :param option_text: 菜单功能项，该方法默认点击【白天和黑夜】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_image_setting(self, option_text='图像设置'):
        """
        :param option_text: 菜单功能项，该方法默认点击【图像设置】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def verify_hdr(self):
        """
        验证HDR
        :return:
        """
        try:
            hdr_texts = ['HDR', '自动', '开', '关']
            hdr_options = ['自动', '开', '关']
            # 找到HDR
            self.scroll_and_click_by_text(text_to_find='HDR')

            # 验证HDR文案
            RemoteSetting().scroll_check_funcs2(texts=hdr_texts, scroll_or_not=False, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=hdr_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)

            # 返回上一级
            self.back_previous_page_by_xpath()

            # 开始遍历验证选项
            self.iterate_and_click_popup_text(option_text_list=hdr_options, menu_text='HDR')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_night_vision_zoom_enhance(self):
        """
        验证夜视增强
        :return:
        """
        try:
            # 找到夜视增强
            self.scroll_and_click_by_text(text_to_find='夜视对焦增强')

            # 点击Switch按钮
            self.scroll_click_right_btn(text_to_find='夜视对焦增强',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')
            time.sleep(3)
            self.scroll_click_right_btn(text_to_find='夜视对焦增强',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def drag_slider_brightness(self, slider_mode='obj'):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :param id_or_xpath: id或者xpath的定位参数
        :param direction: 方向，支持"left", "right", "up", "down"方向
        :param iteration: 拖动次数，若是ios，则此处为移动“步数”，不支持定义拖动次数，
        :return:
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Brightness"]',
                target_id=slider_seek_icon)

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def drag_slider_contrast(self, slider_mode='obj'):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :param id_or_xpath: id或者xpath的定位参数
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Contrast"]',
                target_id=slider_seek_icon)

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def drag_slider_saturation(self, slider_mode='obj'):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :param id_or_xpath: id或者xpath的定位参数
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Saturation"]',
                target_id=slider_seek_icon)

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def drag_slider_sharpness(self, slider_mode='obj'):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :param id_or_xpath: id或者xpath的定位参数
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Sharpen"]',
                target_id=slider_seek_icon)

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_image_setting_slider(self, anti_flicker, night_tt_vision, hdr, brightness_sync, image_config):
        """
        验证图像设置
        :param custom_texts: 图像设置全局文案
        :param custom_options: 图像设置ReoTitle功能项
        :param anti_flicker: 是否支持抗闪烁
        :param night_tt_vision: 是否支持夜视通透模式
        :param hdr: 是否支持HDR
        :param brightness_sync: 是否支持亮度同步
        :param image_config: 图像设置配置yaml文件内容
        :return:
        """
        try:
            # 定义图像设置通用文案
            common_image_setting_texts = ['亮度', '对比度', '饱和度', '锐度', '0', '255']
            common_options = ['亮度', '对比度', '饱和度', '锐度']
            # 抗闪烁通用文案
            common_anti_flicker_texts = ['调整摄像机的拍摄帧率，以减少受到画面中光源闪烁的影响。']
            common_anti_flicker_options = ['抗闪烁']
            # 夜视通透模式通用文案
            common_night_tt_vision_texts = ['优化夜视模式下的画面亮度。']
            common_night_tt_vision_options = ['夜视通透模式']
            # HDR通用文案
            common_hdr_texts = ['合成多张不同曝光的图像，展现更多细节，使画面效果更接近真实环境']
            common_hdr_options = ['HDR']
            # 亮度同步通用文案
            common_brightness_sync_texts = ['同步调节左右摄像机，避免画面亮度相差过大']
            common_brightness_sync_options = ['亮度同步']

            if anti_flicker:
                # 图像设置通用文案拼接抗闪烁文案
                new_image_setting_texts = common_image_setting_texts + common_anti_flicker_texts
                new_image_setting_options = common_options + common_anti_flicker_options

            if night_tt_vision:
                # 图像设置通用文案拼接夜视通透模式文案
                new_image_setting_texts = new_image_setting_texts + common_night_tt_vision_texts
                new_image_setting_options = new_image_setting_options + common_night_tt_vision_options

            if hdr:
                # 图像设置通用文案拼接HDR文案
                new_image_setting_texts = new_image_setting_texts + common_hdr_texts
                new_image_setting_options = new_image_setting_options + common_hdr_options

            if brightness_sync:
                # 图像设置通用文案拼接亮度同步文案
                new_image_setting_texts = new_image_setting_texts + common_brightness_sync_texts
                new_image_setting_options = new_image_setting_options + common_brightness_sync_options

            if not anti_flicker and not night_tt_vision and not hdr and not brightness_sync:
                new_image_setting_texts = common_image_setting_texts
                new_image_setting_options = common_options

            # 验证全局文案
            RemoteSetting().scroll_check_funcs2(texts=new_image_setting_texts)
            # 验证ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=new_image_setting_options, selector='ReoTitle')

            if image_config['brightness']:
                # 验证亮度拖动条
                self.drag_slider_brightness()

            if image_config['contrast']:
                # 验证对比度拖动条
                self.drag_slider_contrast()

            if image_config['saturation']:
                # 验证饱和度拖动条
                self.drag_slider_saturation()

            if image_config['sharpness']:
                # 验证锐度拖动条
                self.drag_slider_sharpness()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_anti_flicker(self):
        """
        验证抗闪烁
        :return:
        """
        try:
            # 定义抗闪烁全局文案
            common_anti_flicker_texts = ['抗闪烁']
            # 定义抗闪烁ReoTitle功能项
            common_anti_flicker_options = ['50HZ', '60HZ', '其他', '关闭']
            # 拼接全局文案
            new_custom_texts = common_anti_flicker_texts + common_anti_flicker_options

            # 验证全局文案
            RemoteSetting().scroll_check_funcs2(texts=new_custom_texts,
                                                scroll_or_not=False,
                                                back2top=False)
            # 验证ReoTitle功能项
            RemoteSetting().scroll_check_funcs2(texts=common_anti_flicker_options,
                                                selector='ReoTitle',
                                                scroll_or_not=False,
                                                back2top=False)
            # 返回上一级
            self.back_previous_page_by_xpath()

            # 遍历popup操作项
            self.iterate_and_click_popup_text(option_text_list=common_anti_flicker_options,
                                              menu_text='抗闪烁')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def day_night_switchover(self, slider_mode='obj'):
        """
        日夜切换阈值
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :return:
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Brightness"]',
                target_id="RNE__Slider_Thumb")

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 点击恢复默认值
            self.scroll_and_click_by_text(text_to_find='恢复默认值')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_mode_switch(self, texts1, texts2):
        """
        验证模式切换
        :return:
        """
        try:
            # 点击进入【白天和黑夜】主页
            self.click_day_and_night()

            # 点击进入 模式切换
            self.scroll_and_click_by_text(text_to_find='模式切换')

            # 点击 自动 模式
            self.scroll_and_click_by_text(text_to_find='自动')
            time.sleep(3)

            # 验证功能文案
            RemoteSetting().scroll_check_funcs2(texts=texts1, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=texts2, selector='ReoTitle', back2top=False)

            # 拖动日夜切换阈值的拖动条
            self.day_night_switchover()

            # 点击 黑白 模式
            self.scroll_and_click_by_text(text_to_find='黑白')
            time.sleep(3)

            # 点击 彩色 模式
            self.scroll_and_click_by_text(text_to_find='彩色')
            time.sleep(3)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def drag_brightness_darkness_slider(self, slider_mode='obj'):
        """
        亮度、暗部调节
        :return:
        """
        try:
            # 亮度的拖动条对象
            brightness_element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Brightness"]',
                target_id="RNE__Slider_Thumb")

            # 暗部调节的拖动条对象
            dark_element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="Shadows"]',
                target_id="RNE__Slider_Thumb")
            num = 1
            for i in (brightness_element_obj, dark_element_obj):
                # 往右拖动
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=i,
                                     direction='right',
                                     iteration=5)

                # 往左拖动
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=i,
                                     direction='left',
                                     iteration=10)

                # 点击恢复默认值
                self.scroll_and_click_by_text(text_to_find=f'(//*[@text="恢复默认值"]){[num]}', el_type='xpath')
                num += 1

            time.sleep(1)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_day_color(self, texts1, texts2):
        """
        验证白天彩色
        """
        try:
            # 点击进入【白天和黑夜】主页
            self.click_day_and_night()

            # 点击进入 白天彩色
            self.scroll_and_click_by_text(text_to_find='白天彩色')

            # 点击 手动 模式
            self.scroll_and_click_by_text(text_to_find='手动')
            time.sleep(1)

            # 验证功能文案
            RemoteSetting().scroll_check_funcs2(texts=texts1, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=texts2, selector='ReoTitle', back2top=False)

            # 拖动亮度、暗部的拖动条
            self.drag_brightness_darkness_slider()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_black_and_white(self, texts1, texts2):
        """验证黑白"""
        try:
            # 点击进入【白天和黑夜】主页
            self.click_day_and_night()

            # 点击进入 黑白
            self.scroll_and_click_by_text(text_to_find='黑白')

            # 点击 手动 模式
            self.scroll_and_click_by_text(text_to_find='手动')
            time.sleep(1)

            # 验证功能文案
            RemoteSetting().scroll_check_funcs2(texts=texts1, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=texts2, selector='ReoTitle', back2top=False)

            # 拖动亮度、暗部的拖动条
            self.drag_brightness_darkness_slider()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_night_vision_color(self, texts1, texts2):
        """验证夜视彩色"""
        try:
            # 点击进入【白天和黑夜】主页
            self.click_day_and_night()

            # 点击进入 夜视彩色
            self.scroll_and_click_by_text(text_to_find='夜视彩色')

            # 点击 手动 模式
            self.scroll_and_click_by_text(text_to_find='手动')
            time.sleep(1)

            # 验证功能文案
            RemoteSetting().scroll_check_funcs2(texts=texts1, back2top=False)
            RemoteSetting().scroll_check_funcs2(texts=texts2, selector='ReoTitle', back2top=False)

            # 拖动亮度、暗部的拖动条
            self.drag_brightness_darkness_slider()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_anti_flicker(self, option_text='抗闪烁'):
        """
        :param option_text: 菜单功能项，该方法默认点击【抗闪烁】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def verify_device_name(self):
        """
        验证设备名称
        :param device_name_list_text: 设备名称配置页的所有文案
        :param device_name_options:  设备名称配置页的选项文案
        :return:
        """
        try:
            # 先将预览视图往上拉至最小,以便于滚动查找设备名称菜单
            self.need_pull_down()

            # 先获取日期菜单项的ReoValue值
            target_element = self.find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="TimeOSD-ReoCell-Navigator"]',
                target_id="ReoValue")
            target_date_value = target_element.info.get('text')
            logger.info(f'当前日期OSD位置为：{target_date_value}')

            # 进入设备名称配置页，点击ReoValue值
            self.scroll_and_click_by_text(text_to_find='设备名称')

            # 验证设备名称配置页文案
            RemoteSetting().scroll_check_funcs2(texts=display_device_name_texts, back2top=False)

            # 将列表display_device_name_reotitle赋值给新的列表
            display_device_name_reotitle02 = copy.deepcopy(display_device_name_reotitle)

            # 验证设备名称配置页的选项文案
            RemoteSetting().scroll_check_funcs2(texts=display_device_name_reotitle, selector='ReoTitle', back2top=False)

            # 点击已经被选中的选项，验证点击无效，停留在当前设备名称配置页,若为隐藏，则无需验证置灰，且不点击【隐藏】选项
            if target_date_value != '隐藏':
                self.scroll_and_click_by_text(text_to_find=target_date_value)

            # 获取当前页面标题文本，验证osd冲突的情况下应置灰指定选项
            element = self.get_element_info(xpath_exp='//*[@resource-id="HeaderTitle"]')
            current_page_title = element.info.get('text')
            if current_page_title != '设备名称':
                pytest.fail('日期OSD位置与设备名称OSD位置冲突，但日期配置页未置灰指定选项！或置灰选项可选！')
            elif target_date_value == '隐藏':
                logger.info('日期OSD位置为隐藏，设备名称配置页无需置灰指定选项！')
            else:
                logger.info(f'设备名称配置页已置灰指定【{target_date_value}】选项')

            # 返回上一页
            self.back_previous_page_by_xpath()
            # 将上述的【target_device_name_value】从date_options列表中剔除
            if target_date_value != '隐藏':
                display_device_name_reotitle02.remove(target_date_value)
            logger.info(f'新的设备名称操作列表为：{display_device_name_reotitle02}')

            # 开始遍历验证除了置灰选项外的日期选项
            self.iterate_and_click_popup_text(option_text_list=display_device_name_reotitle02,
                                              menu_text='设备名称')

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_date(self):
        """
        验证日期
        :param date_list_text: 日期配置页的所有文案
        :param date_options: 日期配置页的选项文案
        :return:
        """
        try:
            # 先将预览视图往上拉至最小,以便于滚动查找日期菜单
            self.need_pull_down()

            # 先获取设备名称菜单项的ReoValue值
            target_element = self.find_element_by_xpath_recursively(
                start_xpath_prefix='//*[@resource-id="ChannelNameOSD-ReoCell-Navigator"]',
                target_id="ReoValue")
            target_device_name_value = target_element.info.get('text')
            logger.info(f'当前设备名称OSD位置为：{target_device_name_value}')

            # 进入日期配置页，点击ReoValue值
            self.scroll_and_click_by_text(text_to_find='日期')

            # 验证日期配置页文案
            RemoteSetting().scroll_check_funcs2(texts=display_date_texts, back2top=False)

            # 将列表display_date_reotitle赋值给新的列表
            display_date_reotitle02 = copy.deepcopy(display_date_reotitle)

            # 验证日期配置页的选项文案
            RemoteSetting().scroll_check_funcs2(texts=display_date_reotitle, selector='ReoTitle', back2top=False)

            # 点击已经被选中的选项，验证点击无效，停留在当前日期配置页,若为隐藏，则无需验证置灰，且不点击【隐藏】选项
            if target_device_name_value != '隐藏':
                self.scroll_and_click_by_text(text_to_find=target_device_name_value)

            # 获取当前页面标题文本，验证osd冲突的情况下应置灰指定选项
            element = self.get_element_info(xpath_exp='//*[@resource-id="HeaderTitle"]')
            current_page_title = element.info.get('text')
            if current_page_title != '日期':
                pytest.fail('设备名称OSD位置与日期OSD位置冲突，但日期配置页未置灰指定选项！或置灰选项可选！')
            elif target_device_name_value == '隐藏':
                logger.info('当前设备名称OSD位置为隐藏，日期配置页无需置灰指定选项！')
            else:
                logger.info(f'日期配置页已置灰指定【{target_device_name_value}】选项')

            # 返回上一页
            self.back_previous_page_by_xpath()
            # 将上述的【target_device_name_value】从date_options列表中剔除
            if target_device_name_value != '隐藏':
                display_date_reotitle02.remove(target_device_name_value)
            logger.info(f'新的日期操作列表为：{display_date_reotitle02}')

            # 开始遍历验证除了置灰选项外的日期选项
            self.iterate_and_click_popup_text(option_text_list=display_date_reotitle02,
                                              menu_text='日期')

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def click_water_mark(self):
        """验证水印"""
        try:
            # 点击两次
            for i in range(2):
                self.scroll_click_right_btn(text_to_find='水印',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup'
                                            )
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_auto_zoom(self):
        """验证自动对焦"""
        try:
            # 定义自动对焦全局文案
            # 点击两次
            for i in range(2):
                self.scroll_click_right_btn(text_to_find='自动对焦',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup'
                                            )
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def access_in_privacy_mask(self, option_text='遮盖区域'):
        """
        :param option_text: 菜单功能项，该方法默认点击【遮盖区域】，并检测是否弹出了提示，弹出则分别点击【取消】、【清空并继续】，清空后最后点击【保存】
        :return:
        """
        try:
            texts = ['取消', '清空并继续']
            xpaths = [
                '//*[@resource-id="CancelDialog-ReoButton-Title"]',
                '//*[@resource-id="ConfirmDialog-ReoButton-Title"]'
            ]

            time.sleep(2)
            self.scroll_and_click_by_text(text_to_find=option_text)

            # 判断是否弹出特定提示
            is_confirmation_prompt_shown = self.is_element_exists(
                element_value='编辑画面遮盖，将会清空之前所有的遮盖区域，是否继续？')

            if is_confirmation_prompt_shown:
                for index, text in enumerate(texts):  # 使用enumerate来同时获取索引和元素值
                    logger.info(f'弹出了遮盖区域提示，正在尝试点击【{text}】.')
                    self.click_by_xpath(xpath_expression=xpaths[index])
                    logger.info(f'已点击【{text}】')

                    if text == '取消':
                        logger.info('点击了【取消】，准备再次点击【遮盖区域】.')
                        self.scroll_and_click_by_text(text_to_find=option_text)

            else:
                logger.info('该设备没有设置任何遮盖区域，未弹出清空弹窗')

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")
            # 可以抛出更通用的异常或者进行更详细的包装，这里简单打印详细错误信息后重新抛出异常
            # logger.error(f"函数执行出错: {err}", exc_info=True)
            # raise  # 抛出异常让调用者决定如何处理，如果是在pytest中，调用者可以根据需要进行相应的测试失败处理等操作

    def verify_user_tips(self, user_tips_text):
        """验证用户提示"""
        try:
            # 点击左下角用户提示按钮
            logger.info('点击左下角用户提示按钮')
            self.click_by_xpath(xpath_expression=self.user_tips_button)
            # 验证用户提示文案
            RemoteSetting().scroll_check_funcs2(texts=user_tips_text,
                                                scroll_or_not=False,
                                                back2top=False
                                                )
            # 验证完毕之后点击我知道了，关闭用户提示
            self.click_by_text(text='我知道了')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_delete_button(self):
        """验证删除按钮"""
        try:
            # 先在预览区画一个遮盖区域
            logger.info('正在预览区左上角画一个遮盖区域')
            self.get_coordinates_and_draw(mode='id',
                                          id_or_xpath=self.shelter_player,
                                          draw_area='左上',
                                          num=1
                                          )
            # 点击删除按钮
            time.sleep(1)
            logger.info('点击删除按钮')
            self.click_by_xpath(xpath_expression=self.delete_button)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_clear_all_button(self):
        """验证清空所有按钮"""
        try:
            # 先在预览区画两个遮盖区域
            logger.info('正在预览区左上角画2个遮盖区域')
            self.get_coordinates_and_draw(mode='id',
                                          id_or_xpath=self.shelter_player,
                                          num=2
                                          )
            # 点击清空所有按钮
            time.sleep(1)
            logger.info('点击清空所有按钮')
            self.click_by_xpath(xpath_expression=self.clear_all_button)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_landscape_button(self):
        """验证横屏按钮"""
        try:
            # 点击横屏按钮
            self.click_by_xpath(xpath_expression=self.fullscreen_switch_button)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_return_vertical_screen_button(self):
        """验证横屏状态下返回竖屏按钮"""
        try:
            # 点击返回竖屏按钮
            self.click_by_xpath(xpath_expression=self.return_vertical_screen_button)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def draw_privacy_mask(self, camera_type, mask_num, mode='xpath', draw_area='左上'):
        """
        画隐私遮盖区域。一般来说：电源最多4个，电池最多8个或者3个。如果是双目，则每个通道独立计数。
        :param camera_type: 摄像头类型，支持DM、GC、ZY三种类型。
        :param mask_num: 某个画面/通道最多可绘制的遮罩数量。
        :param mode: 预览区域的定位方式，支持id或者xpath。当前默认xpath
        :param id_or_xpath: 可遮盖区域的id或者xpath的定位参数。
        :param draw_area: 需要遮盖的区域，支持[左上]、[左下]、[右上]、[右下]的1/4屏，以及[全屏]遮盖，默认左上。
        :return:
        """
        try:
            # 初始化遮罩数量
            mask_nums = mask_num + 1

            # 定义不同摄像头类型对应的操作序列
            camera_actions = {
                'DM': [],  # DM摄像头不需要额外操作
                'GC': ['广角画面', '长焦画面'],  # GC摄像头需要先点击广角，再点击长焦
                'ZY': ['左摄像机', '右摄像机']  # ZY摄像头需要先点击左摄像机，再点击右摄像机
            }

            # 获取指定摄像头类型的操作列表
            actions = camera_actions.get(camera_type, [])

            # 遍历操作列表，执行点击和绘制操作
            for action in actions:
                # 如果操作不为空，执行点击操作
                if action:
                    self.click_by_text(action)
                # 执行绘制隐私遮罩的操作
                self.get_coordinates_and_draw(mode=mode,
                                              id_or_xpath=self.shelter_player,
                                              draw_area=draw_area,
                                              num=mask_nums)

        except Exception as err:
            # 记录错误信息
            pytest.fail(f"绘制隐私遮盖函数执行出错: {err}")

    def verify_privacy_mask(self, camera_type, mask_num):
        """
        验证隐私遮盖
        :param camera_type: 传入摄像头画面类型，GC代表双目的广角与长焦；ZY代表左右摄像机；DM代表单目
        :param mask_num: 传入可遮盖区域的数量，整数
        """
        try:
            # 单目通用全局文案
            DM_texts = ['取消', '遮盖区域', '保存', '清空所有']
            # 广角与长焦通用全局文案
            GC_texts = ['取消', '遮盖区域', '保存', '清空所有', '广角画面', '长焦画面']
            # 左右摄像机通用全局文案
            ZY_texts = ['取消', '遮盖区域', '保存', '清空所有', '左摄像机', '右摄像机']
            # 左下角用户提示
            user_tips = [
                f'在画面中通过手指滑动添加黑色遮挡区域，监控视频中的遮挡区域将不可见，最多可遮挡{mask_num}个区域。',
                '我知道了']

            if camera_type == 'DM':
                # 验证隐私遮盖主页通用文本
                RemoteSetting().scroll_check_funcs2(DM_texts, back2top=False)
            elif camera_type == 'GC':
                # 验证隐私遮盖主页通用文本
                RemoteSetting().scroll_check_funcs2(GC_texts, back2top=False)
            elif camera_type == 'ZY':
                # 验证隐私遮盖主页通用文本
                RemoteSetting().scroll_check_funcs2(ZY_texts, back2top=False)

            # 验证左下角用户提示
            self.verify_user_tips(user_tips_text=user_tips)

            # 验证删除按钮
            self.verify_delete_button()

            # 验证清空所有按钮
            self.verify_clear_all_button()

            # 验证横屏按钮
            self.verify_landscape_button()

            # 验证返回竖屏按钮
            self.verify_return_vertical_screen_button()

            # 绘制隐私遮罩
            self.draw_privacy_mask(camera_type=camera_type, mask_num=mask_num)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_image_layout(self):
        """
        点击进入并验证图像布局
        :return:
        """
        try:
            # 图像布局主页文案
            image_layout_texts = ['取消', '图像布局', '保存', '鱼眼', '展开']
            choose_button = ['取消', '保存']
            choose_button_tips = ['注意：', '取消',
                                  '切换后，摄像机将会重启，并且会清除隐私区域、报警区域、目标尺寸等配置，确定要切换吗？',
                                  '保存']

            def check_choose_button_tips():
                for c in choose_button:
                    self.scroll_and_click_by_text(text_to_find='保存')
                    RemoteSetting().scroll_check_funcs2(texts=choose_button_tips,
                                                        scroll_or_not=False,
                                                        back2top=False)
                    self.click_by_text(text=c)

                    if c == '保存':
                        logger.info('等待30秒，等待摄像机重启.验证返回设备列表页')
                        RemoteSetting().scroll_check_funcs2(texts='设备即将重启，稍后将返回设备列表',
                                                            scroll_or_not=False,
                                                            back2top=False)
                        time.sleep(30)

                        # 验证点击保存重启后的页面返回到设备列表
                        if not self.is_element_exists(element_value='摄像机', scroll_or_not=False):
                            pytest.fail('未能成功返回设备列表页！')

            # 先将预览视图往上拉至最小,以便于滚动查找图像布局按钮
            self.need_pull_down()

            # 先找到图像布局菜单项
            self.is_element_exists(element_value='图像布局')
            # 再查出当前的图像布局类型是否为鱼眼
            current_layout = self.is_element_exists(element_value='鱼眼')
            if current_layout:
                logger.info(f'当前布局为【鱼眼】，切换【展开】布局类型')
                # 滚动查找图像布局按钮
                self.scroll_and_click_by_text(text_to_find='图像布局')
                time.sleep(1)
                # 验证图像布局主页文案
                RemoteSetting().scroll_check_funcs2(texts=image_layout_texts, back2top=False)
                # 点击【展开】模式
                self.click_by_xpath(xpath_expression=self.layout_expand_button)

            else:
                # 滚动查找图像布局按钮
                self.scroll_and_click_by_text(text_to_find='图像布局')
                time.sleep(1)
                logger.info(f'当前布局为【展开】，切换【鱼眼】布局类型')
                # 验证图像布局主页文案
                RemoteSetting().scroll_check_funcs2(texts=image_layout_texts, back2top=False)
                # 点击【鱼眼】模式
                self.click_by_xpath(xpath_expression=self.layout_fisheye_button)

            # 验证弹窗提示内容和按钮选项
            check_choose_button_tips()
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def set_image_layout_type(self, layout_type, device_list_name):
        """
        设置图像布局类型
        :param layout_type: 需要设置的图像布局类型，支持【展开】和【鱼眼】两种类型。
        :param device_list_name: 设备重启后需要从设备列表重新进入远程配置，重新进入显示页面。
        :return:
        """
        try:
            def click_layout_button(set_layout_type):
                # 点击指定布局类型按钮
                if layout_type == '展开':
                    logger.info(f'当前布局为【鱼眼】，切换【展开】布局类型')
                    self.click_by_xpath(xpath_expression=self.layout_expand_button)
                elif layout_type == '鱼眼':
                    logger.info(f'当前布局为【展开】，切换【鱼眼】布局类型')
                    self.click_by_xpath(xpath_expression=self.layout_fisheye_button)
                # 点击保存
                self.click_by_text(text='保存')
                # 点击提示的保存
                self.click_by_text(text='保存')

            # 先将预览视图往上拉至最小,以便于滚动查找图像布局按钮
            # self.drag_element(element_xpath='//com.horcrux.svg.SvgView', direction='up', distance=700, duration=1)
            self.need_pull_down()

            # 先找到图像布局菜单项
            self.is_element_exists(element_value='图像布局')

            # 再查出当前的图像布局类型是否为指定的类型
            current_layout = self.is_element_exists(element_value=layout_type)
            if current_layout:
                logger.info(f'当前布局已经是【{layout_type}】布局类型，无需切换！')
            else:
                # 设置成指定的布局类型
                self.scroll_and_click_by_text(text_to_find='图像布局')
                time.sleep(1)
                # 点击指定布局类型按钮
                click_layout_button(set_layout_type=layout_type)
                logger.info('等待30秒，等待摄像机重启后执行显示模式的测试用例')
                time.sleep(30)
                # 进入远程配置>显示>显示模式
                RemoteSetting().access_in_display(device_list_name=device_list_name)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def check_echo(self):
        """
        验证显示方式的回显
        :return:
        """
        try:
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 验证回显的安装方式是否正确
            RemoteSetting().scroll_check_funcs2(texts='壁挂',
                                                scroll_or_not=False,
                                                back2top=False)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_display_mode_and_rotating_picture(self):
        """
        点击进入并验证显示模式,并旋转画面
        :param mode: 显示模式类型，支持【桌面】【吸顶】【壁挂】3种类型。
        :return:
        """
        try:
            # 先将预览视图往上拉至最小,以便于滚动查找显示模式按钮
            self.need_pull_down()

            # 再找到并点击显示模式菜单项
            self.scroll_and_click_by_text(text_to_find='显示模式')
            # 进入显示模式配置页后，不拖动预览窗口（拖动之后预览窗部分画面被遮挡，可能影响录屏回放后的查看验证）
            # 遍历安装方式
            # 定义显示模式与对应的XPath映射
            display_modes = {
                '桌面': self.display_mode_type_FLOOR,
                '吸顶': self.display_mode_type_TOP,
                '壁挂': self.display_mode_type_WALL
            }

            # 遍历并点击每种显示模式
            for mode_name, xpath in display_modes.items():
                logger.info(f'点击【{mode_name}】模式')
                self.click_by_xpath(xpath_expression=xpath)
                logger.info('等待3秒，录屏预览区域变化')
                time.sleep(3)

            # 旋转画面: 向右
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath='//*[@resource-id="RNE__Slider_Thumb"]',
                                 direction='right',
                                 iteration=5)
            # 旋转画面: 向左
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath='//*[@resource-id="RNE__Slider_Thumb"]',
                                 direction='left',
                                 iteration=10)
            # 旋转画面: 向右
            self.slider_seek_bar(slider_mode='xpath',
                                 id_or_xpath='//*[@resource-id="RNE__Slider_Thumb"]',
                                 direction='right',
                                 iteration=5)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_scenes(self):
        """
        遍历切换室内外场景
        :param scenes_list: 需要遍历的场景配置页文案列表
        :param options: 需要点击和验证的选项列表
        :return:
        """
        try:
            # 定义场景配置页全局文案列表
            common_scenes_texts = ['场景', '室内', '室外']
            # 定义场景配置ReoTitle选项列表
            common_scenes_options = ['室内', '室外']

            # 先将预览视图往上拉至最小,以便于滚动查找显示模式按钮
            self.need_pull_down()

            # 先点击场景菜单进入配置页，验证配置页文案和选项
            self.scroll_and_click_by_text('场景')
            RemoteSetting().scroll_check_funcs2(texts=common_scenes_texts,
                                                scroll_or_not=False,
                                                back2top=False)

            RemoteSetting().scroll_check_funcs2(texts=common_scenes_options,
                                                selector='ReoTitle',
                                                scroll_or_not=False,
                                                back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 遍历切换场景
            self.iterate_and_click_popup_text(option_text_list=common_scenes_options,
                                              menu_text='场景')

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_night_transparent_vision(self):
        """
        验证夜视通透功能
        :return:
        """
        try:
            if self.is_element_exists(element_value='夜视通透模式', max_scrolls=3):
                self.scroll_click_right_btn(text_to_find='夜视通透模式',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
                time.sleep(3)
                self.scroll_click_right_btn(text_to_find='夜视通透模式',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')
            else:
                pytest.fail('当前设备未找到夜视通透功能！')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_splice_region(self):
        """
        验证拼接区域
        :return:
        """
        # 拼接区域的全局文案
        splice_region_texts = ['拼接距离', '距离（米）', '在你设置的距离附近，拼接画面会达到最佳观看效果', '拼接位置',
                               '水平', '垂直', '调整左右两个画面之间的水平或垂直距离差，以达到最佳观看效果',
                               '恢复默认设置']

        def verify_texts(scroll_or_not=False, back2top=False):
            """封装验证文案的函数"""
            RemoteSetting().scroll_check_funcs2(texts=splice_region_texts,
                                                scroll_or_not=scroll_or_not,
                                                back2top=back2top)

        try:

            self.scroll_and_click_by_text('拼接区域')
            time.sleep(3)
            verify_texts()

            # 点击横屏按钮
            self.click_by_xpath('//*[@text=""]')
            # 再次验证横屏后文案
            verify_texts()

            # 返回上一页
            self.back_previous_page_by_xpath()

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_main_texts(self, custom_texts, custom_options):
        """
        验证码流主页面文案
        :param custom_texts: 需要验证的码流主页全局文案
        :param custom_options: 需要验证的码流主页ReoTitle文案
        :return:
        """
        try:
            # 定义码流主页通用文案
            common_stream_main_texts = ['码流', '清晰', '分辨率', '帧率(FPS)', '最大码率(Kbps)', '流畅']
            new_stream_main_texts = common_stream_main_texts + custom_texts + custom_options
            new_stream_main_options = ['清晰', '流畅'] + custom_options
            # 检查码流主页全局文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_main_texts, scroll_or_not=False, back2top=False)
            # 检查码流主页ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_main_options, selector='ReoTitle',
                                                scroll_or_not=False, back2top=False)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_main_texts(self, custom_options):
        """
        码流>清晰页面，验证清晰页面文本和操作
        :param custom_options: 需要验证的码流清晰页面ReoTitle文案
        :return:
        """
        try:
            # 定义清晰主页通用文案
            common_stream_clear_options = ['分辨率', '帧率(FPS)', '最大码率(Kbps)']
            common_stream_clear_texts = ['取消', '清晰', '保存', '分辨率', '帧率(FPS)', '最大码率(Kbps)']
            new_stream_clear_texts = common_stream_clear_texts + custom_options  # 拼接清晰页面全局文案
            new_stream_clear_options = common_stream_clear_options + custom_options  # 拼接清晰页面ReoTitle文案
            # 检查清晰主页全局文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_texts, scroll_or_not=False, back2top=False)
            # 检查清晰主页ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_options, selector='ReoTitle',
                                                scroll_or_not=False, back2top=False)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_fluent_main_texts(self, custom_options):
        """
        码流>流畅页面，验证流畅页面文本和操作
        :param custom_options:
        :return:
        """
        try:
            # 定义流畅主页通用文案
            common_stream_fluent_options = ['分辨率', '帧率(FPS)', '最大码率(Kbps)']
            common_stream_fluent_texts = ['取消', '流畅', '保存', '分辨率', '帧率(FPS)', '最大码率(Kbps)']
            new_stream_fluent_texts = common_stream_fluent_texts + custom_options  # 拼接流畅页面全局文案
            new_stream_fluent_options = common_stream_fluent_options + custom_options  # 拼接流畅页面ReoTitle文案
            # 检查流畅主页全局文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_fluent_texts, scroll_or_not=False, back2top=False)
            # 检查流畅主页ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_fluent_options, selector='ReoTitle',
                                                scroll_or_not=False, back2top=False)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_resolution(self, custom_options):
        """
        码流>清晰页面，验证分辨率操作
        :param custom_options: 需要验证的码流清晰页面ReoTitle文案
        :return:
        """
        try:
            # 定义清晰页面分辨率通用文案
            common_stream_clear_resolution_texts = ['分辨率', '越高视频越清晰']
            new_stream_clear_resolution_texts = common_stream_clear_resolution_texts + custom_options
            # 检查清晰页面分辨率文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_resolution_texts, scroll_or_not=False,
                                                back2top=False)
            # 检查清晰页面分辨率ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=custom_options, selector='ReoTitle',
                                                scroll_or_not=False, back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 开始遍历清晰>分辨率选项
            self.iterate_and_click_popup_text(option_text_list=custom_options, menu_text='分辨率')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_frame_rate(self, custom_options):
        """
        码流>清晰页面，验证帧率操作
        :param custom_options:
        :return:
        """
        try:
            # 定义清晰页面帧率通用文案
            common_stream_clear_frame_rate_texts = ['帧率(FPS)', '每秒钟的帧数，越高画面越流畅']
            new_stream_clear_frame_rate_texts = common_stream_clear_frame_rate_texts + custom_options
            # 检查清晰页面帧率文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_frame_rate_texts, scroll_or_not=False,
                                                back2top=False)
            # 检查清晰页面帧率ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=custom_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 开始遍历清晰>帧率选项
            self.iterate_and_click_popup_text(option_text_list=custom_options, menu_text='帧率(FPS)')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_max_bit_rate(self, custom_options):
        """
        码流>清晰页面，验证最大码率操作
        :param custom_options:
        :return:
        """
        try:
            # 定义清晰页面最大码率通用文案
            common_stream_clear_max_bit_rate_texts = ['最大码率(Kbps)',
                                                      '相同的分辨率、帧率下，码率越大画质越好，网络要求也越高']
            new_stream_clear_max_bit_rate_texts = common_stream_clear_max_bit_rate_texts + custom_options
            # 检查清晰页面最大码率文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_max_bit_rate_texts, scroll_or_not=False,
                                                back2top=False)
            # 检查清晰页面最大码率ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=custom_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 开始遍历清晰>最大码率选项
            self.iterate_and_click_popup_text(option_text_list=custom_options, menu_text='最大码率(Kbps)')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_encoding_format(self, custom_options):
        """
        码流>清晰/流畅页面，验证编码格式操作
        :param custom_options: 需要验证的码流清晰页面编码格式文案
        :return:
        """
        try:
            # 定义清晰/流畅页面编码格式通用文案
            common_stream_clear_encoding_format_texts = ['编码格式',
                                                         'H.265相较于H.264具有更高的编码效率，可以提供更高质量的视频，但相应地需要更高的计算能力和更先进的设备支持。']
            new_stream_clear_encoding_format_texts = common_stream_clear_encoding_format_texts + custom_options
            # 检查清晰/流畅页面编码格式文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_encoding_format_texts, scroll_or_not=False,
                                                back2top=False)
            # 检查清晰/流畅页面编码格式ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=custom_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 开始遍历清晰/流畅>编码格式选项
            self.iterate_and_click_popup_text(option_text_list=custom_options, menu_text='编码格式')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_clear_i_frame_interval(self, custom_options):
        """
        码流>清晰页面，验证I帧间隔操作
        :param custom_options:
        :return:
        """
        try:
            # 定义清晰页面I帧间隔通用文案
            common_stream_clear_i_frame_interval_texts = ['I 帧间隔',
                                                          'I帧间隔小，视频质量高，但文件大。I帧间隔大，文件小，但质量低。']
            new_stream_clear_i_frame_interval_texts = common_stream_clear_i_frame_interval_texts + custom_options
            # 检查清晰页面I帧间隔文案
            RemoteSetting().scroll_check_funcs2(texts=new_stream_clear_i_frame_interval_texts, scroll_or_not=False,
                                                back2top=False)
            # 检查清晰页面I帧间隔ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=custom_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)
            # 返回上一页
            self.back_previous_page_by_xpath()
            # 开始遍历清晰>I帧间隔选项
            self.iterate_and_click_popup_text(option_text_list=custom_options, menu_text='I 帧间隔')
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_frame_rate_control(self, frame_rate_mode):
        """
        码流主页，验证帧率控制
        :param frame_rate_mode: 帧率控制模式,A代表自动，B代表恒定，C代表逐步，
                                入参AB则代表支持自动和恒定，入参ABC则代表支持自动、恒定、逐步
        :return:
        """
        try:
            # 定义帧率控制页面通用文案
            common_auto_texts = ['帧率控制', '自动', '可变帧率，自动调节帧率来保持画质（不适用有快速运动的物体）。']
            common_steady_texts = ['帧率控制', '恒定', '恒定帧率，流畅优先。']
            common_step_texts = ['帧率控制', '逐步', '可变帧率，逐步调节帧率来保持画质（适用有快速运动的物体）。']
            # 定义帧率控制页面ReoTitle文案
            common_auto_options = ['自动']
            common_steady_options = ['恒定']
            common_step_options = ['逐步']

            if frame_rate_mode == 'AB':
                ab_all_texts = common_auto_texts + common_steady_texts
                ab_all_options = common_auto_options + common_steady_options
                # 检查全局文案
                RemoteSetting().scroll_check_funcs2(texts=ab_all_texts, scroll_or_not=False, back2top=False)
                # 检查ReoTitle文案
                RemoteSetting().scroll_check_funcs2(texts=ab_all_options, selector='ReoTitle', scroll_or_not=False,
                                                    back2top=False)
            elif frame_rate_mode == 'ABC':
                abc_all_texts = common_auto_texts + common_steady_texts + common_step_texts
                abc_all_options = common_auto_options + common_steady_options + common_step_options
                # 检查全局文案
                RemoteSetting().scroll_check_funcs2(texts=abc_all_texts, scroll_or_not=False, back2top=False)
                # 检查ReoTitle文案
                RemoteSetting().scroll_check_funcs2(texts=abc_all_options, selector='ReoTitle', scroll_or_not=False,
                                                    back2top=False)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_encoding_format_interval(self, clear_encoding_options, fluent_encoding_options):
        """
        码流主页>清晰/流畅，验证各自的编码格式
        :param clear_encoding_options: 清晰>编码格式文案
        :param fluent_encoding_options: 流畅>编码格式文案
        :return:
        """
        try:
            # 点击清晰，
            self.click_by_text(text='清晰')
            # 点击清晰>编码格式
            self.click_encoding_format()
            self.verify_stream_clear_encoding_format(clear_encoding_options)

            # 点击取消，返回到码流主页
            self.click_by_text('取消')

            # 点击流畅
            self.click_by_text(text='流畅')
            # 点击流畅>编码格式
            self.click_encoding_format()
            self.verify_stream_clear_encoding_format(fluent_encoding_options)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_i_frame_interval(self, clear_i_options, fluent_i_options):
        """
        码流主页，清晰/流畅，验证各自的I帧间隔
        :param clear_i_options: 清晰>I帧间隔文案
        :param fluent_i_options: 流畅>I帧间隔文案
        :return:
        """
        try:
            time.sleep(3)
            # 点击清晰，
            self.click_by_text(text='清晰')
            # 点击清晰>I 帧间隔选项，验证文本
            self.click_i_frame_interval()
            self.verify_stream_clear_i_frame_interval(clear_i_options)

            # 点击取消，返回到码流主页
            self.click_by_text('取消')

            # 点击流畅
            self.click_by_text(text='流畅')
            # 点击流畅>I 帧间隔选项，验证文本
            self.click_i_frame_interval()
            self.verify_stream_clear_i_frame_interval(fluent_i_options)

        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def verify_stream_rate_mode(self):
        """
        码流主页，验证码率控制
        :return:
        """
        try:
            # 定义码率模式页面通用文案
            common_auto_texts = ['码率控制', '固定码率',
                                 '不同的码率控制模式会影响画质和文件存储大小。',
                                 '使用固定的码率来压缩视频。在复杂度差异较大的场景下，可能会导致一些画质损失。',
                                 '动态码率', '自动根据视频内容的复杂度进行码率控制。码率不足时，视频可能会变得模糊。'
                                 ]
            # 定义码率模式页面ReoTitle文案
            common_auto_options = ['固定码率', '动态码率']

            # 验证全局文案
            RemoteSetting().scroll_check_funcs2(texts=common_auto_texts, scroll_or_not=False, back2top=False)
            # 验证ReoTitle文案
            RemoteSetting().scroll_check_funcs2(texts=common_auto_options, selector='ReoTitle', scroll_or_not=False,
                                                back2top=False)
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")
