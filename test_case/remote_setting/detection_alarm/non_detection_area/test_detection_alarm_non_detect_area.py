# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_detection_alarm import RemoteDetectionAlarm
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='detection_alarm.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警设置>侦测报警")
class TestRemoteDetectionAlarm:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击人>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='人',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击车>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='车',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击车>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='动物',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("包裹-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['package']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击包裹>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='包裹',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("侦测报警主页>非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击测试侦测报警主页——>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        edit_texts_res = RemoteDetectionAlarm().clk_test_main_non_detect_area(
            edit_texts=remote_items['non_detection_area']['text'],
            is_both=is_both)

        # 断言
        assert edit_texts_res is True
