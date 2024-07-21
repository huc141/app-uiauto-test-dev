import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import subprocess
import tidevice
from tidevice import Device
import wda


# def get_all_elements_texts_ios(driver, scroll_pause=1):
#     """
#     获取当前页面的所有元素的text文本内容
#     :param scroll_pause:
#     :param max_scrolls:
#     :param driver: uiautomator2的Device对象
#     :return: 文本内容列表
#     """
#     xml_content_set = set()
#
#     # for _ in range(max_scrolls):
#     # 获取页面的 XML 结构
#     page_source = driver.source()
#     print(page_source)
#
#     # 将每次读取的xml内容添加到集合中
#     xml_content_set.add(page_source)
#
#     # 滑动屏幕
#     driver.swipe_up()
#     time.sleep(scroll_pause)  # 等待页面稳定
#
#     # 将每次读取的xml内容追加到文件中
#     with open("H:\\app-uiauto-test-dev\\debug\\destination4.xml", 'a', encoding='utf-8') as f:
#         for xml_content in xml_content_set:
#             f.write(xml_content + '\n')
#
#     return list(xml_content_set)


# def get_all_elements_texts_az(driver, max_scrolls=1, scroll_pause=1):
#     """
#     获取当前页面的所有元素的text文本内容
#     :param scroll_pause:
#     :param max_scrolls:
#     :param driver: uiautomator2的Device对象
#     :return: 文本内容列表
#     """
#     xml_content_set = set()
#
#     for _ in range(max_scrolls):
#         # 获取页面的 XML 结构
#         page_source = driver.dump_hierarchy()
#         print(page_source)
#
#         # 将每次读取的xml内容添加到集合中
#         xml_content_set.add(page_source)
#
#     # 滑动屏幕
#     driver.swipe_ext("up")
#     time.sleep(scroll_pause)  # 等待页面稳定
#
#     # 将每次读取的xml内容追加到文件中
#     with open("D:\\app-uiauto-test-dev\\debug\\destination4.xml", 'a', encoding='utf-8') as f:
#         for xml_content in xml_content_set:
#             f.write(xml_content + '\n')
#
#     return list(xml_content_set)
driver = u2.connect_usb("28131FDH2000K1")

driver(scrollable=True).scroll.to(text="RLC-1212A")

# element = driver(text='RLC-1212A')
# element.click()


# 使用示例
# if __name__ == "__main__":
    # driver = u2.connect_usb("28131FDH2000K1")
    # driver = wda.Client('http://localhost:8100')

    # texts = get_all_elements_texts_ios(driver)
    # texts = get_all_elements_texts_az(driver)
    # print(f"共获取到 {len(texts)} 段XML内容")