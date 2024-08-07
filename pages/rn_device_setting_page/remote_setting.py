# -*- coding: utf-8 -*-
import time
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.ivSelectChannelButton = '//*[@resource-id="com.mcu.reolink:id/ivSelectChannelButton"]'  # nvr的通道按钮

        elif self.platform == 'ios':
            self.ivSelectChannelButton = '(//XCUIElementTypeButton)[2]'

    # def check_remote_setting_text(self, expected_text, exclude_texts,
    #                               xml_az_parse_conditions, xml_ios_parse_conditions):
    #     """
    #     根据设备名，检查对应设备的远程配置功能是否和预期一致
    #     :param xml_az_parse_conditions: 安卓的远程配置主(一级)页面解析条件，用于排除无关文本，筛选出页面功能
    #     :param xml_ios_parse_conditions: iOS的远程配置主(一级)页面解析条件，用于排除无关文本，筛选出页面功能
    #     :param expected_text: 需要检查的预期文本
    #     :param exclude_texts: 需要排除的文本(额外添加需要排除的文本)
    #     :return:
    #     """
    #     return self.verify_page_text(expected_text=expected_text,
    #                                  exclude_texts=exclude_texts,
    #                                  xml_az_parse_conditions=xml_az_parse_conditions,
    #                                  xml_ios_parse_conditions=xml_ios_parse_conditions
    #                                  )

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

    def scroll_check_funcs(self, texts):
        """
        遍历并判断功能项是否存在当前页面
        :param texts: 存储了功能项名称的列表。
        :return: bool
        """
        ele_exists = []
        ele_not_exists = []

        if isinstance(texts, list):
            # 如果 texts 是一个列表，遍历列表中的每个功能项名称
            for text in texts:
                ele_status = self.is_element_exists(text)
                if ele_status:
                    ele_exists.append(text)
                else:
                    ele_not_exists.append(text)

            if len(ele_not_exists) > 0:
                logger.info(f"当前页面存在的功能有：{ele_exists}")
                logger.info(f"当前页面缺失的功能有：{ele_not_exists}")
                return False
            else:
                logger.info(f"需校验的功能项均存在！-->{ele_exists}")
                return True

        elif isinstance(texts, str):
            # 如果 texts 是一个单一的文本，在当前页面滚动查找该文本是否存在
            ele_status = self.is_element_exists(texts)
            if not ele_status:
                logger.info(f"当前页面缺失的功能有：{texts}")
                return False
            else:
                logger.info(f"需校验的功能项均存在！-->{texts}")
                return True

    def scroll_click_remote_setting(self, device_list_name):
        """
        逐一滚动查找设备在设备列表的名称并点击远程设置按钮
        :param device_list_name: 要查找的设备名称
        :return:
        """
        return self.access_in_remote_setting(text_to_find=device_list_name)

    def access_in_remote_wifi(self, device_list_name, sub_name=None, access_mode='ipc'):
        """
        进入指定设备的远程配置的wifi页面.
        接入hub、nvr的设备名称在命名时不能过长导致省略隐藏。
        :param device_list_name: 设备列表里单机设备、hub、nvr的昵称。
        :param sub_name: 若设备接入了hub、nvr设备下的话，则该名称必填。
        :param access_mode: 设备接入方式，支持ipc、hub、nvr。明确设备是单机还是接入NVR下、接入hub下。
        :return:
        """
        # 根据昵称在设备列表中滚动查找该设备并进入远程配置主页
        self.access_in_remote_setting(device_list_name)

        # 如果设备是单机：
        if access_mode == 'ipc':
            time.sleep(2)
            # 进入wifi主页
            self.scroll_and_click_by_text('Wi-Fi')

        # 如果设备接入了nvr：
        elif access_mode == 'nvr' and sub_name is not None:
            time.sleep(2)
            self.scroll_and_click_by_text(self.ivSelectChannelButton, el_type='xpath')
            # 选择通道并点击(但是设备接入nvr后不会显示wifi的远程配置)
            self.scroll_and_click_by_text(sub_name)
            logger.info("设备接入了nvr，页面不显示WiFi功能")

        # 如果设备接入了hub：
        elif access_mode == 'hub' and sub_name is not None:
            time.sleep(2)
            # 根据名称查找hub下的设备卡片，点击并进入hub下的设备的远程配置主页
            self.scroll_and_click_by_text(sub_name)
            # 进入wifi主页
            self.scroll_and_click_by_text('Wi-Fi')

    def access_in_display(self):
        """
        点击显示，进入显示页面
        :return:
        """
        return self.scroll_and_click_by_text('显示')

    def access_in_audio(self):
        """
        点击音频，进入音频页
        :return:
        """
        return self.scroll_and_click_by_text('音频')

    def access_in_light(self):
        """
        点击灯，进入灯下一页
        :return:
        """
        return self.scroll_and_click_by_text('灯')

    def access_in_detection_alarm(self):
        """
        点击侦测报警，进入侦测报警页
        :return:
        """
        return self.scroll_and_click_by_text('侦测报警')

    def access_in_camera_record(self):
        """
        点击摄像机录像，进入摄像机录像页
        :return:
        """
        return self.scroll_and_click_by_text('摄像机录像')

    def access_in_push_notifications(self):
        """
        点击手机推送，进入手机推送页
        :return:
        """
        return self.scroll_and_click_by_text('手机推送')

    def access_in_email_alerts(self):
        """
        点击邮件通知，进入邮件通知页
        :return:
        """
        return self.scroll_and_click_by_text('邮件通知')

    def access_in_ftp(self):
        """
        点击FTP，进入FTP页
        :return:
        """
        return self.scroll_and_click_by_text('FTP')

    def access_in_siren(self):
        """
        点击鸣笛，进入鸣笛页
        :return:
        """
        return self.scroll_and_click_by_text('鸣笛')

    def access_in_linked_devices(self):
        """
        点击已联动的设备，进入已联动的设备页
        :return:
        """
        return self.scroll_and_click_by_text('已联动的设备')

    def access_in_share_camera(self):
        """
        点击分享摄像机，进入分享摄像机页
        :return:
        """
        return self.scroll_and_click_by_text('分享摄像机')

    def access_in_time_lapse(self):
        """
        点击延时摄影，进入延时摄影页
        :return:
        """
        return self.scroll_and_click_by_text('延时摄影')

    def access_in_advanced(self):
        """
        点击高级设置，进入高级设置页
        :return:
        """
        return self.scroll_and_click_by_text('高级设置')
