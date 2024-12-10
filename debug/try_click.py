import time

import pytest
import uiautomator2 as u2


d = u2.connect_usb()


# 在新坐标处进行点击操作
# d.xpath('//*[@text="清空所有"]').click()

import time
import logging
import pytest

logger = logging.getLogger(__name__)


def access_in_privacy_mask(self, option_text='遮盖区域'):
    """
    :param option_text: 菜单功能项，该方法默认点击【遮盖区域】
    :return:
    """
    try:
        texts = ['取消', '清空并继续']
        xpaths = [
            '//*[@resource-id="CancelDialog-ReoButton-Title"]',
            '//*[@resource-id="ConfirmDialog-ReoButton-Title"]'
        ]

        time.sleep(2)
        self.scroll_and_click_by_text(text_to_find=option_text)

        # 提取重复的条件判断部分，判断是否弹出特定提示
        is_confirmation_prompt_shown = self.is_element_exists(element_value='编辑画面遮盖，将会清空之前所有的遮盖区域，是否继续？')
        if is_confirmation_prompt_shown:
            for index, text in enumerate(texts):
                logger.info(f'弹出了遮盖区域提示，正在尝试点击【{text}】.')
                self.click_by_xpath(xpath_expression=xpaths[index])
                logger.info(f'已点击【{text}】')
                # 这里如果需要重复点击操作，可以考虑添加合适的逻辑来判断是否需要重复点击
                # 比如根据点击后的页面元素变化等条件来决定，当前代码只是简单重复点击原选项，可能需要进一步确认逻辑合理性
                self.scroll_and_click_by_text(text_to_find=option_text)
    except Exception as err:
        # 可以抛出更通用的异常或者进行更详细的包装，这里简单打印详细错误信息后重新抛出异常
        logger.error(f"函数执行出错: {err}", exc_info=True)
        raise  # 抛出异常让调用者决定如何处理，如果是在pytest中，调用者可以根据需要进行相应的测试失败处理等操作
