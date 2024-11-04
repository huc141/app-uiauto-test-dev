# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteFtp(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def check_ftp_main_text(self, texts):
        """
        验证邮件通知主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            email_alerts_main_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            return email_alerts_main_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def set_ftp_port(self):
        """
        设置端口
        :return:
        """
        try:
            # 点击清空图标
            self.scroll_and_click_by_text(text_to_find='//android.widget.TextView[@text=""]',
                                          el_type='xpath')
            # 输入端口
            self.scroll_click_right_btn(text_to_find='端口',
                                        className_1='android.widget.TextView',
                                        className_2='android.widget.EditText')
            self.input_text(xpath_exp='', text='21')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def set_transmission_mode(self, trms_text, trm_opt_text):
        """
        设置传输模式
        :param trms_text: 传输模式主页文案
        :param trm_opt_text: 传输模式主页操作选项
        :return:
        """
        try:
            trms_text_res = RemoteSetting().scroll_check_funcs2(texts=trms_text)
            self.iterate_and_click_popup_text(option_text_list=trm_opt_text, menu_text='传输模式')
            if not trms_text_res:
                pytest.fail(f"传输模式主页文案 缺失！")
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_ftp_on(self):
        """
        判断FTP按钮开关状态：
            ①如果为关，则点击打开，打开后配置FTP并保存；
            ②如果为开，则进行下一层判断：
                1.如果是缺省状态，则点击【现在设置】按钮，配置FTP并保存；
                2.如果是已配置状态，则不做其他操作。
        :return:
        """
        try:
            ftp_default_res = True
            alert_info_res = True
            ftp_default_list = ['FTP', '未完成FTP功能配置将无法正常使用此功能。', '现在设置']
            alert_info = ['在FTP服务中，数据将以未加密形式传输，建议您在家庭和工作网络而非公共网络上启用此功能。或开启此设备FTPS加密选项，并同时开启FTP服务器的FTPS选项，以保障数据的传输安全。确认开启？']
            # 如果是关：
            if (not RemoteSetting().scroll_check_funcs2(texts='测试', scroll_or_not=False) and
                    not RemoteSetting().scroll_check_funcs2(texts='现在设置', scroll_or_not=False)):

                self.scroll_click_right_btn(text_to_find='FTP',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')  # 点击FTP
                alert_info_res = RemoteSetting().scroll_check_funcs2(texts=alert_info, scroll_or_not=False)
                self.loop_detect_element_and_click(element_value='取消', scroll_or_not=False)  # 点击取消
                time.sleep(0.5)
                self.scroll_click_right_btn(text_to_find='FTP',
                                            resourceId_1='ReoTitle',
                                            className_2='android.view.ViewGroup')  # 点击FTP
                self.loop_detect_element_and_click(element_value='确定', scroll_or_not=False)  # 点击确定

            # 如果是开-缺省状态：
            if RemoteSetting().scroll_check_funcs2(texts='现在设置', scroll_or_not=False):
                ftp_default_res = RemoteSetting().scroll_check_funcs2(texts=ftp_default_list, scroll_or_not=False)

            return ftp_default_res, alert_info_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_transmission_mode(self, transmission_mode_text, transmission_mode_option_text):
        """
        点击并遍历传输模式
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=transmission_mode_text)
            # 遍历传输模式选项
            self.iterate_and_click_popup_text(option_text_list=transmission_mode_option_text, menu_text='传输模式')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_generate_subdirectories(self, generate_subdirectories_text, generate_subdirectories_option_text):
        """
        点击并遍历生成子目录
        :param generate_subdirectories_text:
        :param generate_subdirectories_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=generate_subdirectories_text)
            # 遍历生成子目录选项
            self.iterate_and_click_popup_text(option_text_list=generate_subdirectories_option_text, menu_text='生成子目录')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_upload(self, upload_text, upload_option_text):
        """
        遍历上传内容
        :param upload_text:
        :param upload_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=upload_text)
            # 遍历上传内容选项
            self.iterate_and_click_popup_text(option_text_list=upload_option_text, menu_text='上传内容')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_video_resolution(self, video_resolution_text, video_resolution_option_text):
        """
        TODO:遍历视频-分辨率
        :param video_resolution_text:
        :param video_resolution_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=video_resolution_text)
            # 遍历视频-分辨率选项
            self.iterate_and_click_popup_text(option_text_list=video_resolution_option_text, menu_text='分辨率', el_type='xpath')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_FTP_recording_extension(self, FTP_recording_extension_text, FTP_recording_extension_option_text):
        """
        点击并遍历FTP录像时长
        :param FTP_recording_extension_text:
        :param FTP_recording_extension_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=FTP_recording_extension_text)
            # 遍历FTP录像时长选项
            self.iterate_and_click_popup_text(option_text_list=FTP_recording_extension_option_text, menu_text='FTP录像时长')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_maximum_video_size(self, maximum_video_size_text, maximum_video_size_option_text):
        """
        点击并遍历文件最大容量
        :param maximum_video_size_text:
        :param maximum_video_size_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=maximum_video_size_text)
            # 遍历FTP录像时长选项
            self.iterate_and_click_popup_text(option_text_list=maximum_video_size_option_text, menu_text='文件最大容量(MB)')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_picture_interval(self, picture_interval_text, picture_interval_option_text):
        """
        点击并遍历间隔
        :param picture_interval_text:
        :param picture_interval_option_text:
        :return:
        """
        try:
            # 检查文案
            text_status = RemoteSetting().scroll_check_funcs2(texts=picture_interval_text)
            # 遍历间隔选项
            self.iterate_and_click_popup_text(option_text_list=picture_interval_option_text, menu_text='间隔')
            return text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def temp_check_ftp_text(self, ftp_config_text):
        """
        验证FTP设置页面的文案，临时方法，待RN出包后重新修改
        :return:
        """
        try:
            self.is_ftp_on()

            self.scroll_and_click_by_text(text_to_find='现在设置')

            # 验证文案
            RemoteSetting().scroll_check_funcs2(texts=ftp_config_text)

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def set_ftp_config(self, text_list, trms_text, trm_opt_text):
        """
        TODO: ftp设置
        :param text_list: FTP设置页面的文案列表
        :param trms_text: 传输模式主页文案
        :param trm_opt_text: 传输模式主页操作选项
        :return:
        """
        try:
            text_to_find_list = ['服务器地址*', '用户名*', '密码', '远程目录']
            text_to_input = ['111.222.333.444', 'autoUserTest', '123456789', '/user/test']
            count = 0

            # 匿名传输
            for i in range(1, 2):
                self.scroll_click_right_btn(text_to_find='匿名传输',
                                            className_1='android.widget.TextView',
                                            className_2='android.view.ViewGroup')

            # 不允许未加密的FTP明文传输
            if '不允许未加密的FTP明文传输' in text_list:
                for i in range(1, 2):
                    self.scroll_click_right_btn(text_to_find='不允许未加密的FTP明文传输',
                                                className_1='android.widget.TextView',
                                                className_2='android.view.ViewGroup')

            # 设置服务器地址、用户名/密码、远程目录
            for i in text_to_find_list:
                self.scroll_click_right_btn(text_to_find=i,
                                            className_1='android.widget.TextView',
                                            className_2='android.widget.EditText')
                self.input_text(xpath_exp='', text=text_to_input[count])
                count += 1

            # 设置端口
            self.set_ftp_port()

            # 设置传输模式
            self.set_transmission_mode(trms_text=trms_text, trm_opt_text=trm_opt_text)

            # 设置生成子目录

            # 设置上传

            # 设置视频-分辨率

            # 设置视频-FTP录像延长

            # 设置视频-视频最大大小(MB)

            # 设置图片-分辨率

            # 设置图片-间隔

            # 设置图片-覆盖

            # TODO: 点击保存
            # self.scroll_and_click_by_text(text_to_find='保存')
            # TODO: 处理弹窗：点击确定/取消
            # self.scroll_and_click_by_text(text_to_find='确定')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")