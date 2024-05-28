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


def timeout_handler():
    """超时处理函数，设置一个全局标志表示超时"""
    global timeout_flag
    timeout_flag = True


# 初始化全局标志
timeout_flag = False

# 设置超时时间，例如5秒
timeout_seconds = 5

# 创建并启动计时器线程
timer = threading.Timer(timeout_seconds, timeout_handler)
timer.start()

while True:
    str1 = input("请输入数字选择：1 使用uiautomator2，2 使用appium，输入'q'退出：")

    # 检查是否超时
    if timeout_flag:
        print("输入超时，自动选择1 使用uiautomator2")
        str1 = "1"
        break

    timer.cancel()  # 如果用户及时输入，取消计时器
    timer = threading.Timer(timeout_seconds, timeout_handler)  # 并重新设置计时器，为下一次输入做准备
    timer.start()

    if str1.lower() == 'q':
        print("程序已退出。")
        break
    elif str1 == "1":
        print(f"你输入了：{str1}，现在启动uiautomator2")
        break
    elif str1 == "2":
        print(f"你输入了：{str1}，现在启动appium")
        break
    else:
        print("无效输入，请按照指示重新输入！")

# 确保计时器线程正确关闭
timer.cancel()
