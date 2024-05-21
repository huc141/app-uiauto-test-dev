import re
import time
from common_tools.app_driver import Driver
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger

DEFAULT_SECONDS = 15


class BasePage:
    # 构造函数
    def __init__(self, device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name):
        self.driver = Driver(device_sn, apk_name).init_driver()
        self.driver.wait_timeout = DEFAULT_SECONDS  # 设置全局等待超时时间为15秒

    def click_by_id(self, id_name):
        """通过id定位单个元素"""
        try:
            time.sleep(3)
            element = self.driver(resourceId=id_name)
            if not element.exists():
                logger.error("该点击元素：%s 不存在", id_name)
                raise ValueError(f"该点击元素：{id_name} 不存在")

            element.click()
            time.sleep(3)
        except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
            logger.error("ValueError: %s", verr)
            raise
        except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
            logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", id_name, err)
            raise

        return self.driver
