import time
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
        self.driver.wait_timeout = DEFAULT_SECONDS  # 设置全局等待超时时间为15秒

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
                element = self.driver.xpath(xpath_expression)
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

    def get_toast(self, toast_text: str, reset=True, default="没有获取到toast提示"):
        """
        获取页面弹出的toast
        :param toast_text: 需要检查的toast文案
        :param reset: 默认为True，即清除缓存的Toast，传False则不清除。
        :param default: 如果10s内没有获取到Toast，则返回此默认消息。
        :return:
        """
        try:

            # 尝试获取Toast消息
            toast_message = self.driver.toast.get_message(wait_timeout=10, cache_timeout=10)
            # 检查是否获取到Toast消息，如果没有则使用默认值
            actual_message = toast_message if toast_message else default
            # 验证Toast消息内容是否符合预期
            if toast_text not in actual_message:
                raise ValueError(f"预期的Toast文本：'{toast_text}' 未在实际Toast：'{actual_message}' 中找到")

            # 根据配置决定是否重置Toast缓存
            if reset:
                self.driver.toast.reset()

            return actual_message  # 成功匹配到Toast，返回其内容

        except Exception as err:
            # 确保在异常情况下也能访问到实际获取的Toast消息或默认值
            toast_message = self.driver.toast.get_message(wait_timeout=10, cache_timeout=10, default=default)
            raise ValueError(f"获取Toast失败，实际消息：'{toast_message}'，原因：{err}")

    def input_text(self, text):
        """
        输入文本,不清空文本框内容，直接输入。调用该方法时不要开启atx悬浮窗。
        :element: 编辑框的xpath表达式
        :text： 要输入的文本内容
        :return:
        """
        try:
            self.driver.send_keys(text)
        except Exception as err:
            logger.error(f"文本输入失败：{err}")

    def input_text_clear(self):
        """
        清空文本框内容并输入。
        :return:
        """
        pass
