# 导入你所需要的页面的包
from pages.welcome_page import WelcomePage
from common_tools.app_driver import driver
import time


# 类 的命名
class TestDemo:
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
        # 停止app
        driver.stop()
        # 清除app缓存
        driver.clear_app_cache()


"""
命令行模式 

        1）运行所有：pytest

        2）运行指定模块：pytest -vs test_0616.py

        3）运行指定目录：pytest -vs ./api_testcase

        4）通过nodeID运行指定的测试函数：

                pytest -vs /test_case/test_welcome.py::TestWelcome::test_04_func
                
                        ① /testcase/test_welcome.py：当前test_welcome.py文件所在路径
                        ② TestWelcome:类名
                        ③ test_04_func：指TestLogin类中的你要运行的方法名
"""