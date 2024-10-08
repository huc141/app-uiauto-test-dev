# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteAdvancedSetting(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    def check_test_advanced_main_text(self, texts):
        """
        验证高级设置主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            advanced_main_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            return advanced_main_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_multiple_accounts_device(self):
        """
        判断是否多账号设备，
            是：则高级设置页面不存在【修改设备密码】的菜单
            不是：则高级设置页面存在【修改设备密码】的菜单
        :return: bool
        """
        try:
            is_multiple_res = RemoteSetting().scroll_check_funcs2(texts='修改设备密码')
            return is_multiple_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_user_management(self):
        """
        点击进入用户管理页面
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='用户管理')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_illegal_login_lockout(self, texts):
        """
        点击测试非法登录锁定
        :return:
        """
        try:
            texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)  # 验证非法登录锁定按钮的文案内容
            self.scroll_click_right_btn(text_to_find='非法登录锁定')
            self.scroll_click_right_btn(text_to_find='非法登录锁定')
            return texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def check_manager_text(self, texts):
        """
        检查管理员栏的文案
        :return:
        """
        try:
            manager_texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)  # 验证管理员栏的文案内容
            return manager_texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_modify_passw(self):
        """
        TODO: 修改密码
        :return:
        """
        pass

    def check_user_text(self, texts):
        """
        检查用户栏的文案
        :return:
        """
        try:
            user_texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)  # 验证用户栏的文案内容
            return user_texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_check_date_time_text(self, texts):
        """
        点击并验证日期和时间的文案
        :return:
        """
        try:
            date_time_texts_res = RemoteSetting().scroll_check_funcs2(texts=texts)  # 验证日期和时间的文案内容
            return date_time_texts_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")