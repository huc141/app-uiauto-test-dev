# while True:  # 创建一个无限循环，直到满足跳出条件
#     str1 = input("请输入数字选择：1 使用uiautomator2，2 使用appium，输入'q'退出：")
#
#     if str1.lower() == 'q':  # 添加退出选项，不区分大小写
#         print("程序已退出。你终止了测试。")
#         break  # 使用break语句跳出循环，结束程序
#
#     if str1 == "1":
#         print(f"你输入了：{str1}，现在启动uiautomator2")
#         break  # 输入有效，执行相应操作后退出循环
#     elif str1 == "2":
#         print(f"你输入了：{str1}，现在启动appium")
#         break  # 输入有效，执行相应操作后退出循环
#     else:
#         print("无效输入，请按照指示重新输入！")  # 无效输入时提醒用户重新输入


import threading
import time

from common_tools.logger import logger


def init_driver2(self):
    while True:  # 创建一个无限循环，直到满足跳出条件
        str1 = input("请输入数字选择：1 使用uiautomator2，2 使用appium，输入'q'退出：")

        if str1.lower() == 'q':  # 添加退出选项，不区分大小写
            print("程序已退出。你终止了测试。")
            break  # 使用break语句跳出循环，结束程序

        if str1 == "1":
            print(f"你输入了：{str1}，现在启动uiautomator2")
            logger.info("开始USB连接手机")
            try:
                self._driver = u2.connect_usb(self._device_sn)
                logger.info("连接成功")
                return self._driver
            except Exception as err:
                logger.error("连接失败，原因为：{}".format(err))
            break  # 输入有效，执行相应操作后退出循环
        elif str1 == "2":
            print(f"你输入了：{str1}，现在启动appium")
            break  # 输入有效，执行相应操作后退出循环
        else:
            print("无效输入，请按照指示重新输入！")  # 无效输入时提醒用户重新输入
