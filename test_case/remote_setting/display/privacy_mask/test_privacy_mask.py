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


@allure.feature("远程配置>常规设置>显示")
class TestRemoteDisplay:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>遮盖区域")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入遮盖区域页面，点击弹窗的取消、清空并继续")
    @pytest.mark.skip
    def test_access_in_privacy_mask(self, device_config):
        # # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'private_mark')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        # RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入遮盖区域主页
        RemoteDisplay().access_in_privacy_mask()

        # 此处的定位方式默认xpath
        # RemoteDisplay().draw_privacy_mask(mode='xpath')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("显示>遮盖区域")
    @allure.story("需人工核查日志和录屏")
    @allure.title("测试进入遮盖区域页面，验证主页文本、左下角用户提示及文本、删除按钮、清空所有按钮、横屏按钮、返回竖屏按钮")
    def test_privacy_mask_main_texts(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['display']['items']['display']
        BasePage().check_key_in_yaml(remote_items, 'private_mark')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示页
        # RemoteSetting().access_in_display(device_list_name=device_config['device_list_name'])

        # 点击进入遮盖区域主页
        RemoteDisplay().access_in_privacy_mask()

        # 验证码流主页文本
        RemoteSetting().scroll_check_funcs2(remote_items['private_mark']['text'], back2top=False)

        # 左下角用户提示及文本
        RemoteDisplay().verify_user_tips(user_tips_text=remote_items['private_mark']['user_tips'])

        # 验证删除按钮
        # TODO:

        # 验证清空所有按钮
        # TODO:

        # 验证横屏按钮
        RemoteDisplay().verify_landscape_button()

        # 验证返回竖屏按钮
        RemoteDisplay().verify_portrait_button()
