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
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 夜间智能模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_floodlight_night_smart(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'night_smart_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 夜间智能模式： 保存
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        key_res = BasePage().is_key_in_yaml(remote_items['night_smart_mode'], 'detect_type')  # 获取是否支持侦测
        floodlight_main_text_res = RemoteLight().click_test_floodlight_night_smart_mode(lights_num=lights_num,
                                                                                        supported_detect_type=key_res,
                                                                                        flood_light_texts=remote_items[
                                                                                            'night_smart_mode']['text'],
                                                                                        options_text=remote_items[
                                                                                            'night_smart_mode'][
                                                                                            'detect_type'][
                                                                                            'option_text'])

        assert floodlight_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 定时模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_floodlight_timer_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'timer_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 定时模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        timer_main_text_res = RemoteLight().click_test_floodlight_timer_mode(lights_num=lights_num,
                                                                             flood_light_texts=remote_items[
                                                                                 'timer_mode']['text'])

        assert timer_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 关 模式")
    @pytest.mark.skip
    def test_remote_floodlight_off(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_off_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 关闭模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        light_off_main_text_res = RemoteLight().click_test_light_off_mode(lights_num=lights_num,
                                                                          flood_light_texts=remote_items[
                                                                              'light_off_mode']['text'])

        assert light_off_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 自动模式")
    @pytest.mark.skip
    def test_remote_floodlight_auto(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'auto_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 关闭模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        flood_light_texts = RemoteLight().click_test_light_auto_mode(lights_num=lights_num,
                                                                     flood_light_texts=remote_items[
                                                                         'auto_mode']['text'])

        assert flood_light_texts is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 智能模式")
    @pytest.mark.skip
    def test_remote_floodlight_smart(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'smart_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 智能模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        key_res = BasePage().is_key_in_yaml(remote_items['smart_mode'], 'detect_type')  # 获取是否支持侦测
        flood_light_texts = RemoteLight().click_test_floodlight_smart_mode(lights_num=lights_num,
                                                                           supported_detect_type=key_res,
                                                                           flood_light_texts=remote_items['smart_mode'][
                                                                               'text'],
                                                                           options_text=
                                                                           remote_items['smart_mode']['detect_type'][
                                                                               'option_text'])

        assert flood_light_texts is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯/泛光灯) > 夜视常亮 模式")
    @pytest.mark.skip
    def test_remote_floodlight_night_vision_steady_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'night_vision_steady_light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 夜视常亮模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        light_off_main_text_res = RemoteLight().click_test_floodlight_night_vision_steady_light_mode(
            lights_num=lights_num,
            flood_light_texts=remote_items['night_vision_steady_light']['text'])

        assert light_off_main_text_res is True
