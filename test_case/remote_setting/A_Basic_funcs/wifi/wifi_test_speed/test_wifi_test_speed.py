# -*- coding: utf-8 -*-
import pytest
import allure
from pages.base_page import BasePage
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_wifi import RemoteWiFi
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
device_dir = g_config.get("device_dir")  # 读取设备配置文件目录
devices_config = read_yaml.load_device_config(device_dir=device_dir,
                                              yaml_file_name='wifi.yaml')  # 读取参数化文件


@allure.epic("远程配置>Wi-Fi")
class TestRemoteWifi:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("Wi-Fi测速")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试打开Wi-Fi测速页")
    def test_wifi_speed_test(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['Wi_Fi']['items']['wifi']
        BasePage().check_key_in_yaml(remote_items, 'wifi_speed_test')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 测试Wi-Fi测速
        RemoteWiFi().access_in_wifi_test()

