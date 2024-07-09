# -*- coding: utf-8 -*-
import time
from common_tools.app_driver import driver
import allure


@allure.epic("项目：Android-Reolink-P2PCN-4.45.0.3.20240508")
@allure.feature("模块：APP安装")
class TestInstallApp:

    @allure.title("验证：安卓app安装")
    @allure.description("预期：正常安装")
    @allure.testcase("https://pms.reolink.com.cn/index.php?m=testcase&f=view&caseID=54170&version=0")
    def test_install_apk(self):
        """
        正向场景
        自动化用例编号：1001
        用例名称：验证安装app
        """
        driver.start_app(True)
        driver.uninstall_app()  # 如果app存在则卸载app
        driver.install_app()  # 安装app
        time.sleep(5)
        driver.stop_app()
