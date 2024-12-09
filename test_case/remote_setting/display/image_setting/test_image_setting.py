# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi', yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示>图像设置")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>亮度")
    def test_remote_brightness(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'brightness')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 拖动亮度条
        RemoteDisplay().drag_slider_brightness()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>抗闪烁")
    def test_remote_anti_flicker(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'anti_flicker')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 点击抗闪烁，验证popup文本
        RemoteDisplay().click_anti_flicker()
        RemoteSetting().scroll_check_funcs2(remote_items['anti_flicker']['text'])
        RemoteSetting().scroll_check_funcs2(remote_items['anti_flicker']['options'], selector='ReoTitle')

        # 返回上一级(文本校验未通过的情况下，直接标记失败，不会执行到后续步骤)
        BasePage().back_previous_page()

        # 遍历popup操作项
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['anti_flicker']['options'], menu_text='抗闪烁')
