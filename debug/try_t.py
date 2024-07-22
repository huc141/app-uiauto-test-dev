# -*- coding: utf-8 -*-
import time
from itertools import product
from time import sleep
import pytest
import wda
import yaml
import os
import uiautomator2 as u2
from pages.base_page import BasePage
from common_tools.logger import logger
import wda
import time
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
import chardet
import os
import pytest
import yaml
from common_tools.read_yaml import read_yaml

p = os.path.join(os.getcwd(), 'config')
print(p)
# 设备文件夹的根目录
config_root_dir = p

# 获取每个设备文件夹的路径
device_dirs = [os.path.join(config_root_dir, d) for d in os.listdir(config_root_dir) if
               os.path.isdir(os.path.join(config_root_dir, d))]
print("每个设备文件夹的路径:")
print(device_dirs)


# 定义一个函数来加载指定设备文件夹中的 YAML 文件
def load_wifi_parse_xml(device_dir):
    yaml_file_path = os.path.join(device_dir, 'wifi_parse_xml.yml')
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def load_wifi_sub_page(device_dir):
    yaml_file_path = os.path.join(device_dir, 'wifi.yml')
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


# 加载所有设备的 YAML 文件内容
wifi_configs = [load_wifi_parse_xml(device_dir) for device_dir in device_dirs]
wifi_sub_pages = [load_wifi_sub_page(device_dir) for device_dir in device_dirs]
print(wifi_configs)

# wifi_configs = read_yaml.wifi_configs
# wifi_sub_pages = read_yaml.wifi_sub_pages

# params = list(product(wifi_configs, wifi_sub_pages))


# 测试类
class TestAppBehavior:
    @pytest.mark.parametrize("wifi_config", wifi_configs)
    def test_wifi_parse(self, wifi_config):
        # 获取配置参数
        device_list_name = wifi_config['device_list_name']
        access_mode = wifi_config['access_mode']
        # 打印信息，实际测试中可能进行其他操作
        print(f"Testing {device_list_name} with app version {access_mode}")

        # model = wifi_sub_page['model']
        # desc = wifi_sub_page['desc']
        # print(f"model:{model},desc:{desc}")

    @pytest.mark.parametrize("wifi_sub_page", wifi_sub_pages)
    def test_wifi_option(self, wifi_sub_page):
        model = wifi_sub_page['model']
        desc = wifi_sub_page['desc']
        print(f"model:{model},desc:{desc}")


# # 运行测试
# pytest.main()



