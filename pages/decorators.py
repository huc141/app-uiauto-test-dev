from functools import wraps
import time

import pytest

from common_tools.read_yaml import read_yaml
from common_tools.logger import logger
from common_tools.app_driver import driver
from pages.base_page import BasePage

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
loading_icon = g_config.get("loading_icon")  # 页面加载loading菊花xpath


class PageLoader:
    def __init__(self):
        self.driver = driver.get_actual_driver()
        self.platform = driver.get_platform()

    def wait_for_element(self, text_or_xpath, d_type='text', timeout=10):
        """
        动态等待text文本元素出现
        :param text_or_xpath: 需要等待的文本内容
        :param d_type: text、xpath
        :param timeout: 超时时间，默认10秒
        :return:
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                if d_type == 'text' and self.driver(text=text_or_xpath).exists:
                    return True
                elif d_type == 'xpath' and self.driver.xpath(text_or_xpath).exists:
                    return True
            except Exception as err:
                # 在这里记录错误，但不会退出循环
                logger.error(f"检查元素时出错: {str(err)}")
            time.sleep(1)
        return False

    def retry_connection(self, num_retries=3):
        for _ in range(num_retries):
            # 优先检查是否已成功进入报警设置页面
            # if self.wait_for_element(text_or_xpath='显示'):
            #     logger.info('远程配置页面已成功加载！')
            # if not self.wait_for_element(text_or_xpath=loading_icon, d_type='xpath') and not self.wait_for_element(
            #         text_or_xpath='加载失败，请点击重试'):
            #     logger.info("远程配置首页已加载！")
            #     break

            if self.wait_for_element(text_or_xpath='加载失败，请点击重试'):
                logger.warning("检测到连接失败，尝试点击重试按钮...")
                BasePage().click_by_text('重试')
            elif self.wait_for_element(text_or_xpath='登录'):
                logger.warning("检测到设备未登录，跳过当前用例！")
                pytest.skip("设备未登录，跳过当前用例！")
            else:
                logger.info('loading中，继续等待')
                time.sleep(5)
        else:
            pytest.fail(f'已重试 {num_retries} 次！页面加载失败！')

    def is_page_loading(self):
        """检查页面是否还在加载"""
        if not self.wait_for_element(text_or_xpath=loading_icon, d_type='xpath') and not self.wait_for_element(
                text_or_xpath='加载失败，请点击重试'):
            logger.info("页面加载完成")
            return True
        else:
            self.retry_connection()

    def wait_until_page_loaded(self):
        """循环检测5次，每次检测后若页面已经成功加载则执行后续操作，若没有成功加载则等待6秒。"""
        max_attempts = 5
        for _ in range(max_attempts):
            if self.is_page_loading():
                return  # 页面已加载完成
            time.sleep(6)  # 等待6秒后再次检测
        pytest.fail("页面加载超时")
        # raise TimeoutError("页面加载超时")


def page_loader_decorator(func):
    """装饰器，用于等待页面加载完成。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        page_loader_instance = PageLoader()
        page_loader_instance.wait_until_page_loaded()  # 在调用原始函数之前执行的代码
        result = func(*args, **kwargs)
        # logger.info("装饰器执行完毕")  # 在调用原始函数之后执行的代码
        return result

    return wrapper
