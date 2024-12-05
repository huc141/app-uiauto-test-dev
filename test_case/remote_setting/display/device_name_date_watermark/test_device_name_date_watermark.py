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

    # 测设备名称
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_device_name(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'device_name')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 点击设备名称，验证popup文本
        RemoteDisplay().click_device_name()
        page_fun = RemoteSetting().scroll_check_funcs2(remote_items['device_name']['text'])

        # 遍历popup操作项
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['device_name']['options'],
            menu_text='设备名称')

        assert page_fun is True

    # 测日期
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_date(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'date')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 点击设备名称，验证popup文本
        RemoteDisplay().click_device_name()
        page_fun = RemoteSetting().scroll_check_funcs2(remote_items['date']['text'])

        # 遍历popup操作项
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['date']['options'],
            menu_text='日期')

        assert page_fun is True

    # 测水印
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_watermark(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'watermark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击水印按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['watermark']['name'])