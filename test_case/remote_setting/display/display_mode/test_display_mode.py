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

@allure.feature("远程配置>常规设置>显示")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>显示模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入显示模式页面，分别点击不同的显示模式类型")
    def test_display_mode(self, device_config):
        pass