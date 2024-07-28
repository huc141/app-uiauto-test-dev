# -*- coding: utf-8 -*-
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class RemoteSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass
        elif self.platform == 'ios':
            pass

    def check_remote_setting_text(self, expected_text, exclude_texts,
                                  xml_az_parse_conditions, xml_ios_parse_conditions):
        """
        根据设备名，检查对应设备的远程配置功能是否和预期一致
        :param xml_az_parse_conditions: 安卓的远程配置主(一级)页面解析条件，用于排除无关文本，筛选出页面功能
        :param xml_ios_parse_conditions: iOS的远程配置主(一级)页面解析条件，用于排除无关文本，筛选出页面功能
        :param expected_text: 需要检查的预期文本
        :param exclude_texts: 需要排除的文本(额外添加需要排除的文本)
        :return:
        """
        return self.verify_page_text(expected_text=expected_text,
                                     exclude_texts=exclude_texts,
                                     xml_az_parse_conditions=xml_az_parse_conditions,
                                     xml_ios_parse_conditions=xml_ios_parse_conditions
                                     )

    def extract_all_names(self, yaml_content, keys_to_extract):
        """
        解析YAML文件，提取指定keys下的items的name，并全部加入到列表中。

        参数:
        file_path (str): YAML文件的路径。
        keys_to_extract (list): 要提取的keys列表。

        返回:
        list: 包含所有提取的name的列表。
        """
        # 初始化空列表
        all_names = []

        # 遍历指定的keys
        for key in keys_to_extract:
            # 获取每个key的items
            items = yaml_content.get(key, {}).get('items', [])
            # 遍历items，提取name并加入到列表中
            for item in items:
                name = item.get('name', '')
                if name:  # 如果name存在，则加入到列表中
                    all_names.append(name)

        all_names_count = len(all_names)

        return all_names

    def scroll_click_remote_setting(self, device_name):
        """
        逐一滚动查找设备名称并点击远程设置按钮
        :param device_name: 要查找的设备名称
        :return:
        """
        return self.access_in_remote_setting(text_to_find=device_name)

    def access_in_wifi(self):
        """
        点击WiFi，进入WiFi页
        :return:
        """
        return self.scroll_and_click_by_text('Wi-Fi')

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


