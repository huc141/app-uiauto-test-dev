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
        lights_main_text_res = RemoteLight().check_lights_main_text(lights_num=lights_num, texts=remote_items['light']['text'])

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
        remote_items = device_config['ipc']['light']['items']['light']['floodlight']
        BasePage().check_key_in_yaml(remote_items, 'night_smart_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击并测试照明灯(白光灯/泛光灯) > 夜间智能模式
        count_lights = device_config['ipc']['light']['items']['light']['text']
        lights_num = RemoteLight().verify_lights_list_length(texts=count_lights)  # 判断灯数量
        RemoteLight().click_floodlight_night_smart_mode(lights_num=lights_num,
                                                        infrared_light_texts=remote_items['night_smart_mode']['text'],
                                                        options_text=remote_items['night_smart_mode']['option_text'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['light']['items']

        # 进入灯>照明灯
        RemoteLight().click_floodlight_night_smart_mode()

        # 测试夜间智能模式：保存
        RemoteLight().click_night_smart_mode()

        # 检查键是否存在，存在则执行当前用例，否则跳过
        is_event_type_exist = device_config['ipc']['light']['items']['floodlight']['subpage']['night_smart_mode']
        BasePage().check_key_in_yaml(is_event_type_exist, 'event_type')

        BasePage().click_checkbox_by_text(
            option_text_list=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'],
            menu_text='侦测')
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'][0])
        BasePage().scroll_and_click_by_text(text_to_find='保存')

        # 测试夜间智能模式：取消
        RemoteLight().click_night_smart_mode()
        BasePage().click_checkbox_by_text(
            option_text_list=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'],
            menu_text='侦测')
        BasePage().scroll_and_click_by_text(text_to_find='取消')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯) > 定时模式")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_floodlight_timer_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'timer_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['light']['items']

        # 进入灯>照明灯
        RemoteLight().click_floodlight()

        # 测试定时模式：取消
        RemoteLight().click_timer_mode()  # 点击定时模式
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][0])  # 选择 开始 时间
        RemoteLight().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 点击取消

        RemoteLight().click_timer_mode()  # 点击定时模式
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][1])  # 点击 结束 时间
        RemoteLight().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 点击取消

        # 测试定时模式：保存
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][0])  # 选择 开始 时间
        RemoteLight().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='保存')  # 点击保存

        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][1])  # 点击 结束 时间
        RemoteLight().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='保存')  # 点击保存

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灯>照明灯(白光灯) > 关 模式")
    @pytest.mark.skip
    def test_remote_floodlight_off(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']['floodlight']['subpage']
        BasePage().check_key_in_yaml(remote_items, 'light_off_mode')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 进入灯>照明灯
        RemoteLight().click_floodlight()

        # 测试 关 模式
        RemoteLight().click_light_off()
        RemoteSetting().back_previous_page_by_xpath()
        light_status_off = RemoteSetting().scroll_check_funcs2('关闭')

        assert light_status_off is True
