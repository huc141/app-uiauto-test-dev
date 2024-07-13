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


# def scroll_and_click_by_text(driver, type, text_to_find='FE-W', max_attempts=10, scroll_pause=1):
#     """
#     在可滚动视图中查找并点击指定文本的元素。
#     :param type: 元素定位类型，支持文本和xpath
#     :param driver: uiautomator2的device对象
#     :param text_to_find: 要查找的文本
#     :param max_attempts: 最大尝试次数
#     :param scroll_pause: 滚动后的暂停时间，秒
#     """
#     ele = None
#     is_find = None
#     attempt = 0
#
#     try:
#         # 根据类型初始化查找元素
#         if type == "text":
#             try:
#                 element = driver(text=text_to_find).right(clickable=True)  # 查找到text_to_find文本右边的第一个元素
#                 # ele = element.right(clickable=True)   # 查找到text_to_find文本右边的第一个元素的右边的第1个元素
#             except Exception as err:
#                 print(f"元素未找到，原因：{err}")
#                 return False
#
#             if element is not None:
#                 ele = element.right(clickable=True)  # 如果第一个元素存在，则再尝试查找文本右边的第一个元素的右边的第1个元素
#
#             if ele is not None:
#
#
#             # 尝试直接滚动到指定文本
#             print(f"Attempting to scroll to '{text_to_find}' directly.")
#             is_find = driver(scrollable=True).scroll.to(text=text_to_find)
#
#         elif type == "xpath":
#             element = driver.xpath(text_to_find)
#             driver(scrollable=True).fling.vert.toBeginning(max_swipes=1000)  # 滑动至顶部
#
#         else:
#             raise ValueError("你可能输入了不支持的元素查找类型···")
#
#         # 检查元素是否存在
#         if ele.exists and element.exists:
#             print(f"元素已找到: '{text_to_find}'")
#             ele.click()
#             print(f"Clicked on '{text_to_find}' directly.")
#             return True
#         elif element.exists and ele is False:
#             element.click()
#
#         # 如果直接滚动未找到，则尝试多次滚动查找
#         while attempt < max_attempts and not is_find:
#             print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
#             driver(scrollable=True).scroll(steps=200)
#             sleep(scroll_pause)  # 等待页面稳定
#
#             # 重新检查元素是否存在
#             if type == "text":
#                 element = driver(text=text_to_find)
#             elif type == "xpath":
#                 element = driver.xpath(text_to_find)
#
#             if ele.exists and element.exists:
#                 print(f"元素已找到: '{text_to_find}'")
#                 ele.click()
#                 print(f"Clicked on '{text_to_find}' after {attempt + 1} attempts.")
#                 return True
#
#             elif element.exists and ele is False:
#                 element.click()
#                 return True
#
#             attempt += 1
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#
#     print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
#     return False


print("----------------------")
# ios-原版
# def scroll_and_click_by_text(driver, el_type='text', text_to_find='FE-W', max_attempts=10, scroll_pause=1):
#     """
#     在可滚动视图中查找指定文本的元素右边的可点击元素并点击。
#     :param driver: facebook-wda的client对象
#     :param el_type: 元素查找类型，支持 'label' 和 'xpath'
#     :param text_to_find: 要查找的文本
#     :param max_attempts: 最大尝试次数
#     :param scroll_pause: 滚动后的暂停时间，秒
#     """
#     attempt = 0
#
#     try:
#         while attempt < max_attempts:
#             # 根据el_type初始化查找元素
#             if el_type == "text":
#                 element = driver(label=text_to_find)
#             elif el_type == "xpath":
#                 element = driver(xpath=f"//*[contains(@name, '{text_to_find}')]")
#             else:
#                 raise ValueError("你可能输入了不支持的元素查找类型···")
#
#             # 尝试查找元素
#             if element.exists:
#                 print(f"元素已找到: '{text_to_find}'")
#                 # 使用 XPath 查找右边的可点击元素
#                 right_element_xpath = f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[1][@visible='true' and @enabled='true']"
#                 right_element_xpath2 = f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[2][@visible='true' and @enabled='true']"
#                 right_element = driver.xpath(right_element_xpath)
#                 right_element2 = driver.xpath(right_element_xpath2)
#                 ele = driver(xpath=right_element_xpath)
#                 ele2 = driver(xpath=right_element_xpath2)
#                 ele_info = ele.label
#                 ele2_info = ele2.label
#                 if right_element.exists and ele_info == 'list device set':
#                     right_element.click()
#                     print(f"Clicked on right element of '{text_to_find}'")
#                     return True
#                 elif right_element2.exists and ele2_info == 'list device set':
#                     right_element2.click()
#                     return True
#                 else:
#                     print(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
#                     return False
#
#             # 滑动屏幕
#             print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
#             driver.swipe_up()
#             time.sleep(scroll_pause)  # 等待页面稳定
#
#             attempt += 1
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#
#     print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
#     return False
print("-----------------------------------------")

# ios-改进版
# def scroll_and_click_by_text(driver, el_type='text', text_to_find='FE-W', max_attempts=10, scroll_pause=1):
#     """
#     在可滚动视图中查找指定文本的元素右边的可点击元素并点击。
#     :param driver: facebook-wda的client对象
#     :param el_type: 元素查找类型，支持 'label' 和 'xpath'
#     :param text_to_find: 要查找的文本
#     :param max_attempts: 最大尝试次数
#     :param scroll_pause: 滚动后的暂停时间，秒
#     """
#     attempt = 0
#
#     def find_and_click(element_xpath):
#         """
#         根据XPath查找元素并点击
#         :param element_xpath: 要查找的元素XPath
#         :return: 是否成功找到并点击元素
#         """
#         element = driver.xpath(element_xpath)
#         if element.exists and element.label == 'list device set':
#             element.click()
#             print(f"Clicked on right element of '{text_to_find}'")
#             return True
#         return False
#
#     try:
#         while attempt < max_attempts:
#             # 根据el_type初始化查找元素
#             if el_type == "text":
#                 element = driver(label=text_to_find)
#             elif el_type == "xpath":
#                 element = driver(xpath=f"//*[contains(@name, '{text_to_find}')]")
#             else:
#                 raise ValueError("你可能输入了不支持的元素查找类型")
#
#             # 尝试查找元素
#             if element.exists:
#                 print(f"元素已找到: '{text_to_find}'")
#                 # 尝试点击右边的可点击元素
#                 if find_and_click(
#                         f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[1][@visible='true' and @enabled='true']"):
#                     return True
#                 if find_and_click(
#                         f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[2][@visible='true' and @enabled='true']"):
#                     return True
#                 else:
#                     print(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
#                     return False
#
#             # 滑动屏幕
#             print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
#             driver.swipe_up()
#             time.sleep(scroll_pause)  # 等待页面稳定
#
#             attempt += 1
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#
#     print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
#     return False


print("--------------------")

# 安卓改进版：
# def scroll_and_click_by_text(driver, el_type='text', text_to_find='FE-W', max_attempts=10, scroll_pause=1):
#     """
#     在可滚动视图中查找指定文本的元素右边的可点击元素并点击。
#     :param el_type:
#     :param driver: uiautomator2的Device对象
#     :param text_to_find: 要查找的文本
#     :param max_attempts: 最大尝试次数
#     :param scroll_pause: 滚动后的暂停时间，秒
#     """
#     attempt = 0
#
#     def find_and_click(element_selector):
#         """
#         根据选择器查找元素并点击
#         :param element_selector: 要查找的元素选择器
#         :return: 是否成功找到并点击元素
#         """
#         element = driver.xpath(element_selector)  # 查找到text_to_find文本右边的第一个元素
#         if element.exists:
#             element2 = driver.xpath(f"//*[@text='{text_to_find}']/following-sibling::*[2][@clickable='true']")
#             if element2.exists:
#                 element2.click()
#             else:
#                 element.click()
#             print(f"Clicked on right element of '{text_to_find}'")
#             return True
#         return False
#
#     try:
#         while attempt < max_attempts:
#             # 查找元素
#             if el_type == "text":
#                 element = driver(text=text_to_find)
#             elif el_type == "xpath":
#                 element = driver.xpath(text_to_find)
#             else:
#                 raise ValueError("你可能输入了不支持的元素查找类型")
#
#             if element.exists:
#                 print(f"元素已找到: '{text_to_find}'")
#                 # 尝试点击右边的可点击元素
#                 if find_and_click(f"//*[@text='{text_to_find}']/following-sibling::*[1][@clickable='true']"):
#                     return True
#                 else:
#                     print(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
#                     return False
#
#             # 滑动屏幕
#             print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
#             driver(scrollable=True).scroll(steps=200)
#             sleep(scroll_pause)  # 等待页面稳定
#
#             attempt += 1
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#
#     print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
#     return False

print("------------------")


# if __name__ == "__main__":
#     driver = u2.connect_usb("28131FDH2000K1")
#     # driver = wda.Client('http://localhost:8100')  # 或者使用其他连接方式，如d = u2.connect('设备IP') for WiFi
#     scroll_and_click_by_text(driver, 'text', text_to_find='REOCYP-332-hhmmkk')

# file = "H:\\app-uiauto-test-dev\\debug\\test.txt"
#
# driver.push(file, "/sdcard/")


# def read_file_from_android(file_path):
#     # 使用adb shell命令读取文件内容
#     cmd = f'adb shell cat {file_path}'
#     try:
#         # 执行命令并获取输出
#         output = subprocess.check_output(cmd, shell=True, text=True)
#         return output
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e.output.strip()}")
#         return None
#
#
# # 示例：读取手机上的/sdcard/myfile.txt文件
# file_content = read_file_from_android('/sdcard/test.txt')
# if file_content:
#     print(file_content)


def get_all_elements_texts(driver, max_scrolls=2, scroll_pause=1):
    """
    获取当前页面的所有元素的text文本内容
    :param scroll_pause:
    :param max_scrolls:
    :param driver: uiautomator2的Device对象
    :return: 文本内容列表
    """
    texts = set()

    for _ in range(max_scrolls):
        # 获取页面的 XML 结构
        page_source = driver.dump_hierarchy()

        # 解析 XML 并提取所有元素的文本内容
        root = ET.fromstring(page_source)

        def parse_element(element):
            text = element.attrib.get('text', '').strip()
            if text:
                texts.add(text)
            for child in element:
                parse_element(child)

        parse_element(root)

        # 滑动屏幕
        driver.swipe_ext("up")
        time.sleep(scroll_pause)  # 等待页面稳定

    return list(texts)


def save_texts_to_file(texts, file_path, exclude_texts=None):
    """
    将文本内容及其数量统计结果写入TXT文件
    :param texts: 文本内容列表
    :param file_path: TXT文件路径
    :param exclude_texts: 要排除的文本内容列表
    """
    if exclude_texts is None:
        exclude_texts = []

    # 排除指定的文本，并确保唯一性
    unique_texts = set(text for text in texts if text not in exclude_texts)

    with open(file_path, 'w', encoding='utf-8') as f:
        for text in sorted(unique_texts):
            f.write(f"{text}\n")


def count_lines_in_file(file_path):
    """
    统计TXT文件中的总行数，不包含空行
    :param file_path: TXT文件路径
    :return: 总行数
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        non_empty_lines = [line for line in lines if line.strip()]
        print(len(non_empty_lines)-1)
    return len(non_empty_lines)-1


# 使用示例
if __name__ == "__main__":
    driver = u2.connect_usb("28131FDH2000K1")
    texts = get_all_elements_texts(driver, max_scrolls=2)
    exclude_texts = ['开', '关', '设置', 'Reolink TrackMix WiFi', '报警设置', '报警通知', '更多', '0', '退出登录设备',
                     '删除']  # 替换为你想要排除的文本
    save_texts_to_file(texts, 'elements_texts.txt', exclude_texts)
    print("文本内容及其数量统计结果已保存到elements_texts.txt文件中。")
    file_path = "H:\\app-uiauto-test-dev\\elements_texts.txt"
    count_lines_in_file(file_path)

