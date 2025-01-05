import os
import subprocess
import time
from datetime import datetime

import yaml
from uiautomator2.exceptions import XPathElementNotFoundError
from common_tools.app_driver import driver
from common_tools.logger import logger
from typing import Literal, List, Any
import pytest
import xml.etree.ElementTree as ET
from common_tools.handle_alerts import handle_alert
from uiautomator2 import Direction

from common_tools.read_yaml import read_yaml

DEFAULT_SECONDS = 15
g_config_back = read_yaml.get_data(key="back", source="global_data")  # 读取全局配置


class BasePage:
    def __init__(self):
        self.driver = driver.get_actual_driver()
        self.platform = driver.get_platform()

    def is_element_exists(self, element_value, selector_type='text', max_scrolls=2, scroll_or_not=True):
        """
        判断元素是否存在当前页面
        :param element_value: 你要找的文本内容，或者对应元素的id、xpath值。
        :param selector_type: 安卓支持：text文本、id、xpath定位；iOS支持text(label)文本、id、xpath定位。
        :param max_scrolls: 最大滚动次数，默认两次。
        :param scroll_or_not: 是否执行滚动查找。布尔值，默认True滚动查找
        :return: bool
        """
        ele_status = None
        try:
            def check_element():
                if self.platform == "android":
                    if selector_type == "text":
                        return self.driver(text=element_value).exists
                    elif selector_type == "id":
                        return self.driver(resourceId=element_value).exists
                    elif selector_type == "xpath":
                        return self.driver.xpath(element_value).exists
                    else:
                        raise ValueError("你可能输入了不支持的 selector type.")

                elif self.platform == "ios":
                    if selector_type == "text":
                        return self.driver(label=element_value)
                    elif selector_type == "id":
                        return self.driver(id=element_value)
                    elif selector_type == "xpath":
                        return self.driver.xpath(element_value)
                    else:
                        raise ValueError("你可能输入了不支持的 selector type.")

            for _ in range(max_scrolls):
                ele_status = check_element()
                if ele_status:
                    break

                if scroll_or_not:
                    self.scroll_screen()
                    logger.info(f"正在滑动屏幕查找：{element_value} 元素")
                    time.sleep(0.5)

            if not ele_status:
                logger.info(f"{element_value} 元素未找到！")

            return ele_status

        except Exception as err:
            logger.error(f"元素未找到 {selector_type}: {element_value}. Error: {err}")
            return False

    def wait_for_element(self, text, timeout=10):
        """
        动态等待text文本元素出现
        :param text: 需要等待的文本内容
        :param timeout: 超时时间，默认10秒
        :return:
        """
        try:
            for _ in range(timeout):
                if self.driver(text=text).exists:
                    return True
                time.sleep(1)
            return False
        except Exception as err:
            logger.error(f"动态等待函数执行出错: {str(err)}")

    def retry_method(self, num_retries=5):
        """
        带动态等待的重试方法。
        :param num_retries: 最大重试次数
        :return: 如果操作成功，返回 True；否则返回 False
        """
        retry_button = '重试'  # 待检测的全局按钮
        loading_text = '加载中，请稍候...'  # 加载提示文本

        for attempt in range(num_retries):
            try:
                # 检测“重试”按钮是否存在
                if self.wait_for_element(text=retry_button):
                    logger.warning(f"检测到【{retry_button}】按钮，尝试第{attempt + 1}次点击...")
                    self.click_by_text(retry_button)
                    logger.info(f"已点击【{retry_button}】按钮，等待页面更新...")
                    time.sleep(6)  # 短暂等待页面刷新

                # 检测“加载中”状态
                elif self.wait_for_element(text=loading_text):
                    logger.warning("页面正在加载中，请等待...")
                    time.sleep(6)  # 短暂等待加载完成

                # 未检测到任何状态
                else:
                    logger.warning("未检测到重试按钮或加载中状态，可能已加载完成...")
                    return True

            except Exception as e:
                logger.error(f"重试操作中发生错误：{e}")

        # 所有重试均失败，报告错误
        pytest.fail(f"已尝试点击【{retry_button}】按钮 {num_retries} 次，但页面加载均失败")

    def loop_detect_element_exist(self, element_value, selector_type='text', loop_times=10, time_interval=3, scroll_or_not=True):
        """
        循环检测元素是否出现，默认循环10次，每次间隔3秒
        :param element_value: 你要找的元素，支持文本、xpath
        :param selector_type: 安卓支持：text文本、xpath定位；iOS支持text(label)文本、xpath定位。
        :param loop_times: 最大循环次数
        :param time_interval: 每次循环间隔时间，默认3秒
        :param scroll_or_not: 是否执行滚动查找。布尔值，默认True滚动查找
        :return: bool
        """
        try:
            retry_button = '重试'  # 待检测的全局按钮
            for i in range(loop_times):
                time.sleep(time_interval)
                logger.info(f"正在循环检测 {element_value} 元素是否出现，第 {i + 1} 次")
                if self.is_element_exists(element_value=element_value, selector_type=selector_type,
                                          max_scrolls=1, scroll_or_not=scroll_or_not):
                    logger.info(f"检测到 {element_value} 元素存在")
                    return True

                elif self.driver(text=retry_button).exists:
                    self.retry_method()

            return False
        except Exception as err:
            logger.error(f"函数执行出错: {str(err)}")

    def loop_detect_element_and_click(self, element_value, selector_type='text', loop_times=10, scroll_or_not=True):
        """
        循环检测元素是否出现，出现则点击，循环10次，每次间隔2秒
        :param element_value: 你要找的元素，支持文本、xpath
        :param selector_type: 安卓支持：text文本、xpath定位；iOS支持text(label)文本、xpath定位。
        :param loop_times: 最大循环次数
        :param scroll_or_not: 是否执行滚动查找。布尔值，默认True滚动查找
        :return: bool
        """
        try:
            for i in range(loop_times):
                time.sleep(2)
                logger.info(f"正在循环检测 {element_value} 元素是否出现，第 {i + 1} 次")
                if self.is_element_exists(element_value=element_value, selector_type=selector_type,
                                          max_scrolls=1, scroll_or_not=scroll_or_not):
                    if selector_type == 'text':
                        self.click_by_text(text=element_value)
                    elif selector_type == 'xpath':
                        self.click_by_xpath(xpath_expression=element_value)
                    return True
            return False
        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def find_element_by_xpath(self, xpath_expression):
        """
        通过xpath定位元素
        :param xpath_expression: xpath表达式
        :return:
        """
        if self.platform == "android":
            return self.driver.xpath(xpath_expression)
        elif self.platform == "ios":
            return self.driver(xpath=xpath_expression)

    def long_click_by(self, text_to_find, el_type='text', max_attempts=5, scroll_pause=0.5, duration=3000):
        """
        在可滚动视图中查找并点击指定文本或xpath的元素。
        :param text_to_find: 要查找的文本/xpath
        :param el_type: 元素定位类型，支持文本text(label)和xpath
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        :param duration: ios长按时间，毫秒，默认3秒
        """
        attempt = 0
        time.sleep(2)

        try:
            if self.platform == "android":
                # 如果未找到，则尝试滚动查找
                while attempt < max_attempts:
                    # 根据类型初始化查找元素
                    if el_type == "text":
                        element = self.driver(text=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver.xpath(text_to_find)
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型el_type！")

                    # 检查元素是否存在
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.long_click()
                        logger.info(f"长按 '{text_to_find}'")
                        return True

                    # 滑动屏幕
                    logger.info(f"正在尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
                    self.driver(scrollable=True).scroll(steps=150)
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

            elif self.platform == "ios":
                while attempt < max_attempts:
                    # 根据el_type初始化查找元素
                    if el_type == "text":
                        element = self.driver(label=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver(xpath=text_to_find)
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型el_type···")

                    # 尝试查找元素并长按
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.press(duration=duration)
                        logger.info(f"长按 '{text_to_find}'")
                        return True

                    # 滑动屏幕
                    logger.info(f"正在尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
                    self.driver.swipe_up()
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def click_by_text(self, text, retries=2, is_click_again: Literal[True, False] = False):
        """
        :param text: 通过文本定位单个元素，并进行点击。
        :param retries: 如果遇到权限弹窗，会自动处理, 如果处理了弹窗，则通过is_click_again参数来判断是否重新尝试点击对应文本的元素.
        :param is_click_again: 接收布尔值，默认为False，代表处理了弹窗之后，不会尝试再次点击text元素；若为True，则处理弹窗之后，再次重新点击text元素
        :return:
        """
        for attempt in range(retries):
            element = None
            try:
                time.sleep(1)
                if self.platform == 'android':
                    element = self.driver(text=text)
                elif self.platform == 'ios':
                    element = self.driver(label=text)

                logger.info(f"正在尝试点击 {text} 元素")
                element.click()
                time.sleep(2)

                if handle_alert.handle_alerts():
                    if is_click_again:
                        continue  # 如果is_click_again==True，则处理了权限弹窗后，重试点击操作
                    else:
                        return True  # 如果is_click_again==False，则处理了权限弹窗后，不重试点击。
                return True
            except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
                logger.error("ValueError: %s", verr)
                raise
            except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
                logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", text, err)
                pytest.fail(f"页面中没有找到id为 {text} 的元素，原因可能是：{err}")
        return False

    def click_by_id(self, resource_id, retries=2, is_click_again: Literal[True, False] = False):
        """
        :param resource_id: 通过id定位单个元素，并进行点击。
        :param retries: 如果遇到权限弹窗，会自动处理, 如果处理了弹窗，则通过is_click_again参数来判断是否重新尝试点击resource_id元素.
        :param is_click_again: 接收布尔值，默认为False，代表处理了弹窗之后，不会尝试再次点击resource_id元素；若为True，则处理弹窗之后，再次重新点击resource_id元素
        :return:
        """
        for attempt in range(retries):
            element = None
            try:
                time.sleep(1)
                if self.platform == 'android':
                    element = self.driver(resourceId=resource_id)
                elif self.platform == 'ios':
                    element = self.driver(label=resource_id)

                if not element.exists:
                    logger.error("该点击元素：%s 不存在", resource_id)
                    raise ValueError(f"该点击元素：{resource_id} 不存在")

                element.click()
                time.sleep(2)

                if handle_alert.handle_alerts():
                    if is_click_again:
                        continue  # 如果is_click_again==True，则处理了权限弹窗后，重试点击操作
                    else:
                        return True  # 如果is_click_again==False，则处理了权限弹窗后，不重试点击。
                return True
            except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
                logger.error("ValueError: %s", verr)
                raise
            except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
                logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", resource_id, err)
                raise
        return False

    def click_by_xpath(self, xpath_expression, retries=2, is_click_again: Literal[True, False] = False):
        """
        :param xpath_expression: 通过xpath定位
        :param retries: 如果遇到权限弹窗，会自动处理, 如果处理了弹窗，则通过is_click_again参数来判断是否重新尝试点击xpath_expression元素.
        :param is_click_again: 接收布尔值，默认为False，代表处理了弹窗之后，不会尝试再次点击xpath_expression元素；若为True，则处理弹窗之后，再次重新点击xpath_expression元素
        :return:
        """
        for attempt in range(retries):
            element = None
            try:
                time.sleep(2)
                if self.platform == 'android':
                    element = self.find_element_by_xpath(xpath_expression)
                elif self.platform == 'ios':
                    element = self.find_element_by_xpath(xpath_expression)

                if not element.exists:
                    logger.error("该点击元素：%s 不存在", xpath_expression)
                    raise ValueError(f"该点击元素：{xpath_expression} 不存在")

                element.click()
                time.sleep(2)

                if handle_alert.handle_alerts():
                    if is_click_again:
                        continue  # 如果is_click_again==True，则处理了权限弹窗后，重试点击操作
                    else:
                        return True  # 如果is_click_again==False，则处理了权限弹窗后，不重试点击。
                return True
            except ValueError as verr:
                logger.error("ValueError: %s", verr)
                raise
            except Exception as err:
                logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", xpath_expression, err)
                raise
        return False

    def scroll_click_right_btn(self, text_to_find, el_type='text', max_attempts=1, scroll_pause=0.5, **kwargs):
        """
        在当前页面滑动查找并点击指定文本右侧的可点击元素/按钮。
        :param el_type: 元素查找类型，支持 文本text(label).
        :param text_to_find: 要查找的文本
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        try:
            def find_and_click_ios(xpath_exp):
                element = self.driver.xpath(xpath_exp)
                if element.exists:
                    element.click()
                    logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的按钮")
                    time.sleep(1)
                    return True
                return False

            def click_button_android(text):
                logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的可点击按钮")
                # self.driver(text=text, resourceId='com.mcu.reolink:id/tv_remote_toggle').right(
                #     clickable='true').click()  # ReoTitle
                # 根据提供的参数决定操作
                if 'resourceId_1' in kwargs and 'resourceId_2' in kwargs:
                    self.driver(text=text_to_find, resourceId=kwargs['resourceId_1']).right(
                        resourceId=kwargs['resourceId_2']).click()
                elif 'resourceId_1' in kwargs and 'className_2' in kwargs:
                    self.driver(text=text_to_find, resourceId=kwargs['resourceId_1']).right(
                        className=kwargs['className_2']).click()
                elif 'className_1' in kwargs and 'resourceId_2' in kwargs:
                    self.driver(text=text_to_find, className=kwargs['className_1']).right(
                        resourceId=kwargs['resourceId_2']).click()
                elif 'className_1' in kwargs and 'className_2' in kwargs:
                    self.driver(text=text_to_find, className=kwargs['className_1']).right(
                        className=kwargs['className_2']).click()
                else:
                    self.driver(text=text, resourceId='com.mcu.reolink:id/tv_remote_toggle').right().click()
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
                element = self.driver(text=text_to_find) if self.platform == "android" else self.driver(
                    label=text_to_find)
            else:
                raise ValueError("你可能输入了不支持的元素查找类型")

            attempt = 0

            if self.platform == "android":
                while attempt <= max_attempts:
                    if element.exists:
                        logger.info(f"【{text_to_find}】元素已找到")
                        click_button_android(text_to_find)
                        break
                    else:
                        # 滑动屏幕
                        logger.info(f"尝试滑动查找 '{text_to_find}'... 第{attempt + 1}次")
                        self.driver(scrollable=True).scroll(steps=150)

                    attempt += 1

            if self.platform == "ios":
                # 判断元素是否可见，不可见则滑动至可见后点击
                e_is_visible = self.driver(text=text_to_find)
                while attempt <= max_attempts:
                    if element.exists and e_is_visible.visible:
                        logger.info(f"【{text_to_find}】元素存在且可见")
                        click_button_ios(text_to_find)
                        break
                    else:
                        # 获取可滑动的元素，此处根据className(Type)定位
                        logger.info(f"尝试滑动查找 '{text_to_find}'... 第{attempt + 1}次")
                        e = self.driver(className='XCUIElementTypeTable')
                        e.scroll('down')
                        time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def get_toast(self, toast_text: str, reset=True, timeout=5.0, default="没有获取到toast提示"):
        """
        废除！该方法不可用！ 获取页面弹出的toast
        :param timeout: 超时时间，默认5秒
        :param toast_text: 需要检查的toast文案
        :param reset: 默认为True，即清除缓存的Toast，传False则不清除
        :param default: 如果10s内没有获取到Toast，则返回此默认消息
        :return:
        """
        # TODO: 待写
        pass

    def take_screenshot(self):
        """
        屏幕截图，主要提供给写用例时需要主动截图的步骤进行调用。
        :return:
        """
        screenshot_save_path = os.path.join(os.getcwd(), 'screenshot/android')
        ios_screenshot_save_path = os.path.join(os.getcwd(), 'screenshot/iOS')

        # 确保保存目录存在
        if not os.path.exists(screenshot_save_path):
            os.makedirs(screenshot_save_path)
            logger.info("创建screenshot/android目录")
        if not os.path.exists(ios_screenshot_save_path):
            os.makedirs(ios_screenshot_save_path)
            logger.info("创建screenshot/iOS目录")

        # 获取当前时间并格式化为字符串
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if self.platform == "android":  # 处理安卓设备的截图
            filename = f"{timestamp}-android.png"
            filepath = os.path.join(screenshot_save_path, filename)
            self.driver.screenshot(filepath)
            logger.info("Taking screenshot on Android device.")

        elif self.platform == "ios":  # 处理iOS设备的截图
            filename = f"{timestamp}-iOS.png"
            filepath = os.path.join(ios_screenshot_save_path, filename)
            self.driver.screenshot(filepath)
            logger.info("Taking screenshot on iOS device.")

        else:
            raise ValueError("可能碰到了不支持当前截图方法的设备类型. Please specify 'android' or 'ios'.")

    def input_text(self, xpath_exp, text):
        """
        输入文本,不清空文本框内容。
        :xpath_exp: 编辑框的xpath表达式
        :text： 要输入的文本内容
        :return:
        """
        try:
            if self.platform == "android":
                time.sleep(1)
                self.driver.xpath(xpath_exp).set_text(text)
                time.sleep(1)
                # self.driver.set_input_ime(True)
                # time.sleep(0.2)
                # self.driver.send_keys(text)
                # for char in text:
                #     os.system('adb shell input text {}'.format(text))
                #     time.sleep(0.2)
            elif self.platform == "ios":
                self.driver(xpath=xpath_exp).set_text(text)

        except Exception as err:
            logger.error(f"内容{text} 输入失败···，原因： {err} ")

    def input_text_clear(self, xpath_exp, text):
        """
        清空文本框内容后输入。
        :param xpath_exp: 编辑框的xpath表达式
        :param text: 要输入的文本内容
        :return:
        """
        try:
            time.sleep(0.8)
            if self.platform == "android":
                self.driver.xpath(xpath_exp).click()
                self.driver.clear_text()
                time.sleep(0.2)
                self.driver.xpath(xpath_exp).set_text(text)
                # self.driver.set_input_ime(True)
                # time.sleep(0.2)
                # self.driver.clear_text()
                # time.sleep(1)
                # self.driver.send_keys(text)
                # for char in text:
                #     os.system('adb shell input text {}'.format(text))
                #     time.sleep(0.2)
            elif self.platform == "ios":
                # 还需要测试一下
                self.driver(xpath=xpath_exp).clear_text()
                time.sleep(0.2)
                self.driver(xpath=xpath_exp).set_text(text)

        except Exception as err:
            logger.error(f"内容 {err} 输入失败···")

    def scroll_and_click_by_text(self, text_to_find, el_type='text', max_attempts=5, scroll_pause=0.5):
        """
        在可滚动视图中查找并点击指定文本或xpath的元素。
        :param text_to_find: 要查找的文本/xpath
        :param el_type: 元素定位类型，支持文本text(label)和xpath
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        is_find = None
        attempt = 0
        time.sleep(2)

        try:
            if self.platform == "android":

                # 如果未找到，则尝试滚动查找
                while attempt < max_attempts:
                    # 根据类型初始化查找元素
                    if el_type == "text":
                        element = self.driver(text=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver.xpath(text_to_find)
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型el_type···")

                    # 检查元素是否存在
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.click()
                        # self.click_by_text(text_to_find)
                        logger.info(f"点击 '{text_to_find}'")
                        return True

                    # 滑动屏幕
                    logger.info(f"正在尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
                    self.driver(scrollable=True).scroll(steps=150)
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

            elif self.platform == "ios":
                while attempt < max_attempts:
                    # 根据el_type初始化查找元素
                    if el_type == "text":
                        element = self.driver(label=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver(xpath=text_to_find)
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型el_type···")

                    # 尝试查找元素并点击
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.click()
                        # self.click_by_text(text_to_find)
                        logger.info(f"点击 '{text_to_find}'")
                        return True

                    # 滑动屏幕
                    logger.info(f"正在尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
                    self.driver.swipe_up()
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

            time.sleep(2)
        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

        logger.info(f"没找到要点击的 【{text_to_find}】 元素，已经尝试了： {max_attempts} 次.")
        pytest.fail(f"没找到要点击的 【{text_to_find}】 元素")
        # return False

    def iterate_and_click_popup_text(self, option_text_list: List[Any], menu_text, el_type='text'):
        """
        根据文本遍历popup弹窗的单选项，执行点击操作，适合点击某个选项后自动返回上一页的操作。
        :param option_text_list: 需要遍历的文本列表
        :param menu_text: 需要点击的popup菜单功能项
        :param el_type: menu_text的定位方式,支持文本和xpath，默认文本
        :return:
        """

        def scroll_check_function(texts):
            """
            遍历并判断功能项(名称)是否存在当前页面
            :param texts: 存储了功能项名称的列表。
            :return: bool
            """
            ele_exists = []
            ele_not_exists = []

            # 定义一个函数来处理文本内容
            def remove_default_keyword(remove_text):
                if "(默认)" in remove_text:
                    return remove_text.replace("(默认)", "").strip()
                else:
                    return remove_text

            if isinstance(texts, list):
                # 如果 texts 是一个列表，遍历列表中的每个功能项名称
                for text in texts:
                    check_text = remove_default_keyword(text)
                    ele_status = self.is_element_exists(check_text)
                    if ele_status:
                        ele_exists.append(check_text)
                    else:
                        ele_not_exists.append(check_text)

                if len(ele_not_exists) > 0:
                    logger.info(f"当前页面存在：{ele_exists}")
                    logger.info(f"当前页面缺失：{ele_not_exists}")
                    pytest.fail(f"当前页面缺失：{ele_not_exists}")
                    # return False
                else:
                    logger.info(f"需校验的文本均存在！-->{ele_exists}")
                    return True

            elif isinstance(texts, str):
                # 如果 texts 是一个单一的文本，在当前页面滚动查找该文本是否存在
                check_text = remove_default_keyword(texts)
                ele_status = self.is_element_exists(check_text)
                if not ele_status:
                    logger.info(f"当前页面缺失：{check_text}")
                    pytest.fail(f"当前页面缺失：{check_text}")
                    # return False
                else:
                    logger.info(f"需校验的文本均存在！-->{check_text}")
                    return True

        try:
            # 遍历文本，执行点击操作
            for i in option_text_list:
                self.scroll_and_click_by_text(text_to_find=menu_text, el_type=el_type)
                time.sleep(1)
                logger.info('点击 ' + i)
                self.click_by_text(i)
                time.sleep(3)
                page_options = scroll_check_function(i)  # 断言
                if i != '取消':
                    assert page_options is True
                elif i == '取消':
                    page_options = scroll_check_function(option_text_list[-2])
                    assert page_options is True
        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def click_checkbox_by_text(self, option_text_list, menu_text, mode=1):
        """
        根据文本对多选框执行点击操作，适合同时选择多个/单个选项后手动点击保存、取消、返回的操作。
        :param option_text_list: 需要遍历的文本列表
        :param menu_text: 需要点击进入多选页面的菜单功能项
        :param mode: 1：根据文本直接多选；2：根据文本点击右边按钮多选
        :return:
        """
        try:
            if mode == 1:
                self.scroll_and_click_by_text(text_to_find=menu_text)
                # 遍历文本，执行点击操作
                for i in option_text_list:
                    time.sleep(0.5)
                    logger.info('点击 ' + i)
                    self.click_by_text(i)
                    time.sleep(0.5)

            elif mode == 2:
                self.scroll_and_click_by_text(text_to_find=menu_text)
                # 遍历文本，执行点击操作
                for i in option_text_list:
                    time.sleep(0.5)
                    logger.info('点击 ' + i)
                    self.scroll_click_right_btn(text_to_find=i)
                    time.sleep(0.5)

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def access_in_remote_setting(self, text_to_find, el_type='text', max_attempts=50, scroll_pause=1):
        """
        在设备列表中滚动查找指定设备名称(支持单机、nvr、hub),并点击远程设置按钮。
        :param el_type: 元素查找类型，支持 文本text(label).
        :param text_to_find: 要查找的文本
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        # TODO: 需要适配hub、nvr

        def retry_connection(num_retries=4):
            for _ in range(num_retries):
                # 优先检查是否已成功进入报警设置页面
                if self.wait_for_element(text='报警通知'):
                    logger.info('远程配置页面已成功加载！')
                    break

                if self.wait_for_element(text='加载失败，请点击重试'):
                    logger.warning("检测到连接失败，尝试点击重试按钮...")
                    self.click_by_text('重试')
                elif self.wait_for_element(text='登录'):
                    logger.warning("检测到设备未登录，跳过当前用例！")
                    pytest.skip("设备未登录，跳过当前用例！")
                else:
                    logger.info('loading中，继续等待')
                    time.sleep(7)
            else:
                pytest.fail(f'已重试 {num_retries} 次，未能连接上该设备！')

        def find_and_click_remote_setting(text):
            time.sleep(2)
            for i in range(3, 0, -1):  # 从3开始递减到1，先检查第三个兄弟元素
                setting_xpath = f"//*[@text='{text}']/following-sibling::*[{i}][@clickable='true']"
                if self.driver.xpath(setting_xpath).exists:
                    self.driver.xpath(setting_xpath).click()
                    retry_connection()
                    return True
                else:
                    continue
            # 若均不存在，则为hub，点击名称进入
            self.click_by_text(text)

        def find_and_click_remote_setting_ios(text):
            for i in range(3, 0, -1):
                setting_xpath = f"//*[contains(@name, '{text}')]/following-sibling::*[{i}][@visible='true' and @enabled='true']"
                if self.driver.xpath(setting_xpath).click():
                    return True
            self.click_by_text(text)
            return False

        attempt = 0
        while attempt < max_attempts:
            element = self.driver(text=text_to_find) if self.platform == "android" else self.driver(label=text_to_find)

            if element.exists:
                logger.info(f"元素已找到: '{text_to_find}'")
                if self.platform == "android":
                    if find_and_click_remote_setting(text_to_find):
                        return True
                elif self.platform == "ios":
                    if find_and_click_remote_setting_ios(text_to_find):
                        return True
            else:
                logger.info(f"尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
                if self.platform == "android":
                    self.driver(scrollable=True).scroll(steps=150)
                elif self.platform == "ios":
                    self.driver.swipe_up()
                time.sleep(scroll_pause)

            attempt += 1

        logger.warning(f"还是没找到 '{text_to_find}' 元素，已尝试 {max_attempts} 次.")
        pytest.skip(f"跳过当前用例！未能找到 '{text_to_find}' 设备，已尝试 {max_attempts} 次.")

    # def parse_and_extract_text(self, xml_content, xml_parse_conditions, exclude_texts=None):
    #     """
    #     解析并提取XML指定文本内容（先这样写）
    #     :param xml_parse_conditions: iOS或安卓的xml解析条件，取自yaml文件
    #     :param xml_content: 获取的xml内容
    #     :param exclude_texts: 需要排除的文本
    #     :return:
    #     """
    #     if exclude_texts is None:
    #         exclude_texts = []
    #
    #     texts = set()
    #
    #     root = ET.fromstring(xml_content)
    #     for elem in root.iter():
    #         match = True
    #         for key, value in xml_parse_conditions.items():
    #             elem_value = elem.attrib.get(key)
    #             if isinstance(value, dict):
    #                 if 'not_equal' in value and elem_value == value['not_equal']:
    #                     match = False
    #                     break
    #             elif elem_value != value:
    #                 match = False
    #                 break
    #         if match:
    #             text = elem.attrib.get('text') if self.platform == "android" else elem.attrib.get('label')
    #             if text and text not in exclude_texts:
    #                 texts.add(text)
    #     return texts

    def scroll_screen(self, max_scrolls=1, direction="up"):
        """
        滚动屏幕
        :param direction: 屏幕的滚动方向：
        :param max_scrolls: 最大滚动次数，默认1次
        :return:
        """
        try:
            if self.platform == "android":
                scroll_method = self.driver.swipe_ext
                # 检查是否可以滚动
                if not self.driver(scrollable=True).exists:
                    return Exception("屏幕不可滚动")

            elif self.platform == "ios":
                # iOS平台默认可以滚动，不需要额外检查
                if direction == "up":
                    scroll_method = self.driver.swipe_up
                else:
                    scroll_method = self.driver.swipe_down
            else:
                raise ValueError("不支持当前平台")

            for _ in range(max_scrolls):
                if self.platform == "android":
                    scroll_method(direction)
                else:
                    time.sleep(1)
                    scroll_method()
                # 每次滚动后稍作等待
                time.sleep(0.5)

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def get_all_texts(self, selector_type, selector, max_scrolls=2):
        """
        滚动获取当前页面所有指定文本
        :param selector_type: 支持安卓className，resource-id定位，iOS的className定位
        :param selector: 元素定位的具体id、className
        :param max_scrolls: 最大滚动次数
        :return:
        """
        my_set = set()

        def get_elements_texts():
            if self.platform == 'android':
                if selector_type == 'id':
                    elements = self.driver(resourceId=selector)
                elif selector_type == 'class':
                    elements = self.driver(className=selector)
                return {element.get_text() for element in elements}

            elif self.platform == 'ios':
                elements = self.driver(id=selector).find_elements()
                return {element.text for element in elements}

        # 获取当前页面所有元素的文本内容
        for _ in range(max_scrolls):
            # 获取当前页面所有元素的文本内容
            new_texts = get_elements_texts()
            my_set.update(new_texts)

            self.scroll_screen()
            time.sleep(0.5)

            # 检查滑动后页面是否有变化
            new_texts = get_elements_texts()
            if not new_texts - my_set:
                break  # 如果滑动后没有新内容，退出循环

            # 添加新获取的文本内容
            my_set.update(new_texts)

        return list(my_set)

    # def get_all_elements_texts(self, exclude_texts, xml_az_parse_conditions, xml_ios_parse_conditions, max_scrolls=2,
    #                            scroll_pause=1):
    #     """
    #     获取当前页面xml文件，解析出当前页面所有功能文案
    #     :param exclude_texts: 需要额外排除的文案
    #     :param xml_az_parse_conditions: 安卓xml解析条件，取自yaml文件
    #     :param xml_ios_parse_conditions: iOSxml解析条件，取自yaml文件
    #     :param max_scrolls: 最大滚动次数
    #     :param scroll_pause: 滚动后的停止时间，秒
    #     :return:
    #     """
    #     all_texts = set()
    #
    #     # 确认当前被测平台是安卓还是iOS
    #     def get_page_source_and_parse(platform):
    #         if platform == "android":
    #             return self.driver.dump_hierarchy()
    #         elif platform == "ios":
    #             return self.driver.source()
    #         else:
    #             raise ValueError("不支持当前平台")
    #
    #     # 根据被测平台选用不同的滚动方法
    #     def swipe_screen(platform):
    #         if platform == "android":
    #             self.driver.swipe_ext("up")
    #         elif platform == "ios":
    #             time.sleep(1)
    #             self.driver.swipe_up()
    #         else:
    #             raise ValueError("不支持当前平台")
    #
    #     # 调用parse_and_extract_text解析方法将xml内容进行解析、去重
    #     def extract_texts_and_update(platform, parse_conditions):
    #         page_source = get_page_source_and_parse(platform)
    #         logger.info("已获取页面XML")
    #
    #         texts = self.parse_and_extract_text(
    #             xml_content=page_source,
    #             xml_parse_conditions=parse_conditions,
    #             exclude_texts=exclude_texts
    #         )
    #         all_texts.update(texts)
    #
    #     time.sleep(2)
    #     parse_conditions = xml_az_parse_conditions if self.platform == "android" else xml_ios_parse_conditions
    #
    #     for _ in range(max_scrolls):
    #         extract_texts_and_update(self.platform, parse_conditions)
    #         swipe_screen(self.platform)
    #         time.sleep(scroll_pause)  # 等待页面稳定
    #
    #     # 将去重后的文本内容写入文件
    #     output_path = os.path.abspath("./elements_texts.txt")
    #     with open(output_path, 'w', encoding='utf-8') as f:
    #         for text in sorted(all_texts):
    #             f.write(text + '\n')
    #
    #     # 统计非空行数
    #     with open(output_path, 'r', encoding='utf-8') as f:
    #         non_empty_lines = sum(1 for line in f if line.strip())
    #
    #     logger.info(f"总非空行数: {non_empty_lines}")
    #
    #     return list(all_texts)

    # def verify_page_text(self, expected_text, exclude_texts,
    #                      xml_az_parse_conditions, xml_ios_parse_conditions):
    #     """
    #     校验页面内容
    #     :param xml_ios_parse_conditions: ios
    #     :param xml_az_parse_conditions:
    #     :param expected_text: 需要检查的预期文本
    #     :param exclude_texts: 需要排除的文本
    #     :return:
    #     """
    #     # 获取页面所有功能名称
    #     texts = self.get_all_elements_texts(exclude_texts=exclude_texts,
    #                                         xml_az_parse_conditions=xml_az_parse_conditions,
    #                                         xml_ios_parse_conditions=xml_ios_parse_conditions
    #                                         )
    #     logger.info(f"获取的页面所有功能名称: {texts}")
    #
    #     # 计算当前页面获取到的功能数量
    #     page_fun_num = len(texts)
    #     logger.info(f"当前页面获取到的功能数量：{page_fun_num}")
    #
    #     # 计算预期设备 → 预期页面 → 预期文案数量
    #     count = len(expected_text)
    #     logger.info(f"预期设备的预期页面的预期文案数量：{count}")
    #
    #     for line in expected_text:
    #         if line not in texts or page_fun_num != count:
    #             logger.info("当前页面功能可能不齐全！需要人工核查！")
    #             return False
    #     logger.info("当前页面功能比对齐全！")
    #     return True

    def read_phone_file(self, device_path):
        """
        读取手机中的文件内容
        :param device_path: 设备中的文件路径
        :return: 文件内容
        """
        if self.platform == "android":
            file_content = self.driver.shell(f"cat {device_path}")
            return file_content

        elif self.platform == "ios":
            command = f"tidevice fsync cat {device_path}"
            # 执行命令并捕获输出
            process = subprocess.run(command, shell=True, check=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     encoding='utf-8', errors='ignore')
            # 如果命令成功执行returncode == 0，函数返回命令的标准输出内容（文件内容）
            if process.returncode == 0:
                logger.info("iPhone文件读取成功")
                return process.stdout
            else:
                logger.info(f"读取文件失败: {process.stderr}")
                return None

    def slider_seek_bar(self, slider_mode, id_or_xpath, direction, iteration=20):
        """
        对拖动条执行操作，支持上、下、左、右方向拖动
        :param slider_mode: slider的定位方式，支持id或者xpath
        :param id_or_xpath: id或者xpath的定位参数
        :param direction: 方向，支持"left", "right", "up", "down"方向
        :param iteration: 拖动次数，若是ios，则此处为移动“步数”，不支持定义拖动次数，
        :return:
        """
        try:
            def operate_on_element(element):
                logger.info(f'正在朝指定的 {direction} 方向滑动.')
                for t in range(1, iteration):
                    element.swipe(direction)
                    t += 1
                    time.sleep(1.5)
                logger.info(f'滑动结束.')

            slider = None
            if self.platform == "android":
                if slider_mode == 'id':
                    slider = self.driver(resourceId=id_or_xpath)
                elif slider_mode == 'xpath':
                    slider = self.driver.xpath(id_or_xpath)
                elif slider_mode == 'obj':
                    operate_on_element(element=id_or_xpath)

                # 按下并朝指定方向移动
                if slider:
                    for i in range(1, iteration):
                        logger.info(f'正在朝指定的 {direction} 方向滑动第{i}次')
                        slider.swipe(direction)
                        i += 1

            if self.platform == "ios":
                if slider_mode == 'id':
                    slider = self.driver(accessibility_id=id_or_xpath)
                else:
                    slider = self.driver.xpath(id_or_xpath)

                # 获取滑动条的当前位置
                rect = slider.bounds

                # 计算起点和终点
                start_x = rect.x  # 滑块的坐标x起点
                start_y = rect.y  # 滑块的坐标y起点

                # 模拟拖动操作
                self.driver.swipe(start_x, start_y, start_x + iteration, start_y, 0.5)  # 1秒完成滑动

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def common_drag_slider_seek_bar(self, start_xpath_prefix, slider_mode='obj'):
        """
        对拖动条执行向右拖动、向左拖动、向右拖动三种固定操作
        :param start_xpath_prefix: 起始xpath前缀
        :param slider_mode: slider的定位方式，支持id、xpath定位，或者直接使用元素对象obj
        :param id_or_xpath: id或者xpath的定位参数
        :param direction: 方向，支持"left", "right"方向
        :param iteration: 拖动次数，若是ios，则此处为移动“步数”，不支持定义拖动次数，
        :return:
        """
        try:
            element_obj = BasePage().find_element_by_xpath_recursively(
                start_xpath_prefix=start_xpath_prefix,
                target_id="RNE__Slider_Thumb")

            # 往右拖动15次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)

            # 往左拖动25次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='left',
                                 iteration=10)

            # 往右拖动5次
            self.slider_seek_bar(slider_mode=slider_mode,
                                 id_or_xpath=element_obj,
                                 direction='right',
                                 iteration=5)
        except Exception as e:
            pytest.fail(f"common_drag_slider_seek_bar函数执行出错: {str(e)}")

    def drag_element(self, element_xpath, direction, distance, duration=1):
        """
        拖动元素到指定方向上的一定距离，支持上、下、左、右方向
        :param element_xpath:  元素的xpath
        :param direction:  方向，支持向"left", "right", "up", "down"方向拖动元素
        :param distance:  距离，单位为像素，int类型
        :param duration:  滑动时间，单位为秒
        :return:
        """
        try:
            if self.platform == "android":
                element = self.driver.xpath(element_xpath)
                # 获取元素的边界坐标
                bounds = element.info['bounds']
                # 计算元素的中心坐标
                center_x = (bounds['left'] + bounds['right']) // 2
                center_y = (bounds['top'] + bounds['bottom']) // 2
                logger.info(f"需要拖动的元素中心坐标为: ({center_x}, {center_y})")

                if direction == "left":
                    # 向左拖动
                    self.driver.drag(center_x, center_y, center_x - distance, center_y, duration)
                elif direction == "right":
                    # 向右拖动
                    self.driver.drag(center_x, center_y, center_x + distance, center_y, duration)
                elif direction == "up":
                    # 向上拖动
                    self.driver.drag(center_x, center_y, center_x, center_y - distance, duration)
                elif direction == "down":
                    # 向下拖动
                    self.driver.drag(center_x, center_y, center_x, center_y + distance, duration)
            time.sleep(1)

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def get_coordinates_and_draw(self, mode, id_or_xpath, draw_area='左上', num=0):
        """
        获取元素的xy轴坐标并画黑框遮盖，支持目前现有设备的画框数量
        :param mode: 定位方式，支持id或者xpath
        :param id_or_xpath: 可遮盖区域的id或者xpath的定位参数
        :param draw_area: 需要遮盖的区域，支持[左上]、[左下]、[右上]、[右下]的1/4屏，以及[全屏]遮盖，默认左上。
        :param num: 画框数量，默认为0，为0时需要指定遮盖区域draw_area.
        :return:
        """
        try:
            if self.platform == "android":
                if mode == 'id':
                    element = self.driver(resourceId=id_or_xpath)
                else:
                    element = self.driver.xpath(id_or_xpath)

                # 获取元素的边界坐标
                bounds = element.info['bounds']

                # 左上角坐标
                top_left_x = bounds['left']
                top_left_y = bounds['top']

                # 左下角坐标
                bottom_left_x = bounds['left']
                bottom_left_y = bounds['bottom']

                # 右上角坐标
                top_right_x = bounds['right']
                top_right_y = bounds['top']

                # 右下角坐标
                bottom_right_x = bounds['right']
                bottom_right_y = bounds['bottom']

                # 中心坐标
                center_x = (bounds['left'] + bounds['right']) // 2
                center_y = (bounds['top'] + bounds['bottom']) // 2

                if num == 0:
                    if draw_area == '左上':
                        self.driver.drag(center_x, center_y, top_left_x, top_left_y, 0.5)  # 0.5 秒内完成拖动
                    elif draw_area == '右上':
                        self.driver.drag(center_x, center_y, top_right_x, top_right_y, 0.5)
                    elif draw_area == '右下':
                        self.driver.drag(center_x, center_y, bottom_right_x, bottom_right_y, 0.5)
                    elif draw_area == '左下':
                        self.driver.drag(center_x, center_y, bottom_left_x, bottom_left_y, 0.5)
                    elif draw_area == '全屏':
                        self.driver.drag(top_left_x, top_left_y, bottom_right_x, bottom_right_y, 1)
                elif num > 0:
                    i = 1
                    while i <= num:
                        s_x = i * 130  # 每次开始画框的x坐标
                        e_x = s_x + 50  # 每次画框结束的x坐标
                        e_y = center_y + 50  # 每次画框结束的y坐标
                        self.driver.drag(s_x, center_y, e_x, e_y, 0.5)  # 0.5 秒内完成拖动
                        i += 1

            if self.platform == "ios":
                if mode == 'id':
                    element = self.driver(accessibility_id=id_or_xpath)
                else:
                    element = self.driver.xpath(id_or_xpath)

                # 获取元素的边界坐标
                bounds = element.bounds

                # 元素宽度、高度
                width = bounds[2]
                height = bounds[3]

                # 左上角坐标
                top_left_x = bounds[0]
                top_left_y = bounds[1]

                # 中心点坐标
                center_x = int(top_left_x + width / 2)
                center_y = int(top_left_y + height / 2)

                # 右上角坐标
                top_right_x = bounds[2]
                top_right_y = 0

                # 右下角坐标
                bottom_right_x = bounds[2]
                bottom_right_y = bounds[1] + bounds[3]

                # 左下角坐标
                bottom_left_x = bounds[0]
                bottom_left_y = bounds[1] + bounds[3]

                if draw_area == '左上':
                    self.driver.swipe(center_x, center_y, top_left_x, top_left_y, 0.5)  # 0.5 秒内完成拖动
                elif draw_area == '右上':
                    self.driver.swipe(center_x, center_y, top_right_x, top_right_y, 0.5)
                elif draw_area == '右下':
                    self.driver.swipe(center_x, center_y, bottom_right_x, bottom_right_y, 0.5)
                elif draw_area == '左下':
                    self.driver.swipe(center_x, center_y, bottom_left_x, bottom_left_y, 0.5)
                elif draw_area == '全屏':
                    self.driver.swipe(top_left_x, top_left_y, bottom_right_x, bottom_right_y, 1)

        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def get_text_coordinates_center(self, text):
        """
        获取某文本元素的中心点坐标
        :param text:
        :return:
        """
        try:
            x, y = self.driver(text=text).center()
            logger.info(f"文本 {text} 的中心点坐标为：{x, y}")
            return x, y
        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    def click_by_coordinates(self, x, y):
        """
        根据坐标进行点击操作
        :param x:
        :param y:
        :return:
        """
        try:
            self.driver.click(x, y)
        except Exception as err:
            pytest.fail(f"函数执行出错: {str(err)}")

    @staticmethod
    def check_key_in_yaml(items, key):
        """
        检查给定的YAML字典中是否存在指定的键。
        :param items: YAML文件中的字典
        :param key: 需要检查的键名列表
        :raises pytest.skip: 如果所有指定的键不存在，则跳过测试
        """
        try:
            if key not in items:
                pytest.skip(f"YAML配置文件中未找到'{key}'键，跳过此测试用例")
            else:
                return True
        except Exception as err:
            # logger.info(f"可能发生了错误: {err}")
            pytest.fail(f"【check_key_in_yaml】方法检查yaml文件中的key出错: {str(err)}")

        # if not any(key in items for key in keys):
        #     pytest.skip(f"YAML配置文件中未找到以下任意键：{', '.join(keys)}，跳过此测试用例")

    @staticmethod
    def is_key_in_yaml(items, key) -> bool:
        """
        检查给定的YAML字典中是否存在指定的键。
        :param items: YAML文件中的字典
        :param key: 需要检查的键名列表
        :return: bool
        """
        try:
            if key not in items:
                logger.info(f"{key} 在yaml中未找到！")
                return False
            else:
                return True
        except Exception as err:
            # logger.info(f"可能发生了错误: {err}")
            pytest.fail(f"【check_key_in_yaml】方法检查yaml文件中的key出错: {str(err)}")

    @staticmethod
    def extract_value_from_yaml(items, key, skip_if_false):
        """
        从给定的YAML字符串中提取指定键的值。
        :param items: YAML格式的字符串。
        :param key: 要提取的键。
        :param skip_if_false: 当键对应的值为False时是否跳过测试。True跳过，False不跳过
        """
        try:
            # 获取指定key的值
            value = items.get(key)

            # 如果key的值为False且skip_if_false为True，则跳过测试
            if not value and skip_if_false:
                logger.info(f"该设备不支持 {key} ！")
                pytest.skip(f"该设备不支持 {key} ！")
            else:
                return value
        except yaml.YAMLError as e:
            logger.error(f"解析YAML文件出错: {e}")
            pytest.fail(f"解析YAML文件出错: {e}")

    def back_previous_page(self):
        """
        手势向右滑模拟：返回上一页（不同手机机型有可能会失效）
        :return:
        """
        try:
            if self.platform == "android":
                logger.info('右滑模拟：返回上一页')
                self.driver.swipe_ext(Direction.HORIZ_BACKWARD)
                time.sleep(0.5)

            if self.platform == "ios":
                logger.info('右滑模拟：返回上一页')
                self.driver.swipe_right()
                time.sleep(0.5)

        except Exception as err:
            # logger.info(f"可能发生了错误: {err}")
            pytest.fail(f"函数执行出错: {str(err)}")

    def back_previous_page_by_xpath(self, xpath_expression=g_config_back):
        """
        RN: 根据xpath定位左上角返回上一页的按钮
        :return:
        """
        try:
            logger.info("返回上一页")
            self.click_by_xpath(xpath_expression=xpath_expression)
            time.sleep(1)
        except Exception as err:
            pytest.fail(f"点击右上角返回按钮执行出错: {str(err)}")

    def scroll_selector(self, id_or_xpath, direction, times=1):
        """
        滚动选择器，如选择时间
        :param id_or_xpath: 选择器可滚动的id或者xpath
        :param direction: 滚动方向, "up", "down", "left", "right"
        :param times: 滚动次数
        :return:
        """
        try:
            if self.platform == "android":
                i = 1
                while i <= times:
                    e = self.driver.xpath(id_or_xpath)
                    time.sleep(0.5)
                    e.scroll(direction)
                    i += 1

            if self.platform == "ios":
                i = 1
                while i <= times:
                    e = self.driver.xpath(id_or_xpath)
                    time.sleep(0.5)
                    e.scroll(direction)
                    i += 1

        except Exception as err:
            # logger.info(f"可能发生了错误: {err}")
            pytest.fail(f"函数执行出错: {str(err)}")

    def find_element_by_xpath_recursively(self, start_xpath_prefix, target_id=None, target_text=None):
        """
        递归查找页面指定的目标元素，遍历同级和子级元素

        :param driver: uiautomator2设备对象
        :param start_xpath_prefix: 当前元素的xpath前缀路径
        :param target_id: 目标元素的resourceId（可选）
        :param target_text: 目标元素的text属性值（可选）
        :return: 返回找到的目标元素对象，如果未找到则返回None
        """
        # 初始化同级元素索引
        sibling_index = 1
        time.sleep(2)
        while True:
            # 构建当前同级元素的xpath
            current_xpath = f"{start_xpath_prefix}[{sibling_index}]"
            current_element = self.driver.xpath(current_xpath)

            # 如果当前同级元素不存在，则退出循环
            if not current_element.exists:
                logger.info('当前元素的匹配不到同级元素！准备遍历当前元素的子元素！')
                break

            # 检查是否匹配目标元素的条件.resourceName实际上就是resourceId。这两个名称指的同一个属性，即Android UI元素的资源ID。
            if (target_id is None or current_element.info.get('resourceName') == target_id) and \
                    (target_text is None or current_element.info.get('text') == target_text):
                return current_element  # 找到目标元素，返回该元素对象

            # 如果没有匹配，递归遍历当前元素的子元素
            child_index = 1
            while True:
                # 构建子元素的xpath路径
                child_xpath = f"{current_xpath}/*[{child_index}]"
                child_element = self.driver.xpath(child_xpath)

                # 如果没有更多子元素，退出子元素循环
                if not child_element.exists:
                    break

                # 递归在子元素中查找
                result = self.find_element_by_xpath_recursively(child_xpath, target_id, target_text)
                if result:
                    logger.info('在子元素中找到目标元素！')
                    return result  # 找到目标元素，返回该元素对象

                child_index += 1  # 检查下一个子元素

            # 检查下一个同级元素
            sibling_index += 1

        # 如果未找到目标元素，返回False
        return False

    def back_to_page_top(self):
        """
        返回页面顶部
        :return:
        """
        try:
            logger.info('尝试返回页面顶部...')
            self.driver(scrollable=True).fling.vert.toBeginning(max_swipes=1000)
        except Exception as err:
            logger.warning(f"返回页面顶部出错: {str(err)}")

    def detect_illegal_functions(self, legal_funcs_ids, max_scroll=3):
        """
        检查页面非法功能，需要事先定义排除的元素xpath列表
        :param legal_funcs_ids: 预期的合法功能名称列表
        :param max_scroll: 页面最大滚动次数。默认3次，特别长的页面适当增加滚动次数
        :return:
        """
        try:
            if isinstance(legal_funcs_ids, list):
                # 定义需要排除的元素xpath列表
                exclude_xpath = [
                    '//*[@resource-id="com.android.systemui:id/wifi_standard"]',
                    '//*[@resource-id="com.android.systemui:id/clock"]',
                    '//*[@resource-id="com.android.systemui:id/operator_name"]',
                    '//*[@resource-id="RNE__ICON__Component"]',
                    '//*[@resource-id="storageText"]',
                    '//*[@resource-id="name"]',
                    '//*[@resource-id="ReoValue"]',
                    '//*[@resource-id="com.android.systemui:id/battery_digit"]',
                    '//*[@resource-id="com.mcu.reolink:id/device_name_tv"]',
                    '//*[@resource-id="com.mcu.reolink:id/device_type_tv"]',
                    '//*[@resource-id="com.mcu.reolink:id/device_storage_tv"]',
                    '//*[@resource-id="com.mcu.reolink:id/tv_sub_right"]',
                    '//*[@resource-id="com.mcu.reolink:id/im_title"]'
                ]

                exclude_elements = []  # 定义需要排除的文案集合
                illegal_functions = []  # 定义非法功能列表
                all_elements = []  # 定义全屏文案集合

                def get_exclude_texts():  # 获取当前页面需要排除的文本内容
                    for i in exclude_xpath:
                        try:
                            exclude_text = self.driver.xpath(i).all()
                            for t in exclude_text:
                                element_text = t.text  # 获取元素的text属性
                                exclude_elements.append(element_text)  # 添加至exclude_elements列表
                                dr_exclude_elements = list(set(exclude_elements))  # 将列表转集合再转列表，去除重复元素
                        except Exception as e_err:
                            logger.error(f'排除的文本内容时出错：{e_err}')
                    logger.info("需排除的内容有：")
                    logger.info(dr_exclude_elements)
                    return dr_exclude_elements

                def get_fullscreen_text():  # 获取当前页面全屏文本
                    fullscreen_text = self.driver.xpath('//android.widget.TextView').all()  # 获取当前页面所有元素的文本内容
                    for s in fullscreen_text:
                        element_texts = s.text  # 获取元素的text属性
                        all_elements.append(element_texts)
                        dr_all_elements = list(set(all_elements))  # 将列表转集合再转列表，去除重复元素
                    logger.info("当前页面全屏文本有：")
                    logger.info(dr_all_elements)
                    return dr_all_elements

                for _ in range(max_scroll):
                    # 先获取当前页面需要排除的文本内容
                    new_exclude_texts = get_exclude_texts()
                    exclude_elements.extend(new_exclude_texts)

                    # 再获取当前页面所有元素的文本内容
                    new_all_texts = get_fullscreen_text()
                    all_elements.extend(new_all_texts)  # 添加至all_elements列表

                    self.driver.swipe_ext(direction='up')
                    time.sleep(0.5)

                # 集合转列表
                whole_page_exclude_elements = list(set(exclude_elements))
                whole_page_all_elements = list(set(all_elements))

                logger.info("循环页面后需要排除的内容：")
                logger.info(whole_page_exclude_elements)
                logger.info("循环页面后全屏的内容：")
                logger.info(whole_page_all_elements)

                # 从全屏文本中删掉需要排除的文本内容,构建出最终文本
                for e in whole_page_exclude_elements:
                    if e in whole_page_all_elements:
                        whole_page_all_elements.remove(e)
                        whole_page_exclude_elements.append(e)
                logger.info('本次移除的文本：')
                logger.info(whole_page_exclude_elements)

                # 检查非法功能
                for element in whole_page_all_elements:
                    if element not in legal_funcs_ids:
                        illegal_functions.append(element)

                # 输出非法功能
                if illegal_functions:
                    logger.info(f"存在非法功能：{illegal_functions}")
                    pytest.fail(f"存在非法功能：{illegal_functions}")
                    # return False
                else:
                    logger.info("没有检测到非法功能。")
                    return True

        except Exception as err:
            logger.info(f"函数执行出错: {str(err)}")

    def get_element_info(self, xpath_exp):
        """
        获取元素属性
        :return:
        """
        try:
            element = self.driver.xpath(xpath=xpath_exp)
            return element
        except Exception as err:
            logger.error(f"获取元素属性出错: {str(err)}")
