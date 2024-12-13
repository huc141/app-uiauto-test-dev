# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_pre_record import RemotePreRecord

devices_config = read_yaml.load_device_config(device_dir='battery/Reolink TrackMix LTE Plus 2',
                                              yaml_file_name='pre_recording_mode.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>预录模式")
class TestRemotePreRecording:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("预录模式>预录模式主页 文案/设置停止预录电量")
    @allure.story("需人工核查日志和录屏")
    def test_remote_pre_record_main_page_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['pre_recording']['items']
        BasePage().check_key_in_yaml(remote_items, 'pre_recording')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘预录模式’菜单项进入
        RemoteSetting().access_in_remote_pre_recording(device_list_name=device_config['device_list_name'])

        # 验证预录模式主页文案
        main_text_res, illegal_funcs_res = RemotePreRecord().check_precording_main_text(main_text=remote_items['pre_recording']['text'])
        # illegal_funcs_res = BasePage().detect_illegal_functions(legal_funcs_ids=remote_items['pre_recording']['text'])

        # TODO: 设置停止预录电量
        RemotePreRecord().set_stop_pre_recording_power()

        # 断言
        assert main_text_res is True
        assert illegal_funcs_res is True
