# -*- coding: utf-8 -*-
import time

import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi',
                                              yaml_file_name='display.yaml')  # 读取参数化文件


@allure.feature("远程配置>常规设置>显示")
class TestRemoteDisplay:

    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.repeat(2)
    @allure.feature("显示>图像布局")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入图像布局页面，分别点击不同的布局类型(该用例会重复执行两次)")
    def test_image_layout(self, device_config):
        # # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'image_layout')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入并验证图像布局
        RemoteDisplay().verify_image_layout(texts=remote_items['image_layout']['text'])

