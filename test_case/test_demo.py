from pages.Terms_Conditions_pop import TermsConditionsPop
import uiautomator2 as u2
from common_tools.app_driver import driver as app_driver


class TestDemo:
    def setup(self):
        driver = u2.connect_usb("VOA6AU89B6GAO7U4")
        driver.app_start("com.mcu.reolink")
        self.welcome = TermsConditionsPop()
        # app_driver.start()

    def test_01(self):
        self.welcome.click_terms_conditions_icon()


t = TestDemo()
t.setup()
t.test_01()