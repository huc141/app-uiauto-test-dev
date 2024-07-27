# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from common_tools.read_yaml import read_yaml

devices_config = read_yaml.load_device_config('reolink_trackmix_wifi')  # 读取参数化文件
print(devices_config)


class TestRemoteSetting:
    @pytest.mark.parametrize("device_name, device_config", devices_config.items())
    def test_remote_setting_main_page(self, device_config, device_name='yulong-test-sd7'):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 读取yaml文件中远程配置页面内容
        remote_setting_page = device_config['ipc']['items']

        # 在设备列表查找到对应设备并进入远程配置
        RemoteSetting().scroll_click_remote_setting(device_name=device_name)

        # 读取预期功能项并遍历，与获取到的功能项进行一一比对和数量核对
        page_fun = RemoteSetting().check_remote_setting_text(remote_setting_page["expected_texts"],
                                                             remote_setting_page["excluded_texts"],
                                                             remote_setting_page["xml_az_parse_conditions"],
                                                             remote_setting_page["xml_ios_parse_conditions"]
                                                             )
        # 断言
        assert page_fun is True
