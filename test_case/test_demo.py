from pages.Terms_Conditions_pop import TermsConditionsPop
from common_tools.app_driver import driver
import time
from common_tools.app_driver import Driver


class TestDemo:
    def test_0(self):
        driver.init_driver()
        driver.uninstall_app()
        driver.install_app()
        # device.start("com.mcu.reolink")

    def test_01(self):
        self.welcome = TermsConditionsPop()
        self.welcome.click_terms_conditions_icon()
        time.sleep(2)
        self.welcome.click_agree_continue_btn()



