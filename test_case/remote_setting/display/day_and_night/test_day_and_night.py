# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi',
                                              yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示>白天和黑夜")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜>模式切换 主页文本")
    @pytest.mark.skip
    def test_remote_day_and_night_main_texts(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 验证白天和黑夜主页文本
        RemoteSetting().scroll_check_funcs2(remote_items['day_and_night']['text'])
        RemoteSetting().scroll_check_funcs2(remote_items['day_and_night']['options'], selector='ReoTitle')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜>模式切换")
    @pytest.mark.skip
    def test_remote_day_and_night_mode_switch(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')
        remote_items = device_config['ipc']['display']['items']['display']['day_and_night']
        BasePage().check_key_in_yaml(remote_items, 'mode_switching')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入白天和黑夜主页,点击进入并验证模式切换，遍历模式切换下的选项
        RemoteDisplay().verify_mode_switch(texts1=remote_items['mode_switching']['text'],
                                           texts2=remote_items['mode_switching']['options']
                                           )

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜>白天彩色")
    @pytest.mark.skip
    def test_remote_day_color(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')
        remote_items = device_config['ipc']['display']['items']['display']['day_and_night']
        BasePage().check_key_in_yaml(remote_items, 'day_color')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        # RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入白天和黑夜主页,点击进入并验证白天彩色，遍历白天彩色下的选项
        RemoteDisplay().verify_day_color(texts1=remote_items['day_color']['text'],
                                           texts2=remote_items['day_color']['options']
                                           )

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜>黑白")
    @pytest.mark.skip
    def test_remote_day_black_white(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')
        remote_items = device_config['ipc']['display']['items']['display']['day_and_night']
        BasePage().check_key_in_yaml(remote_items, 'black_and_white')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        # RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入白天和黑夜主页,点击进入并验证黑白，遍历黑白下的选项
        RemoteDisplay().verify_black_and_white(texts1=remote_items['black_and_white']['text'],
                                               texts2=remote_items['black_and_white']['options']
                                              )

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜>夜视彩色")
    def test_remote_day_black_white(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')
        remote_items = device_config['ipc']['display']['items']['display']['day_and_night']
        BasePage().check_key_in_yaml(remote_items, 'night_vision_color')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        # RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入白天和黑夜主页,点击进入并验证黑白，遍历黑白下的选项
        RemoteDisplay().verify_night_vision_color(texts1=remote_items['night_vision_color']['text'],
                                                  texts2=remote_items['night_vision_color']['options']
                                               )



















