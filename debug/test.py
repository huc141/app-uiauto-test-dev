# -*- coding: utf-8 -*-
import time
from time import sleep
import pytest
import wda
import yaml
import os
import uiautomator2 as u2
from pages.base_page import BasePage
from common_tools.logger import logger
import wda
import time
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
import chardet

driver = u2.connect_usb("28131FDH2000K1")

# driver = wda.Client('http://localhost:8100')


# if __name__ == "__main__":
#     driver = u2.connect_usb("28131FDH2000K1")
#     # driver = wda.Client('http://localhost:8100')  # 或者使用其他连接方式，如d = u2.connect('设备IP') for WiFi
#     scroll_and_click_by_text(driver, 'text', text_to_find='REOCYP-332-hhmmkk')


def get_all_elements_texts(driver, max_scrolls=1, scroll_pause=1):
    """
    获取当前页面的所有元素的text文本内容
    :param scroll_pause:
    :param max_scrolls:
    :param driver: uiautomator2的Device对象
    :return: 文本内容列表
    """
    xml_content_set = set()

    for _ in range(max_scrolls):
        # 获取页面的 XML 结构
        page_source = driver.dump_hierarchy()
        print(page_source)

        # 将每次读取的xml内容添加到集合中
        xml_content_set.add(page_source)

        # 滑动屏幕
        driver.swipe_ext("up")
        time.sleep(scroll_pause)  # 等待页面稳定

        # 将每次读取的xml内容追加到文件中
    with open("D:\\app-uiauto-test-dev\\debug\\destination4.xml", 'a', encoding='utf-8') as f:
        for xml_content in xml_content_set:
            f.write(xml_content + '\n')

    return list(xml_content_set)


# 使用示例
if __name__ == "__main__":
    driver = u2.connect_usb("28131FDH2000K1")
    texts = get_all_elements_texts(driver, max_scrolls=2)
    print(f"共获取到 {len(texts)} 段XML内容")
