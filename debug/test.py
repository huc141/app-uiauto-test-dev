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

# driver = u2.connect_usb("28131FDH2000K1")

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
#     is_find = None
#     attempt = 0
#
#     try:
#         # 根据类型初始化查找元素
#         if type == "text":
#             element = driver(text=text_to_find).right(clickable=True)
#             # driver(text='hello').right(checked=True)
#             # 尝试直接滚动到指定文本
#             print(f"Attempting to scroll to '{text_to_find}' directly.")
#             is_find = driver(scrollable=True).scroll.to(text=text_to_find)
#         elif type == "xpath":
#             element = driver.xpath(text_to_find)
#             driver(scrollable=True).fling.vert.toBeginning(max_swipes=1000)  # 滑动至顶部
#         else:
#             raise ValueError("你可能输入了不支持的元素查找类型···")
#
#         # 检查元素是否存在
#         if element.exists:
#             print(f"元素已找到: '{text_to_find}'")
#             element.click()
#             print(f"Clicked on '{text_to_find}' directly.")
#             return True
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
#             if element.exists:
#                 print(f"元素已找到: '{text_to_find}'")
#                 element.click()
#                 print(f"Clicked on '{text_to_find}' after {attempt + 1} attempts.")
#                 return True
#
#             attempt += 1
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#
#     print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
#     return False

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

# ios-改进版
def scroll_and_click_by_text(driver, el_type='text', text_to_find='FE-W', max_attempts=10, scroll_pause=1):
    """
    在可滚动视图中查找指定文本的元素右边的可点击元素并点击。
    :param driver: facebook-wda的client对象
    :param el_type: 元素查找类型，支持 'label' 和 'xpath'
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    attempt = 0

    def find_and_click(element_xpath):
        """
        根据XPath查找元素并点击
        :param element_xpath: 要查找的元素XPath
        :return: 是否成功找到并点击元素
        """
        element = driver.xpath(element_xpath)
        if element.exists and element.label == 'list device set':
            element.click()
            print(f"Clicked on right element of '{text_to_find}'")
            return True
        return False

    try:
        while attempt < max_attempts:
            # 根据el_type初始化查找元素
            if el_type == "text":
                element = driver(label=text_to_find)
            elif el_type == "xpath":
                element = driver(xpath=f"//*[contains(@name, '{text_to_find}')]")
            else:
                raise ValueError("你可能输入了不支持的元素查找类型")

            # 尝试查找元素
            if element.exists:
                print(f"元素已找到: '{text_to_find}'")
                # 尝试点击右边的可点击元素
                if find_and_click(f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[1][@visible='true' and @enabled='true']"):
                    return True
                if find_and_click(f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[2][@visible='true' and @enabled='true']"):
                    return True
                else:
                    print(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
                    return False

            # 滑动屏幕
            print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
            driver.swipe_up()
            time.sleep(scroll_pause)  # 等待页面稳定

            attempt += 1

    except Exception as e:
        print(f"Error occurred: {e}")

    print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
    return False


if __name__ == "__main__":
    # driver = u2.connect_usb("28131FDH2000K1")
    driver = wda.Client('http://localhost:8100')  # 或者使用其他连接方式，如d = u2.connect('设备IP') for WiFi
    scroll_and_click_by_text(driver, 'text', text_to_find='Reolink Go PT Plus')


# 安卓改进版：
def scroll_and_click_by_text(driver, text_to_find='FE-W', max_attempts=10, scroll_pause=1):
    """
    在可滚动视图中查找指定文本的元素右边的可点击元素并点击。
    :param driver: uiautomator2的Device对象
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    attempt = 0

    def find_and_click(element_selector):
        """
        根据选择器查找元素并点击
        :param element_selector: 要查找的元素选择器
        :return: 是否成功找到并点击元素
        """
        element = driver.xpath(element_selector)
        if element.exists and element.info.get('text') == 'list device set':
            element.click()
            print(f"Clicked on right element of '{text_to_find}'")
            return True
        return False

    try:
        while attempt < max_attempts:
            # 查找元素
            element = driver(text=text_to_find)

            if element.exists:
                print(f"元素已找到: '{text_to_find}'")
                # 尝试点击右边的可点击元素
                if find_and_click(f"//*[@text='{text_to_find}']/following-sibling::*[1][@clickable='true']"):
                    return True
                if find_and_click(f"//*[@text='{text_to_find}']/following-sibling::*[2][@clickable='true']"):
                    return True
                else:
                    print(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
                    return False

            # 滑动屏幕
            print(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
            driver.swipe_ext("up")
            time.sleep(scroll_pause)  # 等待页面稳定

            attempt += 1

    except Exception as e:
        print(f"Error occurred: {e}")

    print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
    return False