import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import wda

from common_tools.logger import logger

# driver = u2.connect_usb("28131FDH2000K1")
# driver = wda.Client('http://localhost:8100')


import time
import logging


def access_in_remote_setting_debug(self, text_to_find, el_type='text', max_attempts=15, scroll_pause=0.5):
    """
    在设备列表中滚动查找指定设备名称,并点击远程设置按钮。先这样写。
    :param el_type: 元素查找类型，支持 文本text(label) 和 'xpath'.
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    attempt = 0
    if self.platform == "android":
        def find_and_click(element_selector):
            """
            根据xpath选择器查找元素并点击
            :param element_selector: xpath表达式
            :return: 是否成功找到并点击元素
            """
            element = self.driver.xpath(element_selector)  # 查找到text_to_find文本右边的第一个元素
            if element.exists:
                element2 = self.driver.xpath(
                    f"//*[@text='{text_to_find}']/following-sibling::*[2][@clickable='true']")
                if element2.exists:
                    element2.click()
                else:
                    element.click()
                time.sleep(2)
                logger.info(f"Clicked on right element of '{text_to_find}'")
                return True
            return False

        try:
            while attempt < max_attempts:
                # 查找元素
                if el_type == "text":
                    element = self.driver(text=text_to_find)
                elif el_type == "xpath":
                    element = self.driver.xpath(text_to_find)
                else:
                    raise ValueError("你可能输入了不支持的元素查找类型")

                if element.exists:
                    logger.info(f"元素已找到: '{text_to_find}'")
                    # 尝试点击右边的可点击元素
                    if find_and_click(f"//*[@text='{text_to_find}']/following-sibling::*[1][@clickable='true']"):
                        return True
                    else:
                        logger.info(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
                        self.driver(text=text_to_find).click()
                        return True

                # 滑动屏幕
                logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                self.driver(scrollable=True).scroll(steps=150)
                time.sleep(scroll_pause)  # 等待页面稳定

                attempt += 1

        except Exception as e:
            logger.info(f"Error occurred: {e}")

        logger.info(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
        self.driver()
        return False

    elif self.platform == "ios":
        def find_and_click(element_selector):
            """
            根据XPath查找元素并点击
            :param element_selector: 要查找的元素XPath
            :return: 是否成功找到并点击元素
            """
            element = self.driver.xpath(element_selector)
            if element.exists and element.label == 'list device set':
                element.click()
                time.sleep(2)
                logger.info(f"Clicked on right element of '{text_to_find}'")
                return True
            return False

        try:
            while attempt < max_attempts:
                # 根据el_type初始化查找元素
                if el_type == "text":
                    element = self.driver(label=text_to_find)
                elif el_type == "xpath":
                    element = self.driver(xpath=f"//*[contains(@name, '{text_to_find}')]")
                else:
                    raise ValueError("你可能输入了不支持的元素查找类型")

                # 尝试查找元素
                if element.exists:
                    logger.info(f"元素已找到: '{text_to_find}'")
                    # 尝试点击右边的可点击元素
                    if find_and_click(
                            f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[1][@visible='true' and @enabled='true']"):
                        return True
                    if find_and_click(
                            f"//*[contains(@name, '{text_to_find}')]/following-sibling::*[2][@visible='true' and @enabled='true']"):
                        return True
                    else:
                        logger.info(f"没有找到目标元素右边的可点击元素: '{text_to_find}'")
                        self.driver(label=text_to_find).click()
                        return True

                # 滑动屏幕
                logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                self.driver.swipe_up()
                time.sleep(scroll_pause)  # 等待页面稳定

                attempt += 1

        except Exception as e:
            logger.info(f"Error occurred: {e}")

        logger.info(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
        return False

