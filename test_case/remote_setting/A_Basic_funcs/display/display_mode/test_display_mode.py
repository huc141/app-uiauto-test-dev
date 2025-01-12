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


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>显示模式")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试图像布局的显示模式，分别点击不同的显示模式类型、并旋转画面")
    def test_display_mode(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'image_layout')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 前置条件：将图像布局设置为展开
        RemoteDisplay().set_image_layout_type(layout_type='展开',
                                              device_list_name=device_config['device_list_name'])

        # 进入显示模式页面，分别点击不同的显示模式类型、并旋转画面
        RemoteDisplay().verify_display_mode_and_rotating_picture()

        # 验证显示模式配置页文案
        # RemoteSetting().scroll_check_funcs2(remote_items['display_mode']['text'], back2top=False)
        # RemoteSetting().scroll_check_funcs2(remote_items['display_mode']['ReoCellGroup-Title'],
        #                                     selector='ReoCellGroup-Title',
        #                                     back2top=False)
        # RemoteSetting().scroll_check_funcs2(remote_items['display_mode']['ReoTitle'],
        #                                     selector='ReoTitle',
        #                                     back2top=False)

        RemoteDisplay().check_echo()
