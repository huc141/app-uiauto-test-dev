import subprocess
import uiautomator2 as u2
from appium.options.android import UiAutomator2Options
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
import os
from appium import webdriver

appium_server_url = 'http://localhost:4723/'


class DDriver:
    def __init__(self, device_sn: str, apk_name: str = '', apk_local_path: str = read_yaml.config_apk_local_path):
        self._device_sn = device_sn
        self._apk_name = apk_name
        self._apk_local_path = apk_local_path
        self._driver = None

    def get_android_driver(self, is_native):
        if is_native:
            app_package = self._apk_name
            app_activity = 'com.android.bc.MainActivity'
        else:
            app_package = 'com.rnclient'
            app_activity = 'com.android.bc.home.HomeActivity'

        capabilities = dict(
            platformName='Android',
            deviceName='Android',
            automationName='uiautomator2',
            appPackage=app_package,
            appActivity=app_activity,
            noReset=True
        )
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        return driver


driver = DDriver(device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name)
