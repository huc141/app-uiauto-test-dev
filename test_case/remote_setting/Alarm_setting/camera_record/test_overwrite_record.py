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
    # TODO: 覆盖录像待修改

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
