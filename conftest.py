# -*- coding: utf-8 -*-
from io import BytesIO
from common_tools.logger import logger
from run import GenerateReports
import allure
import pytest
import uiautomator2 as u2
from common_tools.app_driver import driver
from common_tools.read_yaml import read_yaml

d2 = driver.get_actual_driver()
# d2 = u2.connect_usb(read_yaml.config_device_sn)
gr = GenerateReports()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 后置处理
    outcome = yield
    gr.make_dir()
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        logger.info("用例执行失败，自动截图ing···")
        img = d2.screenshot()
        img_byte_arr = BytesIO()  # 将Image对象转换为字节流
        img.save(img_byte_arr, format='PNG')  # 将截图保存到BytesIO对象中，格式为PNG
        img_byte_arr = img_byte_arr.getvalue()  # 将截图保存到BytesIO对象中，格式为PNG
        allure.attach(img_byte_arr, '失败截图', allure.attachment_type.PNG)  # 将指定的内容作为附件添加到测试报告中。这里将截图的二进制数据作为附件，标题为“失败截图”，类型为PNG。


# 在所有测试用例运行完后调用，适合用于执行所有测试结束后的操作。
def pytest_sessionfinish(session, exitstatus):
    # 所有用例执行完毕，自动生成allure测试报告
    logger.info("正在自动生成测试报告···")
    gr.generate_report()
