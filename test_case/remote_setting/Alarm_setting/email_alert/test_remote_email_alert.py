# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_email_alerts import RemoteEmailAlerts

devices_config = read_yaml.load_device_config(yaml_file_name='email_alerts.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警通知>邮件通知")
class TestRemoteEmailAlerts:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮件通知按钮/邮件设置")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试未配置邮箱的情况下，打开邮件通知按钮、测试按钮、邮件设置页面内容")
    def test_email_alerts_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_alerts')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 验证未配置邮箱的情况下，打开邮件通知按钮、测试按钮、邮件设置页面内容
        key_res = BasePage().check_key_in_yaml(remote_items['email_alerts'], 'supported_test')
        RemoteEmailAlerts().verify_email_alerts_button_and_unsetting(supported_test=key_res)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("计划")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试邮件通知>计划内容")
    @pytest.mark.skip
    def test_remote_email_alerts_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items1, 'plan')

        remote_items = device_config['ipc']['email_alerts']['items']['plan']

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 点击并测试 计划
        supported_alarm = BasePage().is_key_in_yaml(remote_items, 'alarm_type')
        supported_timed = BasePage().is_key_in_yaml(remote_items, 'timed')
        RemoteEmailAlerts().verify_plan(supported_alarm=supported_alarm,
                                        supported_timed=supported_timed,
                                        options_text=remote_items['alarm_type'])

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮件设置")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试邮件设置页面内容")
    @pytest.mark.skip
    def test_remote_email_config(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_config')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 点击并测试 邮件设置
        RemoteEmailAlerts().verify_email_config()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮件内容/移动轨迹/分辨率设置")
    @allure.story("需人工核查日志和录屏")
    @allure.title('测试邮件内容/移动轨迹/分辨率设置')
    @pytest.mark.skip
    def test_remote_email_content(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_content')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().turn_on_email_alert()

        # 点击并遍历邮件内容
        RemoteEmailAlerts().verify_email_content(supported_move_track=remote_items['email_content']['supported_move_track'],
                                                 supported_resolution=remote_items['email_content']['supported_resolution'],
                                                 device_name=device_config['device_list_name'])

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮箱间隔")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试邮件间隔")
    @pytest.mark.skip
    def test_remote_email_interval(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_interval')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 点击并遍历邮件内容
        RemoteEmailAlerts().verify_email_interval(texts=remote_items['email_interval']['text'],
                                                  options=remote_items['email_interval']['options'])

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("未收到邮件？")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试未收到邮件链接正常打开")
    @pytest.mark.skip
    def test_remote_email_not_received(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_not_received')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 点击未收到邮件？链接
        RemoteEmailAlerts().verify_email_not_received_link()



