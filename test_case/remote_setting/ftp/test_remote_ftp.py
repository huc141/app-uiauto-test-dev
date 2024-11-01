# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.rn_device_setting_page.remote_ftp import RemoteFtp

devices_config = read_yaml.load_device_config(device_dir='AReolink_TrackMix_WiFi', yaml_file_name='ftp.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警通知>FTP")
class TestRemoteFtp:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("FTP主页文案")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_ftp_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['ftp']['items']
        BasePage().check_key_in_yaml(remote_items, 'ftp')

        # 启动app，并开启录屏
        # driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        # RemoteSetting().access_in_ftp(device_list_name=device_config['device_list_name'])

        # 判断邮件通知按钮开关状态
        RemoteFtp().is_ftp_on(remote_items['ftp_config']['text'])

        # TODO: 验证主页文案

        # TODO: 断言

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("FTP配置")
    @allure.story("需人工核查日志和录屏")
    def test_ftp_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['ftp']['items']
        BasePage().check_key_in_yaml(remote_items, 'ftp_config')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_ftp(device_list_name=device_config['device_list_name'])

        # 检查FTP配置文案
        ftp_text_status = RemoteFtp().temp_check_ftp_text(ftp_config_text=remote_items['ftp_config']['text'])

        # 遍历传输模式
        transmission_mode_text_status = RemoteFtp().click_and_test_transmission_mode(
            transmission_mode_text=remote_items['ftp_config']['transmission_mode']['text'],
            transmission_mode_option_text=remote_items['ftp_config']['transmission_mode']['option_text'])

        # 遍历生成子目录
        generate_subdirectories_text_status = RemoteFtp().click_and_test_generate_subdirectories(
            generate_subdirectories_text=remote_items['ftp_config']['generate_subdirectories']['text'],
            generate_subdirectories_option_text=remote_items['ftp_config']['generate_subdirectories']['option_text'])

        # 遍历上传内容
        upload_text_status = RemoteFtp().click_and_test_upload(upload_text=remote_items['ftp_config']['upload']['text'],
                                                               upload_option_text=remote_items['ftp_config']['upload'][
                                                                   'option_text'])

        # TODO: 遍历视频-分辨率

        # 遍历FTP录像时长
        recording_extension_text_status = RemoteFtp().click_and_test_FTP_recording_extension(
            FTP_recording_extension_text=remote_items['ftp_config']['FTP_recording_extension']['text'],
            FTP_recording_extension_option_text=remote_items['ftp_config']['FTP_recording_extension']['option_text'])

        # 遍历文件最大容量
        maximum_video_size_text_status = RemoteFtp().click_and_test_maximum_video_size(
            maximum_video_size_text=remote_items['ftp_config']['maximum_video_size']['text'],
            maximum_video_size_option_text=remote_items['ftp_config']['maximum_video_size']['option_text'])

        # TODO:遍历视频-覆盖策略

        # TODO:遍历图片-分辨率

        # 遍历图片-间隔
        picture_interval_text_status = RemoteFtp().click_and_test_picture_interval(
            picture_interval_text=remote_items['ftp_config']['picture_interval']['text'],
            picture_interval_option_text=remote_items['ftp_config']['picture_interval']['option_text'])

        # TODO:遍历图片-覆盖策略

        # 断言
        assert ftp_text_status is True
        assert transmission_mode_text_status is True
        assert generate_subdirectories_text_status is True
        assert upload_text_status is True
        assert recording_extension_text_status is True
        assert maximum_video_size_text_status is True
        assert picture_interval_text_status is True
