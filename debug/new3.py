import os
import time
from typing import Literal

import pytest
import yaml
import uiautomator2 as u2
import wda
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_setting import RemoteSetting

d = u2.connect_usb()
# c = wda.Client('http://localhost:8100')
# s = c.session()

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

# d.swipe_ext('right', scale=0.9)  # 模拟手势向右滑动返回上一级菜单

# 安卓滑动条
# 滑动条
# 先定位：
# element = d(resourceId='RNE__Slider_Thumb')

# 按下并项右移动
# for i in range(1, 20):
#     element.swipe("right")
#     i += 1

# 按下并向左移动
# for i in range(1, 20):
#     element.swipe("left")
#     i += 1

# iOS滑动条
# s.swipe_right()
# c.swipe_right()
# slider = s(xpath='//XCUIElementTypeImage[2]')

# 获取滑动条的当前位置
# rect = slider.bounds
# print(rect)

# 使用拖动操作，模拟手动滑动条
# 计算起点和终点
# start_x = rect.x  # 滑块的x起点
# start_y = rect.y  # 滑块的y起点

# end_x = rect.x + rect.width * 0.7  # 拖动到 70% 的位置，控制亮度
# end_y = start_y  # 垂直方向保持不变

# 模拟拖动操作
# s.tap_hold(start_x, start_y, 10)
# for i in range(1, 20):
#     slider = s(xpath='//XCUIElementTypeImage[2]')
#     s.swipe(start_x, start_y, start_x+30, start_y, 1)  # 1秒完成滑动
#     i += 1


# 安卓
# 遮盖区域
# 假设红色方框的区域是某个元素，可以通过 resourceId 或其他属性定位
element = d.xpath('//*[@resource-id="com.mcu.reolink:id/shelter_player"]')
#
# 获取元素的边界坐标
bounds = element.info['bounds']
print(bounds)

# 左上角坐标
# start_x = bounds['left']
# start_y = bounds['top']

# 右下角坐标
# end_x = bounds['right']
# end_y = bounds['bottom']

# 从左上角向右下角拖动,全屏遮盖
# d.drag(start_x, start_y, end_x, end_y, 1)  # 0.5 秒完成拖动

# 清空当前通道
# d(text='清空当前通道').click()

# 从中心点开始1/4遮盖
# 计算中心坐标
# center_x = (bounds['left'] + bounds['right']) // 2
center_y = (bounds['top'] + bounds['bottom']) // 2

middle_y = center_y
middle_x = 0



# 右下角坐标
# end_x = bounds['right']
# end_y = bounds['bottom']

# 从中心点向右下角拖动
i = 0
while i <= 8:
    s_x = i * 130
    e_x = s_x + 50
    e_y = middle_y + 50
    d.drag(s_x, middle_y, e_x, e_y, 0.5)  # 0.5 秒内完成拖动
    i += 1



# ios
# 遮盖区域
# 假设红色方框的区域是某个元素，可以通过 resourceId 或其他属性定位
# element = s(
#     xpath='//XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]')

# 获取元素的边界坐标
# bounds = element.bounds
# print(bounds)
#
# # 左上角坐标
# top_left_x = bounds[0]
# top_left_y = bounds[1]

# 元素宽度、高度
# width = bounds[2]
# height = bounds[3]

# 中心点坐标
# center_x = int(top_left_x + width / 2)
# center_y = int(top_left_y + height / 2)
# print(center_x)
# print(center_y)

# 左上角坐标
# top_left_x = bounds[0]
# top_left_y = 0

# 右上角坐标
# top_right_x = bounds[2]
# top_right_y = 0

# 右下角坐标
# bottom_right_x = bounds[2]
# bottom_right_y = bounds[1] + bounds[3]

# 左下角坐标
# bottom_left_x = bounds[0]
# bottom_left_y = bounds[1] + bounds[3]

# s.swipe(center_x, center_y, top_left_x, top_left_y, 1)  # 左上角
# s.swipe(center_x, center_y, top_right_x, top_right_y, 1)  # 右上角
# s.swipe(center_x, center_y, bottom_right_x, bottom_right_y, 1)  # 1秒完成滑动 右下角
# s.swipe(center_x, center_y, bottom_left_x, bottom_left_y, 1)  # 1秒完成滑动 左下角
# s.swipe(top_left_x, top_left_y, bottom_right_x, bottom_right_y, 1)  # 全屏：右下角到左上角

# ele = s(name='WaterMark-ReoCell-Switch')
# # ele.click()
#
# is_id = ele.child(name='RNE__LISTITEM__padView').child(name='ReoSwitch:1')
# print(is_id.exists)