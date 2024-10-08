# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteShareCamera(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def check_share_camera_main_text(self, texts):
        """
        验证分享摄像机主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            share_camera_main_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            return share_camera_main_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
