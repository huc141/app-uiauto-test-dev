# -*- coding: utf-8 -*-
import sys
from typing import Iterable
import yaml
import os


class ReadYaml:
    __raw_data = dict()

    def __init__(self):
        # os.chdir("..")  # 注意：修改pycharm运行配置后，注销该行代码。
        p = os.path.join(os.getcwd(), 'config')
        for fname in os.listdir(p):  # 该函数会返回一个包含指定目录下所有文件和子目录名称的列表。
            if fname.split('.')[-1] not in ['yml', 'yaml']:  # [-1]：这表示获取列表的最后一个元素，即文件扩展名。对于 'example.yml'，它会得到 'yml'。
                continue
            with open(file=os.path.join(p, fname), encoding='utf-8') as stream:  # 打开file文件，as stream：将打开的文件对象赋值给名为 stream 的变量
                self.__raw_data[fname.split('.')[0]] = yaml.safe_load(stream)  # 获取文件名的前缀如case.yml中的case，作为__raw_data字典的键，值是从 YAML 文件加载得到的数据.

        self.config_device_sn = self.get_data('config_device_sn', '')  # 获取手机序列号
        self.config_apk_name = self.get_data('config_apk_name', '')  # 获取安装包名称
        self.config_apk_local_path = self.get_data('apk_local_path')  # 获取安装包的本地地址
        self.wda_bundle_id = self.get_data('wda_bundle_id')  # 获取wda安装包名称
        self.uids_file_list = self.get_data('uids', source='uids')  # 获取uid列表
        print("---------------")
        print(self.uids_file_list)

    def get_data(self, key: str, default: str = '', source: str = 'phone') -> str:
        if key in self.__raw_data[source]:  # self.__raw_data[source] 表示从类实例的 __raw_data 字典中获取一个名为 source 的子字典。
            return self.__raw_data[source][key]  # self.__raw_data[source][key] 表示从 source 子字典中获取键为 key 的value值。
        else:
            return default

    def load_uids(self, uid_file_path: str):
        with open(uid_file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data.get('uids', [])


read_yaml = ReadYaml()
read_yaml.__init__()
