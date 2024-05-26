import subprocess
import uiautomator2 as u2
from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
import os
from appium import webdriver


class Driver:
    def __init__(self, device_sn: str, apk_name: str = '', apk_local_path: str = read_yaml.config_apk_local_path):
        self._device_sn = device_sn
        self._apk_name = apk_name
        self._apk_local_path = apk_local_path
        self._driver = None

    def init_driver(self):
        """
        连接手机
        :return:
        """
        logger.info("开始USB连接手机")
        try:
            self._driver = u2.connect_usb(self._device_sn)
            logger.info("连接成功")
            return self._driver
        except Exception as err:
            logger.error("连接失败，原因为：{}".format(err))
            return None

    def start(self):
        """
        启动reolink app
        :return:
        """
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

    def get_app_info(self) -> dict:
        """
        获取reolink app的信息
        :return:
        """
        try:
            if self._driver:
                app_info = self._driver.app_info(self._apk_name)
                logger.info("app信息获取成功···")
                return app_info
        except Exception as err:
            logger.error("APP信息获取失败，原因为：%s", err)

    def get_device_info(self) -> dict:
        """
        获取手机信息
        :return:
        """
        try:
            if self._driver:
                device_info = self._driver.device_info
                logger.info("获取手机信息成功···")
                return device_info
        except Exception as err:
            logger.error("获取手机信息失败，原因为：%s", err)

    def install_app(self):
        """
        安装app
        :return:
        """
        try:
            if self._driver:
                self._driver.app_install(self._apk_local_path)
                logger.info("app安装成功···")
        except Exception as err:
            logger.error("app安装失败，原因为：%s", err)

    def uninstall_app(self):
        """
        卸载reolink app
        :return:
        """
        try:
            if self._apk_name in self._driver.app_list():
                self._driver.app_uninstall(self._apk_name)
                logger.info("卸载reolink app成功")
        except Exception as err:
            logger.error("卸载app失败，原因：%s", err)

    def clear_app_cache(self):
        """
        清除app缓存
        :return:
        """
        if self._driver:
            self._driver.app_clear(self._apk_name)
            logger.info("清除reolink app缓存成功···")

    def stop(self):
        """
        停止app
        :return:
        """
        self._driver.app_stop(self._apk_name)
        logger.info("reolink app已停止运行")

    def get_wifi_status(self):
        """
        函数获取当前手机的WiFi状态：
        Wi-Fi is enabled：WiFi已开启（不代表已经连上WiFi）
        Wi-Fi is disabled：WiFi已关闭
        :return: 
        """
        try:
            # 使用双引号将字符串包括在命令中
            adb_command = 'adb shell dumpsys wifi | findstr "Wi-Fi"'
            result = subprocess.run(adb_command, shell=True, capture_output=True, text=True, encoding='utf-8')

            # 检查命令的输出
            if result.returncode == 0:
                output = result.stdout.strip()
                if "Wi-Fi is enabled" in output:
                    logger.info("Wi-Fi is enabled")
                    return "Wi-Fi is enabled"
                elif "Wi-Fi is disabled" in output:
                    logger.info("Wi-Fi is disabled")
                    return "Wi-Fi is disabled"
                else:
                    logger.info("Wi-Fi status unknown")
                    return "Wi-Fi status unknown"
            else:
                logger.error(f"Error executing command: {result.stderr}")
                return f"Error executing command: {result.stderr}"
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            return f"Exception occurred: {str(e)}"

    def turn_off_wifi(self):
        """
        关闭手机WiFi
        :return:
        """
        try:
            result = os.system('adb shell cmd wifi set-wifi-enabled disabled')
            if self.get_wifi_status() == "Wi-Fi is disabled":
                logger.info("wifi关闭成功:%s", result)
            return result
        except Exception as err:
            logger.error("wifi关闭失败，原因：%s", err)

    def turn_on_wifi(self):
        """
        开启手机WiFi(不一定会自动连上WiFi)
        :return:
        """
        try:
            result = os.system('adb shell cmd wifi set-wifi-enabled enabled')
            if self.get_wifi_status() == "Wi-Fi is enabled":
                logger.info('wifi已打开：%s', result)
            return result
        except Exception as err:
            logger.error("wifi开启失败，原因：%s", err)

    def get_element_info(self):
        try:
            element = self.init_driver().info
            return element
        except Exception as err:
            return f"Exception occurred: {str(err)}"


driver = Driver(device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name)
