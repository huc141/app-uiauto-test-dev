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
    @allure.feature("邮件通知主页文案")
    @allure.story("需人工核查日志和录屏")
    def test_email_alerts_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_alerts')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 验证主页文案
        email_alerts_main_text_status = RemoteEmailAlerts().check_email_alerts_main_text(
            texts=remote_items['email_alerts']['text'])

        # 断言
        assert email_alerts_main_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("计划")
    @allure.story("需人工核查日志和录屏")
    def test_remote_email_alerts_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'plan')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 点击并测试 计划
        plan_text = remote_items['plan']
        plan_alarm_main_text_res, plan_timed_main_text_res, plan_alarm_type_text_res = RemoteEmailAlerts().click_and_test_plan(
            plan_alarm_text=plan_text['alarm']['text'],
            plan_timed_text=plan_text['timed']['text'],
            alarm_type_text=plan_text['alarm']['alarm_type']['text'],
            alarm_type_option_text=plan_text['alarm']['alarm_type']['option_text'])

        # 断言
        assert plan_alarm_main_text_res is True
        assert plan_timed_main_text_res is True
        assert plan_alarm_type_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮件设置")
    @allure.story("需人工核查日志和录屏")
    def test_remote_email_config(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_config')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 点击并测试 邮件设置
        email_config_text_status = RemoteEmailAlerts().click_and_test_email_config(
            email_config_text=remote_items['email_config']['text'])

        # 断言
        assert email_config_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮件内容")
    @allure.story("需人工核查日志和录屏")
    def test_remote_email_content(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_content')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 点击并遍历邮件内容
        RemoteEmailAlerts().click_and_test_email_content(option_text=remote_items['email_content']['text'])

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("邮箱间隔")
    @allure.story("需人工核查日志和录屏")
    def test_remote_email_interval(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_interval')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 点击并遍历邮件内容
        RemoteEmailAlerts().click_and_test_email_interval(option_text=remote_items['email_interval']['text'])

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("未收到邮件？")
    @allure.story("需人工核查日志和录屏")
    def test_remote_email_interval(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['email_alerts']['items']
        BasePage().check_key_in_yaml(remote_items, 'email_not_received')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteEmailAlerts().is_email_alert_on()

        # 点击未收到邮件？链接
        not_received_link_res = RemoteEmailAlerts().click_email_not_received_link()

        assert not_received_link_res is True


