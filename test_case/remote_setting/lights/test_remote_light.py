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
    @allure.feature("灯>灯主页 文案")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_lights_page_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']
        BasePage().check_key_in_yaml(remote_items, 'light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 验证灯主页文案
        lights_num = RemoteLight().verify_lights_list_length(texts=remote_items['light']['text'])  # 判断灯数量
        lights_main_text_res = RemoteLight().check_lights_main_text(lights_num=lights_num,
                                                                    texts=remote_items['light']['text'])

        # 断言
        assert lights_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>红外灯")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
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
        infrared_main_text_res = RemoteLight().click_and_test_infrared_light(lights_num=lights_num,
                                                                             infrared_light_texts=
                                                                             remote_items['infrared_light'][
                                                                                 'subpage']['text'],
                                                                             options_text=
                                                                             remote_items['infrared_light'][
                                                                                 'subpage']['options_text'])

        assert infrared_main_text_res is True

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
                                                                                        flood_light_texts=remote_items['night_smart_mode']['text'],
                                                                                        options_text=remote_items['night_smart_mode']['detect_type']['option_text'])

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
    def test_remote_floodlight_off(self, device_config):
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
    def test_remote_floodlight_off(self, device_config):
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
                                                                           flood_light_texts=remote_items['smart_mode']['text'],
                                                                           options_text=remote_items['smart_mode']['detect_type']['option_text'])

        assert flood_light_texts is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>状态灯 > 关闭 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_status_lights_off(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['status_lights']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_off_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试状态灯 > 关闭模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        status_lights_main_text_res = RemoteLight().click_test_status_lights_off(lights_num=lights_num,
                                                                                 status_lights_texts=remote_items[
                                                                                     'text'])

        assert status_lights_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>状态灯 > 开启 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_status_lights_off(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['status_lights']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_on_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试状态灯 > 开启模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        status_lights_main_text_res = RemoteLight().click_test_status_lights_on(lights_num=lights_num,
                                                                                status_lights_texts=remote_items[
                                                                                    'text'])

        assert status_lights_main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 关闭 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_doorbell_button_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['button_light']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_off_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 关闭模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        button_light__main_text_res = RemoteLight().click_doorbell_button_light_off(lights_num=lights_num,
                                                                                    button_light_texts=remote_items[
                                                                                        'text'])

        assert button_light__main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 自动 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_doorbell_button_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['button_light']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_auto_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 自动模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        button_light__main_text_res = RemoteLight().click_doorbell_button_light_auto(lights_num=lights_num,
                                                                                     button_light_texts=remote_items[
                                                                                         'text'])

        assert button_light__main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 自动且夜间常亮 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_doorbell_button_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['button_light']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_auto_on_night_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 自动且夜间常亮模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        button_light__main_text_res = RemoteLight().click_doorbell_button_light_auto_on_night(lights_num=lights_num,
                                                                                              button_light_texts=
                                                                                              remote_items['text'])

        assert button_light__main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>门铃按钮灯 > 常亮 模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_doorbell_button_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['light']['button_light']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_always_on_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试门铃按钮灯 > 常亮模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        button_light__main_text_res = RemoteLight().click_doorbell_button_light_always_on(lights_num=lights_num,
                                                                                          button_light_texts=
                                                                                          remote_items['text'])

        assert button_light__main_text_res is True
