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
# driver = wda.Client('http://localhost:8100')


def scroll_click_right_btn(text_to_find, el_type='text', max_attempts=1, scroll_pause=0.5, platform='android', **kwargs):
    """
    在设备列表中滚动查找指定设备名称(支持单机、nvr、hub),并点击远程设置按钮。
    :param className: 被点击元素的className
    :param resourceId: 元素id
    :param platform:
    :param el_type: 元素查找类型，支持 文本text(label).
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """
    try:
        def find_and_click_ios(xpath_exp):
            element = driver.xpath(xpath_exp)
            if element.exists:
                element.click()
                logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的按钮")
                time.sleep(1)
                return True
            return False

        def click_button_android(text_to_find):
            logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的可点击按钮")
            # dd = driver(text=text_to_find, resourceId='ReoTitle').right(clickable='true')
            # logger.info(dd)
            # driver(text=text_to_find, className=kwargs.get('className1')).right(className=kwargs.get('className2')).click()
            # 根据提供的参数决定操作
            if 'resourceId_1' in kwargs and 'resourceId_2' in kwargs:
                driver(text=text_to_find, resourceId=kwargs['resourceId_1']).right(resourceId=kwargs['resourceId_2']).click()
            elif 'resourceId_1' in kwargs and 'className_2' in kwargs:
                driver(text=text_to_find, resourceId=kwargs['resourceId_1']).right(className=kwargs['className_2']).click()
            elif 'className_1' in kwargs and 'resourceId_2' in kwargs:
                driver(text=text_to_find, className=kwargs['className_1']).right(resourceId=kwargs['resourceId_2']).click()
            elif 'className_1' in kwargs and 'className_2' in kwargs:
                driver(text=text_to_find, className=kwargs['className_1']).right(className=kwargs['className_2']).click()
            else:
                driver(text=text_to_find).right().click()
            time.sleep(1)
            return True

        def click_button_ios(text):
            # 这里的xpath表达式中的下标可能需要根据具体页面分析，先暂时这样写
            if find_and_click_ios(
                    f"//*[contains(@name, '{text}')]/following-sibling::*[3][@visible='true']"):
                return True
            else:
                logger.info(f"没有找到目标元素{text}右边的按钮")
                return False

        # 根据el_type初始化查找元素
        if el_type == "text":
            element = driver(text=text_to_find) if platform == "android" else driver(label=text_to_find)
        else:
            raise ValueError("你可能输入了不支持的元素查找类型")

        attempt = 0

        if platform == "android":
            while attempt <= max_attempts:
                if element.exists:
                    logger.info(f"【{text_to_find}】元素已找到")
                    click_button_android(text_to_find)
                    driver.xpath(xpath='').set_text('111.111.111.111')
                    break
                else:
                    # 滑动屏幕
                    logger.info(f"尝试滑动查找 '{text_to_find}'... 第{attempt + 1}次")
                    driver(scrollable=True).scroll(steps=150)

                attempt += 1

        if platform == "ios":
            # 判断元素是否可见，不可见则滑动至可见后点击
            e_is_visible = driver(text=text_to_find)
            while attempt <= max_attempts:
                if element.exists and e_is_visible.visible:
                    logger.info(f"【{text_to_find}】元素存在且可见")
                    click_button_ios(text_to_find)
                    break
                else:
                    # 获取可滑动的元素，此处根据className(Type)定位
                    logger.info(f"尝试滑动查找 '{text_to_find}'... 第{attempt + 1}次")
                    e = driver(className='XCUIElementTypeTable')
                    e.scroll('down')
                    time.sleep(scroll_pause)  # 等待页面稳定

                attempt += 1

    except Exception as err:
        logger.info(f"可能发生了错误: {err}")
        return False


scroll_click_right_btn(text_to_find='匿名传输',
                       className_1='android.widget.TextView',
                       className_2='android.view.ViewGroup')
