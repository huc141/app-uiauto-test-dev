from pages.base_page import BasePage
from common_tools.app_driver import driver as app_driver


class TermsConditionsPop(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_terms_conditions(self):
        """
        点击勾选启动页自动弹出的【声明与条款】单选按钮
        :return:
        """
        if app_driver:
            app_driver.