import sys
from typing import Iterable
import yaml
import os


class ReadYaml:
    __raw_data = dict()

    def __init__(self):
        # os.chdir("..")  # 注意：修改pycharm运行配置后，注销该行代码。
        p = os.path.join(os.getcwd(), 'config')
        for fname in os.listdir(p):
            # 如果文件的扩展名不是 'yml' 或 'yaml'，则跳过这个文件，不执行后续的处理。这个逻辑用于过滤掉不是 YAML 文件的内容，只处理 'config' 目录下的 YAML 文件。
            # fname.split('.')：这会将文件名（如 'example.yml'）按照点号分割成一个列表，即 ['example', 'yml']。
            if fname.split('.')[-1] not in ['yml', 'yaml']:  # [-1]：这表示获取列表的最后一个元素，即文件扩展名。对于 'example.yml'，它会得到 'yml'。
                continue
            with open(file=os.path.join(p, fname), encoding='utf-8') as stream:  # 打开file文件，as stream：将打开的文件对象赋值给名为 stream 的变量
                self.__raw_data[fname.split('.')[0]] = yaml.safe_load(stream)  # 获取文件名的前缀如case.yml中的case，作为__raw_data字典的键，值是从 YAML 文件加载得到的数据.
                # safe_load是 PyYAML 库的函数，用于从打开的 YAML 文件流中加载数据。这里的 stream 是 open 函数返回的文件对象。

        self.config_device_sn = self.get_data('config_device_sn', '')  # 获取手机序列号
        self.config_apk_name = self.get_data('config_apk_name', '')  # 获取安装包名称
        self.config_apk_local_path = self.get_data('apk_local_path')  # 获取安装包的本地地址
        self.wda_bundle_id = self.get_data('wda_bundle_id')  # 获取wda安装包名称
        self.uids_file_list = self.get_data('uids', source='uids')  # 获取uid列表

    def get_data(self, key: str, default: str = '', source: str = 'phone') -> str:
        """Get specific config"""
        # 这是一个三元表达式，用于返回根据给定键从配置数据中检索的值，如果键不存在，则返回默认值。
        # return self.__raw_data[source][key] if key in self.__raw_data[source] else default
        # 改写为if-else更易读的结构
        if key in self.__raw_data[source]:  # self.__raw_data[source] 表示从类实例的 __raw_data 字典中获取一个名为 source 的子字典。
            return self.__raw_data[source][key]  # self.__raw_data[source][key] 表示从 source 子字典中获取键为 key 的value值。
        else:
            return default

    def load_uids(self, uid_file_path='H:\\app-uiauto-test-dev\\config\\uids.yaml'):
        with open(uid_file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data.get('uids', [])


read_yaml = ReadYaml()
# read_yaml.__init__()
