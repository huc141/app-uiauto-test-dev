# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_detection_alarm import RemoteDetectionAlarm
from pages.rn_device_setting_page.remote_light import RemoteLight
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='detection_alarm.yaml')  # 读取参数化文件


@allure.feature("远程配置>侦测报警")
class TestRemoteDetectionAlarm:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("测非侦测区域")
    @allure.story("需人工核查日志和录屏")
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 遍历并滚动查找当前侦测报警主页面功能项，判断是否存在
        remote_funs_text = device_config['ipc']['detection_alarm']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 进入侦测报警>非侦测区域
        RemoteDetectionAlarm().click_non_detection_area()

        # 测试绘制非侦测区域: 竖屏
        RemoteDetectionAlarm().draw_portrait_non_detection_area()

        # 测试绘制非侦测区域: 横屏
        RemoteDetectionAlarm().draw_landscape_non_detection_area()

        # 断言
        assert page_fun is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("测移动标记")
    @allure.story("需人工核查日志和录屏")
    def test_remote_motion_mark(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'motion_mark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>移动标记
        RemoteDetectionAlarm().click_motion_mark_switch()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("测灵敏度")
    @allure.story("需人工核查日志和录屏")
    def test_remote_motion_mark(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'sensitivity_motion')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘灯’菜单项进入灯主页
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>灵敏度
        RemoteDetectionAlarm().click_sensitivity_motion()

        # 灵敏度主页功能项验证，判断是否存在
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 测移动侦测
        RemoteDetectionAlarm().click_motion_detect()  # 点击移动侦测
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['motion_detect']['text']
        motion_detect_text = RemoteSetting().scroll_check_funcs2(remote_funs_text)
        # TODO: 拖动滑动条

        # 添加分段灵敏度
        RemoteDetectionAlarm().click_add_multi_time_sensitivity_motion()
        # 编辑灵敏度分段：取消
        BasePage().scroll_and_click_by_text(
            text_to_find=remote_items['floodlight']['subpage']['timer_mode']['hidden_text'][0])  # 选择 开始 时间
        RemoteLight().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 点击取消




        # 断言
        assert page_fun is True
        assert motion_detect_text is True

