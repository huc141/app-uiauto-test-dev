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

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置
        remote_setting_wifi = device_config['ipc']['items']

        # 在远程设置主页点击‘Wi-Fi’菜单项进入Wi-Fi页
        RemoteSetting().access_in_remote_wifi(device_list_name=device_config['device_list_name'])

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_wifi, 'name')

        # 遍历并滚动查找当前页面指定元素，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs(page_fun_list)

        # 断言
        assert page_fun is True

        # 测试WiFi频段偏好
        wifi_band_preference_text = device_config['ipc']['items']
        wifi_band_preference_test(wifi_band_preference_text[0]['options'])


# 辅助函数
def wifi_band_preference_test(text_list):
    """
    测试wifi频段偏好
    :return:
    """
    # 点击进入wifi频段偏好页面
    RemoteWiFi().access_in_wifi_band_preference()

    # 检查wifi频段偏好页面文案
    page_fun_list = RemoteSetting().scroll_check_funcs(text_list)

    # 断言
    assert page_fun_list is True

    # TODO: 点击仅5G

    # TODO: 点击进入wifi频段偏好页面

    # TODO: 点击仅2.4G

    # TODO: 点击进入wifi频段偏好页面

    # TODO: 点击 自动
