# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(yaml_file_name='display.yaml')  # 读取参数化文件


class TestRemoteDisplay:

    # 测垂直翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_vertical_flip(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_setting_display = device_config['ipc']['display']['items'].values()
        remote_items = device_config['ipc']['display']['items']

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 遍历并滚动查找当前页面指定元素，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs(page_fun_list)

        # 点击垂直翻转按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['vertical_flip']['name'])

        # 断言
        assert page_fun is True

    # 测水平翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_horizontal_flip(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 点击水平翻转按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['horizontal_flip']['name'])

    # 测码流
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_stream(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_setting_display = device_config['ipc']['display']['items'].values()
        remote_items = device_config['ipc']['display']['items']

        # 点击进入码流页
        RemoteDisplay().access_in_stream()

        # 验证码流主页文本
        page_fun_stream_text = RemoteSetting().scroll_check_funcs(remote_items['stream']['subpage']['text'])

        # 进入码流>清晰页面，验证清晰页面文本和操作
        RemoteDisplay().access_in_clear()
        page_fun_clear_text = RemoteSetting().scroll_check_funcs(remote_items['stream']['subpage']['clear']['subpage']['text'])

        # 点击清晰>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        page_fun_resolution_text = RemoteSetting().scroll_check_funcs(remote_items['stream']['subpage']['clear']['subpage']['resolution']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['resolution']['options'],
            menu_text='分辨率')

        # 点击清晰>帧率选项，验证文本
        RemoteDisplay().click_frame_rate()
        page_fun_frame_rate = RemoteSetting().scroll_check_funcs(remote_items['stream']['subpage']['clear']['subpage']['frame_rate']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['frame_rate']['options'],
            menu_text='帧率(fps)')

        # 点击清晰>最大码率选项，验证文本、返回码流主页
        RemoteDisplay().click_max_bit_rate()
        page_fun_max_bit_rate = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['clear']['subpage']['max_bit_rate']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['clear']['subpage']['max_bit_rate']['options'],
            menu_text='最大码率(kbps)')
        BasePage().scroll_and_click_by_text("保存")

        # 进入码流>流畅页面，验证流畅页面文本和操作
        RemoteDisplay().access_in_fluent()
        page_fun_fluent_text = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['fluent']['subpage']['text'])

        # 点击流畅>分辨率选项，验证文本、执行操作
        RemoteDisplay().click_resolution()
        page_fun_fluent_resolution_text = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['fluent']['subpage']['resolution']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['resolution']['options'],
            menu_text='分辨率')

        # 点击流畅>帧率选项，验证文本、执行操作
        RemoteDisplay().click_frame_rate()
        page_fun_fluent_frame_rate = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['fluent']['subpage']['frame_rate']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['frame_rate']['options'],
            menu_text='帧率(fps)')

        # 点击流畅>最大码率选项，验证文本、返回码流主页
        RemoteDisplay().click_max_bit_rate()
        page_fun_fluent_max_bit_rate = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['fluent']['subpage']['max_bit_rate']['text'])
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['stream']['subpage']['fluent']['subpage']['max_bit_rate']['options'],
            menu_text='最大码率(kbps)')
        BasePage().scroll_and_click_by_text("保存")

        # 点击帧率控制,验证文本
        RemoteDisplay().click_frame_rate_mode()
        page_fun_frame_rate_mode = RemoteSetting().scroll_check_funcs(
            remote_items['stream']['subpage']['frame_rate_mode']['text'])
        BasePage().iterate_and_click_popup_text(option_text_list=remote_items['stream']['subpage']['frame_rate_mode']['options'],
                                                menu_text='帧率控制')

        assert page_fun_stream_text is True

        assert page_fun_clear_text is True

        assert page_fun_resolution_text is True

        assert page_fun_frame_rate is True

        assert page_fun_max_bit_rate is True

        assert page_fun_fluent_text is True

        assert page_fun_fluent_resolution_text is True

        assert page_fun_fluent_frame_rate is True

        assert page_fun_fluent_max_bit_rate is True

        assert page_fun_frame_rate_mode is True

    # 测隐私遮盖（遮盖区域）
    @pytest.mark.parametrize("device_config", devices_config)
    def test_privacy_mask(self, device_config):
        BasePage().get_coordinates_and_draw(mode='xpath',
                                            id_or_xpath='//*[@resource-id="com.mcu.reolink:id/shelter_player"]',
                                            draw_area='全屏')





