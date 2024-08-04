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
wd = wda.Client('http://localhost:8100')
wd(type='B').click()

# def get_all_texts(resource_id):
#     all_texts = []
#     previous_page_texts = []
#     retry_count = 0
#
#     while True:
#         # 获取当前页面所有元素的文本内容
#         current_texts = []
#         elements = d(resourceId=resource_id)
#         for element in elements:
#             text = element.get_text()
#             if text not in all_texts:  # 避免重复添加
#                 current_texts.append(text)
#
#         # 合并到所有文本列表
#         all_texts.extend(current_texts)
#
#         # 检查是否没有新的内容
#         if current_texts == previous_page_texts:
#             retry_count += 1
#             if retry_count >= 2:  # 连续两次滚动后没有新内容，认为获取完成
#                 break
#         else:
#             retry_count = 0
#
#         previous_page_texts = current_texts
#
#         # 滚动页面
#         d(scrollable=True).scroll.vert.forward()
#         time.sleep(1)  # 等待滚动完成
#
#     return all_texts
#
#
# # 获取所有元素的文本内容
# resource_id = 'com.mcu.reolink:id/tv_remote_sub'  # 替换为实际的资源ID
# all_texts = get_all_texts(resource_id)
#
# # 输出所有获取到的文本内容
# print("获取到的所有文本内容：")
# for text in all_texts:
#     print(text)


# 获取页面所有功能名称
start = time.perf_counter()


def scroll_screen(driver, platform, max_scrolls=1):
    """
    滚动屏幕
    :param driver: 驱动实例
    :param platform: 平台类型 ("android" 或 "ios")
    :param max_scrolls: 最大滚动次数，默认1次
    :return:
    """
    platform = platform.lower()  # 将平台名称转换为小写，确保一致性

    if platform == "android":
        scroll_method = driver.swipe_ext
        direction = "up"
    elif platform == "ios":
        scroll_method = driver.swipe_up
    else:
        raise ValueError(f"不支持当前平台: {platform}")

    for _ in range(max_scrolls):
        if platform == "android":
            scroll_method(direction)
        else:
            scroll_method()
            time.sleep(0.5)  # iOS平台需要短暂等待UI更新


def get_all_texts(selector_type, selector, max_scrolls=1):
    """
    滚动获取当前页面所有指定文本
    :param selector_type: 支持安卓className，resource-id定位，iOS的className定位
    :param selector: 对应的value值
    :param max_scrolls: 最大滚动次数
    :return:
    """
    my_set = set()

    def get_elements_texts():
        if selector_type == 'id':
            elements = d(resourceId=selector)
        elif selector_type == 'class':
            elements = d(className=selector)
        return {element.get_text() for element in elements}

    # 获取当前页面所有元素的文本内容
    for _ in range(max_scrolls):
        # 获取当前页面所有元素的文本内容
        new_texts = get_elements_texts()
        my_set.update(new_texts)

        scroll_screen(d, "android")
        time.sleep(0.5)

        # 检查滑动后页面是否有变化
        new_texts = get_elements_texts()
        if not new_texts - my_set:
            break  # 如果滑动后没有新内容，退出循环

        # 添加新获取的文本内容
        my_set.update(new_texts)
    print(my_set)
    return list(my_set)


resource_id = 'com.mcu.reolink:id/tv_remote_sub'  # 替换为实际的资源ID
get_all_texts(selector_type='id', selector=resource_id)


end = time.perf_counter()
print("运行耗时", end - start)

# 计算所获得的功能名称数量

# 计算预期设备>预期页面的功能数量

# 遍历预期名称，验证文本和数量是否相等


# 示例用法
# driver = d  # 替换为实际的驱动实例
# scroll_screen(driver, platform="android", max_scrolls=1)
