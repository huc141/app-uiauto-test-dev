from pages.welcome_page import WelcomePage
from common_tools.app_driver import driver
import time
from common_tools.app_driver import Driver


class TestWelcome:
    """
    正向场景
    自动化用例编号：1001
    用例名称：验证安装卸载app
    """

    def test_install_apk(self):
        # 连接手机
        driver.init_driver()
        # 如果app存在则卸载app
        driver.uninstall_app()
        # 安装app
        driver.install_app()

    """
    正向场景
    自动化用例编号：1002
    用例名称：验证app欢迎页同意条款后进入设备列表页
    """

    def test_agree_terms(self):
        # 初始化欢迎页的页面对象
        self.welcome = WelcomePage()
        time.sleep(2)
        # 点击同意【声明与条款】勾选框
        self.welcome.click_terms_conditions_icon()
        time.sleep(2)
        # 点击【同意并继续】按钮
        self.welcome.click_agree_continue_btn()
        time.sleep(3)
        # 停止app
        driver.stop()
        # 清除app缓存
        driver.clear_app_cache()
