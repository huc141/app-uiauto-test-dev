import re
from common_tools.app_driver import Driver
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml

DEFAULT_SECONDS = 15


class BasePage:
    # 构造函数
    def __init__(self, device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name):
        self.driver = Driver(device_sn, apk_name).init_driver()
        self.driver.wait_timeout = DEFAULT_SECONDS  # 设置全局等待超时时间为15秒

    def click_by_id(self, id_name):
        """通过id定位单个元素"""
        try:
            print("UI元素是否存在：↓↓↓↓↓↓↓")
            print(self.driver(resourceId=id_name).exists())
            self.driver(resourceId=id_name).click()
        except Exception as e:
            print("页面中没有找到id为%s的元素" % id_name)
            raise e
