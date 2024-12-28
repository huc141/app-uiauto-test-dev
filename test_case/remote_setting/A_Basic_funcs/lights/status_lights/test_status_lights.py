# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_light import RemoteLight

devices_config = read_yaml.load_device_config(yaml_file_name='light.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>灯")
class TestRemoteLight:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>状态灯 > 关闭 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("验证关闭状态灯")
    def test_status_lights_off(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'status_lights')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试状态灯 > 关闭模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().click_test_status_lights_off(lights_num=lights_num)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>状态灯 > 开启 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("验证开启状态灯")
    def test_status_lights_on(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'status_lights')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试状态灯 > 开启模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().click_test_status_lights_on(lights_num=lights_num)


