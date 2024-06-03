import time
from common_tools.app_driver import driver
from common_tools.logger import logger
from typing import Literal

DEFAULT_SECONDS = 15


class BasePage:
    def __init__(self):
        # if not driver._driver:  # # 检查 driver 是否已经初始化
        #     self.driver = driver.init_driver()
        # else:
        #     self.driver = driver._driver
        self.driver = driver.get_actual_driver()
        self.driver.wait_timeout = DEFAULT_SECONDS  # 设置全局等待超时时间为15秒

    def handle_alerts(self):
        """
        定义并处理常见弹窗
        """
        alert_buttons = [
            'com.android.permissioncontroller:id/permission_allow_foreground_only_button'  # 系统权限弹窗：仅在使用该应用时允许
        ]

        for button in alert_buttons:
            if self.driver(resourceId=button).exists:
                print(f"Found alert with button: {button}")
                self.driver(resourceId=button).click()
                return True
        return False

    # def click_by_id(self, resource_id):
    #     """通过id定位单个元素"""
    #     try:
    #         time.sleep(3)
    #         element = self.driver(resourceId=resource_id)
    #         if not element.exists():
    #             logger.error("该点击元素：%s 不存在", resource_id)
    #             raise ValueError(f"该点击元素：{resource_id} 不存在")
    #
    #         element.click()
    #         time.sleep(3)
    #     except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
    #         logger.error("ValueError: %s", verr)
    #         raise
    #     except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
    #         logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", resource_id, err)
    #         raise
    #     # return self.driver

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
                if self.handle_alerts():
                    if is_click_again:
                        continue  # 如果处理了权限弹窗，重试点击操作
                    else:
                        return True
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
                if self.handle_alerts():
                    if is_click_again:
                        continue  # 如果处理了权限弹窗，重试点击操作
                    else:
                        return True
                return True
            except ValueError as verr:  # 专门捕获并处理 ValueError 异常，可以在此处添加特定的处理逻辑。
                logger.error("ValueError: %s", verr)
                raise
            except Exception as err:  # 捕获并处理所有其他类型的异常，确保程序不会因为未处理的异常而崩溃。
                logger.error("页面中没有找到id为 %s 的元素，原因可能是：%s", xpath_expression, err)
                raise
        return False

    def input_text(self, text):
        """
        输入文本,不清空文本框内容，直接输入。
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
