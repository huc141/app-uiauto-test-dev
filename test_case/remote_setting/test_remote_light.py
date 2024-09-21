# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(yaml_file_name='light.yaml')  # 读取参数化文件


class TestRemoteLight:
    # 测红外灯
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_infrared_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']
        BasePage().check_key_in_yaml(remote_items, 'infrared_light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 遍历并滚动查找当前页面功能项，判断是否存在
        remote_funs_text = device_config['ipc']['light']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 获取yaml文件指定key的值
        remote_setting_display = device_config['ipc']['light']['items'].values()
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 断言
        assert page_fun is True

    # 测照明灯(白光灯)
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_infrared_light(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['light']['items']

        # 遍历并滚动查找当前页面功能项，判断是否存在
        remote_funs_text = device_config['ipc']['light']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 获取yaml文件指定key的值
        remote_setting_display = device_config['ipc']['light']['items'].values()
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')
