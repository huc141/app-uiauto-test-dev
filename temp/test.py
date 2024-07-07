# -*- coding: utf-8 -*-
import pytest
import yaml
import os

from common_tools.logger import logger


class ReadYaml:
    __raw_data = dict()

    def __init__(self):
        # os.chdir("..")  # 注意：修改pycharm运行配置后，注销该行代码。
        p = os.path.join(os.getcwd(), 'config')
        for fname in os.listdir(p):  # 该函数会返回一个包含指定目录下所有文件和子目录名称的列表。
            if fname.split('.')[-1] not in ['yml', 'yaml']:  # [-1]：这表示获取列表的最后一个元素，即文件扩展名。对于 'example.yml'，它会得到 'yml'。
                continue
            with open(file=os.path.join(p, fname),
                      encoding='utf-8') as stream:  # 打开file文件，as stream：将打开的文件对象赋值给名为 stream 的变量
                self.__raw_data[fname.split('.')[0]] = yaml.safe_load(
                    stream)  # 获取文件名的前缀如case.yml中的case，作为__raw_data字典的键，值是从 YAML 文件加载得到的数据.

        self.config_device_sn = self.get_data('config_device_sn', '')  # 获取手机序列号
        self.config_apk_name = self.get_data('config_apk_name', '')  # 获取安装包名称
        self.config_apk_local_path = self.get_data('apk_local_path')  # 获取安装包的本地地址
        self.wda_bundle_id = self.get_data('wda_bundle_id')  # 获取wda安装包名称
        self.uids_file_list = self.get_data('uids', source='uids')  # 获取uid
        print("---------------")
        print(self.uids_file_list)

    def get_data(self, key: str, default: str = '', source: str = 'phone') -> str:
        if key in self.__raw_data[source]:  # self.__raw_data[source] 表示从类实例的 __raw_data 字典中获取一个名为 source 的子字典。
            return self.__raw_data[source][key]  # self.__raw_data[source][key] 表示从 source 子字典中获取键为 key 的value值。
        else:
            return default

    def load_uids(self, uid_file_path='H:\\app-uiauto-test-dev\\config\\uids.yaml'):
        with open(uid_file_path, 'r') as file:
            data = yaml.safe_load(file)
            print(data.get('uids', {}))
        return data.get('uids', {})


read_yaml = ReadYaml()
read_yaml.__init__()
print("---------分割线---------------")
uids_config = read_yaml.load_uids()


@pytest.mark.parametrize("uid_config", uids_config.values(), ids=uids_config.keys())
def ttt(uid_config):
    print(uid_config['method'],
          uid_config['identifier'],
          uid_config['is_stand_alone'],
          uid_config['is_net'],
          uid_config['account'],
          uid_config['passwd'])


# @pytest.mark.parametrize("config", data.items())
# def test_add_device_by_uid(config):
#     driver.start(True)
#     device_list_page = DeviceListPage()  # 初始化设备列表对像
#     device_list_page.click_add_device_button()  # 点击设备列表右上角的添加按钮
#     add_device_page = AddDevicePage()  # 初始化添加设备页面的对象
#     add_device_page.click_manual_input(config['method'],
#                                        config['identifier'],
#                                        config['is_stand_alone'],
#                                        config['is_net'],
#                                        config['account'],
#                                        config['passwd'])


def identify_page_type(self,
                       is_stand_alone: bool = True,
                       is_net: bool = True,
                       account: str = 'admin',
                       passwd: str = 'reolink123'):
    """
    判断页面是【选择设备的使用方式】 or 【选择网络接入方式】 or 【访问设备】的登录页
    :param passwd: 登录密码
    :param account: 设备登录账号
    :param is_stand_alone: 是否单机使用。默认为是.
    :param is_net: 是否网线接入，默认为是。
    :return: 页面类型
    """
    try:
        # 字典映射页面元素到处理方法
        page_handlers = {
            self.access_device_title: self._handle_access_device_login,
            self.device_network_access_method_title: self._handle_network_access_method,
            self.device_usage_method_title: self._handle_device_usage_method,
            self.net_connection_example_title: self._handle_net_example
        }

        # 遍历字典，识别当前页面并调用相应的处理方法
        for title, handler in page_handlers.items():
            if self.is_element_exists('xpath', title):
                logger.info(f"当前页面为【{title}】")
                return handler(is_stand_alone, is_net, account, passwd)

        logger.warning("未能识别当前页面类型")
        return "unknown_page"

    except Exception as e:
        logger.error(f"识别页面类型时发生错误: {e}")
        return "error"


def _handle_device_usage_method(self, is_stand_alone, is_net, account, passwd):
    """
    处理选择设备使用方式页面的逻辑
    :param is_stand_alone: 是否单机使用
    :param is_net: 是否网线接入
    """
    if is_stand_alone:
        self.click_device_stand_alone_use()
    else:
        self.click_device_connect_to_hub()
    return self.identify_page_type(is_stand_alone, is_net, account, passwd)


def _handle_network_access_method(self, is_stand_alone, is_net, account, passwd):
    """
    处理选择网络接入方式页面的逻辑
    :param is_net: 是否网线接入
    """
    if is_net:
        self.click_device_wire_connection()
    else:
        self.click_device_wifi_setted()
    return self.identify_page_type(is_stand_alone, is_net, account, passwd)


def _handle_net_example(self, *args):
    """
    处理选择网线接入后的示意图页面，点击下一步或者访问摄像机按钮
    :param self:
    :return:
    """
    page_example_btns = ["访问摄像机", "下一步"]
    for btns in page_example_btns:
        if self.is_element_exists('text', btns):
            self.click_by_xpath(self.manual_input_button)
        else:
            logger.error("没有识别到这两个按钮")
    return self.identify_page_type()


def _handle_access_device_login(self, account, passwd, *args):
    """
    处理访问设备登录页的逻辑
    :param account: 设备登录账号
    :param passwd: 登录密码
    """
    self.access_device(account, passwd)
    return "access_device_login"
