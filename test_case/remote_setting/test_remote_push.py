# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_push_notifications import RemotePush
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='push.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警通知>手机推送")
class TestRemoteDetectionAlarm:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("访客电话提醒")
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['push']['items']
        BasePage().check_key_in_yaml(remote_items, 'visitor_phone_remind')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_push_notifications(device_list_name=device_config['device_list_name'])

        # 开启访客电话提醒并验证文案
        RemotePush().is_visitor_phone_remind_on()
        visitor_phone_remind_text_status = RemotePush().click_and_test_visitor_phone_remind(
            texts=remote_items['visitor_phone_remind']['text'])

        # 断言
        assert visitor_phone_remind_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("设备通知铃声")
    @allure.story("需人工核查日志和录屏")
    def test_device_notify_ringtone(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['push']['items']
        BasePage().check_key_in_yaml(remote_items, 'device_notify_ringtone')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_push_notifications(device_list_name=device_config['device_list_name'])

        # 开启设备通知铃声并验证文案
        RemotePush().is_device_notify_ringtone_on()
        device_notify_ringtone_text_status = RemotePush().click_and_test_visitor_phone_remind(
            texts=remote_items['device_notify_ringtone']['text'])

        # 遍历报警铃声
        RemotePush().click_and_test_device_notify_ringtone(
            option_text_list=remote_items['device_notify_ringtone']['alarm_ring']['option_text'])

        # 断言
        assert device_notify_ringtone_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("计划")
    @allure.story("需人工核查日志和录屏")
    def test_push_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['push']['items']
        BasePage().check_key_in_yaml(remote_items, 'schedule')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_push_notifications(device_list_name=device_config['device_list_name'])

        # 验证手机推送主页的 计划 文案 和 计划页的文案，验证报警类型
        push_plan_text_status = RemotePush().check_plan_text(texts_list=remote_items['schedule']['text'])  # 验证手机推送主页的 计划 文案
        plan_text_status = RemotePush().click_and_test_push_plan(texts_list=remote_items['schedule']['subpage']['text'])  # 计划页的文案
        push_alarm_type_text = RemotePush().click_and_test_push_alarm_type(texts_list=remote_items['schedule']['subpage']['subpage']['text'])  # 验证报警类型文案

        # 测试推送间隔和文案
        push_interval_text_status = RemotePush().check_push_interval_text(texts_list=remote_items['schedule']['push_interval']['text'])
        RemotePush().click_and_test_push_interval(option_text_list=remote_items['schedule']['push_interval']['option_text'])

        # 断言
        assert push_plan_text_status is True
        assert plan_text_status is True
        assert push_alarm_type_text is True
        assert push_interval_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("延时通知")
    @allure.story("需人工核查日志和录屏")
    def test_push_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['push']['items']
        BasePage().check_key_in_yaml(remote_items, 'delay_notifications')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_push_notifications(device_list_name=device_config['device_list_name'])

        # 遍历延迟时间
        RemotePush().click_and_test_delay_notifications(
            option_text_list=remote_items['delay_notifications']['delay_time']['option_text'])
