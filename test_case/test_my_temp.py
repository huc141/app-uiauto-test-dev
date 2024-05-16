# from common_tools.app_driver import driver
#
#
# class TestMyTemp:
#     def test_turn_off_wifi(self):
#         driver.init_driver()
#         driver.turn_off_wifi()

import subprocess
import os


def get_device_list():
    a = os.system('adb shell cmd wifi set-wifi-enabled enabled')
    return a


log = get_device_list()

print(log)
