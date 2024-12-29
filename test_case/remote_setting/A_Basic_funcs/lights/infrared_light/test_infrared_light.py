# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_light import RemoteLight

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
device_dir = g_config.get("device_dir")  # 读取设备配置文件目录
devices_config = read_yaml.load_device_config(device_dir=device_dir,
                                              yaml_file_name='light.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>灯")
class TestRemoteLight:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>红外灯")
    @allure.story("需人工核查日志和录屏")
    @allure.title('测试红外灯配置页文案和操作选项')
    def test_remote_infrared_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items, 'infrared_light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试红外灯和配置
        lights_num = RemoteLight().verify_lights_list_length(texts=remote_items['text'])  # 判断灯数量
        RemoteLight().verify_and_test_infrared_light(lights_num=lights_num,
                                                     options_text=remote_items['infrared_light']['options'])

