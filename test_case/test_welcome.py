from pages.Terms_Conditions_pop import TermsConditionsPop
from common_tools.app_driver import driver
import time
from common_tools.app_driver import Driver


class TestWelcome:
    def test_install_apk(self):
        driver.init_driver()
        driver.clear_app_cache()
        driver.uninstall_app()
        driver.install_app()
        # driver.start()

    def test_agree_terms(self):
        self.welcome = TermsConditionsPop()
        time.sleep(2)
        # # self.welcome.click_disagree_exit_btn()
        self.welcome.click_terms_conditions_icon()
        time.sleep(2)
        self.welcome.click_agree_continue_btn()



