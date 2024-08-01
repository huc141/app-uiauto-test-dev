import yaml
import os
from common_tools.read_yaml import read_yaml

devices_config = read_yaml  # 读取参数化文件
print(devices_config)
# 读取yaml文件中远程配置页面内
remote_setting_page = devices_config['ipc']['items']
# print(remote_setting_page)


# def extract_value(yaml_content, keys):
#     def get_value(data, keys):
#         if not keys or data is None:
#             return data
#         key = keys[0]
#         if isinstance(data, dict):
#             return get_value(data.get(key), keys[1:])
#         elif isinstance(data, list) and isinstance(key, int):
#             return get_value(data[key], keys[1:])
#         return None
#
#     data = yaml.safe_load(yaml_content)
#     return get_value(data, keys)


# def extract_value(data, keys):
#     def get_value(data, keys):
#         if not keys or data is None:
#             return data
#         key = keys[0]
#         if isinstance(data, dict):
#             return get_value(data.get(key), keys[1:])
#         elif isinstance(data, list) and isinstance(key, int):
#             return get_value(data[key], keys[1:])
#         return None
#
#     return get_value(data, keys)


# 示例用法
# yaml_content = '''
# ipc:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
#
#     - name: 'Wi-Fi测速'
#       key: 'wifi_speed_test'
#       desc: '设置>Wi-Fi>Wi-Fi测速'
#       type: 'navigation'
#       subpage:
#         name: 'Wi-Fi测速'
#         desc: '设置>Wi-Fi>Wi-Fi测速>Wi-Fi测速'
#         type: 'button'
#         options:
#           - '开始测速'
#
#     - name: '未连接'
#       key: 'disconnect'
#       desc: '设置>Wi-Fi>未连接'
#       type: 'text'
#
#     - name: '添加其他网络'
#       key: 'add_other_network'
#       desc: '设置>Wi-Fi>添加其他网络'
#       type: 'navigation'
#       subpage:
#         name: '输入密码'
#         key: 'input_password'
#         desc: '设置>Wi-Fi>添加其他网络>输入密码'
#         type: 'page'
#         options:
#           - 'wifi名称'
#           - 'wifi密码'
#           - '取消'
#           - '保存'
#
# hub:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
#
# nvr:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
# '''
# keys = ['ipc', 'items', 0]
# value = extract_value(devices_config, keys)
# print(value)


# path = 'H:\\app-uiauto-test-dev\\config'
#
# for item in os.listdir(path):
#     if os.path.isdir(os.path.join(path, item)):
#         print(item)  # 输出每一个文件夹的名字
