# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_privacy_mode import RemotePrivacyMode
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='privacy_mode.yaml')  # 读取参数化文件


@allure.epic("远程配置>更多>隐私模式")
class TestRemotePrivacyMode:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("隐私模式")
    def test_remote_privacy_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['privacy_mode']['items']
        BasePage().check_key_in_yaml(remote_items, 'privacy_mode')

        # 启动app，并开启录屏
        driver.start_app()

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_privacy_mode(device_list_name=device_config['device_list_name'])

        # 验证隐私模式功能
        RemotePrivacyMode().verify_privacy_mode(device_name=device_config['device_list_name'])


