# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(yaml_file_name='display.yaml')  # 读取参数化文件


@allure.feature("远程配置>常规设置>显示")
class TestRemoteDisplay:

    # 测隐私遮盖（遮盖区域）
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_privacy_mask(self, device_config):
        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['display']['items']

        # 检查键是否存在，存在则执行当前用例，否则跳过
        BasePage().check_key_in_yaml(remote_items, 'private_mark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入遮盖区域主页
        RemoteDisplay().access_in_privacy_mask()

        # 验证码流主页文本
        page_fun_privacy_mask_text = RemoteSetting().scroll_check_funcs(remote_items['private_mark']['subpage']['text'])

        # 此处的定位方式默认xpath
        RemoteDisplay().draw_privacy_mask(mode='xpath')

        assert page_fun_privacy_mask_text is True