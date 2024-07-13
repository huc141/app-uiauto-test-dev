import pytest
from common_tools.app_driver import driver
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from common_tools.read_yaml import read_yaml
from common_tools.assert_ui import assertui


class TestRemoteSettingAudio:
    def test_remote_setting_audio(self):
        # 启动app，并开启录屏
        driver.start_app(True)

        # 在设备列表查找到对应设备并进入远程配置
        RemoteSetting().scroll_click_remote_setting(device_name="Reolink TrackMix WiFi")

        # 获取当前页面所有功能项并写入txt文件中，统计出功能数量

        # 读取预期功能项并遍历，与获取到的功能项进行一一比对和数量核对

        # 断言

