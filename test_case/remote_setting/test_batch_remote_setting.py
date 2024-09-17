# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from common_tools.read_yaml import read_yaml

devices_config = read_yaml.load_device_config()  # 读取设备能力集参数化文件
element_config = read_yaml.get_data(key="remote_setting", source="global_data")  # 读取全局配置


class TestRemoteSetting:
    @pytest.mark.parametrize("device_config", devices_config)
    def test_remote_setting_main_page(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 读取yaml文件中远程配置页面内容
        remote_setting_page = device_config['ipc']['items']

        # 在设备列表查找到对应设备并进入远程配置
        RemoteSetting().scroll_click_remote_setting(device_list_name=device_config['device_list_name'])

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_page, 'name')

        # 遍历并滚动查找当前页面指定元素，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs2(texts=page_fun_list, selector=element_config)

        # 断言
        assert page_fun is True
