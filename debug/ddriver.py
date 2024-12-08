import os
import time

import pytest
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import wda

from common_tools.logger import logger

# driver = u2.connect_usb("28131FDH2000K1")
# driver = wda.Client('http://localhost:8100')


import time
import logging


def access_in_remote_setting(self, text_to_find, el_type='text', max_attempts=15, scroll_pause=0.5):
    """
    在设备列表中滚动查找指定设备名称(支持单机、nvr、hub),并点击远程设置按钮。
    :param el_type: 元素查找类型，支持 文本text(label).
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    attempt = 0

    def retry_method(num=4):
        count_num = 1
        while count_num <= num:
            status = self.driver(text='连接失败，点击重试')

            if count_num == num and status:
                pytest.fail(f'已重试 {num} 次，未能连接上该设备！')
            elif status:
                self.click_by_text(text='连接失败，点击重试')
                time.sleep(5)
                count_num += 1
            else:
                break

    def find_and_click_android(text):

        setting_element1 = f"//*[@text='{text}']/following-sibling::*[1][@clickable='true']"

        setting_element2 = f"//*[@text='{text}']/following-sibling::*[2][@clickable='true']"

        setting_element3 = f"//*[@text='{text}']/following-sibling::*[3][@clickable='true']"

        logger.info(f"尝试点击这个 '{text}' 元素右边的远程设置按钮")

        if self.driver.xpath(setting_element3).exists:
            self.driver.xpath(setting_element3).click()

        elif self.driver.xpath(setting_element2).exists:
            self.driver.xpath(setting_element2).click()

        elif self.driver.xpath(setting_element1).exists:
            self.driver.xpath(setting_element1).click()

        time.sleep(25)
        retry_method()

        return False

    def find_and_click_ios(xpath_exp):
        element = self.driver.xpath(xpath_exp)
        if element.exists and element.label == 'list device set':
            element.click()
            logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的远程设置按钮")
            time.sleep(3)
            return True
        return False

    def find_and_click_android_xpath(text):
        if find_and_click_android(text=text):
            return True
        else:
            logger.info(f"没有找到目标元素右边的远程设置按钮: '{text}'")
            # self.driver(text=text).click()
            self.click_by_text(text)
            return True

    def find_and_click_ios_xpath(text):
        if find_and_click_ios(
                f"//*[contains(@name, '{text}')]/following-sibling::*[1][@visible='true' and @enabled='true']"):
            return True
        if find_and_click_ios(
                f"//*[contains(@name, '{text}')]/following-sibling::*[2][@visible='true' and @enabled='true']"):
            return True
        else:
            logger.info(f"没有找到目标元素右边的远程设置按钮: '{text}'")
            # self.driver(label=text).click()
            self.click_by_text(text)
            return True

    try:
        while attempt < max_attempts:
            # 根据el_type初始化查找元素
            if el_type == "text":
                element = self.driver(text=text_to_find) if self.platform == "android" else self.driver(
                    label=text_to_find)
            elif el_type == "xpath":
                element = self.driver.xpath(text_to_find)
            else:
                raise ValueError("你可能输入了不支持的元素查找类型")

            if element.exists:
                logger.info(f"元素已找到: '{text_to_find}'")
                if self.platform == "android":
                    if find_and_click_android_xpath(text_to_find):
                        return True
                elif self.platform == "ios":
                    if find_and_click_ios_xpath(text_to_find):
                        return True

            # 滑动屏幕
            logger.info(f"尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
            if self.platform == "android":
                self.driver(scrollable=True).scroll(steps=150)
            elif self.platform == "ios":
                self.driver.swipe_up()
            time.sleep(scroll_pause)  # 等待页面稳定

            attempt += 1

    except Exception as err:
        # logger.info(f"可能发生了错误: {err}")
        pytest.fail(f"函数执行出错: {str(err)}")

    logger.info(f"还是没找到 '{text_to_find}' 元素，已经尝试了 {max_attempts} 次.")
    return False

