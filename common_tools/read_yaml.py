import sys
from typing import Iterable
import yaml
import os


class ReadYaml:
    __raw_data = dict()

    def __init__(self):
        p = os.path.join(os.getcwd(), 'config')

        # 设备文件夹的根目录
        config_root_dir = p

        # 获取每个设备文件夹的路径
        device_dirs = [os.path.join(config_root_dir, d) for d in os.listdir(config_root_dir) if
                       os.path.isdir(os.path.join(config_root_dir, d))]

        # 读取 config 文件夹下的所有 YAML 文件
        for fname in os.listdir(p):
            if fname.split('.')[-1] not in ['yml', 'yaml']:
                continue
            with open(file=os.path.join(p, fname),
                      encoding='utf-8') as stream:  # 打开file文件，as stream：将打开的文件对象赋值给名为 stream 的变量
                self.__raw_data[fname.split('.')[0]] = yaml.safe_load(
                    stream)  # 获取文件名的前缀如case.yml中的case，作为__raw_data字典的键，值是从 YAML 文件加载得到的数据.

        # 配置常规参数
        self.config_device_sn = self.get_data('config_device_sn', '')  # 获取手机序列号
        self.config_apk_name = self.get_data('config_apk_name', '')  # 获取安装包名称
        self.config_apk_local_path = self.get_data('apk_local_path')  # 获取安装包的本地地址
        self.wda_bundle_id = self.get_data('wda_bundle_id')  # 获取wda安装包名称
        self.uids_file_list = self.get_data('uids', source='uids')  # 获取uid列表
        self.devices_main_remote_setting_config = self.get_data("devices",
                                                                source="devices_main_remote_setting")  # 获取设备配置

        # 定义一个函数来加载指定设备文件夹中的 YAML 文件
        def load_device_config(device_dir):
            wifi_parse_xml_path = os.path.join(device_dir, 'wifi_parse_xml.yml')
            wifi_path = os.path.join(device_dir, 'wifi.yml')

            with open(wifi_parse_xml_path, 'r', encoding='utf-8') as wifi_parse_xml_file:
                wifi_parse_xml_config = yaml.safe_load(wifi_parse_xml_file)

            with open(wifi_path, 'r', encoding='utf-8') as wifi_file:
                wifi_config = yaml.safe_load(wifi_file)

            # 合并两个配置文件的内容
            return {**wifi_parse_xml_config, **wifi_config}

        # 加载所有设备的 YAML 文件内容
        self.device_configs = [load_device_config(device_dir) for device_dir in device_dirs]
        # self.wifi_configs = [load_wifi_parse_xml(device_dir) for device_dir in device_dirs]
        # self.wifi_sub_pages = [load_wifi_sub_page(device_dir) for device_dir in device_dirs]

    def get_data(self, key: str, default: str = '', source: str = 'phone') -> str:
        """Get specific config"""
        # 用于返回根据给定键从配置数据中检索的值，如果键不存在，则返回默认值。
        if key in self.__raw_data[source]:
            return self.__raw_data[source][key]
        else:
            return default


read_yaml = ReadYaml()
