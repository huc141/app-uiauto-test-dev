# -*- coding: utf-8 -*-
import time
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteDetectionAlarm(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.time_selector_hour = ''
            self.time_selector_min = ''

        elif self.platform == 'ios':
            self.time_selector_hour = ''
            self.time_selector_min = ''
