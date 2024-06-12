# -*- coding: utf-8 -*-
from io import BytesIO
from common_tools.logger import logger
from run import GenerateReports
import allure
import pytest
import uiautomator2 as u2
from common_tools.app_driver import driver
from pages.base_page import BasePage
from common_tools.read_yaml import read_yaml

d2 = driver.get_actual_driver()
gr = GenerateReports()


# @pytest.fixture()
# def start():
#     # try:
#     #     d2.start()
#     # except Exception as err:
#     #     raise err
#     yield
#     try:
#         d2.stop()
#     except Exception as err:
#         raise err


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 后置处理
    outcome = yield
    gr.make_dir()
    report = outcome.get_result()
    if report.when == 'call':
        if report.failed or report.passed:
            logger.info("用例执行失败/成功，自动截图ing···")
            # test_name = item.name
            file_path = './screen_record/'
            img = d2.screenshot()
            test_name = driver.take_screenrecord(False)
            img_byte_arr = BytesIO()  # 将Image对象转换为字节流
            img.save(img_byte_arr, format='PNG')  # 将截图保存到BytesIO对象中，格式为PNG
            img_byte_arr = img_byte_arr.getvalue()  # 将截图保存到BytesIO对象中，格式为PNG
            allure.attach(img_byte_arr, '自动截图',
                          allure.attachment_type.PNG)  # 将指定的内容作为附件添加到测试报告中。这里将截图的二进制数据作为附件，标题为“失败截图”，类型为PNG。
            allure.attach.file(file_path, name=f"{test_name}_screenrecord", attachment_type=allure.attachment_type.MP4)


# 在所有测试用例运行完后调用，适合用于执行所有测试结束后的操作。
def pytest_sessionfinish(session, exitstatus):
    # 所有用例执行完毕，自动生成allure测试报告
    logger.info("正在自动生成测试报告···")
    gr.generate_report()
