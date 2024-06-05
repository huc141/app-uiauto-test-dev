from common_tools.app_driver import driver
from pages.device_list_page import DeviceListPage


class TestMyTemp:
    def test_add_device_by_uid(self):
        driver.start()
        device_list_page = DeviceListPage()  # 初始化设备列表对像
        device_list_page.get_toast("111111")
