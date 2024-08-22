# -*- coding: utf-8 -*-
import pytest
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='display.yaml')  # 读取参数化文件


class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    def test_remote_vertical_flip(self, device_config):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_setting_display = device_config['ipc']['display']['items'].values()
        remote_items = device_config['ipc']['display']['items']

        # 读取yaml文件中预期功能项
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 遍历并滚动查找当前页面指定元素，判断是否存在
        page_fun = RemoteSetting().scroll_check_funcs(page_fun_list)

        # 点击垂直翻转按钮
        BasePage().scroll_click_right_btn(text_to_find=remote_items['vertical_flip']['name'])

        # 断言
        assert page_fun is True
