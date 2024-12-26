import time
import uiautomator2 as u2
import os
import wda
import subprocess
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from common_tools.screen_record import scr


class Driver:
    def __init__(self, device_sn: str, apk_name: str = '', apk_local_path: str = read_yaml.config_apk_local_path):
        self._device_sn = device_sn  # 手机序列号
        self._apk_name = apk_name  # 被测包名
        self._apk_local_path = apk_local_path  # apk包的所在路径
        self._driver = None
        self._platform = None  # 被测平台：iOS/安卓
        self.record_proc = None  # 录屏进程
        self._wda_process = None  # wda服务进程
        self.v_name = None  # 录屏文件名
        self.wda_bundle_id = read_yaml.wda_bundle_id  # wda包名

    def init_driver(self):
        """
        该方法用于初始化驱动，调用后会要求用户选择被测平台，根据被测平台启动不同的设备驱动
        :return:
        """
        if self._driver:  # 如果已经初始化，则直接返回现有的驱动
            return self._driver

        while True:
            str1 = input("请输入数字选择：1 使用uiautomator2测试安卓，2 使用Facebook-wda测试iOS(!!!先确认yml文件中的APP包名!!!): ")
            if str1 == '1':
                print(f"你输入了：{str1}，现在启动uiautomator2")
                logger.info("开始USB连接手机")
                try:
                    self._driver = u2.connect_usb(self._device_sn)
                    self._platform = "android"
                    logger.info("安卓设备连接成功")
                    return self._driver
                except Exception as err:
                    logger.error("连接失败，原因为：{}".format(err))
                break  # 输入有效，执行相应操作后退出循环

            elif str1 == '2':
                print(f"你输入了：{str1}，现在启动Facebook-wda")
                logger.info("开始使用tidevice启动WDA(请确保8100端口不被占用)···")
                try:
                    self._wda_process = subprocess.Popen(
                        ['tidevice', '-u', self._device_sn, 'wdaproxy', '-B', self.wda_bundle_id, '--port', '8100'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    self._driver = wda.Client('http://localhost:8100')  # 确保 WebDriverAgent 正在运行并监听该端口
                    logger.info("等待WDA服务启动···")
                    time.sleep(6)  # 等待WDA服务启动

                    logger.info("正在获取WDA服务启动状态···")
                    status_info = self._driver.status()
                    message = "WebDriverAgent is ready to accept commands"
                    if message in status_info.get("message", ""):
                        logger.info("WDA服务启动成功")
                    else:
                        logger.error("WDA服务启动失败")
                    self._platform = "ios"
                    return self._driver

                except Exception as err:
                    logger.error("连接失败，原因为：{}".format(err))
                break

            else:
                print("无效输入，请按照指示重新输入！")

    def get_actual_driver(self):
        if not self._driver:
            self.init_driver()
        return self._driver

    def get_platform(self):
        return self._platform

    def __getattr__(self, item):
        """
        当试图访问 Driver 实例上不存在的属性或方法时，__getattr__ 会被调用。
        它会在 self._driver 上查找该属性或方法，如果找到就返回。
        如果 self._driver 还没有初始化或不存在该属性，则抛出 AttributeError。
        :param item:
        :return:
        """
        if not self._driver:
            logger.info("正在访问 Driver 实例的一个不存在的属性，自动调用 __getattr__ 方法")
            self.init_driver()
        return getattr(self._driver, item)

    def stop_app(self):
        """
        停止app
        :return:
        """
        try:
            if self._platform == "android":
                self._driver.app_stop(self._apk_name)
            elif self._platform == "ios":
                self._driver.session().app_terminate(self._apk_name)
            else:
                logger.error(f"未知的平台类型：{self._platform}")
                return

            logger.info(f"已停止APP：{self._apk_name}")
        except Exception as err:
            logger.error(f"停止app时发生错误：{err}")

    def start_app(self, is_record=False):
        """
        启动reolink app
        :return:
        """
        try:
            if not self._driver:
                self.init_driver()

            if self._driver:
                self.stop_app()  # 先停止reolink app，再重新启动
                time.sleep(1.5)
                logger.info("开始启动app···")

                scr.take_screenrecord(is_record)  # 启动安卓/iOS录屏, 是否启动则取决于is_record参数值

                if self._platform == "android":
                    self._driver.app_start(self._apk_name)
                    logger.info("安卓app启动成功···")
                elif self._platform == "ios":
                    self._driver.session().app_activate(self._apk_name)
                    logger.info("iOS-app启动成功···")
                time.sleep(4)

        except Exception as err:
            logger.error(f"APP启动失败，原因为：{err}", )

    def get_app_info(self) -> dict:
        """
        获取reolink app的信息
        :return:
        """
        try:
            if self._driver:
                if self._platform == "android":
                    app_info = self._driver.app_info(self._apk_name)
                    logger.info("app信息获取成功···")
                    return app_info

                elif self._platform == "ios":
                    app_info = self._driver.app_current()
                    return app_info

        except Exception as err:
            logger.error("APP信息获取失败，原因为：%s", err)

    def get_device_info(self) -> dict:
        """
        获取手机信息
        :return:
        """
        device_info = None
        try:
            if self._driver:
                if self._platform == "android":
                    device_info = self._driver.device_info

                elif self._platform == "ios":
                    device_info = self._driver.device_info()

                else:
                    raise ValueError("不支持的平台")

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
                if self._platform == "android":
                    self._driver.app_install(self._apk_local_path)

                elif self._platform == "ios":
                    udid_option = f"--udid {self._device_sn} " if self._device_sn else ""  # 条件表达式，用于根据 udid 的值来构建一个字符串
                    os.system(f"tidevice {udid_option}install {self._apk_local_path}")
                logger.info("app安装成功···")

        except Exception as err:
            logger.error("app安装失败，原因为：%s", err)

    def uninstall_app(self):
        """
        卸载reolink app
        :return:
        """
        try:
            if self._platform == "android":
                if self._apk_name in self._driver.app_list():
                    self._driver.app_uninstall(self._apk_name)

            elif self._platform == "ios":
                os.system(f"tidevice uninstall {self._apk_name}")
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

    @staticmethod
    def get_wifi_status():
        """
        只能用于安卓
        函数获取当前手机的WiFi状态：
        Wi-Fi is enabled：WiFi已开启（不代表已经连上WiFi）
        Wi-Fi is disabled：WiFi已关闭
        :return: 
        """
        try:
            # 使用双引号将字符串包括在adb命令中
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

    @staticmethod
    def turn_off_wifi(self):
        """
        只能用于安卓。
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

    @staticmethod
    def turn_on_wifi(self):
        """
        只能用于安卓。
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


driver = Driver(device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name)