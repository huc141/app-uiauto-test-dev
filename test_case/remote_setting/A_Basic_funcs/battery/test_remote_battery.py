# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_battery import RemoteBattery

devices_config = read_yaml.load_device_config(device_dir='battery/Reolink Altas PT Ultra',
                                              yaml_file_name='battery.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>电池")
class TestRemoteBattery:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("电池>电池主页 文案")
    @allure.story("需人工核查日志和录屏")
    @allure.title('测试远程设置的电池页功能')
    def test_remote_battery(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['battery']['items']['battery']
        BasePage().check_key_in_yaml(remote_items, 'text')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示主页
        RemoteSetting().access_in_battery(device_list_name=device_config['device_list_name'])

        # 验证电池页的文案和功能
        RemoteBattery().check_battery_page(text=remote_items['text'],
                                           options=remote_items['options'])
