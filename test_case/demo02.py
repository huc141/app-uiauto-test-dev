from pages.welcome_page import WelcomePage
from common_tools.app_driver import driver
from common_tools.assert_ui import assertui
import allure


@allure.epic("项目：这里填项目名称，你可以填写用的是哪个app版本来测试的")
@allure.feature("模块：测的是哪个模块，比如APP的登录页")
class TestWelcome:

    # @allure.title("验证：安卓app安装卸载")
    # @allure.description("预期：正常安装卸载")
    # @allure.testcase("https://pms.reolink.com.cn/index.php?m=testcase&f=view&caseID=54170&version=0")
    # def test_install_apk(self):
    #     """
    #     正向场景
    #     自动化用例编号：1001
    #     用例名称：验证安装卸载app
    #     """
    #     driver.init_driver()  # 连接手机
    #     driver.uninstall_app()  # 如果app存在则卸载app
    #     driver.install_app()  # 安装app

    @allure.title("验证：这里填写自动化用例标题")
    @allure.description("预期：填写预期结果")
    @allure.testcase("这里填写禅道上对应的某条自动化用例链接地址")
    def test_disagree_terms(self):
        driver.start_app()
        welcome = WelcomePage()  # 初始化欢迎页的页面对象
        welcome.click_disagree_exit_btn()  # 点击【不同意并退出】按钮
        driver.stop_app()  # 停止app
        driver.clear_app_cache()  # 清除app缓存

    @allure.title("验证：同理")
    @allure.description("预期：同理")
    @allure.testcase("同理")
    def test_agree_terms(self):
        driver.start_app()
        welcome = WelcomePage()  # 初始化欢迎页的页面对象
        welcome.click_terms_conditions_icon()  # 点击勾选【声明与条款】勾选框
        assertui.assert_clickable('com.mcu.reolink:id/btn', True)  # 断言点击勾选框后【同意并继续】按钮的可点击状态
        welcome.click_agree_continue_btn()  # 点击【同意并继续】按钮
        driver.stop_app()  # 停止app
        driver.clear_app_cache()  # 清除app缓存
