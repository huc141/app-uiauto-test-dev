from common_tools.app_driver import driver as app_driver
from common_tools.read_yaml import read_yaml
import time


class AppInfo:
    def __init__(self, driver):
        self.driver = driver

    def uninstall_app(self):
        self.driver.uninstall_app()

    def install_app(self):
        self.driver.install_app(read_yaml.get_data('apk_local_path'))

    def get_app_info(self):
        self.driver.start()


app_info = AppInfo(app_driver)
app_info.uninstall_app()
time.sleep(6)
app_info.install_app()
