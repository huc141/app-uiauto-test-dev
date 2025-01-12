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
    @allure.feature("图像设置>主页文案")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 主页文案/亮度/亮度同步/对比度/饱和度/锐度的 拖动条")
    def test_remote_image_setting_main_texts(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'image_setting')

        remote_items1 = device_config['ipc']['display']['items']['display']['image_setting']
        anti_flicker = BasePage().extract_value_from_yaml(remote_items1, 'anti_flicker', skip_if_false=False)
        night_tt_vision = BasePage().extract_value_from_yaml(remote_items1, 'night_transparent_vision', skip_if_false=False)
        hdr = BasePage().extract_value_from_yaml(remote_items1, 'hdr', skip_if_false=False)
        brightness_sync = BasePage().extract_value_from_yaml(remote_items1, 'brightness_sync', skip_if_false=False)

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 拖动亮度/对比度/饱和度/锐度滑动条
        RemoteDisplay().verify_image_setting_slider(anti_flicker=anti_flicker,
                                                    night_tt_vision=night_tt_vision,
                                                    hdr=hdr,
                                                    brightness_sync=brightness_sync,
                                                    image_config=remote_items1)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>抗闪烁")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置页面，遍历抗闪烁")
    @pytest.mark.skip
    def test_remote_anti_flicker(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().extract_value_from_yaml(remote_items, 'anti_flicker', skip_if_false=True)

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()
        # 点击抗闪烁
        RemoteDisplay().click_anti_flicker()
        # 变量抗闪烁选项
        RemoteDisplay().verify_anti_flicker()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>夜视通透模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 显示>图像设置页面，夜视通透模式")
    @pytest.mark.skip
    def test_remote_night_transparent_vision(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().extract_value_from_yaml(remote_items, 'night_transparent_vision', skip_if_false=True)

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
    @pytest.mark.skip
    def test_remote_hdr(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().extract_value_from_yaml(remote_items, 'hdr', skip_if_false=True)

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 遍历HDR
        RemoteDisplay().verify_hdr()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("图像设置>夜视对焦增强")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试 进入显示>图像设置，测试夜视对焦增强")
    @pytest.mark.skip
    def night_vision_zoom_enhance(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']['image_setting']
        BasePage().extract_value_from_yaml(remote_items, 'night_vision_zoom_enhance',
                                           skip_if_false=True)

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入图像设置
        RemoteDisplay().click_image_setting()

        # 测试也是对焦增强
        RemoteDisplay().verify_night_vision_zoom_enhance()
