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


@allure.epic("远程配置>报警设置>侦测报警")
class TestRemoteDetectionAlarm:
    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("非侦测区域")
    @allure.story("需人工核查日志和录屏")
    def test_remote_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
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
    @allure.feature("移动标记")
    @allure.story("需人工核查日志和录屏")
    def test_remote_motion_mark(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'motion_mark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>移动标记
        RemoteDetectionAlarm().click_motion_mark_switch()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灵敏度>移动侦测")
    @allure.story("需人工核查日志和录屏")
    def test_remote_sensitivity_motion_detect(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']
        BasePage().check_key_in_yaml(remote_items, 'motion_detect')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>灵敏度
        RemoteDetectionAlarm().click_sensitivity_motion()

        # 灵敏度主页功能项验证，判断是否存在
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['text']
        page_fun = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 测移动侦测
        RemoteDetectionAlarm().click_motion_detect()  # 点击移动侦测
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['motion_detect'][
            'text']
        motion_detect_text = RemoteSetting().scroll_check_funcs2(remote_funs_text)
        # TODO: 拖动滑动条

        # 测试灵敏度分段：取消
        RemoteDetectionAlarm().click_add_multi_time_sensitivity_motion()  # 添加分段灵敏度
        RemoteDetectionAlarm().click_start_time()  # 点击开始时间
        RemoteDetectionAlarm().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='确定')  # 点击确定
        RemoteDetectionAlarm().click_end_time()  # 点击结束时间
        RemoteDetectionAlarm().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='确定')  # 点击确定
        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 取消保存分段
        check_cancel_text = RemoteSetting().scroll_check_funcs2('编辑分段')  # 验证页面不存在“编辑分段”文案

        # 测试灵敏度分段：保存
        RemoteDetectionAlarm().click_add_multi_time_sensitivity_motion()  # 添加分段灵敏度
        RemoteDetectionAlarm().click_start_time()  # 点击开始时间
        RemoteDetectionAlarm().time_selector()  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='确定')  # 点击确定
        RemoteDetectionAlarm().click_end_time()  # 点击结束时间
        RemoteDetectionAlarm().time_selector(iteration=2)  # 选择时、分
        BasePage().scroll_and_click_by_text(text_to_find='确定')  # 点击确定
        BasePage().scroll_and_click_by_text(text_to_find='保存')  # 保存分段
        check_save_text = RemoteSetting().scroll_check_funcs2('编辑分段')  # 验证页面存在“编辑分段”文案

        # 测试灵敏度分段：删除
        RemoteDetectionAlarm().delete_multi_time_sensitivity_motion()
        check_delete_text = RemoteSetting().scroll_check_funcs2('编辑分段')  # 验证页面不存在“编辑分段”文案

        # 断言
        assert page_fun is True
        assert motion_detect_text is True
        assert check_cancel_text is False
        assert check_save_text is True
        assert check_delete_text is False

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("灵敏度>智能侦测")
    @allure.story("需人工核查日志和录屏")
    def test_remote_sensitivity_smart_detect(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']
        BasePage().check_key_in_yaml(remote_items, 'smart_detect')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>灵敏度
        RemoteDetectionAlarm().click_sensitivity_motion()

        # 测智能侦测
        RemoteDetectionAlarm().click_smart_detect()  # 点击智能侦测
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['smart_detect'][
            'text']
        motion_detect_text = RemoteSetting().scroll_check_funcs2(remote_funs_text)
        # TODO: 拖动滑动条：人
        # TODO: 拖动滑动条：车
        # TODO: 拖动滑动条：动物

        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 点击取消
        RemoteDetectionAlarm().click_smart_detect()  # 点击智能侦测
        BasePage().scroll_and_click_by_text(text_to_find='保存')  # 点击保存

        # 断言
        assert motion_detect_text is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("延时报警")
    def test_remote_sensitivity_alarm_delay(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'alarm_delay')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>延时报警
        RemoteDetectionAlarm().click_alarm_delay()

        # 验证文案
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['smart_detect'][
            'text']
        alarm_delay_text = RemoteSetting().scroll_check_funcs2(remote_funs_text)

        # 测延时报警：取消/保存
        BasePage().scroll_and_click_by_text(text_to_find='取消')  # 点击取消
        RemoteDetectionAlarm().click_alarm_delay()  # 点击延时报警
        BasePage().scroll_and_click_by_text(text_to_find='保存')  # 点击保存

        # 断言
        assert alarm_delay_text is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("目标尺寸")
    def test_remote_object_size(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'object_size')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>延时报警
        RemoteDetectionAlarm().click_alarm_delay()

        # 验证文案
        remote_funs_text = device_config['ipc']['detection_alarm']['items']['sensitivity_motion']['smart_detect'][
            'text']
        alarm_delay_text = RemoteSetting().scroll_check_funcs2(remote_funs_text)


