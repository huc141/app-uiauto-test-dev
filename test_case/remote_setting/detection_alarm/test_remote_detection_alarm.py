# -*- coding: utf-8 -*-
import pytest
import allure
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_detection_alarm import RemoteDetectionAlarm
from pages.rn_device_setting_page.remote_setting import RemoteSetting

devices_config = read_yaml.load_device_config(yaml_file_name='detection_alarm.yaml')  # 读取参数化文件


@allure.epic("远程配置>报警设置>侦测报警")
class TestRemoteDetectionAlarm:

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("侦测报警主页 文案")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_detection_alarm_main_text(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'detection_alarm')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击‘侦测报警’菜单项进入
        RemoteSetting().access_in_light(device_list_name=device_config['device_list_name'])

        # 验证侦测报警主页文案
        smart_tracking = BasePage().is_key_in_yaml(remote_items, 'smart_tracking')  # 获取该设备是否支持智能追踪
        main_text_res = RemoteDetectionAlarm().check_detection_alarm_main_text(
                                                main_text=remote_items['detection_alarm']['text'],
                                                smart_tracking=smart_tracking)

        # 断言
        assert main_text_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-目标尺寸")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_person_object_size(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'object_size')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试人——目标尺寸
        is_both = remote_items['object_size']['left_right_camera']
        main_texts_res, texts_res = RemoteDetectionAlarm().click_test_person_object_size(main_texts=remote_items['text'],
                                                                                         texts=remote_items['object_size']['text'],
                                                                                         is_both=is_both)
        # 断言
        assert main_texts_res is True
        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_person_non_detect_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击人>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='人',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-智能侦测")
    @allure.story("需人工核查日志和录屏")
    def test_remote_person_smart_detection(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'smart_detection')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试人——智能侦测
        RemoteDetectionAlarm().click_test_person_smart_detection()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-灵敏度")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_person_draw_sensitivity(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'sensitivity')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试人——灵敏度
        RemoteDetectionAlarm().clk_draw_sensitivity(non_detect_type='人')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("人-延时报警")
    @allure.story("需人工核查日志和录屏")
    def test_remote_person_alarm_delay(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['person']
        BasePage().check_key_in_yaml(remote_items, 'alarm_delay')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试人——智能侦测
        RemoteDetectionAlarm().click_test_person_alarm_delay()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-目标尺寸")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_car_object_size(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'object_size')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试车——目标尺寸
        is_both = remote_items['object_size']['left_right_camera']
        main_texts_res, texts_res = RemoteDetectionAlarm().click_test_car_object_size(main_texts=remote_items['text'],
                                                                                      texts=remote_items['object_size']['text'],
                                                                                      is_both=is_both)
        # 断言
        assert main_texts_res is True
        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-灵敏度")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_car_draw_sensitivity(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'sensitivity')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试车——灵敏度
        RemoteDetectionAlarm().clk_draw_sensitivity(non_detect_type='车')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_car_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击车>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='车',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-智能侦测")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_car_smart_detection(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'smart_detection')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试车——智能侦测
        RemoteDetectionAlarm().click_test_car_smart_detection()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("车-延时报警")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_car_alarm_delay(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['car']
        BasePage().check_key_in_yaml(remote_items, 'alarm_delay')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试车——智能侦测
        RemoteDetectionAlarm().click_test_car_alarm_delay()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-目标尺寸")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_animal_object_size(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'object_size')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试动物——目标尺寸
        is_both = remote_items['object_size']['left_right_camera']
        main_texts_res, texts_res = RemoteDetectionAlarm().click_test_animal_object_size(main_texts=remote_items['text'],
                                                                                         texts=remote_items['object_size']['text'],
                                                                                         is_both=is_both)
        # 断言
        assert main_texts_res is True
        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-灵敏度")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_animal_draw_sensitivity(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'sensitivity')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试动物——灵敏度
        RemoteDetectionAlarm().clk_draw_sensitivity(non_detect_type='动物')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_animal_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击车>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='动物',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-智能侦测")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_animal_smart_detection(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'smart_detection')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试动物——智能侦测
        RemoteDetectionAlarm().click_test_animal_smart_detection()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("动物-延时报警")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_animal_alarm_delay(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['animal']
        BasePage().check_key_in_yaml(remote_items, 'alarm_delay')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试动物——智能侦测
        RemoteDetectionAlarm().click_test_animal_alarm_delay()

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("包裹-目标尺寸")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_package_object_size(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['package']
        BasePage().check_key_in_yaml(remote_items, 'object_size')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试包裹——目标尺寸
        is_both = remote_items['object_size']['left_right_camera']
        main_texts_res, texts_res = RemoteDetectionAlarm().click_test_package_object_size(main_texts=remote_items['text'],
                                                                                          texts=remote_items['object_size']['text'],
                                                                                          is_both=is_both)
        # 断言
        assert main_texts_res is True
        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("包裹-灵敏度")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_package_draw_sensitivity(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['package']
        BasePage().check_key_in_yaml(remote_items, 'sensitivity')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试包裹——灵敏度
        RemoteDetectionAlarm().clk_draw_sensitivity(non_detect_type='包裹')

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("包裹-非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_package_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['package']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击包裹>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        RemoteDetectionAlarm().clk_test_ai_non_detect_area(non_detect_type='包裹',
                                                           edit_texts=remote_items['non_detection_area']['text'],
                                                           is_both=is_both)

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("MD/其他")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_motion_detect(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']['motion_detection']
        BasePage().check_key_in_yaml(remote_items, 'add_multi_time_sensitivity')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击并测试MD/其他-添加灵敏度分段
        main_texts_res, texts_res = RemoteDetectionAlarm().click_test_motion_detect(
            main_texts=remote_items['text'],
            add_multi_time_texts=remote_items['add_multi_time_sensitivity']['text'])

        # 断言
        assert main_texts_res is True
        assert texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("侦测报警主页>非侦测区域")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_main_non_detection_area(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'non_detection_area')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 点击测试侦测报警主页——>非侦测区域
        is_both = remote_items['non_detection_area']['left_right_camera']
        edit_texts_res = RemoteDetectionAlarm().clk_test_main_non_detect_area(edit_texts=remote_items['non_detection_area']['text'],
                                                                              is_both=is_both)

        # 断言
        assert edit_texts_res is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("智能追踪")
    @allure.story("需人工核查日志和录屏")
    def test_remote_smart_tracking(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'smart_tracking')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 开启并测试智能追踪
        options_dict = remote_items['smart_tracking']  # 传参字典
        result = RemoteDetectionAlarm().click_test_smart_tracking(options=options_dict)

        # 断言
        assert result['smart_tracking'] is True
        assert result['hril_tracking_range'] is True
        assert result['left_texts'] is True
        assert result['right_texts'] is True
        assert result['plan_text'] is True

    @pytest.mark.parametrize("device_config", devices_config)
    @allure.feature("移动标记")
    @allure.story("需人工核查日志和录屏")
    @pytest.mark.skip
    def test_remote_motion_mark(self, device_config):
        # 检查键是否存在，存在则执行当前用例，否则跳过
        remote_items = device_config['ipc']['detection_alarm']['items']
        BasePage().check_key_in_yaml(remote_items, 'motion_mark')

        # 启动app，并开启录屏
        driver.start_app(True)

        # 设备列表中滚动查找到单机、nvr、hub并进入远程配置，在远程设置主页点击菜单项@allure.feature进入侦测报警
        RemoteSetting().access_in_detection_alarm(device_list_name=device_config['device_list_name'])

        # 进入侦测报警>移动标记
        RemoteDetectionAlarm().click_motion_mark_switch()

        # 不确定移动标记在rn上加在哪里了(貌似放在了显示模块的一级菜单)
