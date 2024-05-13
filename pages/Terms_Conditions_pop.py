from pages.base_page import BasePage


class TermsConditionsPop(BasePage):
    def __init__(self, device_sn=None, apk_name=None):
        super().__init__(device_sn, apk_name)
        self.agree_term_button = "com.mcu.reolink:id/agree_term_button"
        self.agree_continue_btn = "com.mcu.reolink:id/btn"

    def click_terms_conditions_icon(self):
        """
        点击勾选启动页自动弹出的【声明与条款】单选按钮
        :return:
        """
        return self.click_by_id(id_name=self.agree_term_button)

    def click_agree_continue_btn(self):
        """
        点击欢迎页自动弹出的【声明与条款】的【同意并继续】按钮
        :return:
        """
        return self.click_by_id(id_name=self.agree_continue_btn)
