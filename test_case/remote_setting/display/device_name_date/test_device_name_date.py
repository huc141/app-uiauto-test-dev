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

    # 测设备名称
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>设备名称")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入设备名称页面，遍历设备名称配置")
    @pytest.mark.skip
    def test_remote_device_name(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'device_name')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击设备名称，验证popup文本
        RemoteDisplay().verify_device_name(remote_items['device_name']['text'],
                                           remote_items['device_name']['options'])

    # 测日期
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>日期")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入日期页面，遍历日期配置")
    @pytest.mark.skip
    def test_remote_date(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'date')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 进入日期页面，遍历日期配置
        RemoteDisplay().verify_date(remote_items['date']['text'],
                                    remote_items['date']['options']
                                    )



