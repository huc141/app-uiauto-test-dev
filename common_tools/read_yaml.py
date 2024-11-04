import sys
from typing import Iterable
import yaml
import os


class ReadYaml:
    __raw_data = dict()
    # 设备文件夹的根目录
    config_root_dir = os.path.join(os.getcwd(), 'config')

    def __init__(self):
        # p = os.path.join(os.getcwd(), 'config')

        # 读取 config 文件夹下的所有 YAML 文件
        for fname in os.listdir(self.config_root_dir):
            if fname.split('.')[-1] not in ['yml', 'yaml']:
                continue
            with open(file=os.path.join(self.config_root_dir, fname),
                      encoding='utf-8') as stream:
                self.__raw_data[fname.split('.')[0]] = yaml.safe_load(
                    stream)

        # 配置常规参数
        self.config_device_sn = self.get_data('config_device_sn', '')  # 获取手机序列号
        self.config_apk_name = self.get_data('config_apk_name', '')  # 获取安装包名称
        self.config_apk_local_path = self.get_data('apk_local_path')  # 获取安装包的本地地址
        self.wda_bundle_id = self.get_data('wda_bundle_id')  # 获取wda安装包名称
        self.uids_file_list = self.get_data('uids', source='uids')  # 获取uid列表
        self.devices_main_remote_setting_config = self.get_data("devices", source="devices_main_remote_setting")  # 获取设备配置

    # 定义一个函数来加载指定设备文件夹中的 YAML 文件
    def load_device_config(self, device_dir=None, yaml_file_name='setting.yaml'):
        device_configs = []

        if device_dir is None:
            device_dirs = [os.path.join(self.config_root_dir, d) for d in os.listdir(self.config_root_dir) if
                           os.path.isdir(os.path.join(self.config_root_dir, d))]
        else:
            device_dirs = [os.path.join(self.config_root_dir, device_dir)]

        # for _dir in device_dirs:
        #     yaml_path = os.path.join(_dir, yaml_file_name)
        #     if os.path.exists(yaml_path):
        #         try:
        #             with open(yaml_path, 'r', encoding='utf-8') as file:
        #                 config = yaml.safe_load(file)
        #                 device_configs.append(config)
        #         except Exception as e:
        #             print(f"Warning: {yaml_path} does not exist in {_dir}")
        #             print(f"Error loading {yaml_path}: {e}")
        for _dir in device_dirs:
            for root, dirs, files in os.walk(_dir):
                for filename in files:
                    if yaml_file_name and filename != yaml_file_name:
                        continue
                    if filename.endswith('.yaml') or filename.endswith('.yml'):
                        yaml_path = os.path.join(root, filename)
                        try:
                            with open(yaml_path, 'r', encoding='utf-8') as file:
                                config = yaml.safe_load(file)
                                device_configs.append(config)
                        except Exception as e:
                            print(f"Warning: Error loading {yaml_path}")
                            print(f"Error: {e}")

        return device_configs

    def get_data(self, key: str, default: str = '', source: str = 'phone') -> str:
        """Get specific config"""
        # 用于返回根据给定键从配置数据中检索的值，如果键不存在，则返回默认值。
        if key in self.__raw_data[source]:
            return self.__raw_data[source][key]
        else:
            return default


read_yaml = ReadYaml()
