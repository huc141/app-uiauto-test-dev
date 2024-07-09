# -*- coding: utf-8 -*-
from common_tools.app_driver import driver
from pages.rn_device_list_page import RnDeviceListPage


class TestRnDemo:
    def test_mark(self):
        driver.start_app()
        device_list_page = RnDeviceListPage()
        device_list_page.click_camera_mark_button()
        driver.stop_app()
