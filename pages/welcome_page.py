from pages.base_page import BasePage


class WelcomePage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.agree_term_button = "com.mcu.reolink:id/agree_term_button"
            self.agree_continue_btn = "com.mcu.reolink:id/btn"
            self.disagree_exit_btn = "com.mcu.reolink:id/cancel_button"
        elif self.platform == 'ios':
            self.agree_term_button = "待定···"
            self.agree_continue_btn = "待定···"
            self.disagree_exit_btn = "待定···"

    def click_terms_conditions_icon(self):
        """
        点击勾选启动页自动弹出的【声明与条款】单选按钮
        :return:
        """
        return self.click_by_id(resource_id=self.agree_term_button)

    def click_agree_continue_btn(self):
        """
        点击欢迎页自动弹出的【声明与条款】的【同意并继续】按钮
        :return:
        """
        return self.click_by_id(resource_id=self.agree_continue_btn)

    def click_disagree_exit_btn(self):
        """
        点击欢迎页自动弹出的【声明与条款】的【不同意并退出】按钮
        :return:
        """
        return self.click_by_id(resource_id=self.disagree_exit_btn)
