# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_light import RemoteLight

devices_config = read_yaml.load_device_config(yaml_file_name='light.yaml')  # 读取参数化文件


# 按钮灯仅门铃才有
@allure.epic("远程配置>常规设置>灯")
class TestRemoteLight:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>按钮灯 主页文案")
    @allure.story("需人工核查日志和录屏")
    @allure.title('验证按钮灯 主页文案')
    def test_remote_floodlight_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items, 'button_light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试按钮灯主页文案
        count_lights = remote_items['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().check_button_light_main_text(lights_num=lights_num)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 关闭 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title('验证门铃按钮灯关闭 模式')
    @pytest.mark.skip
    def test_doorbell_button_light_off(self, device_config):
        # 检查button_light键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'button_light')

        # 检查light_off_mode键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['button_light']
        BasePage().check_key_in_yaml(remote_items, 'light_off_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 关闭模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().verify_doorbell_button_light_off(lights_num=lights_num)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 自动 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title('验证门铃按钮灯自动 模式')
    @pytest.mark.skip
    def test_doorbell_button_light_auto(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'button_light')

        remote_items = device_config['ipc']['light']['items']['light']['button_light']
        BasePage().check_key_in_yaml(remote_items, 'light_auto_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 自动模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().verify_doorbell_button_light_auto(lights_num=lights_num)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 自动且夜间常亮 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title('验证门铃按钮灯自动且夜间常亮 模式')
    @pytest.mark.skip
    def test_doorbell_button_light_auto_night_steady_on(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'button_light')

        remote_items = device_config['ipc']['light']['items']['light']['button_light']
        BasePage().check_key_in_yaml(remote_items, 'light_auto_on_night_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 自动且夜间常亮模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().verify_doorbell_button_light_auto_on_night(lights_num=lights_num)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 常亮 模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title('验证门铃按钮灯 > 常亮 模式')
    @pytest.mark.skip
    def test_doorbell_button_light_steady_on(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items1 = device_config['ipc']['light']['items']['light']
        BasePage().check_key_in_yaml(remote_items1, 'button_light')

        remote_items = device_config['ipc']['light']['items']['light']['button_light']
        BasePage().check_key_in_yaml(remote_items, 'light_always_on_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 常亮模式
        count_lights = remote_items1['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().verify_doorbell_button_light_always_on(lights_num=lights_num)

