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
        """
        判断元素是否存在
        :param selector_type: 安卓支持：text文本、id、xpath定位；iOS支持text(label)文本、id、xpath定位
        :param element_value: 对应的文本、id、xpath值
        :return: bool
        """
        try:
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

        except Exception as err:
            logger.error(f"元素未找到 {selector_type}: {element_value}. Error: {err}")

            return False

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

                if not element.exists:
                    logger.error("该点击元素：%s 不存在", text)
                    raise ValueError(f"该点击元素：{text} 不存在")

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
                raise
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
                toast_message = self.find_element_by_xpath('//*[contains(@text,{})]'.format(toast_text))
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
            time.sleep(0.2)
            if self.platform == "android":
                self.driver.xpath(xpath_exp).set_text(text)
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
            time.sleep(0.2)
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

    def scroll_and_click_by_text(self, el_type, text_to_find, max_attempts=15, scroll_pause=0.5):
        """
        在可滚动视图中查找并点击指定文本或xpath的元素。
        :param el_type: 元素定位类型，支持文本text(label)和xpath
        :param text_to_find: 要查找的文本/xpath
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        is_find = None
        attempt = 0

        try:
            if self.platform == "android":
                # 根据类型初始化查找元素
                if el_type == "text":
                    element = self.driver(text=text_to_find)
                    # 尝试直接滚动到指定文本
                    logger.info(f"Attempting to scroll to '{text_to_find}' directly.")
                    is_find = self.driver(scrollable=True).scroll.to(text=text_to_find)
                elif el_type == "xpath":
                    element = self.driver.xpath(text_to_find)
                    self.driver(scrollable=True).fling.vert.toBeginning(max_swipes=1000)  # 滑动至顶部
                else:
                    raise ValueError("你可能输入了不支持的元素查找类型···")

                # 检查元素是否存在
                if element.exists:
                    logger.info(f"元素已找到: '{text_to_find}'")
                    element.click()
                    logger.info(f"Clicked on '{text_to_find}' directly.")
                    return True

                # 如果直接滚动未找到，则尝试多次滚动查找
                while attempt < max_attempts and not is_find:
                    logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                    self.driver(scrollable=True).scroll(steps=200)
                    time.sleep(scroll_pause)  # 等待页面稳定

                    # 重新检查元素是否存在
                    if type == "text":
                        element = self.driver(text=text_to_find)
                    elif type == "xpath":
                        element = self.driver.xpath(text_to_find)

                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.click()
                        logger.info(f"Clicked on '{text_to_find}' after {attempt + 1} attempts.")
                        return True

                    attempt += 1

            elif self.platform == "ios":
                while attempt < max_attempts:
                    # 根据el_type初始化查找元素
                    if el_type == "text":
                        element = self.driver(label=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver(xpath=text_to_find)
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型···")

                    # 尝试查找元素
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.click()
                        logger.info(f"Clicked on '{text_to_find}' directly.")
                        return True

                    # 滑动屏幕
                    logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                    self.driver.swipe_up()
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

        except Exception as err:
            logger.info(f"Error occurred: {err}")

        logger.info(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
        return False

    def access_in_remote_setting(self, text_to_find, el_type='text', max_attempts=15, scroll_pause=0.5):
        """
        在设备列表中滚动查找指定设备名称,并点击远程设置按钮。
        :param el_type: 元素查找类型，支持 文本text(label) 和 'xpath'.
        :param text_to_find: 要查找的文本
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        attempt = 0
        if self.platform == "android":
            def find_and_click(element_selector):
                """
                根据选择器查找元素并点击
                :param element_selector: 要查找的元素选择器
                :return: 是否成功找到并点击元素
                """
                element = self.driver.xpath(element_selector)  # 查找到text_to_find文本右边的第一个元素
                if element.exists:
                    element2 = self.driver.xpath(f"//*[@text='{text_to_find}']/following-sibling::*[2][@clickable='true']")
                    if element2.exists:
                        element2.click()
                    else:
                        element.click()
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
                            return False

                    # 滑动屏幕
                    logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                    self.driver(scrollable=True).scroll(steps=150)
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

            except Exception as e:
                logger.info(f"Error occurred: {e}")

            logger.info(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
            return False

        elif self.platform == "ios":
            def find_and_click(element_xpath):
                """
                根据XPath查找元素并点击
                :param element_xpath: 要查找的元素XPath
                :return: 是否成功找到并点击元素
                """
                element = self.driver.xpath(element_xpath)
                if element.exists and element.label == 'list device set':
                    element.click()
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
                            return False

                    # 滑动屏幕
                    logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
                    self.driver.swipe_up()
                    time.sleep(scroll_pause)  # 等待页面稳定

                    attempt += 1

            except Exception as e:
                logger.info(f"Error occurred: {e}")

            logger.info(f"Failed to find and click on '{text_to_find}' after {max_attempts} attempts.")
            return False
