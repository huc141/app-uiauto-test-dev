from pages.base_page import BasePage


class TermsConditionsPop(BasePage):
    def __init__(self):
        super().__init__()
        self.agree_term_button = "com.mcu.reolink:id/agree_term_button"

    def click_terms_conditions_icon(self):
        """
        点击勾选启动页自动弹出的【声明与条款】单选按钮
        :return:
        """
        if self is not None:
            return self.click_by_id(id_name=self.agree_term_button)
