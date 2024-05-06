import uiautomator2 as u2
from common_tools.read_yaml import read_yaml


class Driver:
    def __init__(self, device_sn: str, apk_name: str):
        self._device_sn = device_sn
        self._apk_name = apk_name
        self._driver = u2.connect_usb(self._device_sn)  # 连接手机

    # 启动reolink app
    def start(self):
        if self._driver:
            self._driver.app_start(self._apk_name)
            all_paks = self._driver.app_list()  # 列出所有正在运行的APP，返回一个列表
            running_app = self._driver.app_current()  # 获取当前打开的APP信息，返回一个字典
            print("当前手机：%s 正在运行的所有app包名：%s" % (self._device_sn, all_paks))
            print("当前手机：%s 正在运行的app包名： %s" % (self._device_sn, running_app))
            return all_paks, running_app

    # 获取reolink app的信息
    def get_app_info(self) -> dict:
        if self._driver:
            app_info = self._driver.app_info(self._apk_name)
            # print(app_info)
            return app_info

    # 获取手机信息
    def get_device_info(self) -> dict:
        if self._driver:
            device_info = self._driver.device_info
            return device_info

    # 安装app
    def install_app(self, apk_local_path: str):
        if self._driver:
            self._driver.app_install(apk_local_path)

    # 卸载reolink app
    def uninstall_app(self):
        if self._driver:
            self._driver.app_uninstall(self._apk_name)

    # 清除app缓存
    def clear_app_cache(self):
        if self._driver:
            self._driver.app_clear(self._apk_name)

    def quit(self):
        self._driver.app_stop(self._apk_name)


driver = Driver(device_sn=read_yaml.config_device_sn, apk_name=read_yaml.config_apk_name)
