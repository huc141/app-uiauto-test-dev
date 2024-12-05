# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(yaml_file_name='display.yaml')  # 读取参数化文件


@allure.feature("远程配置>常规设置>显示")
class TestRemoteDisplay:

    # 测垂直翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_vertical_flip(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查'vertical_flip'键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'vertical_flip')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_setting_display = device_config['ipc']['display']['items'].values()

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 遍历并滚动查找当前页面功能项，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs2(page_fun_list)

        # 点击垂直翻转按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['vertical_flip']['name'])

        # 断言
        assert page_fun is True

    # 测水平翻转
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_horizontal_flip(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'horizontal_flip')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 点击水平翻转按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['horizontal_flip']['name'])
