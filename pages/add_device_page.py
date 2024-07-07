# -*- coding: utf-8 -*-
from typing import Literal
from common_tools.logger import logger
from pages.base_page import BasePage


class AddDevicePage(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            self.manual_input_button = '//*[@resource-id="com.mcu.reolink:id/tv_input_uid_ip"]'  # 按钮：手动输入
            self.manual_input_uid = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'  # UID选项的输入框

            self.manual_ip = '//*[@resource-id="com.mcu.reolink:id/tv_ip"]'  # IP选项
            self.manual_input_ip = '(//*[@resource-id="com.mcu.reolink:id/edit_text"])[1]'  # IP选项的输入框

            self.manual_authlink = '//*[@resource-id="com.mcu.reolink:id/tv_link"]'  # 授权链接选项
            self.manual_input_authlink = '//*[@resource-id="com.mcu.reolink:id/edit_text"]'  # 授权链接的输入框

            self.btn_next_step = '//*[@resource-id="com.mcu.reolink:id/btn_next"]'  # 按钮：下一步 （输入UID/IP/授权链接后点击）

            self.device_usage_method_title = '//*[@resource-id="com.mcu.reolink:id/tvTitle"]'  # 页面标题：选择设备的使用方式
            self.device_connect_to_hub = '//*[@resource-id="com.mcu.reolink:id/clHomeBase"]'  # 按钮：接入Home Hub使用
            self.device_stand_alone_use = '//*[@resource-id="com.mcu.reolink:id/clSelf"]'  # 按钮：单机使用

            self.device_network_access_method_title = '//*[@text="选择网络接入方式"]'  # 页面标题：选择网络接入方式
            self.device_wire_connection = '//*[@resource-id="com.mcu.reolink:id/llWireCard"]'  # 按钮：选择网线连接
            self.device_wifi_setted = '//*[@resource-id="com.mcu.reolink:id/llAlreadyConnectCard"]'  # 按钮：已配置wifi

            self.net_connection_example_title = '//*[@resource-id="com.mcu.reolink:id/base_navigationbar_title"]'  # 页面标题：添加新设备 (选择网线连接后进入的页面示意图)
            self.net_connection_example_btn = '//*[@resource-id="com.mcu.reolink:id/btn_connect"]'  # 选择网线连接后进入的页面示意图，按钮：访问摄像机
            self.net_next_step_btn = '//*[@resource-id="com.mcu.reolink:id/next_step_button"]'  # 选择网线连接后进入的页面示意图，按钮：下一步 （这个页面做一个遍历把，发现这样的按钮则直接点击）

            self.access_device_title = '//*[@text="访问设备"]'  # 页面标题：访问设备
            self.clear_device_account_btn = '//*[@resource-id="com.mcu.reolink:id/clear_button"]'  # 访问设备登录页按钮：清除设备账号
            self.device_account_text = '//android.widget.EditText[@text="输入用户名"]'  # 设备账号文本输入框
            self.device_passwd_text = '//android.widget.EditText[@text="输入密码"]'  # 设备密码文本输入框
            self.device_access_btn = '//*[@resource-id="com.mcu.reolink:id/btn_next"]'  # 按钮：访问

        elif self.platform == 'ios':
            self.manual_input_button = ''
            self.manual_input_uid = ''
            self.btn_next_step = ''

    def input_by_uid(self, uid):
        """
        设备列表-添加设备：输入设备uid并点击下一步
        uid: 你要添加的设备UID
        """
        self.click_by_xpath(self.manual_input_uid)
        self.input_text(uid)
        self.click_by_xpath(self.btn_next_step)

    def input_by_ip(self, ip):
        """
        设备列表-添加设备：输入设备ip并点击下一步
        :param ip: 设备ip
        :return:
        """
        self.click_by_xpath(self.manual_ip)
        self.click_by_xpath(self.manual_input_ip)
        self.input_text(ip)
        self.click_by_xpath(self.btn_next_step)

    def input_by_authlink(self, authlink):
        """
        设备列表-添加设备：输入设备授权链接并点击下一步
        :param authlink: 设备的授权链接
        :return:
        """
        self.click_by_xpath(self.manual_authlink)
        self.click_by_xpath(self.manual_input_authlink)
        self.input_text(authlink)
        self.click_by_xpath(self.btn_next_step)

    def click_device_wire_connection(self):
        """
        点击选择网线连接
        :return:
        """
        self.click_by_xpath(self.device_wire_connection)
        logger.info("点击选择网线连接")

    def click_device_wifi_setted(self):
        """
        点击已配置wifi
        :return:
        """
        self.click_by_xpath(self.device_wifi_setted)
        logger.info("点击已配置WiFi")

    def click_device_stand_alone_use(self):
        """
        点击单机使用
        :return:
        """
        self.click_by_xpath(self.device_stand_alone_use)
        logger.info("点击单机使用")

    def click_device_connect_to_hub(self):
        """
        点击接入home hub使用
        :return:
        """
        self.click_by_xpath(self.device_connect_to_hub)
        # TODO: 接入homehub的后续流程待开发
        logger.info("点击接入home hub使用")

    def access_device(self, account, passwd):
        """
        访问设备
        :param account: 设备账号
        :param passwd: 设备登录密码
        :return:
        """
        if account != 'admin':
            self.click_by_xpath(self.clear_device_account_btn)
            self.click_by_xpath(self.device_account_text)
            self.input_text(account)

        self.click_by_xpath(self.device_passwd_text)
        self.input_text(passwd)
        self.click_by_xpath(self.device_access_btn)
        logger.info("点击访问")

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

        except Exception as err:
            logger.error(f"识别页面类型时发生错误: {err}")
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
                self.click_by_text(btns)
                break
            else:
                logger.error("没有识别到这两个按钮")
        return self.identify_page_type()

    def _handle_access_device_login(self, is_stand_alone, is_net, account, passwd):
        """
        处理访问设备登录页的逻辑
        :param account: 设备登录账号
        :param passwd: 登录密码
        """
        self.access_device(account=account, passwd=passwd)
        return "access_device_login"

    def click_manual_input(self,
                           method='uid',
                           identifier=None,
                           is_stand_alone: Literal[True, False] = True,
                           is_net: Literal[True, False] = True,
                           account='admin',
                           passwd='reolink123'):
        """
        点击手动输入按钮,并选择以何种方式添加设备，并自动输入uid/ip/授权链接，然后点击下一步
        :param method: 配网方式：uid、ip、授权链接
        :param identifier: 对应的uid、ip、授权链接
        :param is_stand_alone: 是否单机使用，默认为是
        :param is_net: 是否网线连接，默认为是
        :param account: 登录设备的账号名，默认为admin
        :param passwd: 登录设备的密码，默认为app测试组所统一设置的reolink123
        :return:
        """
        self.click_by_xpath(self.manual_input_button)  # 点击按钮：手动输入

        input_methods = {
            "uid": self.input_by_uid,
            "ip": self.input_by_ip,
            "authlink": self.input_by_authlink
        }
        # 确保 method 是小写，避免重复转换
        method = method.lower()

        # 使用字典映射来选择对应的方法并调用
        if method in input_methods:
            input_methods[method](identifier)
            self.identify_page_type(is_stand_alone, is_net, account, passwd)
        else:
            raise ValueError(f"你可能输入了不支持的 method: {method}")
