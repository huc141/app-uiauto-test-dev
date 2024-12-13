# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_audio import RemoteAudio

devices_config = read_yaml.load_device_config(yaml_file_name='audio.yaml')   # 读取参数化文件


@allure.epic("远程配置>常规设置>音频")
class TestRemoteAudio:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>自动回复>等待时长")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_waiting_time(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']['auto_reply']
        BasePage().check_key_in_yaml(remote_items, 'waiting_time')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 点击并测试等待时长
        texts_res = RemoteAudio().click_test_waiting_time(texts=remote_items['waiting_time']['text'],
                                                          option_text_list=remote_items['waiting_time']['option_text'])

        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>自动回复>录制自动回复")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_record_autoresponders(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']['auto_reply']
        BasePage().check_key_in_yaml(remote_items, 'record_autoresponders')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 点击自动回复
        RemoteAudio().click_auto_reply()

        # 点击录制自动回复，暂时仅验证文案
        texts_res = RemoteAudio().click_record_auto_reply(texts=remote_items['record_autoresponders']['text'])

        assert texts_res is True




















