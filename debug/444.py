import time
import logging

import pytest

from common_tools.logger import logger


def access_in_remote_setting(self, text_to_find='Reolink Altas Go PT', el_type='text', max_attempts=15, scroll_pause=0.5):
    """
    在设备列表中滚动查找指定设备名称(支持单机、nvr、hub),并点击远程设置按钮。
    :param el_type: 元素查找类型，支持 文本text(label).
    :param text_to_find: 要查找的文本
    :param max_attempts: 最大尝试次数
    :param scroll_pause: 滚动后的暂停时间，秒
    """

    def retry_connection(num_retries=4):
        for _ in range(num_retries):
            if self.driver(text='连接失败，点击重试').exists:
                self.click_by_text('连接失败，点击重试')
                time.sleep(10)
            else:
                # 如果检测到【报警设置】元素，则跳出循环
                if self.driver(text='报警设置').exists:
                    break
                else:
                    logger.info('loading中，继续等待')
                    time.sleep(10)
        else:
            pytest.fail(f'已重试 {num_retries} 次，未能连接上该设备！')

    def find_and_click_remote_setting(text):
        for i in range(3, 0, -1):  # 从3开始递减到1，先检查第三个兄弟元素
            setting_xpath = f"//*[@text='{text}']/following-sibling::*[{i}][@clickable='true']"
            if self.driver.xpath(setting_xpath).exists:
                self.driver.xpath(setting_xpath).click()
                retry_connection()
                return True
            else:
                logging.info(f"未找到该设备的远程设置按钮！")
                return False

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
            print(f"元素已找到: '{text_to_find}'")
            if self.platform == "android":
                if find_and_click_remote_setting(text_to_find):
                    return True
            elif self.platform == "ios":
                if find_and_click_remote_setting_ios(text_to_find):
                    return True
        else:
            print(f"尝试滚动查找 '{text_to_find}'... 第{attempt + 1}次")
            if self.platform == "android":
                self.driver(scrollable=True).scroll(steps=150)
            elif self.platform == "ios":
                self.driver.swipe_up()
            time.sleep(scroll_pause)

        attempt += 1

    print(f"还是没找到 '{text_to_find}' 元素，已经尝试了 {max_attempts} 次.")
    return False
