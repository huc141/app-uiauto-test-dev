import logging
import uiautomator2 as u2
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger


class Driver:
    def __init__(self, device_sn: str, apk_name: str = '', apk_local_path: str = read_yaml.config_apk_local_path):
        self._device_sn = device_sn
        self._apk_name = apk_name
        self._apk_local_path = apk_local_path
        self._driver = None

    # 连接手机
    def init_driver(self):
        logger.info("开始USB连接手机")
        try:
            self._driver = u2.connect_usb(self._device_sn)
            logger.info("连接成功")
            return self._driver
        except Exception as err:
            logger.error("连接失败，原因为：{}".format(err))
            return None

    # 启动reolink app
    def start(self):
        try:
            if self._driver:
                logger.info("开始启动app···")
                self._driver.app_start(self._apk_name)
                all_paks = self._driver.app_list()  # 列出所有正在运行的APP，返回一个列表
                running_app = self._driver.app_current()  # 获取当前打开的APP信息，返回一个字典
                logger.info("app启动成功···")
                logger.info("当前手机：%s 正在运行的app包名： %s" % (self._device_sn, running_app))
                return all_paks, running_app
        except Exception as err:
            logger.error("APP启动失败，原因为：%s", err)

    # 获取reolink app的信息
    def get_app_info(self) -> dict:
        try:
            if self._driver:
                app_info = self._driver.app_info(self._apk_name)
                logger.info("app信息获取成功···")
                return app_info
        except Exception as err:
            logger.error("APP信息获取失败，原因为：%s", err)

    # 获取手机信息
    def get_device_info(self) -> dict:
        try:
            if self._driver:
                device_info = self._driver.device_info
                logger.info("获取手机信息成功···")
                return device_info
        except Exception as err:
            logger.error("获取手机信息失败，原因为：%s", err)

    # 安装app
    def install_app(self):
        try:
            if self._driver:
                self._driver.app_install(self._apk_local_path)
                logger.info("app安装成功···")
        except Exception as err:
            logger.error("app安装失败，原因为：%s", err)

    # 卸载reolink app
    def uninstall_app(self):
        try:
            if self._apk_name in self._driver.app_list():
                self._driver.app_uninstall(self._apk_name)
                logger.info("卸载reolink app成功")
        except Exception as err:
            logger.error("卸载app失败，原因：%s", err)

    # 清除app缓存
    def clear_app_cache(self):
        if self._driver:
            self._driver.app_clear(self._apk_name)
            logger.info("清除reolink app缓存成功···")

    def stop(self):
        self._driver.app_stop(self._apk_name)
        logger.info("reolink app已停止运行")


driver = Driver(device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name)
