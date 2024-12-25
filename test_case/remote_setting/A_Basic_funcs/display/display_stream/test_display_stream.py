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

        # 点击取消，返回到码流主页
        BasePage().click_by_text('取消')

    # ====================↓ 编码格式 ↓====================
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>清晰/流畅>编码格式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入显示>码流>清晰/流畅>编码格式， 并验证配置文本和操作")
    def test_remote_stream_encoding_format(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']
        BasePage().check_key_in_yaml(remote_items, 'clear')

        remote_items1 = device_config['ipc']['display']['items']['display']['stream']['clear']
        BasePage().check_key_in_yaml(remote_items1, 'encoding_format')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 测试清晰/流畅 的编码格式
        RemoteDisplay().verify_stream_encoding_format_interval(
                       clear_encoding_options=remote_items['clear']['encoding_format']['options'],
                       fluent_encoding_options=remote_items['fluent']['encoding_format']['options'])

    # ====================↓ I 帧间隔 ↓====================
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>清晰/流畅>I 帧间隔")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入显示>码流>清晰/流畅>I 帧间隔， 并验证配置文本和操作")
    def test_remote_stream_i_interval(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']
        BasePage().check_key_in_yaml(remote_items, 'clear')

        remote_items1 = device_config['ipc']['display']['items']['display']['stream']['clear']
        BasePage().check_key_in_yaml(remote_items1, 'i_frame_interval')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 测试清晰/流畅 的I帧间隔
        RemoteDisplay().verify_stream_i_frame_interval(
                        clear_i_options=remote_items['clear']['i_frame_interval']['options'],
                        fluent_i_options=remote_items['fluent']['i_frame_interval']['options'])

    # ====================↓ 帧率控制 ↓====================

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>帧率控制")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入帧率控制页面，遍历帧率控制配置")
    def test_remote_frame_rate_control(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']
        BasePage().check_key_in_yaml(remote_items, 'frame_rate_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击帧率控制
        RemoteDisplay().click_frame_rate_mode()

        # 点击帧率控制,验证popup文本
        RemoteDisplay().verify_stream_frame_rate_control(frame_rate_mode=remote_items['frame_rate_mode']['support_mode'])

    # ====================↓ 码率控制 ↓====================
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>码率控制")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入码率控制页面，遍历码率控制配置")
    @pytest.mark.skip(reason="暂时不执行")
    def test_remote_rate_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']
        BasePage().check_key_in_yaml(remote_items, 'rate_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击码率控制
        RemoteDisplay().click_rate_mode()

        # 点击码率模式,验证popup文本
        RemoteDisplay().verify_stream_rate_mode()
