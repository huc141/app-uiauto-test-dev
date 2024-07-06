import pytest
from pages.device_list_page import DeviceListPage
from pages.add_device_page import AddDevicePage
from common_tools.app_driver import driver


class TestAddDevice:
    # @pytest.mark.parametrize("uid, identifier", uid, identifier)
    def test_add_device_by_uid(self):
        driver.start(True)
        device_list_page = DeviceListPage()  # 初始化设备列表对像
        device_list_page.click_add_device_button()  # 点击设备列表右上角的添加按钮
        add_device_page = AddDevicePage()  # 初始化添加设备页面的对象
        add_device_page.click_manual_input("uid", "952700Y006TG1NQO")  # 点击“添加”设备按钮并点击“手动输入”按钮
        # add_device_page.input_by_uid('')  # 输入uid并点击下一步

    def test_add_device_by_ip(self):
        pass

    def test_add_device_by_authlink(self):
        pass
