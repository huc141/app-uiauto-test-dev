import os
import time
from typing import Literal

import pytest
import yaml
import uiautomator2 as u2

from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.rn_device_setting_page.remote_setting import RemoteSetting

driver = u2.connect_usb()

# devices_config = read_yaml.load_device_config(yaml_file_name='wifi.yaml')  # 读取参数化文件
# print(devices_config)
#
# remote_setting_wifi = devices_config[0]['device_list_name']
#
# print('------------------')
#
# print(remote_setting_wifi)
#
# print('------------------')
# page_fun = RemoteSetting().scroll_check_funcs(remote_setting_wifi)

# 读取yaml文件中预期功能项
# page_fun_list = RemoteSetting().extract_yaml_names(remote_setting_wifi, 'name')
# print(page_fun_list)


# 提取ipc和hub部分items中的name值
# ipc_names = [item['name'] for item in remote_setting_wifi['advanced_setting_page']['items'].values()]
# hub_names = [item['name'] for item in devices_config[0]['hub']['advanced_setting_page']['items'].values()]

# 打印结果
# print("ipc部分items的name值:", ipc_names)
# print("hub部分items的name值:", hub_names)
def scroll_screen(max_scrolls=1, direction="up", platform='android'):
    """
    滚动屏幕
    :param platform:
    :param direction: 屏幕的滚动方向：
    :param max_scrolls: 最大滚动次数，默认1次
    :return:
    """

    if platform == "android":
        scroll_method = driver.swipe_ext

    elif platform == "ios":
        scroll_method = driver.swipe_up
    else:
        raise ValueError("不支持当前平台")

    for _ in range(max_scrolls):
        if platform == "android":
            scroll_method(direction)
        else:
            time.sleep(1)
            scroll_method()


def get_all_texts(selector_type, selector, max_scrolls=2, platform='android'):
    """
    滚动获取当前页面所有指定文本
    :param platform:
    :param selector_type: 支持安卓className，resource-id定位，iOS的className定位
    :param selector: 对应的value值
    :param max_scrolls: 最大滚动次数
    :return:
    """
    # TODO: 需要和rn开发确定定位元素的方法，才好提取指定元素
    my_set = set()

    def get_elements_texts():
        if platform == 'android':
            if selector_type == 'id':
                elements = driver(resourceId=selector)
            elif selector_type == 'class':
                elements = driver(className=selector)
            return {element.get_text() for element in elements}

        elif platform == 'ios':
            elements = driver(id=selector).find_elements()
            return {element.text for element in elements}

    # 获取当前页面所有元素的文本内容
    for _ in range(max_scrolls):
        # 获取当前页面所有元素的文本内容
        new_texts = get_elements_texts()
        my_set.update(new_texts)

        scroll_screen()
        time.sleep(0.5)

        # 检查滑动后页面是否有变化
        new_texts = get_elements_texts()
        if not new_texts - my_set:
            break  # 如果滑动后没有新内容，退出循环

        # 添加新获取的文本内容
        my_set.update(new_texts)

    return list(my_set)


def scroll_check_funcs2(texts, selector, selector_type='id'):
    """
    遍历并判断功能项(名称)是否存在当前页面，同时比对数量是否正确。
    :param selector_type: 元素的定位方式，默认根据id进行文本提取。
    :param selector: 元素定位的具体id。
    :param texts: 存储了预期功能项名称的列表。
    :return:
    """
    # TODO: 待验证该方法是否可用
    ele_exists = []  # 当前页面存在的功能
    ele_not_exists = []  # 当前页面缺失的功能
    try:
        # 先滚动页面获取指定id的文本
        actual_texts = get_all_texts(selector=selector, selector_type=selector_type)

        if isinstance(texts, list):
            # 如果 texts 是一个列表，遍历列表中的每个功能项名称
            for text in texts:
                is_in_actual_texts = text in actual_texts
                if is_in_actual_texts:
                    ele_exists.append(text)
                else:
                    ele_not_exists.append(text)

            # 检查是否list2中的所有元素都在list1中
            all_elements_exist = all(ele_exists)
            # 检查两个列表的长度是否相同
            lengths_are_equal = len(actual_texts) == len(texts)

            if all_elements_exist and lengths_are_equal:
                logger.info(f"需校验的功能项均存在！-->{texts}")
                return True
            else:
                logger.info(f"当前页面存在的功能有：{ele_exists}")
                logger.info(f"当前页面缺失的功能有：{ele_not_exists}")
                return False

        elif isinstance(texts, str):
            # 如果 texts 是一个单一的文本，在当前页面滚动查找该文本是否存在
            ele_status = True
            if not ele_status:
                logger.info(f"当前页面缺失的功能有：{texts}")
                return False
            else:
                logger.info(f"需校验的功能项均存在！-->{texts}")
                return True

    except Exception as err:
        logger.info(f"可能发生了错误: {err}")
        return False
