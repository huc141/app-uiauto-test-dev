# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_share_camera import RemoteShareCamera

devices_config = read_yaml.load_device_config(yaml_file_name='email_alerts.yaml')  # 读取参数化文件


@allure.epic("远程配置>更多>分享摄像机")
class TestRemoteShareCamera:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("分享摄像机主页文案")
    @allure.story("需人工核查日志和录屏")
    def test_email_alerts_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']
        BasePage().check_key_in_yaml(remote_items, 'share_camera')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_email_alerts(device_list_name=device_config['device_list_name'])

        # 验证分享摄像机主页文案
        RemoteShareCamera().check_share_camera_main_text(texts=remote_items['share_camera']['text'])
