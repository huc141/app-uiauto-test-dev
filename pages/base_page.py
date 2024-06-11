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
        # if not driver._driver:  # # 检查 driver 是否已经初始化
        #     self.driver = driver.init_driver()
        # else:
        #     self.driver = driver._driver
        self.driver = driver.get_actual_driver()
        # self.driver.wait_timeout = DEFAULT_SECONDS

    def find_element_xpath(self, xpath_expression):
        """
        通过xpath找元素
        :param xpath_expression: xpath表达式
        :return: 元素对象
        """
        return self.driver.xpath(xpath_expression)

    def click_by_id(self, resource_id, retries=2, is_click_again: Literal[True, False] = False):
        """
        :param resource_id: 通过id定位单个元素，并进行点击。
        :param retries: 如果遇到权限弹窗，会自动处理, 如果处理了弹窗，则通过is_click_again参数来判断是否重新尝试点击resource_id元素.
        :param is_click_again: 接收布尔值，默认为False，代表处理了弹窗之后，不会尝试再次点击resource_id元素；若为True，则处理弹窗之后，再次重新点击resource_id元素
        :return:
        """
        for attempt in range(retries):
            try:
                time.sleep(2)
                element = self.driver(resourceId=resource_id)
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
            try:
                time.sleep(2)
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

    def auto_screenshot(self, file_path):
        """
        用例失败后自动截图，这个方法为临时方法，后面可能会取消掉
        :param file_path: 截图文件的保存路径
        :return:
        """
        self.driver.screenshot(file_path)

    def take_screenshot(self, device_type="Android"):
        """
        屏幕截图，主要提供给写用例时需要主动截图的步骤进行调用。
        :param device_type: 设备类型，根据设备类型保存截图位置，默认Android
        :return:
        """
        screenshot_save_path = os.path.join(os.getcwd(), 'screenshot/android')
        # 确保保存目录存在
        if not os.path.exists(screenshot_save_path):
            os.makedirs(screenshot_save_path)

        # 获取当前时间并格式化为字符串
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if device_type.lower() == 'android':
            # 使用uiautomator2截图逻辑
            filename = f"{timestamp}-android.png"
            filepath = os.path.join(screenshot_save_path, filename)
            self.driver.screenshot(filepath)
            logger.info("Taking screenshot on Android device.")
        elif device_type.lower() == 'ios':
            # TODO: 处理iOS设备的截图
            print("Taking screenshot on iOS device.")
        else:
            raise ValueError("Unsupported device type. Please specify 'android' or 'ios'.")

    def stop_screenrecord(self):
        """
        停止录制屏幕
        """
        self.driver.screenrecord.stop()
        logger.info("Screen recording stopped")

    def take_screenrecord(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_name = f"{timestamp}.mp4"
        self.driver.screenrecord(video_name)
        logger.info(f"Screen recording started···")

    def input_text(self, text):
        """
        使用adb命令输入文本,不清空文本框内容，直接输入，不支持中文。
        :element: 编辑框的xpath表达式
        :text： 要输入的文本内容
        :return:
        """
        try:
            self.driver.set_input_ime(True)
            time.sleep(0.2)
            self.driver.send_keys(text)
            # for char in text:
            #     os.system('adb shell input text {}'.format(text))
            #     time.sleep(0.2)
        except Exception as err:
            logger.error(f"文本输入失败：{err}")

    def input_text_clear(self):
        """
        清空文本框内容并输入。
        :return:
        """
        pass
