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
    @allure.feature("音频>音频主页 文案")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_audio_page_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']
        BasePage().check_key_in_yaml(remote_items, 'audio')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 验证音频主页文案
        main_text_res = RemoteAudio().check_audio_main_text(main_text=remote_items['audio']['text'])

        # 断言
        assert main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>录制声音")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_record_sound(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'record_audio')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 点击两次录制声音按钮
        RemoteAudio().click_test_record_sound()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>门铃按钮的声音")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_doorbell_button_sound(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'doorbell_button_sound')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 点击两次 门铃按钮的声音 按钮
        RemoteAudio().click_test_doorbell_button_sound()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>设备音量")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_device_volume_and_audition(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'device_volume_and_speaker_volume')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 对【设备音量】拖动条执行操作，支持上、下、左、右方向拖动。对试听按钮进行点击
        RemoteAudio().drag_slider_device_volume()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>试听")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_device_volume_and_audition(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'sound_test')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 对【设备音量】拖动条执行操作，支持上、下、左、右方向拖动。对试听按钮进行点击
        RemoteAudio().click_sound_test()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>音频降噪")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_noise_reduction(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['audio']['items']['audio']
        BasePage().check_key_in_yaml(remote_items, 'noise_reduction')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘音频’菜单项进入
        RemoteSetting().access_in_audio(device_list_name=device_config['device_list_name'])

        # 测试【音频降噪】拖动条，验证文案
        text_res = RemoteAudio().click_test_noise_reduction(texts=remote_items['audio']['noise_reduction']['text'])

        assert text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("音频>自动回复>等待时长")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_noise_reduction(self, device_config):
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
    def test_remote_noise_reduction(self, device_config):
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




















