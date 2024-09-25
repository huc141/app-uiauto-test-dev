# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='light.yaml')  # 读取参数化文件


@allure.feature("远程配置>侦测报警")
class TestRemoteDetectionAlarm:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("测非侦测区域")
    def test_remote_non_detection_area(self, device_config):
        pass
