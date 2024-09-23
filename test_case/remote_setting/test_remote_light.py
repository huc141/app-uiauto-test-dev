# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_light import RemoteLight

devices_config = read_yaml.load_device_config(yaml_file_name='light.yaml')  # 读取参数化文件


@allure.feature("远程配置>灯")
class TestRemoteLight:
    # 测红外灯
    @pytest.mark.parametrize("device_config", devices_config)
    @pytest.mark.skip
    def test_remote_infrared_light(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']
        BasePage().check_key_in_yaml(remote_items, 'infrared_light')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 遍历并滚动查找当前页面功能项，判断是否存在
        remote_funs_text = device_config['ipc']['light']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 获取yaml文件指定key的值
        remote_setting_display = device_config['ipc']['light']['items'].values()
        page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 进入灯>红外灯
        RemoteLight().click_infrared_light()

        # 测试红外灯：自动
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['infrared_light']['subpage']['options'][1])
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['infrared_light']['subpage']['options'][0])
        RemoteSetting().back_previous_page_by_xpath()
        light_status_auto = RemoteSetting().scroll_check_funcs2('自动')

        # 测试红外灯：关闭
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['infrared_light']['subpage']['options'][0])
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['infrared_light']['subpage']['options'][1])
        RemoteSetting().back_previous_page_by_xpath()
        light_status_off = RemoteSetting().scroll_check_funcs2('保持关闭')

        # 断言
        assert page_fun is True
        assert light_status_auto is True
        assert light_status_off is True

    # 测照明灯(白光灯)
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.story("需人工核查录屏")
    def test_remote_floodlight(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['light']['items']
        BasePage().check_key_in_yaml(remote_items, 'floodlight')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        # RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 获取yaml文件指定配置
        remote_items = device_config['ipc']['light']['items']

        # 遍历并滚动查找当前页面功能项，判断是否存在
        remote_funs_text = device_config['ipc']['light']['text']

        # 获取yaml文件指定key的值
        remote_setting_display = device_config['ipc']['light']['items'].values()
        # page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_display, 'name')

        # 进入灯>照明灯
        # RemoteLight().click_floodlight()

        # 测试夜间智能模式：保存
        # RemoteLight().click_night_smart_mode()
        # BasePage().click_checkbox_by_text(
        #     option_text_list=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'],
        #     menu_text='侦测')
        # BasePage().scroll_and_click_by_text(
        #     text_to_find=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'][0])
        # BasePage().scroll_and_click_by_text(text_to_find='保存')

        # 测试夜间智能模式：取消
        # RemoteLight().click_night_smart_mode()
        # BasePage().click_checkbox_by_text(
        #     option_text_list=remote_items['floodlight']['subpage']['night_smart_mode']['hidden_text'],
        #     menu_text='侦测')
        # BasePage().scroll_and_click_by_text(text_to_find='取消')

        # 测试定时模式：取消
        RemoteLight().click_timer_mode()  # 点击定时模式
        # 点击 开始
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][0])
        # 选择时、分
        RemoteLight().time_selector()
        # 点击取消
        BasePage().scroll_and_click_by_text(
            text_to_find='取消')

        RemoteLight().click_timer_mode()
        # 点击 结束
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][1])
        RemoteLight().time_selector()
        # 点击取消
        BasePage().scroll_and_click_by_text(
            text_to_find='取消')

        BasePage().scroll_and_click_by_text(
            text_to_find='保存')
