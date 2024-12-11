# -*- coding: utf-8 -*-
import time
import pytest
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteDisplay(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.shelter_player = 'PrivacyMask_Operation_Area'  # 隐私遮盖可画框区域
            self.user_tips_button = '//*[@resource-id="ReoIcon-Question"]'  # 用户提示按钮
            self.delete_button = '//*[@resource-id="ReoIcon-Delet"]'  # 删除按钮
            self.clear_all_button = '//*[@resource-id="ReoIcon-Retry1x"]'  # 清空所有按钮
            self.fullscreen_switch_button = '//*[@resource-id="ReoIcon-Fullscreen"]'  # 全屏按钮
            self.return_vertical_screen_button = '//*[@resource-id="ReoIcon-Left"]'  # 返回竖屏按钮
            self.layout_expand_button = '//*[@resource-id="ImageLayoutExpand"]'  # 图像布局 > 展开按钮
            self.layout_fisheye_button = '//*[@resource-id="ImageLayoutOriginal"]'  # 图像布局 > 鱼眼按钮

        elif self.platform == 'ios':
            self.shelter_player = ''

    def check_display_main_text(self, texts):
        """
        验证显示主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            display_main_text_res = RemoteSetting().scroll_check_funcs2(texts=texts, selector='ReoTitle')

            return display_main_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_vertical_flip_switch_button(self):
        """
        点击垂直翻转按钮
        :return:
        """
        try:
            BasePage().scroll_click_right_btn(text_to_find='垂直翻转',
                                              resourceId_1='ReoTitle',
                                              className_2='android.view.ViewGroup'
                                              )
            return True
        except Exception as err:
            logger.info(f"可能发生了错误: {err}")
            return False

    def click_horizontal_flip_switch_button(self):
        """
        点击水平翻转按钮
        :return:
        """
        try:
            BasePage().scroll_click_right_btn(text_to_find='水平翻转',
                                              resourceId_1='ReoTitle',
                                              className_2='android.view.ViewGroup'
                                              )
            return True
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

    def click_motion_mark(self, option_text='移动标记'):
        """点击移动标记"""
        try:
            # 点击两次
            for i in range(2):
                self.scroll_click_right_btn(text_to_find=option_text,
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

    def click_encoding_format(self, option_text='编码格式'):
        """
        :param option_text: 菜单功能项，该方法默认点击【编码格式】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def click_i_frame_interval(self, option_text='i帧间隔'):
        """
        :param option_text: 菜单功能项，该方法默认点击【i帧间隔】
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
                target_id="RNE__Slider_Thumb")

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=15)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=25)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
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
                                 iteration=15)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=25)

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
                                     iteration=15)

                # 往左拖动
                self.slider_seek_bar(slider_mode=slider_mode,
                                     id_or_xpath=i,
                                     direction='left',
                                     iteration=20)

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

    def click_device_name(self, option_text='设备名称'):
        """
        :param option_text: 菜单功能项，该方法默认点击【设备名称】
        :return:
        """
        self.scroll_and_click_by_text(text_to_find=option_text)

    def verify_date(self):
        """验证日期"""
        # TODO:
        pass

    def click_water_mark(self, option_text='水印'):
        """验证水印"""
        try:
            # 点击两次
            for i in range(2):
                self.scroll_click_right_btn(text_to_find=option_text,
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
                self.click_by_text(text='保存')
            else:
                logger.info('该设备没有设置任何遮盖区域')

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

    def verify_image_layout(self, texts):
        """
        点击进入并验证图像布局
        :param texts: 预期显示的文案列表
        :return:
        """
        try:
            choose_button = ['取消', '保存']
            choose_button_tips = ['注意：', '取消', '切换后，摄像机将会重启，并且会清除隐私区域、报警区域、目标尺寸等配置，确定要切换吗？', '保存']

            def check_choose_button_tips():
                for c in choose_button:
                    self.scroll_and_click_by_text(text_to_find='保存')
                    RemoteSetting().scroll_check_funcs2(
                                                        texts=choose_button_tips,
                                                        scroll_or_not=False,
                                                        back2top=False)
                    self.click_by_text(text=c)

                    if c == '保存':
                        logger.info('等待30秒，等待摄像机重启.验证返回设备列表页')
                        RemoteSetting().scroll_check_funcs2(texts='设备即将重启，稍后将返回设备列表',
                                                            scroll_or_not=False,
                                                            back2top=False)
                        time.sleep(30)

                        # 验证重启后的页面
                        if not self.is_element_exists(element_value='摄像机', scroll_or_not=False):
                            pytest.fail('未能成功返回设备列表页！')

            # 先将预览视图往上拉至最小,以便于滚动查找图像布局按钮
            self.drag_element(element_xpath='//com.horcrux.svg.SvgView', direction='up', distance=700, duration=1)

            # 先找到图像布局菜单项
            self.is_element_exists(element_value='图像布局')
            # 再查出当前的图像布局类型是否为鱼眼
            current_layout = self.is_element_exists(element_value='鱼眼')
            if current_layout:
                # 滚动查找图像布局按钮
                self.scroll_and_click_by_text(text_to_find='图像布局')
                time.sleep(1)
                # 验证图像布局主页文案
                RemoteSetting().scroll_check_funcs2(texts=texts, back2top=False)
                logger.info(f'当前布局为【鱼眼】，切换【展开】布局类型')
                # 点击【展开】模式
                self.click_by_xpath(xpath_expression=self.layout_expand_button)

            else:
                # 滚动查找图像布局按钮
                self.scroll_and_click_by_text(text_to_find='图像布局')
                time.sleep(1)
                # 验证图像布局主页文案
                RemoteSetting().scroll_check_funcs2(texts=texts, back2top=False)
                # 点击【鱼眼】模式
                self.click_by_xpath(xpath_expression=self.layout_fisheye_button)
                logger.info(f'当前布局为【展开】，切换【鱼眼】布局类型')

            # 验证弹窗提示内容和按钮选项
            check_choose_button_tips()
        except Exception as err:
            pytest.fail(f"函数执行出错: {err}")

    def draw_privacy_mask(self, mode=id, draw_area='左上'):
        """
        画隐私遮盖区域。一般来说：电源最多4个，电池最多8个或者3个。如果是双目，则每个通道独立计数。
        :param mode: 预览区域的定位方式，支持id或者xpath。当前默认id
        :param id_or_xpath: 可遮盖区域的id或者xpath的定位参数。
        :param draw_area: 需要遮盖的区域，支持[左上]、[左下]、[右上]、[右下]的1/4屏，以及[全屏]遮盖，默认左上。
        :param num: 画框数量，默认为0，为0时需要指定遮盖区域draw_area，若不指定，则默认左上遮盖。
        :return:
        """
        # TODO:适配RN
        try:
            # 暂时没法直接区分电源电池，所以，干脆画满
            if not self.is_element_exists(element_value='广角画面') and not self.is_element_exists(
                    element_value='左摄像机'):
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=9)

            if self.is_element_exists(element_value='广角画面'):
                self.click_by_text('广角画面')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

            if self.is_element_exists(element_value='长焦画面'):
                self.click_by_text('长焦画面')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

            if self.is_element_exists(element_value='左摄像机'):
                self.click_by_text('左摄像机')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

            if self.is_element_exists(element_value='右摄像机'):
                self.click_by_text('右摄像机')
                self.get_coordinates_and_draw(mode=mode, id_or_xpath=self.shelter_player, draw_area=draw_area, num=5)

        except Exception as err:
            logger.info(f"可能发生了错误: {err}")
            return False

    def indoor_and_outdoor_scenes(self):
        """场景"""
        # TODO:
        pass
