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


def check_remote_setting_text(self):
    pass
