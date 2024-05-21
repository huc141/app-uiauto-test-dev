from pages.welcome_page import WelcomePage
from common_tools.app_driver import driver
from common_tools.assert_ui import assertui
import allure


@allure.epic("项目：Android-Reolink-P2PCN-4.45.0.3.20240508")
@allure.feature("模块：APP欢迎页")
class TestWelcome:

    @allure.title("验证：安卓app安装卸载")
    @allure.description("预期：正常安装卸载")
    @allure.testcase("https://pms.reolink.com.cn/index.php?m=testcase&f=view&caseID=54170&version=0")
    def test_install_apk(self):
        """
        正向场景
        自动化用例编号：1001
        用例名称：验证安装卸载app
        """
        driver.init_driver()  # 连接手机
        driver.uninstall_app()  # 如果app存在则卸载app
        driver.install_app()  # 安装app

    @allure.title("验证：验证不同意隐私条款则退出app")
    @allure.description("预期：正常退出app")
    @allure.testcase("https://pms.reolink.com.cn/index.php?m=testcase&f=view&caseID=54170&version=0")
    def test_disagree_terms(self):
        welcome = WelcomePage()  # 初始化欢迎页的页面对象
        welcome.click_disagree_exit_btn()  # 点击【不同意并退出】按钮
        driver.clear_app_cache()  # 清除app缓存

    @allure.title("验证：验证同意隐私条款可正常进入app")
    @allure.description("预期：正常进入app")
    @allure.testcase("https://pms.reolink.com.cn/index.php?m=testcase&f=view&caseID=54170&version=0")
    def test_agree_terms(self):
        """
        正向场景
        自动化用例编号：1002
        用例名称：验证app欢迎页同意条款后进入设备列表页
        """
        driver.start()
        welcome = WelcomePage()  # 初始化欢迎页的页面对象
        welcome.click_terms_conditions_icon()  # 点击勾选【声明与条款】勾选框
        assertui.assert_clickable('com.mcu.reolink:id/btn', True)  # 断言点击勾选框后【同意并继续】按钮的可点击状态
        welcome.click_agree_continue_btn()  # 点击【同意并继续】按钮
        driver.stop()  # 停止app
        driver.clear_app_cache()  # 清除app缓存
