# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_advanced import RemoteAdvancedSetting

devices_config = read_yaml.load_device_config(yaml_file_name='advanced_setting.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警通知>邮件通知")
class TestRemoteAdvancedSetting:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("高级设置主页文案")
    @allure.story("需人工核查日志和录屏")
    def test_advanced_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['advanced_setting']['items']
        BasePage().check_key_in_yaml(remote_items, 'advanced_setting')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_advanced(device_list_name=device_config['device_list_name'])

        # 验证主页文案
        advanced_main_text_status = RemoteAdvancedSetting().check_test_advanced_main_text(
            texts=remote_items['advanced_setting']['text'])

        # 断言
        assert advanced_main_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("用户管理")
    @allure.story("需人工核查日志和录屏")
    def test_user_management(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['advanced_setting']['items']['advanced_setting']
        BasePage().check_key_in_yaml(remote_items, 'user_management')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_advanced(device_list_name=device_config['device_list_name'])

        # 点击并进入用户管理主页，验证非法登录锁定






