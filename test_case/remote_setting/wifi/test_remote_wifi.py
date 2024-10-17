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
    @allure.feature("Wi-Fi主页文案")
    @allure.story("需人工核查日志和录屏")
    def test_remote_wifi_page_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']
        BasePage().check_key_in_yaml(remote_items, 'Wi_Fi')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 验证Wi-Fi主页文案
        wifi_main_text_res = RemoteWiFi().check_wifi_main_text(texts=remote_items['Wi_Fi']['items']['wifi']['text'])

        # 获取yaml文件指定配置
        # remote_setting_wifi = device_config['ipc']['Wi_Fi']['items'].values()
        #
        # # 读取yaml文件中预期功能项
        # page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_wifi, 'name')
        #
        # # 遍历并滚动查找当前页面指定元素，判断是否存在
        # page_fun = RemoteSetting().scroll_check_funcs(page_fun_list)

        # 断言
        assert wifi_main_text_res is True

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

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("Wi-Fi测速")
    @allure.story("需人工核查日志和录屏")
    def test_wifi_speed_test(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['Wi_Fi']['items']['wifi']
        BasePage().check_key_in_yaml(remote_items, 'wifi_speed_test')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 测试Wi-Fi测速
        wifi_test_speed_text, google_speed_page = RemoteWiFi().access_in_wifi_test(
            text_list=remote_items['wifi_speed_test']['subpage']['text'])

        # 断言
        assert wifi_test_speed_text is True
        assert google_speed_page is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("未连接")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_wifi_disconnect(self, device_config):
        pass

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("添加其他网络")
    @allure.story("需人工核查日志和录屏")
    def test_add_other_network(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['Wi_Fi']['items']['wifi']
        BasePage().check_key_in_yaml(remote_items, 'add_other_network')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 测试添加其他网络
        switch_wifi = remote_items['add_other_network']['subpage']
        add_network_text = RemoteWiFi().access_in_add_network(
            text_list=switch_wifi['text'],
            wifi_name=switch_wifi['options_text']['input_wifi_name'],
            wifi_passw=switch_wifi['options_text']['input_wifi_passw'])

        # 断言
        assert add_network_text is True
