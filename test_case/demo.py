# 导入你所需要的页面的包
from pages.welcome_page import WelcomePage
from common_tools.app_driver import driver
from common_tools.assert_ui import assertui


# 类的命名
class TestWelcome:

    def test_install_apk(self):
        """
        正向场景
        自动化用例编号：1001
        用例名称：验证安装卸载app
        """
        driver.init_driver()  # 连接手机
        driver.uninstall_app()  # 如果app存在则卸载app
        driver.install_app()  # 安装app

    def test_disagree_terms(self):
        welcome = WelcomePage()  # 初始化欢迎页的页面对象
        welcome.click_disagree_exit_btn()  # 点击【不同意并退出】按钮
        driver.clear_app_cache()  # 清除app缓存

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


"""
命令行模式 

        1）运行所有：pytest

        2）运行指定模块：pytest -vs test_0616.py

        3）运行指定目录：pytest -vs ./api_testcase

        4）通过nodeID运行指定的测试函数：

                pytest -vs ./test_case/test_welcome.py::TestWelcome::test_install_apk
                
                        ① ./testcase/test_welcome.py：当前test_welcome.py文件所在路径
                        ② TestWelcome:类名
                        ③ test_install_apk：指test_install_apk：TestWelcome类中的你要运行的方法名
"""
