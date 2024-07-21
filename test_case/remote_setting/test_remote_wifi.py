# -*- coding: utf-8 -*-
import os
import pytest
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_wifi import RemoteWiFi

wifi_configs = read_yaml.wifi_configs  # 读取参数化文件


class TestRemoteWifi:
    @pytest.mark.parametrize("wifi_config", wifi_configs)
    def test_remote_wifi_page(self, wifi_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置
        RemoteWiFi().access_in_remote_wifi(device_name=wifi_config['device_list_name'],
                                           sub_name=wifi_config['sub_name'],
                                           type_desc=wifi_config['type_desc'])
        # 读取wifi.yaml文件中wifi主页内容
        remote_wifi_page = wifi_configs['sub_pages']['wifi']

        # 读取预期功能项并遍历，与获取到的功能项进行一一比对和数量核对
        page_fun = RemoteWiFi().check_remote_wifi_text(remote_wifi_page["expected_texts"],
                                                       remote_wifi_page["excluded_texts"],
                                                       remote_wifi_page["xml_az_parse_conditions"],
                                                       remote_wifi_page["xml_ios_parse_conditions"])
        # 断言
        assert page_fun is True

