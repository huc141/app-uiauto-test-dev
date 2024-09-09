import os
import time
from typing import Literal

import pytest
import yaml
import uiautomator2 as u2

from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_setting import RemoteSetting

d = u2.connect_usb()

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

# 滑动条
# 先定位：
# element = d.xpath('//*[@resource-id="com.mcu.reolink:id/remote_config_progress_seek_bar"]')

# 按下并移动
# element.swipe("right")


# 遮盖区域
# 假设红色方框的区域是某个元素，可以通过 resourceId 或其他属性定位
element = d.xpath('//*[@resource-id="com.mcu.reolink:id/shelter_player"]')

# 获取元素的边界坐标
bounds = element.info['bounds']

# 左上角坐标
start_x = bounds['left']
start_y = bounds['top']

# 右下角坐标
end_x = bounds['right']
end_y = bounds['bottom']

# 从左上角向右下角拖动,全屏遮盖
d.drag(start_x, start_y, end_x, end_y, 1)  # 0.5 秒完成拖动

# 清空当前通道
d(text='清空当前通道').click()

# 从中心点开始1/4遮盖
# 计算中心坐标
center_x = (bounds['left'] + bounds['right']) // 2
center_y = (bounds['top'] + bounds['bottom']) // 2

# 右下角坐标
end_x = bounds['right']
end_y = bounds['bottom']

# 从中心点向右下角拖动
d.drag(center_x, center_y, end_x, end_y, 0.5)  # 0.5 秒内完成拖动




# d.touch.down(10, 10)  # 模拟按下
# time.sleep(.01)  # down 和 move 之间的延迟，自己控制
# d.touch.move(15, 15)  # 模拟移动
# d.touch.up(10, 10)  # 模拟抬起
