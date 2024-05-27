from appium import webdriver
from appium.options.android import UiAutomator2Options

appium_server_url = 'http://localhost:4723'
capabilities = {
    'platformName': 'Android',
    'automationName': 'uiautomator2',
    'deviceName': '127.0.0.1:62001',
    'appPackage': 'com.mcu.reolink',
    'appActivity': 'com.android.bc.MainActivity',
}
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)


def test_driver():
    webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
