# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_camera_record import RemoteCameraRecord

devices_config = read_yaml.load_device_config(device_dir='battery/Reolink Video Doorbell-1AA1',
                                              yaml_file_name='camera_record.yaml')  # 读取参数化文件


@allure.epic("远程配置>摄像机录像")
class TestRemoteCameraRecord:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("摄像机录像>摄像机录像主页文案")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试报摄像机录像主页文案")
    def test_remote_alarm_record_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['camera_record']['items']
        BasePage().check_key_in_yaml(remote_items, 'camera_record')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘摄像机录像’菜单项进入
        RemoteSetting().access_in_camera_record(device_list_name=device_config['device_list_name'])

        # 验证摄像机录像主页文案
        RemoteCameraRecord().check_camera_record_main_text(text=remote_items['camera_record']['text'],
                                                           options=remote_items['camera_record']['options'])







