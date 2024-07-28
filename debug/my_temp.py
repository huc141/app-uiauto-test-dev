import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

import yaml

from common_tools.logger import logger
from common_tools.read_yaml import read_yaml

# devices_config = read_yaml.devices_main_remote_setting_config  # 读取参数化文件
# print(devices_config)
# print('-------------------------------------')

devices_config = read_yaml.load_device_config('reolink_trackmix_wifi', 'setting.yaml')  # 读取参数化文件
print(devices_config)


# print(devices_config)
# name = devices_config['ipc']['items']
# print(devices_config)


# 修改方法以提取指定keys下的items的name，并将它们全部加入到列表中，然后统计这个列表的长度。

def extract_all_names(yaml_content, keys_to_extract):
    """
    解析YAML文件，提取指定keys下的items的name，并全部加入到列表中。

    参数:
    file_path (str): YAML文件的路径。
    keys_to_extract (list): 要提取的keys列表。

    返回:
    list: 包含所有提取的name的列表。
    """
    # 初始化空列表
    all_names = []

    # 遍历指定的keys
    for key in keys_to_extract:
        # 获取每个key的items
        items = yaml_content.get(key, {}).get('items', [])
        # 遍历items，提取name并加入到列表中
        for item in items:
            name = item.get('name', '')
            if name:  # 如果name存在，则加入到列表中
                all_names.append(name)

    return all_names


# # 调用方法，并传入上传的YAML文件路径和要提取的keys
# keys_to_extract = ['ipc']
all_names = extract_all_names(devices_config, ['ipc'])
all_names_count = len(all_names)
print(all_names)
print(all_names_count)
