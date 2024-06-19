# -*- coding: utf-8 -*-
from common_tools.logger import logger
from pages.base_page import BasePage


class RnDeviceListPage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == "android":
            self.camera_mark_button = '(//*[@text="Mark"])[1]'
        elif self.platform == "ios":
            self.camera_mark_button = '待定'

    def click_camera_mark_button(self):
        """
        点击设备列表里某个设备的Mark按钮
        :return:
        """
        try:
            return self.click_by_xpath(self.camera_mark_button)
        except Exception as err:
            logger.info(err)
