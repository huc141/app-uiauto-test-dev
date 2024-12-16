# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi',
                                              yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>亮度")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，拖动亮度条")
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
    @allure.feature("图像设置>对比度")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，拖动对比度条")
    def test_remote_contrast(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'contrast')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 拖动对比度条
        RemoteDisplay().drag_slider_contrast()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>饱和度")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，拖动饱和度条")
    def test_remote_saturation(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'saturation')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 拖动饱和度条
        RemoteDisplay().drag_slider_saturation()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>锐度")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，拖动锐度条")
    def test_remote_sharpness(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'saturation')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 拖动锐度条
        RemoteDisplay().drag_slider_sharpness()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>抗闪烁")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，遍历抗闪烁")
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

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>夜视通透模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，点击夜视通透模式")
    def test_remote_night_transparent_vision(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'night_transparent_vision')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 夜视通透模式
        RemoteDisplay().verify_night_transparent_vision()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>HDR")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，测试HDR")
    def test_remote_hdr(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().check_key_in_yaml(remote_items, 'hdr')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 遍历HDR
        RemoteDisplay().verify_hdr(remote_items['hdr']['text'], remote_items['hdr']['options'])

