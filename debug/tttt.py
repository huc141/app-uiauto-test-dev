import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import subprocess
import tidevice
from tidevice import Device
import wda

# driver = u2.connect_usb("28131FDH2000K1")


# def read_device_file(device, device_path):
#     """
#     使用 uiautomator2 读取安卓设备中的文件内容
#     :param device: uiautomator2 的 Device 对象
#     :param device_path: 安卓设备中的文件路径
#     :return: 文件内容
#     """
#     file_content = device.shell(f"cat {device_path}")
#     return file_content
#
#
# # 示例用法
# if __name__ == "__main__":
#     device_path = "/sdcard/destination.xml"  # 替换为安卓设备中的文件路径
#     driver = u2.connect_usb("28131FDH2000K1")  # 连接设备
#
#     content = read_device_file(driver, device_path)
#     print("文件内容如下：")
#     print(content)

# driver.push("destination.xml", "/sdcard/")


# def read_device_file(device_path):
#     """
#     使用 tidevice 读取 iPhone 设备中的文件内容
#     :param device_udid: iPhone 设备的 UDID
#     :param device_path: iPhone 设备中的文件路径
#     :return: 文件内容
#     """
# 连接设备
# device = tidevice.Device(device_udid)

# 使用 fsync cat 命令读取文件内容
# file_content = device.fsync("cat", device_path)
# os.system("tidevice fsync push H:\\app-uiauto-test-dev\\debug\\destination.xml /Downloads/destination.xml")
# os.system("tidevice fsync tree /Downloads/")
# file_content = os.system("tidevice fsync cat /Downloads/destination.xml")
# content = file_content.decode('utf-8')

# command = f"tidevice fsync cat {device_path}"
#
# # 执行命令并捕获输出
# process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                          encoding='utf-8', errors='ignore')
# if process.returncode == 0:
#     return process.stdout
# else:
#     print(f"读取文件失败: {process.stderr}")
#     return None


# 示例用法
# if __name__ == "__main__":
#     driver = wda.Client('http://localhost:8100')
#     device_udid = "3db17f31334a5dbbe98c6d03b110f9ae0115e352"  # 替换为你的 iPhone 设备的 UDID
#     device_path = "/Downloads/destination.xml"  # 替换为 iPhone 设备中的文件路径
#
#     content = read_device_file(device_path)
#     if content:
#         print("文件内容如下：")
#         print(content)
# 获取指定路径的绝对路径
path = "../elements_texts.txt"
abs_path = os.path.abspath(path)

# 输出绝对路径
print(abs_path)
