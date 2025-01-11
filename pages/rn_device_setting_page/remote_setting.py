# -*- coding: utf-8 -*-
import time
import pytest
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
_access_mode = g_config.get('access_mode')  # 设备接入方式
_nvr_name = g_config.get('nvr_name')  # nvr名称
_hub_name = g_config.get('hub_name')  # hub名称


class RemoteSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.ivSelectChannelButton = '//*[@resource-id="com.mcu.reolink:id/ivSelectChannelButton"]'  # nvr的通道按钮
            self.base_navigationbar_title = '//*[@resource-id="com.mcu.reolink:id/base_navigationbar_title"]'  # 页面标题栏
            self.base_left_button = '//*[@resource-id="com.mcu.reolink:id/base_left_button"]'  # 页面标题栏的返回按钮

        elif self.platform == 'ios':
            self.ivSelectChannelButton = '(//XCUIElementTypeButton)[2]'
            self.base_navigationbar_title = ''
            self.base_left_button = ''

    @staticmethod
    def extract_yaml_names(dict_list, key):
        """
        从给定的字典列表中提取指定键的值。
        参数:
            yaml_content: 包含字典的列表。
            key (list): 要提取的键名。

        返回:
            list: 包含所有提取的name的列表。
        """
        # 初始化空列表
        all_names = []

        # 遍历指定的keys
        for item in dict_list:
            if key in item:
                all_names.append(item[key])
        return all_names

    def scroll_check_funcs(self, texts, scroll_or_not=True, back2top=True):
        """
        遍历并判断功能项(名称)是否存在当前页面
        :param texts: 存储了预期功能项名称的列表。
        :param scroll_or_not: 是否执行滚动查找。布尔值，默认True滚动查找
        :param back2top:
        :return: bool
        """
        ele_exists = []
        ele_not_exists = []

        try:
            time.sleep(1)
            if isinstance(texts, list):
                # 如果 texts 是一个列表，遍历列表中的每个功能项名称
                for text in texts:
                    ele_status = self.is_element_exists(element_value=text, max_scrolls=5, scroll_or_not=scroll_or_not)
                    if ele_status:
                        ele_exists.append(text)
                    else:
                        ele_not_exists.append(text)

                if len(ele_not_exists) > 0:
                    logger.info(f"当前页面存在的功能有：{ele_exists}")
                    logger.warning(f"当前页面缺失的功能有：{ele_not_exists}")
                    if back2top:
                        self.back_to_page_top()
                    pytest.fail(f"当前页面缺失的功能有：{ele_not_exists}")

                else:
                    logger.info(f"需校验的功能项均存在！-->{ele_exists}")
                    if back2top:
                        self.back_to_page_top()
                    return True

            elif isinstance(texts, str):
                # 如果 texts 是一个单一的文本，在当前页面滚动查找该文本是否存在
                ele_status = self.is_element_exists(texts, scroll_or_not=scroll_or_not)
                if not ele_status:
                    logger.warning(f"当前页面缺失的功能有：{texts}")
                    if back2top:
                        self.back_to_page_top()
                    pytest.fail(f"当前页面缺失的功能有：{texts}")
                else:
                    logger.info(f"需校验的功能项均存在！-->{texts}")
                    if back2top:
                        self.back_to_page_top()
                    return True

        except Exception as err:
            if back2top:
                self.back_to_page_top()
            logger.error(f"函数执行出错: {err}")
            # return False

    def scroll_check_funcs2(self, texts, selector=None, selector_type='id', scroll_or_not=True, back2top=True):
        """
        遍历并判断功能项(名称)是否存在当前页面，同时比对数量是否正确。
        :param texts: 待验证的文案列表
        :param selector: 元素定位的具体id。
        :param selector_type: 元素的定位方式，根据id进行文本提取。
        :param texts: 存储了预期功能项名称的列表。
        :param scroll_or_not: 是否执行滚动查找。布尔值，默认True滚动查找
        :param back2top: 查找结束后是否返回页面顶部(可能会失败)。布尔值，默认True返回。
        :return:
        """
        ele_exists = []  # 预期存在的功能
        ele_not_exists = []  # 当前页面缺失的功能

        try:
            time.sleep(1)
            if selector is not None:
                # 先滚动页面提取指定id的文本（功能项）
                actual_texts = self.get_all_texts(selector=selector,
                                                  selector_type=selector_type,
                                                  max_scrolls=5)

                if isinstance(texts, list):
                    # 如果 texts 是一个列表，遍历yaml文件中的每个功能项名称是否存在actual_texts列表中
                    for text in texts:
                        is_in_actual_texts = text in actual_texts
                        if is_in_actual_texts:
                            ele_exists.append(text)
                        else:
                            ele_not_exists.append(text)

                    # 检查所有预期功能是否在actual_texts中，并检查两个列表的长度是否相同
                    all_elements_exist = all(ele_exists)
                    lengths_are_equal = len(actual_texts) == len(texts)

                    if all_elements_exist and lengths_are_equal and ele_not_exists == []:
                        logger.info(f"预期功能项均存在！-->{texts}")
                        if back2top:
                            self.back_to_page_top()
                        return True

                    elif len(actual_texts) > len(texts):
                        unique_fun = [item for item in actual_texts if item not in texts]
                        if back2top:
                            self.back_to_page_top()
                        logger.info(f"预期功能项有：{texts}")
                        logger.info(f"当前页面实际功能项有：{actual_texts}")
                        logger.warning(f"当前页面缺失的功能有：{ele_not_exists}")
                        logger.warning(f"当前页面多余的功能有：{unique_fun}，功能数量与预期不符！可能存在非法能力集！")
                        pytest.fail(f"当前页面多余的功能有：{unique_fun}，缺失的功能有：{ele_not_exists}, 功能数量与预期不符！可能存在非法能力集！")

                    else:
                        unique_fun = [item for item in actual_texts if item not in texts]
                        # 将当前页面滑动回顶部
                        if back2top:
                            self.back_to_page_top()
                        logger.info(f"预期功能项有：{texts}")
                        logger.info(f"当前页面实际功能项有：{actual_texts}")
                        logger.warning(f"当前页面缺失的功能有：{ele_not_exists}")
                        logger.warning(f'当前页面多余的功能有：{unique_fun}')
                        pytest.fail(f"当前页面缺失的功能有：{ele_not_exists}")

                elif isinstance(texts, str):
                    # 如果 texts 是一个单一的文本，在当前页面滚动查找该文本是否存在
                    ele_status = self.is_element_exists(element_value=texts, max_scrolls=5, scroll_or_not=scroll_or_not)
                    if not ele_status:
                        if back2top:
                            self.back_to_page_top()
                        logger.warning(f"当前页面缺失的功能有：{texts}")
                        pytest.fail(f"当前页面缺失的功能有：{texts}")
                    else:
                        logger.info(f"需校验的功能项均存在！-->{texts}")
                        if back2top:
                            self.back_to_page_top()
                        return True

            else:
                return self.scroll_check_funcs(texts=texts, scroll_or_not=scroll_or_not, back2top=back2top)

            # 将当前页面滑动回顶部
            if back2top:
                self.back_to_page_top()

        except Exception as err:
            if back2top:
                self.back_to_page_top()
            logger.info(f"可能发生了错误: {err}")
            return False

    def scroll_click_remote_setting(self, device_list_name):
        """
        逐一滚动查找设备在设备列表的名称并点击远程设置按钮
        :param device_list_name: 要查找的设备名称
        :return:
        """
        try:
            self.access_in_remote_setting(text_to_find=device_list_name)
        except Exception as e:
            pytest.fail(f"查找设备在设备列表的名称并点击远程设置按钮出错：{str(e)}")

    def access_in_remote_pre_recording(self, device_list_name, sub_name=None, access_mode=_access_mode):
        """
        进入指定设备的远程配置的预录模式主页
        :param device_list_name: 设备列表里单机设备、hub、nvr的昵称。
        :param sub_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param access_mode: 设备接入方式，支持ipc、hub、nvr。明确设备是单机还是接入NVR下、接入hub下。
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入预录模式主页
                self.scroll_and_click_by_text('预录模式')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入预录模式主页
                self.scroll_and_click_by_text('预录模式')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入预录模式主页
                self.scroll_and_click_by_text('预录模式')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_remote_wifi(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        进入指定设备的远程配置的wifi页面.
        接入hub、nvr的设备名称在命名时不能过长导致省略隐藏。
        :param device_list_name: 设备列表里单机设备、hub、nvr的昵称。
        :param nvr_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param hub_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param access_mode: 设备接入方式，支持ipc、hub、nvr。明确设备是单机还是接入NVR下、接入hub下。
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('Wi-Fi')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('Wi-Fi')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('Wi-Fi')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_battery(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        进入指定设备的远程配置的电池页面.
        接入hub、nvr的设备名称在命名时不能过长导致省略隐藏。
        :param device_list_name: 设备列表里单机设备、hub、nvr的昵称。
        :param nvr_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param hub_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param access_mode: 设备接入方式，支持ipc、hub、nvr。明确设备是单机还是接入NVR下、接入hub下。
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('电池')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('电池')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('电池')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_display(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击显示，进入显示页面
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                # 进入显示主页
                self.loop_detect_element_and_click('显示')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入显示主页
                self.loop_detect_element_and_click('显示')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入显示主页
                self.loop_detect_element_and_click('显示')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_audio(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击音频，进入音频页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入灯主页
                self.scroll_and_click_by_text('音频')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入灯主页
                self.scroll_and_click_by_text('音频')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入灯主页
                self.scroll_and_click_by_text('音频')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_light(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击灯，进入灯主页或者灯的配置页。
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入灯主页
                self.loop_detect_element_and_click('灯')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入灯主页
                self.loop_detect_element_and_click('灯')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入灯主页
                self.loop_detect_element_and_click('灯')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_detection_alarm(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击侦测报警，进入侦测报警页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入侦测报警主页
                self.scroll_and_click_by_text('侦测报警')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入侦测报警主页
                self.scroll_and_click_by_text('侦测报警')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入侦测报警主页
                self.scroll_and_click_by_text('侦测报警')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_camera_record(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击摄像机录像，进入摄像机录像页
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入灯主页
                self.loop_detect_element_and_click('摄像机录像')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入灯主页
                self.loop_detect_element_and_click('摄像机录像')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入灯主页
                self.loop_detect_element_and_click('摄像机录像')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_cloud_recording(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击云录像，进入云录像页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入云录像主页
                self.scroll_and_click_by_text('云录像')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入云录像主页
                self.scroll_and_click_by_text('云录像')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入云录像主页
                self.scroll_and_click_by_text('云录像')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_push_notifications(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击手机推送，进入手机推送页
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('手机推送')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('手机推送')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('手机推送')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_email_alerts(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击邮件通知，进入邮件通知页
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入邮件通知主页
                self.loop_detect_element_and_click('邮件通知')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入邮件通知主页
                self.loop_detect_element_and_click('邮件通知')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入邮件通知主页
                self.loop_detect_element_and_click('邮件通知')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_ftp(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击FTP，进入FTP页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入FTP主页
                self.scroll_and_click_by_text('FTP')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入FTP主页
                self.scroll_and_click_by_text('FTP')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入FTP主页
                self.scroll_and_click_by_text('FTP')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_pir(self, device_list_name, nvr_name=_nvr_name, hub_name=_hub_name, access_mode=_access_mode):
        """
        点击PIR传感器，进入PIR传感器页
        :return:
        """
        try:
            # 如果设备是单机：
            if access_mode == 'ipc':
                # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
                self.access_in_remote_setting(device_list_name)
                time.sleep(2)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('PIR 传感器')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and nvr_name is not None:
                # 根据昵称在设备列表中滚动查找该nvr设备并进入远程配置主页
                self.access_in_remote_setting(nvr_name)
                time.sleep(2)
                self.loop_detect_element_and_click(self.ivSelectChannelButton, selector_type='xpath')
                # 选择通道并点击
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('PIR 传感器')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and hub_name is not None:
                # 根据昵称在设备列表中滚动查找该hub设备并进入远程配置主页
                self.access_in_remote_setting(hub_name)
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.loop_detect_element_and_click(device_list_name)
                # 进入PIR传感器主页
                self.loop_detect_element_and_click('PIR 传感器')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_siren(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击鸣笛，进入鸣笛页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('鸣笛')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('鸣笛')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('鸣笛')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_linked_devices(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击已联动的设备，进入已联动的设备页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入已联动的设备主页
                self.scroll_and_click_by_text('已联动的设备')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入已联动的设备主页
                self.scroll_and_click_by_text('已联动的设备')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入已联动的设备主页
                self.scroll_and_click_by_text('已联动的设备')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_share_camera(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击分享摄像机，进入分享摄像机页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入分享摄像机主页
                self.scroll_and_click_by_text('分享摄像机')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入分享摄像机主页
                self.scroll_and_click_by_text('分享摄像机')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入分享摄像机主页
                self.scroll_and_click_by_text('分享摄像机')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_time_lapse(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击延时摄影，进入延时摄影页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入延时摄影主页
                self.scroll_and_click_by_text('延时摄影')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入延时摄影主页
                self.scroll_and_click_by_text('延时摄影')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入延时摄影主页
                self.scroll_and_click_by_text('延时摄影')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_advanced(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击高级设置，进入高级设置页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('高级设置')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('高级设置')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入鸣笛主页
                self.scroll_and_click_by_text('高级设置')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def access_in_privacy_mode(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        点击隐私模式，进入隐私模式主页
        :return:
        """
        try:
            # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
            self.access_in_remote_setting(device_list_name)

            # 如果设备是单机：
            if access_mode == 'ipc':
                time.sleep(2)
                # 进入隐私模式主页
                self.loop_detect_element_and_click('隐私模式')

            # 如果设备接入了nvr：
            elif access_mode == 'nvr' and sub_name is not None:
                time.sleep(2)
                self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
                # 选择通道并点击
                self.scroll_and_click_by_text(sub_name)
                # 进入隐私模式主页
                self.loop_detect_element_and_click('隐私模式')

            # 如果设备接入了hub：
            elif access_mode == 'hub' and sub_name is not None:
                time.sleep(2)
                # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
                self.scroll_and_click_by_text(sub_name)
                # 进入隐私模式主页
                self.loop_detect_element_and_click('隐私模式')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
