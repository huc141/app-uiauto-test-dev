# -*- coding: utf-8 -*-
import os
import time
from io import BytesIO
from common_tools.logger import logger
from run import GenerateReports
import allure
import pytest
from common_tools.app_driver import driver
from common_tools.screen_record import scr

d2 = driver.get_actual_driver()  # 获取安卓/ios驱动
gr = GenerateReports()


# 在整个测试会话开始时被调用一次。这里的“测试会话”指的是从pytest命令行工具启动测试到测试结束的整个过程，可能包含多个测试文件和成百上千的测试用例,
# 适合那些跨测试文件的、需要在所有测试运行前准备好的资源设置.
# def pytest_sessionstart(session):
#     pass

def pytest_runtest_setup(item):  # 在每个测试用例的setup之前调用。
    # 开启录屏
    pass


def pytest_runtest_teardown(item):  # 在每个测试用例的teardown之后调用。
    # 结束录屏
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 后置处理
    outcome = yield
    gr.make_dir()
    report = outcome.get_result()

    if report.when == 'call':
        if report.failed or report.passed:
            test_name = item.name

            img = d2.screenshot()  # 失败自动截图(ios/安卓的截图调用的方法名称相同，由返回的d2驱动来控制)
            img_byte_arr = BytesIO()  # 将Image对象转换为字节流
            img.save(img_byte_arr, format='PNG')  # 将截图保存到BytesIO对象中，格式为PNG
            img_byte_arr = img_byte_arr.getvalue()  # 将截图保存到BytesIO对象中，格式为PNG
            allure.attach(img_byte_arr, '自动截图', allure.attachment_type.PNG)  # 将指定内容作为附件添加到测试报告。这里将截图的二进制数据作为附件，标题为“自动截图”，类型为PNG。
            logger.info("用例执行成功/失败，已自动截图")

            base_path = os.path.join(os.getcwd(), 'a_screen_record')  # 获取录屏文件的保存路径
            # time.sleep(2)
            screenrecord_name = scr.take_screenrecord(False)  # 停止录屏
            if screenrecord_name:
                screen_record_file_path = os.path.join(base_path, screenrecord_name)  # 拼接保存路径和录屏文件名
                print("screen_record_file_path的文件路径： " + screen_record_file_path)
                allure.attach.file(screen_record_file_path, name=f"{screenrecord_name}",
                                   attachment_type=allure.attachment_type.MP4)
            else:
                logger.warning(f"该{test_name}用例没有开启录屏")
                print(f"该【{test_name}】用例没有开启录屏")


def pytest_sessionfinish(session, exitstatus):  # 在所有测试用例运行完后调用，用于执行所有测试结束后的操作。
    # 所有用例执行完毕，自动生成allure测试报告
    logger.info("正在自动生成测试报告···")
    gr.generate_report()
    scr.take_screenrecord(False)  # 终止录屏进程
