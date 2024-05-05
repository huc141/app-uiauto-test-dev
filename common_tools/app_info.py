from common_tools.app_driver import driver as app_driver


class AppInfo:
    def __init__(self, driver):
        self.driver = driver

    def get_app_info(self):
        self.driver.start()


app_info = AppInfo(app_driver)
app_info.get_app_info()
