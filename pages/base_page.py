import os
import time
from datetime import datetime
from uiautomator2.exceptions import XPathElementNotFoundError
from common_tools.app_driver import driver
from common_tools.logger import logger
from typing import Literal
from common_tools.handle_alerts import handle_alert

DEFAULT_SECONDS = 15


class BasePage:
    def __init__(self):
        self.driver = driver.get_actual_driver()
        self.platform = driver.get_platform()

    def is_element_exists(self, selector_type, element_value):
        try:
            if self.platform == 'android':
                if selector_type == "text":
                    return self.driver(text=element_value).exists(timeout=3)
                elif selector_type == "resourceId":
                    return self.driver(resourceId=element_value).exists(timeout=3)
                elif selector_type == "xpath":
                    return self.driver.xpath(element_value).exists(timeout=3)
                else:
                    raise ValueError("你可能输入了不支持的 selector type.")
            elif self.platform == 'ios':
                if selector_type == "text":
                    # TODO: 待完成
                    pass
                elif selector_type == "resourceId":
                    # TODO: 待完成
                    pass
                elif selector_type == "xpath":
                    # TODO: 待完成
                    pass
                else:
                    raise ValueError("你可能输入了不支持的 selector type.")
        except Exception as err:
            logger.error(f"元素未找到 {selector_type}: {element_value}. Error: {err}")
            return False

    def find_element_xpath(self, xpath_expression):
        """
        通过xpath定位元素
        :param xpath_expression: xpath表达式
        :return: 元素对象
        """
        if self.platform == 'android':
            return self.driver.xpath(xpath_expression)
        elif self.platform == 'ios':
            return self.driver(xpath=xpath_expression)

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

                if not element.exists():
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
        :param is_click_again: 接收布尔值，默认为False，代表处理了弹窗之后，不会尝试再次点击resource_id元素；若为True，则处理弹窗之后，再次重新点击xpath_expression元素
        :return:
        """
        for attempt in range(retries):
            element = None
            try:
                time.sleep(2)
                if self.platform == 'android':
                    element = self.find_element_xpath(xpath_expression)
                elif self.platform == 'ios':
                    element = self.find_element_xpath(xpath_expression)

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
            except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
                logger.error("ValueError: %s", verr)
                raise
            except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
                logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", xpath_expression, err)
                raise
        return False

    def get_toast(self, toast_text: str, reset=True, timeout=5.0, default="没有获取到toast提示"):
        """
        废除！该方法不可用！ 获取页面弹出的toast
        :param timeout: 超时时间，默认5秒
        :param toast_text: 需要检查的toast文案
        :param reset: 默认为True，即清除缓存的Toast，传False则不清除
        :param default: 如果10s内没有获取到Toast，则返回此默认消息
        :return:
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 尝试获取Toast文本内容
                toast_message = self.find_element_xpath('//*[contains(@text,{})]'.format(toast_text))
                # 验证Toast消息内容是否符合预期
                if toast_message:
                    logger.info(f"Toast message found: {toast_message}")
                    return toast_message
            except XPathElementNotFoundError:
                pass

            # 根据配置决定是否重置Toast缓存, 默认重置
            if reset:
                self.driver.toast.reset()

            # 每隔0.5秒重新尝试获取一次toast消息
            time.sleep(0.5)

        # 确保在异常情况下也能访问到实际获取的Toast消息或默认值
        logger.error(f"获取Toast失败，返回默认消息：'{default}'")
        return default

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
        if not os.path.exists(ios_screenshot_save_path):
            os.makedirs(ios_screenshot_save_path)

        # 获取当前时间并格式化为字符串
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if self.platform == 'android':
            # 使用uiautomator2截图
            filename = f"{timestamp}-android.png"
            filepath = os.path.join(screenshot_save_path, filename)
            self.driver.screenshot(filepath)
            logger.info("Taking screenshot on Android device.")
        elif self.platform == 'ios':
            # 处理iOS设备的截图
            filename = f"{timestamp}-iOS.png"
            filepath = os.path.join(ios_screenshot_save_path, filename)
            self.driver.screenshot(filepath)
            print("Taking screenshot on iOS device.")
        else:
            raise ValueError("Unsupported device type. Please specify 'android' or 'ios'.")

    def input_text(self, text):
        """
        使用adb命令输入文本,不清空文本框内容，直接输入，不支持中文。
        :element: 编辑框的xpath表达式
        :text： 要输入的文本内容
        :return:
        """
        try:
            if self.platform == 'android':
                self.driver.set_input_ime(True)
                time.sleep(0.2)
                self.driver.send_keys(text)
                # for char in text:
                #     os.system('adb shell input text {}'.format(text))
                #     time.sleep(0.2)
            elif self.platform == 'ios':
                # TODO: wda的输入方法
                self.driver.set_text(text)
                logger.info("wda的输入方法，未完成···")
        except Exception as err:
            logger.error(f"内容 {err} 输入失败···")

    def input_text_clear(self, text):
        """
        清空文本框内容并输入。
        :return:
        """
        try:
            if self.platform == 'android':
                self.driver.set_input_ime(True)
                time.sleep(0.2)
                self.driver.clear_text()
                time.sleep(1)
                self.driver.send_keys(text)
                # for char in text:
                #     os.system('adb shell input text {}'.format(text))
                #     time.sleep(0.2)
            elif self.platform == 'ios':
                # TODO: wda的输入方法
                self.driver.clear_text()
                time.sleep(1)
                self.driver.set_text(text)
                logger.info("wda的输入方法，未完成···")
        except Exception as err:
            logger.error(f"内容 {err} 输入失败···")
