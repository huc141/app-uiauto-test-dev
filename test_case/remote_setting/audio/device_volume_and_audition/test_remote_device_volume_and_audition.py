# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_audio import RemoteAudio

devices_config = read_yaml.load_device_config(yaml_file_name='audio.yaml')   # 读取参数化文件


@allure.epic("远程配置>常规设置>音频")
class TestRemoteAudio:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>设备音量")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_device_volume_and_audition(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'device_volume_and_speaker_volume')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 对【设备音量】拖动条执行操作，支持上、下、左、右方向拖动。对试听按钮进行点击
        RemoteAudio().drag_slider_device_volume()