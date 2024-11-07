# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_light import RemoteLight

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi', yaml_file_name='light.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>灯")
class TestRemoteLight:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>灯主页 文案")
    @allure.story("需人工核查日志和录屏")
    def test_remote_lights_page_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']
        BasePage().check_key_in_yaml(remote_items, 'light')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        # RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 验证灯主页文案
        lights_num = RemoteLight().verify_lights_list_length(texts=remote_items['light']['text'])  # 判断灯数量
        lights_main_text_res = RemoteLight().check_lights_main_text(lights_num=lights_num,
                                                                    texts=remote_items['light']['text'])

        # 断言
        assert lights_main_text_res is True
