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

d = u2.connect_usb()


def get_all_texts(resource_id):
    all_texts = []
    previous_page_texts = []
    retry_count = 0

    while True:
        # 获取当前页面所有元素的文本内容
        current_texts = []
        elements = d(resourceId=resource_id)
        for element in elements:
            text = element.get_text()
            if text not in all_texts:  # 避免重复添加
                current_texts.append(text)

        # 合并到所有文本列表
        all_texts.extend(current_texts)

        # 检查是否没有新的内容
        if current_texts == previous_page_texts:
            retry_count += 1
            if retry_count >= 2:  # 连续两次滚动后没有新内容，认为获取完成
                break
        else:
            retry_count = 0

        previous_page_texts = current_texts

        # 滚动页面
        d(scrollable=True).scroll.vert.forward()
        time.sleep(1)  # 等待滚动完成

    return all_texts


# 获取所有元素的文本内容
resource_id = 'com.mcu.reolink:id/tv_remote_sub'  # 替换为实际的资源ID
all_texts = get_all_texts(resource_id)

# 输出所有获取到的文本内容
print("获取到的所有文本内容：")
for text in all_texts:
    print(text)
