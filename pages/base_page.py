import os
import subprocess
import time
from datetime import datetime
from uiautomator2.exceptions import XPathElementNotFoundError
from common_tools.app_driver import driver
from common_tools.logger import logger
from typing import Literal
import xml.etree.ElementTree as ET
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

    def scroll_and_click_by_text(self, text_to_find, el_type='text', max_attempts=5, scroll_pause=0.5):
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

                # 如果直接滚动未找到，则尝试多次滚动查找
                while attempt < max_attempts:
                    # 根据类型初始化查找元素
                    if el_type == "text":
                        element = self.driver(text=text_to_find)
                    elif el_type == "xpath":
                        element = self.driver.xpath(text_to_find)
                        # self.driver(scrollable=True).fling.vert.toBeginning(max_swipes=1000)  # 滑动至顶部
                    else:
                        raise ValueError("你可能输入了不支持的元素查找类型···")

                    # 检查元素是否存在
                    if element.exists:
                        logger.info(f"元素已找到: '{text_to_find}'")
                        element.click()
                        logger.info(f"Clicked on '{text_to_find}' directly.")
                        return True

                    # 滑动屏幕
                    logger.info(f"Scrolling to find '{text_to_find}'... 第{attempt + 1}次")
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
                        raise ValueError("你可能输入了不支持的元素查找类型···")

                    # 尝试查找元素并点击
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
        建议只使用text文本定位，因为最终找不到元素会直接按照文本点击一次。先这样写。
        :param el_type: 元素查找类型，支持 文本text(label) 和 'xpath'.
        :param text_to_find: 要查找的文本
        :param max_attempts: 最大尝试次数
        :param scroll_pause: 滚动后的暂停时间，秒
        """
        attempt = 0

        def find_and_click_android(element_selector):
            element = self.driver.xpath(element_selector)
            if element.exists:
                element2 = self.driver.xpath(
                    f"//*[@text='{text_to_find}']/following-sibling::*[2][@clickable='true']")
                if element2.exists:
                    element2.click()
                else:
                    element.click()
                time.sleep(2)
                logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的元素")
                return True
            return False

        def find_and_click_ios(element_selector):
            element = self.driver.xpath(element_selector)
            if element.exists and element.label == 'list device set':
                element.click()
                time.sleep(2)
                logger.info(f"尝试点击这个 '{text_to_find}' 元素右边的元素")
                return True
            return False

        def find_and_click_android_xpath(text):
            if find_and_click_android(f"//*[@text='{text}']/following-sibling::*[1][@clickable='true']"):
                return True
            else:
                logger.info(f"没有找到目标元素右边的可点击元素: '{text}'")
                self.driver(text=text).click()
                return True

        def find_and_click_ios_xpath(text):
            if find_and_click_ios(
                    f"//*[contains(@name, '{text}')]/following-sibling::*[1][@visible='true' and @enabled='true']"):
                return True
            if find_and_click_ios(
                    f"//*[contains(@name, '{text}')]/following-sibling::*[2][@visible='true' and @enabled='true']"):
                return True
            else:
                logger.info(f"没有找到目标元素右边的可点击元素: '{text}'")
                self.driver(label=text).click()
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
            logger.info(f"可能发生了错误: {err}")

        logger.info(f"还是没找到 '{text_to_find}' 元素，已经尝试了 {max_attempts} 次.")
        return False

    def parse_and_extract_text(self, xml_content, xml_parse_conditions, exclude_texts=None):
        """
        解析并提取XML指定文本内容（先这样写）
        :param xml_parse_conditions: iOS或安卓的xml解析条件，取自yaml文件
        :param xml_content: 获取的xml内容
        :param exclude_texts: 需要排除的文本
        :return:
        """
        if exclude_texts is None:
            exclude_texts = []

        texts = set()

        root = ET.fromstring(xml_content)
        for elem in root.iter():
            match = True
            for key, value in xml_parse_conditions.items():
                elem_value = elem.attrib.get(key)
                if isinstance(value, dict):
                    if 'not_equal' in value and elem_value == value['not_equal']:
                        match = False
                        break
                elif elem_value != value:
                    match = False
                    break
            if match:
                text = elem.attrib.get('text') if self.platform == "android" else elem.attrib.get('label')
                if text and text not in exclude_texts:
                    texts.add(text)
        return texts

    def scroll_screen(self, max_scrolls=1):
        """
        滚动屏幕
        :param max_scrolls: 最大滚动次数，默认1次
        :return:
        """

        if self.platform == "android":
            scroll_method = self.driver.swipe_ext
            direction = "up"

        elif self.platform == "ios":
            scroll_method = driver.swipe_up
        else:
            raise ValueError("不支持当前平台")

        for _ in range(max_scrolls):
            if self.platform == "android":
                scroll_method(direction)
            else:
                time.sleep(1)  # iOS平台需要短暂等待UI更新
                scroll_method()

    def get_all_texts(self, selector_type, selector, max_scrolls=2):
        """
        滚动获取当前页面所有指定文本
        :param selector_type: 支持安卓className，resource-id定位，iOS的className定位
        :param selector: 对应的value值
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
                elements = self.driver(className=selector).find_elements()
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

    def get_all_elements_texts(self, exclude_texts, xml_az_parse_conditions, xml_ios_parse_conditions, max_scrolls=2,
                               scroll_pause=1):
        """
        获取当前页面xml文件，解析出当前页面所有功能文案
        :param exclude_texts: 需要额外排除的文案
        :param xml_az_parse_conditions: 安卓xml解析条件，取自yaml文件
        :param xml_ios_parse_conditions: iOSxml解析条件，取自yaml文件
        :param max_scrolls: 最大滚动次数
        :param scroll_pause: 滚动后的停止时间，秒
        :return:
        """
        all_texts = set()

        # 确认当前被测平台是安卓还是iOS
        def get_page_source_and_parse(platform):
            if platform == "android":
                return self.driver.dump_hierarchy()
            elif platform == "ios":
                return self.driver.source()
            else:
                raise ValueError("不支持当前平台")

        # 根据被测平台选用不同的滚动方法
        def swipe_screen(platform):
            if platform == "android":
                self.driver.swipe_ext("up")
            elif platform == "ios":
                time.sleep(1)
                self.driver.swipe_up()
            else:
                raise ValueError("不支持当前平台")

        # 调用parse_and_extract_text解析方法将xml内容进行解析、去重
        def extract_texts_and_update(platform, parse_conditions):
            page_source = get_page_source_and_parse(platform)
            logger.info("已获取页面XML")

            texts = self.parse_and_extract_text(
                xml_content=page_source,
                xml_parse_conditions=parse_conditions,
                exclude_texts=exclude_texts
            )
            all_texts.update(texts)

        time.sleep(2)
        parse_conditions = xml_az_parse_conditions if self.platform == "android" else xml_ios_parse_conditions

        for _ in range(max_scrolls):
            extract_texts_and_update(self.platform, parse_conditions)
            swipe_screen(self.platform)
            time.sleep(scroll_pause)  # 等待页面稳定

        # 将去重后的文本内容写入文件
        output_path = os.path.abspath("./elements_texts.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            for text in sorted(all_texts):
                f.write(text + '\n')

        # 统计非空行数
        with open(output_path, 'r', encoding='utf-8') as f:
            non_empty_lines = sum(1 for line in f if line.strip())

        logger.info(f"总非空行数: {non_empty_lines}")

        return list(all_texts)

    def verify_page_text(self, expected_text, exclude_texts,
                         xml_az_parse_conditions, xml_ios_parse_conditions):
        """
        校验页面内容
        :param xml_ios_parse_conditions: ios
        :param xml_az_parse_conditions:
        :param expected_text: 需要检查的预期文本
        :param exclude_texts: 需要排除的文本
        :return:
        """
        # 获取页面所有功能名称
        texts = self.get_all_elements_texts(exclude_texts=exclude_texts,
                                            xml_az_parse_conditions=xml_az_parse_conditions,
                                            xml_ios_parse_conditions=xml_ios_parse_conditions
                                            )
        logger.info(f"获取的页面所有功能名称: {texts}")

        # 计算当前页面获取到的功能数量
        page_fun_num = len(texts)
        logger.info(f"当前页面获取到的功能数量：{page_fun_num}")

        # 计算预期设备 → 预期页面 → 预期文案数量
        count = len(expected_text)
        logger.info(f"预期设备的预期页面的预期文案数量：{count}")

        for line in expected_text:
            if line not in texts or page_fun_num != count:
                logger.info("当前页面功能可能不齐全！需要人工核查！")
                return False
        logger.info("当前页面功能比对齐全！")
        return True

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

    def scroll_find_element(self):
        """
        滚动检查元素是否在当前页面
        :return: bool
        """
        # TODO: 滚动检查元素是否在当前页面
        pass
