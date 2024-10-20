# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_siren import RemoteSirenAlerts

devices_config = read_yaml.load_device_config(yaml_file_name='siren.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警通知>鸣笛")
class TestRemoteSirenAlerts:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("鸣笛主页文案")
    @allure.story("需人工核查日志和录屏")
    def test_siren_alerts_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['siren']['items']
        BasePage().check_key_in_yaml(remote_items, 'siren')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_siren(device_list_name=device_config['device_list_name'])

        # 判断鸣笛按钮开关状态，没开则开
        RemoteSirenAlerts().is_siren_alert_on()

        # 验证主页文案
        siren_alerts_main_text_status = RemoteSirenAlerts().check_siren_alerts_main_text(texts=remote_items['siren']['text'])

        # 断言
        assert siren_alerts_main_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("鸣笛声音>添加自定义声音")
    @allure.story("需人工核查日志和录屏")
    def test_siren_custom_sound(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['siren']['items']
        BasePage().check_key_in_yaml(remote_items, 'siren_sound')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_siren(device_list_name=device_config['device_list_name'])

        # 判断鸣笛按钮开关状态，没开则开
        RemoteSirenAlerts().is_siren_alert_on()

        # 点击添加自定义声音并录制自定义声音
        bf_res, af_res = RemoteSirenAlerts().clk_test_custom_sound()

        # 断言
        assert bf_res is True
        assert af_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("鸣笛声音>编辑、重录、清空自定义声音")
    @allure.story("需人工核查日志和录屏")
    def test_rerecord_custom_sound(self, device_config):
        """
        点击编辑自定义声音按钮，重录自定义声音、清空自定义声音文件
        :return:
        """
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['siren']['items']
        BasePage().check_key_in_yaml(remote_items, 'siren_sound')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_siren(device_list_name=device_config['device_list_name'])

        # 判断鸣笛按钮开关状态，没开则开
        RemoteSirenAlerts().is_siren_alert_on()

        # 点击编辑自定义声音并重录自定义声音、清空自定义声音文件
        siren_main_res = RemoteSirenAlerts().clear_custom_sound()

        # 断言
        assert siren_main_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("计划")
    @allure.story("需人工核查日志和录屏")
    def test_remote_siren_alerts_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['siren']['items']
        BasePage().check_key_in_yaml(remote_items, 'siren')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_siren(device_list_name=device_config['device_list_name'])

        # 判断鸣笛按钮开关状态
        RemoteSirenAlerts().is_siren_alert_on()

        # 点击并测试 计划
        plan_text = remote_items['siren']['plan']
        email_plan_alarm_text_status = RemoteSirenAlerts().click_and_test_plan(
            plan_main_text=plan_text['text'],
            alarm_type_text=plan_text['subpage']['text'],
            alarm_type_option_text=plan_text['subpage']['option_text'])

        # 断言
        assert email_plan_alarm_text_status is True
