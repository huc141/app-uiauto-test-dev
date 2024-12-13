# -*- coding: utf-8 -*-
import pytest
import allure
from pages.base_page import BasePage
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_wifi import RemoteWiFi
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='wifi.yaml')  # 读取参数化文件


@allure.epic("远程配置>Wi-Fi")
class TestRemoteWifi:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("未连接")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_wifi_disconnect(self, device_config):
        pass
