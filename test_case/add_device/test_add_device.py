import pytest
from pages.device_list_page import DeviceListPage
from pages.add_device_page import AddDevicePage
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml
from common_tools.assert_ui import assertui

uids_config = read_yaml.uids_file_list  # 读取参数化文件


class TestAddDevice:
    @pytest.mark.parametrize("uid_config", uids_config.values(), ids=uids_config.keys())
    def test_add_device_by_uid(self, uid_config):
        driver.start_app(True)
        device_list_page = DeviceListPage()  # 初始化设备列表对像
        device_list_page.click_add_device_button()  # 点击设备列表右上角的添加按钮
        add_device_page = AddDevicePage()  # 初始化添加设备页面的对象
        add_device_page.click_manual_input(method=uid_config['method'],
                                           identifier=uid_config['identifier'],
                                           is_stand_alone=uid_config['is_stand_alone'],
                                           is_net=uid_config['is_net'],
                                           account=uid_config['account'],
                                           passwd=uid_config['passwd']
                                           )  # 点击“添加”设备按钮并点击“手动输入”按钮
        assert assertui.assert_text_in('//*[@resource-id="com.mcu.reolink:id/player_toolbar_setting"]')
