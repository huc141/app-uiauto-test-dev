import re
import uiautomator2 as u2
from common_tools.app_driver import Driver
from common_tools.read_yaml import read_yaml
DEFAULT_SECONDS = 10


class BasePage:
    # 构造函数
    def __init__(self, device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name):
        self.apk_name = apk_name
        self.device_sn = device_sn
        self.driver = Driver(device_sn, apk_name).init_driver()

    def click_by_id(self, id_name):
        """通过id定位单个元素"""
        try:
            self.driver.implicitly_wait(DEFAULT_SECONDS)
            self.driver(resourceId=id_name).click()
        except Exception as e:
            print("页面中没有找到id为%s的元素" % id_name)
            raise e
