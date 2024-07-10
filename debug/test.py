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

driver = u2.connect_usb("28131FDH2000K1")


def scroll_and_click_by_text(driver, text_to_find='FE-W', max_attempts=10, scroll_pause=1):
    """
    在可滚动视图中查找并点击指定文本的元素。
    :param d: uiautomator2的device对象
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    attempt = 0
    while attempt < max_attempts:
        try:
            # 尝试直接查找并点击元素，避免不必要的滚动
            element = driver(text=text_to_find)
            if element.exists:
                element.click()
                print(f"Clicked on '{text_to_find}' after {attempt + 1} attempts.")
                return True
            else:
                driver(scrollable=True).scroll.toEnd()
        except Exception as e:
            print(f"Error occurred: {e}")
        # 如果未找到，尝试滚动查找
        print(f"Scrolling to find '{text_to_find}'...")
        sleep(scroll_pause)  # 等待页面稳定
        attempt += 1

    print(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
    return False


if __name__ == "__main__":
    driver = u2.connect_usb()  # 或者使用其他连接方式，如d = u2.connect('设备IP') for WiFi
    scroll_and_click_by_text(driver, 'RLC-81MA')
















# 在拥有scrollable属性的元素上垂直滚动，滚动到text属性为hello的元素位置
# driver(scrollable=True).scroll.to(text='FE-W')
# driver(text='FE-W').click()

# driver.swipe_ext('up', scale=1)

# scrollable_element = driver(text='small Home Hub')


# driver.xpath('//*[@text="small Home Hub"]').click()

# driver(text='KKKKKKKKKKKKKKKKKKKKKKKK').click()


# print("--------------------------------")

# ios_driver = wda.Client('http://localhost:8100')
# element = ios_driver(xpath="(//XCUIElementTypeButton)[2]")  # 定位添加按钮
# element.click()  # 点击添加按钮
#
# element = ios_driver(xpath='(//*[@label="手动输入"])[2]')  # 定位手动输入
# element.click()  # 点击手动输入
# ios_driver(xpath='(//XCUIElementTypeTextField)').set_text("564186156")  # 定位输入框，赋值给ee
