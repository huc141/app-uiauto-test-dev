# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

devices_config = read_yaml.load_device_config(device_dir='apower/AReolink_TrackMix_WiFi', yaml_file_name='display.yaml')  # 读取参数化文件


# TODO: 需要适配为RN
@allure.epic("远程配置>常规设置>显示>白天和黑夜")
class TestRemoteDisplay:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("白天和黑夜")
    def test_remote_day_and_night(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'day_and_night')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击白天和黑夜，验证popup文本
        RemoteDisplay().click_day_and_night()
        RemoteSetting().scroll_check_funcs2(remote_items['day_and_night']['text'])
        RemoteSetting().scroll_check_funcs2(remote_items['day_and_night']['options'], selector='ReoTitle')
        # 遍历popup操作项
        BasePage().iterate_and_click_popup_text(
            option_text_list=remote_items['anti_flicker']['options'], menu_text='白天和黑夜')
