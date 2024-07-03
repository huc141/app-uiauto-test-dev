from pages.device_list_page import DeviceListPage
from pages.add_device_page import AddDevicePage
from common_tools.app_driver import driver


class TestAddDevice:
    def test_add_device_by_uid(self):
        driver.start(True)
        device_list_page = DeviceListPage()  # 初始化设备列表对像
        device_list_page.click_add_device_button()  # 点击设备列表右上角的添加按钮
        add_device_page = AddDevicePage()  # 初始化添加设备页面的对象
        add_device_page.click_manual_input()  # 点击“手动输入”按钮
        add_device_page.input_by_uid('952700Y005S613CC')  # 输入uid并点击下一步

    def test_add_device_by_ip(self):
        pass

    def test_add_device_by_authlink(self):
        pass
