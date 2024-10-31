# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting


class RemoteEmailAlerts(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    @staticmethod
    def check_email_alerts_main_text(texts):
        """
        验证邮件通知主页文案
        :param texts: 待验证的文案列表
        :return:
        """
        try:
            email_alerts_main_text_status = RemoteSetting().scroll_check_funcs2(texts=texts)
            return email_alerts_main_text_status
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def set_email_config(self, email='1349983371@qq.com', passw='123456789'):
        """
        邮件设置
        :param email: 邮箱账号
        :param passw: 邮箱密码
        :return:
        """
        try:
            if not RemoteSetting().scroll_check_funcs2(texts='邮件设置'):
                time.sleep(1)
                # 设置邮箱
                self.input_text_clear(xpath_exp='//*[@text="输入邮箱"]', text=email)
                time.sleep(1)
                self.input_text(xpath_exp='//*[@text="输入密码"]', text=passw)

                # 点击保存
                self.scroll_and_click_by_text(text_to_find='保存')
                # 处理弹窗：点击确定/取消
                self.loop_detect_element_and_click(element_value='确定')

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def is_email_alert_on(self):
        """
        判断邮件通知按钮开关状态：
            ①如果为关，则点击打开，打开后配置邮件并保存；
            ②如果为开，则进行下一层判断：
                1.如果是缺省状态，则点击【现在设置】按钮，配置邮件并保存；
                2.如果是已配置状态，则不做其他操作。
        :return:
        """
        try:
            email_default_res = True
            email_default_list = ['邮件设置', '邮件通知', '检测到移动事件时，自动发送邮件提醒用户。',
                                  '未设置邮件信息将无法发送邮件通知。', '现在设置']
            # 如果是关：
            if (not RemoteSetting().scroll_check_funcs2(texts='测试') and
                    not RemoteSetting().scroll_check_funcs2(texts='现在设置')):
                self.scroll_click_right_btn(text_to_find='邮件通知')

                self.set_email_config()  # 设置邮箱

            # 如果是开-缺省状态：
            if RemoteSetting().scroll_check_funcs2(texts='现在设置'):
                email_default_res = RemoteSetting().scroll_check_funcs2(texts=email_default_list)
                self.scroll_and_click_by_text('现在设置')

                self.set_email_config()  # 设置邮箱

            return email_default_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_email_alarm_type(self, texts_list, option_text):
        """
        点击邮件通知>计划>报警>报警类型，验证文案内容
        :param texts_list: 报警类型页面需要验证的文案列表
        :param option_text: 操作列表
        :return:
        """
        try:
            self.scroll_and_click_by_text(text_to_find='报警类型')
            plan_alarm_type_text_res = RemoteSetting().scroll_check_funcs2(texts=texts_list)
            RemoteSetting().click_checkbox_by_text(option_text_list=option_text, menu_text='报警类型')
            time.sleep(1)
            self.scroll_and_click_by_text(text_to_find='保存')  # 点击报警类型的保存按钮
            self.scroll_and_click_by_text(text_to_find='保存')  # 保存当前计划
            return plan_alarm_type_text_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_plan(self, plan_alarm_text, plan_timed_text, alarm_type_text, alarm_type_option_text):
        """
        测试 计划
        :param plan_alarm_text: 计划>报警> 文案
        :param plan_timed_text: 计划>定时 文案
        :param alarm_type_text: 计划>报警>报警类型 文案
        :param alarm_type_option_text: 计划>报警>报警类型 操作选项
        :return:
        """
        try:
            self.scroll_and_click_by_text('计划')
            # 验证计划>报警>文案内容
            self.scroll_and_click_by_text('报警')
            plan_alarm_main_text_res = RemoteSetting().scroll_check_funcs2(texts=plan_alarm_text)

            # 验证计划>定时 文案内容
            self.scroll_and_click_by_text('定时')
            plan_timed_main_text_res = RemoteSetting().scroll_check_funcs2(texts=plan_timed_text)

            # 点击报警>报警类型
            self.scroll_and_click_by_text('报警')
            plan_alarm_type_text_res = self.click_and_test_email_alarm_type(texts_list=alarm_type_text,
                                                                            option_text=alarm_type_option_text)

            result = {
                'plan_alarm_main_text': plan_alarm_main_text_res,
                'plan_timed_main_text': plan_timed_main_text_res,
                'plan_alarm_type_text': plan_alarm_type_text_res
            }

            return result

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_email_config(self, email_config_text):
        """
        点击并测试邮件设置。
        测试策略：
            进入邮件设置，验证文案；
            点击发件邮箱，进入邮件设置编辑页，编辑发件邮箱、关闭/开启SSL、点击添加邮箱、点击?帮助；
            点击保存。
        :return:
        """
        try:
            self.scroll_and_click_by_text('邮件设置')
            email_config_text_status = RemoteSetting().scroll_check_funcs2(texts=email_config_text)

            # 进入发件邮箱
            self.scroll_and_click_by_text('134****371@qq.com')
            # TODO: 编辑发件邮箱、点击?帮助

            # 关闭/开启SSL
            self.scroll_click_right_btn(text_to_find='SSL or TLS',
                                        className_1='android.widget.TextView',
                                        className_2='android.widget.LinearLayout')
            self.scroll_and_click_by_text('取消')
            self.scroll_click_right_btn(text_to_find='SSL or TLS',
                                        className_1='android.widget.TextView',
                                        className_2='android.widget.LinearLayout')
            self.scroll_and_click_by_text('关闭')
            self.scroll_click_right_btn(text_to_find='SSL or TLS',
                                        className_1='android.widget.TextView',
                                        className_2='android.widget.LinearLayout')
            self.scroll_and_click_by_text('保存')

            # 点击添加邮箱
            self.scroll_and_click_by_text('+ 添加邮箱')
            self.input_text(xpath_exp='//*[@text="输入邮箱地址"]', text='autotestemail@gmail.com')
            self.scroll_and_click_by_text('保存')

            return email_config_text_status

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_email_content(self, option_text):
        """
        点击并遍历邮件内容
        :param option_text: 需要遍历的邮件内容列表
        :return:
        """
        try:
            self.scroll_and_click_by_text('邮件内容')
            self.iterate_and_click_popup_text(option_text_list=option_text, menu_text='邮件内容')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_and_test_email_interval(self, option_text):
        """
        点击并遍历邮箱间隔
        :param option_text: 需要遍历的邮箱间隔列表
        :return:
        """
        try:
            self.scroll_and_click_by_text('邮箱间隔')
            self.iterate_and_click_popup_text(option_text_list=option_text, menu_text='邮箱间隔')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def click_email_not_received_link(self):
        """
        点击未收到邮件？链接
        :return:
        """
        try:
            self.scroll_and_click_by_text('未收到邮件？')
            time.sleep(4)
            page_res = RemoteSetting().scroll_check_funcs2(texts='Troubleshooting - Fail to Get Alerts via Emails')
            self.back_previous_page()
            res = self.loop_detect_element_exist(element_value='邮件设置')
            if not res:
                pytest.fail(f"进入【未收到邮件？】页面后，未能返回到邮件通知页面！")

            return page_res
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
