# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_cloud_recording import RemoteCloudRecord

devices_config = read_yaml.load_device_config(device_dir='apower/Reolink Video Doorbell WiFi-W',
                                              yaml_file_name='cloud_recording.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警设置>云录像")
class TestRemoteCloudRecording:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("云录像>存储时长主页 文案")
    @allure.story("需人工核查日志和录屏")
    def test_remote_cloud_storage_duration(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['cloud_recording']['items']
        BasePage().check_key_in_yaml(remote_items, 'storage_duration')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘云录像’菜单项进入
        RemoteSetting().access_in_cloud_recording(device_list_name=device_config['device_list_name'])

        # 验证存储时长主页文案
        RemoteCloudRecord().check_storage_duration_text()
