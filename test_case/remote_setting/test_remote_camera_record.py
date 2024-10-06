# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_camera_record import RemoteCameraRecord

devices_config = read_yaml.load_device_config(yaml_file_name='camera_record.yaml')  # 读取参数化文件


@allure.epic("远程配置>摄像机录像")
class TestRemoteCameraRecord:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("报警录像>报警录像计划")
    @allure.story("需人工核查日志和录屏")
    def test_remote_alarm_recording_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['camera_record']['items']
        BasePage().check_key_in_yaml(remote_items, 'alarm_recording_plan')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_camera_record(device_list_name=device_config['device_list_name'])

        # 验证 摄像机主页>报警录像 文案内容
        remote_text = device_config['ipc']['camera_record']['alarm_recording_text']
        camera_recording_page_text_status = RemoteCameraRecord().check_camera_alarm_recording_page_text(texts_list=remote_text)

        # 验证 摄像机主页>报警录像>报警录像计划 文案内容
        remote_alarm_recording_plan_text = device_config['ipc']['camera_record']['items']['alarm_recording_plan']['text']
        alarm_recording_plan_text_status = RemoteCameraRecord().click_and_test_alarm_recording_plan(texts_list=remote_alarm_recording_plan_text)

        # 验证 摄像机主页>报警录像>报警录像计划>报警类型 文案内容
        alarm_type_text = device_config['ipc']['camera_record']['items']['alarm_recording_plan']['alarm_type']['text']
        alarm_type_text_status = RemoteCameraRecord().click_and_test_alarm_recording_plan(texts_list=alarm_type_text)

        # 断言
        assert camera_recording_page_text_status is True
        assert alarm_recording_plan_text_status is True
        assert alarm_type_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("报警录像>定时录像计划")
    @allure.story("需人工核查日志和录屏")
    def test_remote_alarm_recording_plan(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['camera_record']['items']
        BasePage().check_key_in_yaml(remote_items, 'timed_recording_plan')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_camera_record(device_list_name=device_config['device_list_name'])

        # 验证 摄像机主页>定时录像 文案内容
        remote_timed_text = device_config['ipc']['camera_record']['timed_recording_text']
        camera_timed_recording_page_text_status = RemoteCameraRecord().check_camera_timed_recording_page_text(
            texts_list=remote_timed_text)

        # 验证 摄像机主页>定时录像>定时录像计划 文案内容
        remote_alarm_recording_plan_text = device_config['ipc']['camera_record']['items']['timed_recording_plan'][
            'text']
        alarm_recording_plan_text_status = RemoteCameraRecord().check_timed_recording_text(
            texts_list=remote_alarm_recording_plan_text)

        # 断言
        assert camera_timed_recording_page_text_status is True
        assert alarm_recording_plan_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("报警录像>录像延时时长")
    @allure.story("需人工核查日志和录屏")
    def test_remote_record_delay_duration(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['camera_record']['items']
        BasePage().check_key_in_yaml(remote_items, 'record_delay_duration')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_camera_record(device_list_name=device_config['device_list_name'])

        # 验证录像延时时长文案
        record_delay_duration_text = device_config['ipc']['camera_record']['items']['record_delay_duration']['text']
        record_delay_duration_text_text_status = RemoteCameraRecord().check_camera_timed_recording_page_text(
            texts_list=record_delay_duration_text)

        # 点击录像延时时长，遍历点击延时时长选项
        record_delay_duration_option_text = device_config['ipc']['camera_record']['items']['record_delay_duration']['option_text']
        RemoteCameraRecord().click_and_test_record_delay_duration(option_text_list=record_delay_duration_option_text)

        # 断言
        assert record_delay_duration_text_text_status is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("报警录像>覆盖录像")
    @allure.story("需人工核查日志和录屏")
    def test_remote_overwrite_record(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['camera_record']['items']
        BasePage().check_key_in_yaml(remote_items, 'overwrite_record')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_camera_record(device_list_name=device_config['device_list_name'])

        # 点击两次覆盖录像的开关按钮
        RemoteCameraRecord().click_and_test_overwrite_record()
