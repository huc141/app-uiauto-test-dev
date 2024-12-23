# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_display import RemoteDisplay

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
device_dir = g_config.get("device_dir")  # 读取设备配置文件目录
devices_config = read_yaml.load_device_config(device_dir=device_dir,
                                              yaml_file_name='display.yaml')  # 读取参数化文件


@allure.epic("远程配置>常规设置>显示")
class TestRemoteDisplay:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>遮盖区域")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入遮盖区域页面，验证主页文本、左下角用户提示及文本、删除按钮、清空所有按钮、横屏按钮、返回竖屏按钮")
    def test_privacy_mask_main_texts(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'private_mark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入遮盖区域主页
        RemoteDisplay().access_in_privacy_mask()

        # 测试隐私遮盖相关按钮和文案
        RemoteDisplay().verify_privacy_mask(camera_type=remote_items['private_mark']['camera_type'],
                                            mask_num=remote_items['private_mark']['mask_num'])


