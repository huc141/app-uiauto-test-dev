# -*- coding: utf-8 -*-
import os

import yaml

p = os.path.join(os.getcwd(), 'config')
print(p)

# 设备文件夹的根目录
config_root_dir = p

# 获取每个设备文件夹的路径
device_dirs = [os.path.join(config_root_dir, d) for d in os.listdir(config_root_dir) if
               os.path.isdir(os.path.join(config_root_dir, d))]
print("每个设备文件夹的路径:")
print(device_dirs)

# devices_list_path = os.path.join(os.getcwd(), 'config')
# wifi_parse_xml_path = os.path.join(devices_list_path, 'devices_list.yml')
# print(wifi_parse_xml_path)


# 定义一个函数来加载指定设备文件夹中的两个 YAML 文件
def load_device_config(device_dir):
    devices_list_path = os.path.join(os.getcwd(), 'config')
    # wifi_parse_xml_path = os.path.join(devices_list_path, 'devices_list.yml')
    wifi_path = os.path.join(device_dir, 'wifi.yaml')

    # print(wifi_parse_xml_path)

    # 初始化配置字典
    wifi_parse_xml_config = {}
    wifi_config = {}

    # 尝试加载 devices_list.yml 文件
    # if os.path.exists(wifi_parse_xml_path):
    #     try:
    #         with open(wifi_parse_xml_path, 'r', encoding='utf-8') as wifi_parse_xml_file:
    #             wifi_parse_xml_config = yaml.safe_load(wifi_parse_xml_file)
    #     except Exception as e:
    #         print(f"Error loading {wifi_parse_xml_path}: {e}")

    # 尝试加载 wifi.yaml 文件
    if os.path.exists(wifi_path):
        try:
            with open(wifi_path, 'r', encoding='utf-8') as wifi_file:
                wifi_config = yaml.safe_load(wifi_file)
        except Exception as e:
            print(f"Error loading {wifi_path}: {e}")

    # 合并两个配置文件的内容
    return {**wifi_parse_xml_config, **wifi_config}


# # 加载所有设备的配置文件内容
device_configs = [load_device_config(device_dir) for device_dir in device_dirs]
print(device_configs)
print('-------------------------------------')
# print(device_configs[0]['devices'])

# wifi_configs = read_yaml.wifi_configs
# wifi_sub_pages = read_yaml.wifi_sub_pages

# params = list(product(wifi_configs, wifi_sub_pages))


# 测试类
# class TestAppBehavior:
#     # 假设的辅助函数，用于执行WiFi测试
#     def perform_wifi_test(self, device_list_name, model, access_mode):
#         # 这个函数应该是实际执行WiFi测试的逻辑
#         pass
#
#     @pytest.mark.parametrize("device_config", device_configs)
#     def test_wifi_parse(self, device_config):
#         # 获取配置参数
#         device_list_name = device_config['device_list_name']
#         access_mode = device_config['access_mode']
#         # 打印信息，实际测试中可能进行其他操作
#         print(f"Testing {device_list_name} with app version {access_mode}")
#
#         model = device_config['model']
#         desc = device_config['desc']
#         print(f"model:{model},desc:{desc}")
#
#         # 假设我们有一个函数来执行WiFi测试
#         actual_result = self.perform_wifi_test(device_list_name, model, access_mode)
#
#         assert actual_result


# # 运行测试
# pytest.main()
