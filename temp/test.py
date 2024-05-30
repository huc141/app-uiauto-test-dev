import uiautomator2 as u2

from common_tools.read_yaml import read_yaml

# 在模块级别初始化Driver实例
driver_instance = None


class Driver:
    def __init__(self, device_sn: str, apk_name: str = '', apk_local_path: str = read_yaml.config_apk_local_path):
        self._device_sn = device_sn
        self._apk_name = apk_name
        self._apk_local_path = apk_local_path
        self._driver = None

    def init_driver(self):
        # ...（保持init_driver的原有逻辑不变）
        global driver_instance
        driver_instance = self._driver
        return driver_instance

    # ...（Driver类的其他方法保持不变）


def initialize_test_environment():
    """初始化测试环境，确保Driver实例被创建并初始化"""
    global driver_instance
    if driver_instance is None:
        driver = Driver(device_sn="39261FDJG0060S", apk_name="com.mcu.reolink")
        driver.init_driver()


class BasePage:
    def __init__(self):
        global driver_instance
        if driver_instance is None:
            initialize_test_environment()
        self.driver = driver_instance
        self.driver.wait_timeout = 15

    # ...（BasePage类的其他方法保持不变）


class WelcomePage(BasePage):
    def __init__(self):
        super().__init__()
        self.agree_term_button = "com.mcu.reolink:id/agree_term_button"
        self.agree_continue_btn = "com.mcu.reolink:id/btn"
        self.disagree_exit_btn = "com.mcu.reolink:id/cancel_button"

    def click_terms_conditions_icon(self):
        """
        点击勾选启动页自动弹出的【声明与条款】单选按钮
        :return:
        """
        return self.click_by_id(id_name=self.agree_term_button)


class TestWelcome:

    @classmethod
    def setup_class(cls):
        initialize_test_environment()

    def test_install_apk(self):
        # 使用共享的Driver实例
        self.driver.uninstall_app()
        self.driver.install_app()

# 其他测试类同样可以访问driver_instance
