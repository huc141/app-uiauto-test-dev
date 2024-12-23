# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
device_dir = g_config.get("device_dir")  # 读取设备配置文件目录
devices_config = read_yaml.load_device_config(device_dir=device_dir,
                                              yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入显示>码流页面， 并验证清晰和流畅页面的配置文本和操作")
    def test_remote_stream(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'stream')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 验证码流主页文本
        RemoteDisplay().verify_stream_main_texts(custom_texts=remote_items['stream']['text'],
                                                 custom_options=remote_items['stream']['options'])

        # ====================↓ 清晰配置 ↓====================

        # 进入码流>清晰页面，验证清晰页面文本和操作
        RemoteDisplay().access_in_clear()
        RemoteDisplay().verify_stream_clear_main_texts(custom_options=remote_items['stream']['clear']['text'])

        # 点击清晰>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        RemoteDisplay().verify_stream_clear_resolution(remote_items['stream']['clear']['resolution']['options'])

        # 点击清晰>帧率选项，验证文本
        RemoteDisplay().click_frame_rate()
        RemoteDisplay().verify_stream_clear_frame_rate(remote_items['stream']['clear']['frame_rate']['options'])

        # 点击清晰>最大码率选项，验证文本
        RemoteDisplay().click_max_bit_rate()
        RemoteDisplay().verify_stream_clear_max_bit_rate(remote_items['stream']['clear']['max_bit_rate']['options'])

        # 点击清晰>编码格式选项，验证文本、执行操作
        RemoteDisplay().click_encoding_format()
        RemoteDisplay().verify_stream_clear_encoding_format(remote_items['stream']['clear']['encoding_format']['options'])

        # 点击清晰>I 帧间隔选项，验证文本
        RemoteDisplay().click_i_frame_interval()
        RemoteDisplay().verify_stream_clear_i_frame_interval(remote_items['stream']['clear']['i_frame_interval']['options'])

        # 点击取消，返回到码流主页
        BasePage().click_by_text('取消')

        # ====================↓ 流畅配置 ↓====================

        # 进入码流>流畅页面，验证流畅页面文本和操作
        RemoteDisplay().access_in_fluent()
        RemoteDisplay().verify_stream_fluent_main_texts(custom_options=remote_items['stream']['fluent']['text'])

        # 点击流畅>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        RemoteDisplay().verify_stream_clear_resolution(remote_items['stream']['fluent']['resolution']['options'])

        # 点击流畅>帧率选项，验证文本、执行操作
        RemoteDisplay().click_frame_rate()
        RemoteDisplay().verify_stream_clear_frame_rate(remote_items['stream']['fluent']['frame_rate']['options'])

        # 点击流畅>最大码率选项，验证文本、返回码流主页
        RemoteDisplay().click_max_bit_rate()
        RemoteDisplay().verify_stream_clear_max_bit_rate(remote_items['stream']['fluent']['max_bit_rate']['options'])

        # 点击流畅>编码格式选项，验证文本、执行操作
        RemoteDisplay().click_encoding_format()
        RemoteDisplay().verify_stream_clear_encoding_format(remote_items['stream']['fluent']['encoding_format']['options'])

        # 点击流畅>I 帧间隔选项，验证文本
        RemoteDisplay().click_i_frame_interval()
        RemoteDisplay().verify_stream_clear_i_frame_interval(remote_items['stream']['fluent']['i_frame_interval']['options'])

        # 点击取消，返回到码流主页
        BasePage().click_by_text('取消')

    # ====================↓ 帧率控制 ↓====================

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>帧率控制")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入帧率控制页面，遍历帧率控制配置")
    def test_remote_frame_rate_control(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'frame_rate_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击帧率控制,验证popup文本
        RemoteDisplay().click_frame_rate_mode()
        RemoteSetting().scroll_check_funcs2(
            remote_items['frame_rate_mode']['text'],
            back2top=False)
        RemoteSetting().scroll_check_funcs2(
            remote_items['frame_rate_mode']['options'],
            selector='ReoTitle',
            back2top=False)
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['frame_rate_mode']['options'],
            menu_text='帧率控制')

    # ====================↓ 码率模式 ↓====================
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>码率模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入码率模式页面，遍历码率模式配置")
    def test_remote_rate_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'rate_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击码率模式,验证popup文本
        RemoteDisplay().click_rate_mode()
        RemoteSetting().scroll_check_funcs2(remote_items['rate_mode']['text'], back2top=False)
        RemoteSetting().scroll_check_funcs2(remote_items['stream']['subpage']['rate_mode']['options'],
                                            selector='ReoTitle',
                                            back2top=False)
        BasePage().iterate_and_click_popup_text(option_text_list=remote_items['rate_mode']['options'],
                                                menu_text='码率模式')
