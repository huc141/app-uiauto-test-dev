# -*- coding: utf-8 -*-
from common_tools.app_driver import driver
from common_tools.logger import logger
from pages.base_page import BasePage


class AssertUI(BasePage):
    def __init__(self):
        super().__init__()
        logger.info("UI断言初始化init_driver···")
        self.driver = driver.get_actual_driver()

    def assert_clickable(self, id_name: str, expect: bool):
        """
        传入元素id进行定位，传入expect期望值。
        :param id_name:元素id
        :param expect: 期望值，只接受布尔值
        :return:
        """
        if not self.driver:
            logger.error("self.driver不存在")
            return

        if not self.driver(resourceId=id_name).exists:  # 验证该元素是否存在
            logger.error('需要点击的UI元素: %s, 不存在', id_name)
            assert False, f"元素 {id_name} 不存在"

        logger.info('需要点击的UI元素: %s, 存在', id_name)
        element_is_clickable = self.driver(resourceId=id_name).info['clickable']  # 获取该元素的clickable属性
        element_is_enable = self.driver(resourceId=id_name).info['enabled']  # 获取该元素的enabled属性

        if element_is_enable and element_is_clickable:  # 如果两个属性均为True，则为真，否则为False
            logger.info('需要点击的元素： %s，当前已激活可点击状态', id_name)
            _element_is_clickable = True
        else:
            _element_is_clickable = False
        assert _element_is_clickable == expect, "【断言失败】，实际值{}与期望值{}不相等".format(
            _element_is_clickable, expect)

    def assert_text_in(self, expect_text):
        """
        检查expected_text是否存在于text中
        使用Python内置的count方法计算text中expected_text出现的次数
        如果expected_text在text中出现，那么其出现次数应大于0
        如果expected_text不在text中，断言将失败，并抛出一个AssertionError异常。异常的错误消息将包含期望的文本和实际的文本。
        """
        if expect_text is not None:
            if self.is_element_exists('xpath', expect_text):
                print("预期结果为为真")
                return True
            else:
                raise AssertionError(f"未找到预期文本：{expect_text}")

    # toast断言

    # 断言预期的元素是否可见：assertVisible

    # 断言实际值是否包含预期值:assertIn

    # 断言实际值是否不包含预期值:assertNotIn

    # 断言实际值是否等于预期值:assertEqual、assertNotEqual

    # 断言为真、假:assertTrue、assertFalse

    # 断言实际值与预期值的大小关系(大于、小于、等于)：

    # 断言预期文件是否存在:assert_output file_exist

    # 断言长度:assertLen


assertui = AssertUI()
