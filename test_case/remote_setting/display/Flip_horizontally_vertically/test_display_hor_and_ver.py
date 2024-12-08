# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:

    # 测垂直翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>垂直翻转")
    def test_remote_vertical_flip(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']['display']

        # 检查'vertical_flip'键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'vertical_flip')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击垂直翻转按钮
        RemoteDisplay().click_vertical_flip_switch_button()

    # 测水平翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>水平翻转")
    def test_remote_horizontal_flip(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']['display']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'horizontal_flip')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击水平翻转按钮
        RemoteDisplay().click_horizontal_flip_switch_button()
