import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import subprocess
import tidevice
from tidevice import Device
import wda

import importlib
import os

from common_tools.logger import logger

driver = u2.connect_usb()


element = driver.xpath('//com.horcrux.svg.SvgView')

# 获取元素的边界坐标
bounds = element.info['bounds']

# 中心坐标
center_x = (bounds['left'] + bounds['right']) // 2
center_y = (bounds['top'] + bounds['bottom']) // 2

driver.drag(center_x, center_y, center_x, center_y-700, 1)

print(bounds)
print(center_x)
print(center_y)

# target_element_xpath = '//*[@resource-id="HeaderTitle"]'
#
# target_element = driver.xpath(target_element_xpath)
#
# # 拖动操作
# driver.drag_to(target_element)


# 定义一个方法：拖动某个元素移动一定的距离
def drag_element(element, distance):
    # 获取元素的边界坐标
    bounds = element.info['bounds']
    # 计算元素的中心坐标
    center_x = (bounds['left'] + bounds['right']) // 2
    center_y = (bounds['top'] + bounds['bottom']) // 2
    # 计算目标位置的坐标
    target_x = center_x