# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi', yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入显示>码流页面， 并验证清晰和流畅页面的配置文本和操作")
    @pytest.mark.skip
    def test_remote_stream(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'stream')

        # 启动app，并开启录屏
        driver.start_app()

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流页
        RemoteDisplay().access_in_stream()

        # 验证码流主页文本
        RemoteSetting().scroll_check_funcs2(remote_items['stream']['subpage']['text'])

        # ====================↓ 清晰配置 ↓====================

        # 进入码流>清晰页面，验证清晰页面文本和操作
        RemoteDisplay().access_in_clear()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['text'])

        # 点击清晰>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['resolution']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['resolution']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['resolution']['options'],
            menu_text='分辨率')

        # # 点击清晰>帧率选项，验证文本
        RemoteDisplay().click_frame_rate()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['frame_rate']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['frame_rate']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['frame_rate']['options'],
            menu_text='帧率(FPS)')

        # # 点击清晰>最大码率选项，验证文本
        RemoteDisplay().click_max_bit_rate()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['max_bit_rate']['text'])
        RemoteSetting().scroll_check_funcs2(
                remote_items['stream']['subpage']['clear']['subpage']['max_bit_rate']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['max_bit_rate']['options'],
            menu_text='最大码率(Kbps)')

        # 点击清晰>编码格式选项，验证文本、执行操作
        RemoteDisplay().click_encoding_format()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['encoding_format']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['encoding_format']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['encoding_format']['options'],
            menu_text='编码格式')

        # 点击编码格式>i帧间隔选项，验证文本
        RemoteDisplay().click_i_frame_interval()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['i_frame_interval']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['clear']['subpage']['i_frame_interval']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['i_frame_interval']['options'],
            menu_text='i帧间隔')

        # 保存清晰页的配置, 返回码流主页
        BasePage().scroll_and_click_by_text("保存")

        # ====================↓ 流畅配置 ↓====================

        # 进入码流>流畅页面，验证流畅页面文本和操作
        RemoteDisplay().access_in_fluent()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['text'])

        # 点击流畅>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['resolution']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['resolution']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['resolution']['options'],
            menu_text='分辨率')

        # 点击流畅>帧率选项，验证文本、执行操作
        RemoteDisplay().click_frame_rate()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['frame_rate']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['frame_rate']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['frame_rate']['options'],
            menu_text='帧率(fps)')

        # 点击流畅>最大码率选项，验证文本、返回码流主页
        RemoteDisplay().click_max_bit_rate()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['max_bit_rate']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['max_bit_rate']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['max_bit_rate']['options'],
            menu_text='最大码率(kbps)')

        # 点击清晰>编码格式选项，验证文本、执行操作
        RemoteDisplay().click_encoding_format()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['encoding_format']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['encoding_format']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['encoding_format']['options'],
            menu_text='编码格式')

        # 点击编码格式>i帧间隔选项，验证文本
        RemoteDisplay().click_i_frame_interval()
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['i_frame_interval']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['stream']['subpage']['fluent']['subpage']['i_frame_interval']['options'],
            selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['i_frame_interval']['options'],
            menu_text='i帧间隔')

        # 保存流畅页的配置, 返回码流主页
        BasePage().scroll_and_click_by_text("保存")

    # ====================↓ 帧率控制 ↓====================

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>码流>帧率控制")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入帧率控制页面，遍历帧率控制配置")
    def test_remote_frame_rate_control(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['stream']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'frame_rate_mode')

        # 启动app，并开启录屏
        driver.start_app()

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击帧率控制,验证popup文本
        RemoteDisplay().click_frame_rate_mode()
        RemoteSetting().scroll_check_funcs2(
            remote_items['frame_rate_mode']['text'])
        RemoteSetting().scroll_check_funcs2(
            remote_items['frame_rate_mode']['options'],
            selector='ReoTitle')
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
        driver.start_app()

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入码流主页
        RemoteDisplay().access_in_stream()

        # 点击码率模式,验证popup文本
        RemoteDisplay().click_rate_mode()
        RemoteSetting().scroll_check_funcs2(remote_items['rate_mode']['text'])
        RemoteSetting().scroll_check_funcs2(remote_items['stream']['subpage']['rate_mode']['options'],
                                             selector='ReoTitle')
        BasePage().iterate_and_click_popup_text(option_text_list=remote_items['rate_mode']['options'],
                                                menu_text='码率模式')


