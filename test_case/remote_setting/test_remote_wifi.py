# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_wifi import RemoteWiFi
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='wifi.yaml')  # 读取参数化文件


class TestRemoteWifi:
    @pytest.mark.parametrize("device_config", devices_config)
    def test_remote_wifi_page(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_setting_wifi = device_config['ipc']['Wi_Fi']['items'].values()

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_wifi, 'name')

        # 遍历并滚动查找当前页面指定元素，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs(page_fun_list)

        # 测试WiFi频段偏好
        wifi_band_preference_text = device_config['ipc']['Wi_Fi']['items']['wifi_band_preference']['options']
        RemoteWiFi().access_in_wifi_band_preference(wifi_band_preference_text)

        # 测试Wi-Fi测速
        wifi_test_speed_text = device_config['ipc']['Wi_Fi']['items']['wifi_speed_test']['subpage']['text']
        RemoteWiFi().access_in_wifi_test(wifi_test_speed_text)

        # 测试添加其他网络
        check_text_list = device_config['ipc']['Wi_Fi']['items']['add_other_network']['subpage']['text']
        switch_wifi = device_config['ipc']['Wi_Fi']['items']['add_other_network']['subpage']['options']
        RemoteWiFi().access_in_add_network(text_list=check_text_list,
                                           wifi_name=switch_wifi['input_wifi_name'],
                                           wifi_passw=switch_wifi['input_wifi_passw'])

        # 断言
        assert page_fun is True
