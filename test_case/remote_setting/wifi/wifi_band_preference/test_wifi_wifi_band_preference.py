# -*- coding: utf-8 -*-
import pytest
import allure
from pages.base_page import BasePage
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_wifi import RemoteWiFi
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi', yaml_file_name='wifi.yaml')  # 读取参数化文件


@allure.epic("远程配置>Wi-Fi")
class TestRemoteWifi:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("Wi-Fi频段偏好")
    @allure.story("需人工核查日志和录屏")
    def test_wifi_band_preference(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['Wi_Fi']['items']['wifi']
        BasePage().check_key_in_yaml(remote_items, 'wifi_band_preference')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入@allure.feature
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 测试WiFi频段偏好
        wifi_band_preference_text = RemoteWiFi().access_in_wifi_band_preference(
            text_list=remote_items['wifi_band_preference']['text'],
            option_text_list=remote_items['wifi_band_preference']['options_text'])

        assert wifi_band_preference_text is True
