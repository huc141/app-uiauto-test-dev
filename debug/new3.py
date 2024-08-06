import os
from typing import Literal

import pytest
import yaml
import uiautomator2 as u2
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_setting import RemoteSetting

# d = u2.connect_usb()

devices_config = read_yaml.load_device_config(yaml_file_name='wifi.yaml')  # 读取参数化文件
print(devices_config)

remote_setting_wifi = devices_config[0]['ipc']['items'][1]['subpage']['text']

print('------------------')
# page_fun = RemoteSetting().scroll_check_funcs(remote_setting_wifi)

print(remote_setting_wifi)
