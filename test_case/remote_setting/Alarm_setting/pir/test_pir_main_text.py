# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_pir_setting import RemotePirSetting

devices_config = read_yaml.load_device_config(yaml_file_name='pir.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警设置>PIR传感器")
class TestRemotePIRSetting:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("PIR传感器>主页 文案")
    @allure.story("需人工核查日志和录屏")
    @allure.title('测试远程设置的PIR传感器主页开和关状态下的文本')
    def test_remote_pir_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['pir']['items']['pir']
        BasePage().check_key_in_yaml(remote_items, 'text')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘显示’菜单项进入显示主页
        RemoteSetting().access_in_pir(device_list_name=device_config['device_list_name'])

        # 验证PIR传感器主页的文案
        RemotePirSetting().check_pir_main_text(text1=remote_items['text'],
                                               text2=remote_items['options'])

