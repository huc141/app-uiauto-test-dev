import os
from typing import Literal

import pytest
import yaml
import uiautomator2 as u2
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_setting import RemoteSetting
from pages.base_page import BasePage

d = u2.connect_usb()
element = d(text='音频')
element.click()


# d.xpath('//*[@text="音频"]').click()
# d.xpath('//*[@text="3600-3932100"]').set_text('11111')





# devices_config = read_yaml.load_device_config(yaml_file_name='wifi.yaml')  # 读取参数化文件
# print(devices_config)
#
# remote_setting_wifi = devices_config[0]['device_list_name']
#
# print('------------------')
#
# print(remote_setting_wifi)
#
# print('------------------')
# page_fun = RemoteSetting().scroll_check_funcs(remote_setting_wifi)

# 读取yaml文件中预期功能项
# page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_wifi, 'name')
# print(page_fun_list)


# 提取ipc和hub部分items中的name值
# ipc_names = [item['name'] for item in remote_setting_wifi['advanced_setting_page']['items'].values()]
# hub_names = [item['name'] for item in devices_config[0]['hub']['advanced_setting_page']['items'].values()]

# 打印结果
# print("ipc部分items的name值:", ipc_names)
# print("hub部分items的name值:", hub_names)


