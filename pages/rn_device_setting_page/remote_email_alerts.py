# -*- coding: utf-8 -*-
import time
from typing import Literal
import pytest
from common_tools.logger import logger
from common_tools.read_yaml import read_yaml
from pages.base_page import BasePage
from pages.rn_device_setting_page.remote_setting import RemoteSetting

g_config = read_yaml.read_global_data(source="global_data")  # 读取全局配置
_ReoIcon_Draw = g_config.get('ReoIcon_Draw')  # 计划主页底部涂画按钮
_ReoIcon_Erase = g_config.get('ReoIcon_Erase')  # 计划主页底部擦除按钮
draw_text = g_config.get('draw_text')  # 选择涂抹按钮后显示的文案
erase_text = g_config.get('erase_text')  # 选择擦除按钮后显示的文案
alarm_type_selector = g_config.get('alarm_type_selector')  # 计划>报警类型 选项
switch_on = g_config.get('switch_on')  # switch开关打开状态
SSL_or_TLS = g_config.get('SSL_or_TLS')  # SSL or TLS 弹窗文案
reo_title_id = g_config.get('reo_title_id')  # ReoTitle选项id
common_email_alerts_off_texts = g_config.get('common_email_alerts_off_texts')  # 邮件通知主页关闭按钮
email_setting_list = g_config.get('email_setting_list')  # 邮件通知设置列表
common_email_now_setting_texts = g_config.get('common_email_now_setting_texts')  # 邮件通知【现在设置】页的内容
common_email_passw_help = g_config.get('common_email_passw_help')  # 邮件通知【现在设置】页的密码帮助xpath
common_email_passw_help_texts = g_config.get('common_email_passw_help_texts')  # 邮件通知【现在设置】页的密码帮助文案
common_smtp_help_texts = g_config.get('common_smtp_help_texts')  # 邮件通知【现在设置】页的发件服务器是什么的SMTP帮助文案
common_email_smtp_help = g_config.get('common_email_smtp_help')  # 邮件通知【现在设置】页的发件服务器是什么的SMTP帮助xpath
common_email_clear_texts = g_config.get('common_email_clear_texts')  # 邮件设置页的清空邮件配置按钮二次确认弹窗文案
email_plan_cell_texts = g_config.get('email_plan_cell_texts')  # 邮件通知主页>计划单元格的内容
email_plan_time_tips = g_config.get('email_plan_time_tips')  # 邮件通知>计划>定时 解释文案
email_plan_alarm_tips = g_config.get('email_plan_alarm_tips')  # 邮件通知>计划>报警 解释文案
erase_all_btn = g_config.get('erase_all_btn')  # 计划表【全部清除】按钮二次确认弹窗内容
common_email_content_texts = g_config.get('common_email_content_texts')  # 邮件内容主页通用文案
common_email_content_reotitle = g_config.get('common_email_content_reotitle')  # 邮件内容主页选项
turkey_b194_resolution = g_config.get('turkey_b194_resolution')  # 土耳其B194设备支持分辨率设置
turkey_b194_resolution_options = g_config.get('turkey_b194_resolution_options')  # 土耳其B194设备支持的分辨率选项


class RemoteEmailAlerts(BasePage):
    def __init__(self):
        super().__init__()
        if self.platform == 'android':
            pass

        elif self.platform == 'ios':
            pass

    # 点击测试按钮
    def click_test_button(self):
        """
        点击测试按钮
        :return:
        """
        try:
            self.click_by_text(text='测试')
            time.sleep(7)
            # 处理可能的弹窗
            for button in ['确定', '取消', '稍后']:
                if self.is_element_exists(element_value=button):
                    logger.info(f'点击 【{button}】 按钮')
                    self.click_by_text(text=button)
        except Exception as e:
            pytest.fail(f'点击测试按钮失败，错误信息：{e}')

    # 点击邮件通知开关
    def click_email_switch_button(self):
        """
        点击邮件通知开关
        """
        self.scroll_click_right_btn(text_to_find='邮件通知',
                                    resourceId_1='ReoTitle',
                                    className_2='android.view.ViewGroup')

    def _set_email_and_password(self, email, password):
        """
        输入邮箱和密码并保存,同时检查页面内容，点击【为什么要输入邮箱密码】、【发件服务器是什么】
        :param email: 邮箱账号
        :param password: 邮箱密码
        :return:
        """

        def _click_ssl_tls_option():
            """
            点击SSL或TLS选项
            """
            self.scroll_click_right_btn(text_to_find='SSL or TLS',
                                        resourceId_1='ReoTitle',
                                        className_2='android.view.ViewGroup')

        def _handle_ssl_tls(ssl_tls_switch):
            """
            处理SSL或TLS设置
            :param ssl_tls_switch: SSL或TLS开关状态
            """
            # 检查SSL或TLS是否已经开启，如果未开启则进行开启操作
            if not ssl_tls_switch:
                _click_ssl_tls_option()  # 点击开启
                time.sleep(2)  # 等待操作完成
                _click_ssl_tls_option()  # 再次点击关闭
            else:
                _click_ssl_tls_option()  # 点击关闭

            # 验证SSL or TLS 弹窗文案
            RemoteSetting().scroll_check_funcs2(texts=SSL_or_TLS, scroll_or_not=False, back2top=False)

            # 点击弹窗的确定按钮
            self.loop_detect_element_and_click(element_value='确定')

        try:
            # 先检查邮箱设置页内容
            RemoteSetting().scroll_check_funcs2(texts=email_setting_list, scroll_or_not=False, back2top=False)

            # 设置邮箱
            self.input_text_clear(xpath_exp='//*[@text="输入邮箱"]', text=email)
            self.input_text_clear(xpath_exp='//*[@text="输入密码"]', text=password)

            # 检查SSL或TLS开关状态并处理
            ssl_tls_switch_on = self.is_element_exists(element_value=switch_on, selector_type='id', scroll_or_not=False)
            _handle_ssl_tls(ssl_tls_switch_on)

            # 检查【为什么要输入邮箱密码】
            self.click_by_xpath(xpath_expression=common_email_passw_help)
            RemoteSetting().scroll_check_funcs2(texts=common_email_passw_help_texts,
                                                scroll_or_not=False,
                                                back2top=False)
            self.back_previous_page_by_xpath()

            # 检查【发件服务器是什么】 TODO:缺定位id
            self.click_by_xpath(xpath_expression=common_email_smtp_help)
            RemoteSetting().scroll_check_funcs2(texts=common_smtp_help_texts,
                                                scroll_or_not=False,
                                                back2top=False)
            self.back_previous_page_by_xpath()

            # 点击保存
            self.scroll_and_click_by_text(text_to_find='保存')
            time.sleep(8)  # 等待保存操作完成

            # 处理可能的弹窗
            for button in ['确定', '取消', '稍后']:
                if self.is_element_exists(element_value=button):
                    self.click_by_text(text=button)

        except Exception as e:
            pytest.fail(f"输入邮箱和密函数执行出错: {str(e)}")

    # 清空邮件设置
    def clear_email_config(self):
        """
        清空邮件设置
        :return:
        """
        try:
            # 点击邮箱设置菜单项
            self.click_by_text(text='邮箱设置')
            time.sleep(2)
            # 点击清空
            self.click_by_text(text='清空')
            time.sleep(2)
            # 验证弹窗内容：
            RemoteSetting().scroll_check_funcs2(texts=common_email_clear_texts,
                                                scroll_or_not=False,
                                                back2top=False)
            # 点击确定
            self.click_by_text(text='清空')
            time.sleep(3)
            if self.is_element_exists(element_value='现在设置'):
                logger.info('清空邮件设置成功！')
        except Exception as e:
            pytest.fail(f"清空邮件设置时出错: {str(e)}")

    def set_email_config(self, email='1349983371@qq.com', passw='123456789'):
        """
        邮件设置
        :param email: 邮箱账号
        :param passw: 邮箱密码
        :return:
        """
        try:
            # 未设置，点击现在设置
            if self.is_element_exists(element_value='现在设置'):
                # 先检查【现在设置】页面的内容
                RemoteSetting().scroll_check_funcs2(texts=common_email_now_setting_texts,
                                                    scroll_or_not=False,
                                                    back2top=False)
                self.click_by_text(text='现在设置')
                self._set_email_and_password(email, passw)
                return False

            # 未设置，已进入邮箱设置页
            elif self.is_element_exists(element_value='SMTP服务'):
                self._set_email_and_password(email, passw)
                return False

            # 已设置
            elif self.is_element_exists(element_value='未收到邮件？'):
                logger.info('该设备的邮件已设置，准备执行清空邮箱配置操作...')
                self.clear_email_config()
                return True

            else:
                pytest.fail('邮箱设置未知错误！可能未检测到指定元素！')

        except Exception as e:
            pytest.fail(f"设置邮件配置时出错: {str(e)}")

    def turn_on_email_alert(self):
        """
        判断邮件通知按钮开关状态：
            如果为关，则点击打开，打开后配置邮件并保存，并同时验证页面内容
        :return:
        """
        try:
            # 如果是关：
            if not self.is_element_exists(element_value=switch_on, selector_type='id', scroll_or_not=False):

                # 验证邮件通知关闭状态下主页内容：
                RemoteSetting().scroll_check_funcs2(texts=common_email_alerts_off_texts,
                                                    scroll_or_not=False,
                                                    back2top=False)

                # 点击右键通知开关，尝试开启
                self.click_email_switch_button()

                time.sleep(5)

                is_clear = self.set_email_config()  # 设置邮箱
                return is_clear

            # 如果是开：
            else:
                is_clear = self.set_email_config()  # 设置邮箱
                return is_clear

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_email_alerts_button_and_unsetting(self, supported_test):
        """
        测试未配置邮箱的情况下，打开邮件通知按钮、测试按钮、邮件设置页面内容
        :param supported_test: 是否支持测试按钮
        :return:
        """
        try:
            # 打开且配置邮件通知
            is_clear = self.turn_on_email_alert()

            # 如果清空了邮件配置，则重新配置邮件
            if is_clear:
                self.turn_on_email_alert()

            if supported_test:
                self.click_test_button()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_plan(self, supported_alarm, supported_timed, options_text):
        """
        测试 计划
        :param supported_alarm: 是否支持报警
        :param supported_timed: 是否支持定时
        :param options_text:
        :return:
        """

        def check_plan_common_texts():
            # 验证计划主页通用内容
            common_plan_texts = ['取消', '计划', '保存', '00', '02', '04', '06', '08', '10', '12', '14', '16', '18',
                                 '20',
                                 '22', '24', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
            RemoteSetting().scroll_check_funcs2(texts=common_plan_texts, scroll_or_not=False, back2top=False)

            # 验证底部涂抹按钮文案：擦除
            self.click_by_xpath(xpath_expression=_ReoIcon_Erase)
            RemoteSetting().scroll_check_funcs2(texts=erase_text, scroll_or_not=False, back2top=False)
            self.click_by_text('全部清除')  # 点击右下角全部清除按钮
            RemoteSetting().scroll_check_funcs2(texts=erase_all_btn, scroll_or_not=False, back2top=False)  # 验证二次弹窗内容
            self.click_by_text('全部清除')  # 点击二次弹窗中的全部清除按钮
            # 验证底部涂抹按钮文案：涂画
            self.click_by_xpath(xpath_expression=_ReoIcon_Draw)
            RemoteSetting().scroll_check_funcs2(texts=draw_text, scroll_or_not=False, back2top=False)
            self.click_by_text('全选')  # 点击右下角全选按钮

        def handle_alarm_type():
            """处理报警型页面的遍历和保存操作"""
            detect_text = ['取消', '报警类型', '保存']  # 报警类型全局文案
            detect_options = options_text['options']  # 报警类型选项文案
            self.click_checkbox_by_text(option_text_list=detect_options, menu_text='报警类型')
            self.scroll_and_click_by_text(text_to_find=detect_options[0])  # 保底选项，防止下一步无法点击保存
            RemoteSetting().scroll_check_funcs2(texts=detect_text, scroll_or_not=False, back2top=False)  # 验证报警类型页面通用文案
            RemoteSetting().scroll_check_funcs2(texts=detect_options, selector=alarm_type_selector, scroll_or_not=False, back2top=False)  # 验证报警类型选项文案
            self.scroll_and_click_by_text('保存')

        try:
            # 先打开邮件通知按钮
            self.turn_on_email_alert()

            # 验证邮件通知主页>计划单元格文案内容
            RemoteSetting().scroll_check_funcs2(texts=email_plan_cell_texts, scroll_or_not=False, back2top=False)

            # 点击进入计划主页
            self.click_by_text('计划')

            # 验证计划主页通用内容
            check_plan_common_texts()

            # 同时支持报警和定时
            if supported_alarm and supported_timed:
                # 验证计划>定时 文案内容
                self.click_by_text('定时')
                RemoteSetting().scroll_check_funcs2(texts=email_plan_time_tips, scroll_or_not=False, back2top=False)

                self.click_by_text('报警')
                RemoteSetting().scroll_check_funcs2(texts=email_plan_alarm_tips, scroll_or_not=False, back2top=False)

                # 点击报警>报警类型
                self.click_by_text('报警类型')
                handle_alarm_type()

            # 仅支持报警
            else:
                RemoteSetting().scroll_check_funcs2(texts=email_plan_alarm_tips, scroll_or_not=False, back2top=False)
                handle_alarm_type()

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_email_config(self):
        """
        点击并测试邮件设置。
        :param email_num: 可设置的收件邮箱数量
        :return:
        """

        def check_email_config_common_texts():
            """验证邮件设置页面通用内容"""
            common_email_config_texts = ['邮件设置', '清空', '邮件通过第一个邮箱发送到收件邮箱', '收件邮箱', '添加邮箱']
            RemoteSetting().scroll_check_funcs2(texts=common_email_config_texts, scroll_or_not=False, back2top=False)

        def add_email_addresses(email_num):
            """添加邮箱地址，直到达到最大邮箱数量限制"""
            max_emails = 3
            for i in range(max_emails - email_num):
                self.click_by_text('添加邮箱')
                email_address = f'{i}_autotestemail@gmail.com'
                self.input_text(xpath_exp='//*[@text="输入邮箱地址"]', text=email_address)
                self.scroll_and_click_by_text('保存')

        try:
            # 先打开邮件通知开关
            self.turn_on_email_alert()
            # 进入邮件设置
            self.click_by_text('邮件设置')
            # 验证邮件设置页面通用内容
            check_email_config_common_texts()

            # 进入发件邮箱
            self.scroll_and_click_by_text('134****371@qq.com')
            # 编辑邮件设置
            self._set_email_and_password(email='1349983371@qq.com', password='123456789')

            # 获取当前已设置的收件邮箱数量
            current_email_num = len(self.get_all_texts(selector=reo_title_id, selector_type='id', max_scrolls=1))
            # 如果当前邮箱数量小于最大限制，则添加邮箱
            if current_email_num < 3:
                add_email_addresses(current_email_num)
            elif current_email_num >= 3:
                # 如果当前邮箱数量等于或超过最大限制，检查是否还能添加邮箱
                if self.is_element_exists('添加邮箱'):
                    pytest.fail(f"当前已设置了3个收件邮箱，但还能进入添加邮箱页面！")

            # 编辑邮箱
            self.click_by_text('0_autotestemail@gmail.com')
            time.sleep(3)
            self.input_text_clear(xpath_exp='//*[@resource-id="RecipientEmail-ReoInput"]',
                                  text='00_autotestemail@gmail.com')
            self.click_by_text('保存')
            time.sleep(3)
            if not self.is_element_exists('00_autotestemail@gmail.com'):
                pytest.fail(f"编辑邮箱后，未检测到编辑后的邮箱！")

            # 删除邮箱
            self.click_by_text('00_****ail@gmail.com')
            time.sleep(3)
            self.click_by_text('删除')
            # 验证删除二次弹窗内容
            no_sender_tip = ['删除提示', '删除后将无法收到邮件通知。您确定要删除吗？', '取消', '删除']
            RemoteSetting().scroll_check_funcs2(texts=no_sender_tip, scroll_or_not=False, back2top=False)
            self.click_by_text('删除')
            time.sleep(3)
            if self.is_element_exists('00_****ail@gmail.com'):
                pytest.fail(f"检测到删除后的邮箱！邮箱删除不成功！")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_email_content(self, supported_move_track, supported_resolution, device_name):
        """
        点击并遍历邮件内容/移动轨迹/分辨率设置
        :param supported_move_track: 是否支持移动轨迹
        :param supported_resolution: 是否支持分辨率设置
        :param device_name: 设备名称(用于处理土耳其特殊版本，在设备列表的命名要与global_data中的turkey_b194_resolution一致)
        :return:
        """

        # 定义测试移动轨迹的方法
        def handle_move_track():
            # 点击移动轨迹菜单项
            self.click_by_text('移动轨迹')
            # 验证页面内容
            move_track_texts = ['移动轨迹', '在邮件中额外发送一张侦测目标的移动轨迹图。', '移动时间戳',
                                '显示目标移动的时间']
            reo_title_id_texts = ['移动轨迹', '移动时间戳']

            if not self.is_element_exists('移动时间戳'):
                self.scroll_click_right_btn(text_to_find='移动轨迹',
                                            resourceId_1=reo_title_id,
                                            className_2='android.view.ViewGroup')

                self.scroll_click_right_btn(text_to_find='移动时间戳',
                                            resourceId_1=reo_title_id,
                                            className_2='android.view.ViewGroup')
            else:
                self.scroll_click_right_btn(text_to_find='移动时间戳',
                                            resourceId_1=reo_title_id,
                                            className_2='android.view.ViewGroup')
                time.sleep(3)

            RemoteSetting().scroll_check_funcs2(texts=move_track_texts)
            RemoteSetting().scroll_check_funcs2(texts=reo_title_id_texts,
                                                selector=reo_title_id,
                                                scroll_or_not=False)

            self.scroll_click_right_btn(text_to_find='移动轨迹',
                                        resourceId_1=reo_title_id,
                                        className_2='android.view.ViewGroup')
            # 返回上一页
            self.back_previous_page_by_xpath()

        def handle_b194_resolution():
            # 点击分辨率设置菜单项
            self.click_by_text('分辨率设置')
            # 验证页面内容
            resolution_texts = ['图片分辨率', '清晰', '流畅']
            reo_title_id_texts = ['清晰', '流畅']

            RemoteSetting().scroll_check_funcs2(texts=resolution_texts)
            RemoteSetting().scroll_check_funcs2(texts=reo_title_id_texts,
                                                selector=reo_title_id,
                                                scroll_or_not=False)

            # 返回上一页
            self.back_previous_page_by_xpath()

            # 遍历分辨率选项
            self.iterate_and_click_popup_text(option_text_list=reo_title_id_texts, menu_text='分辨率设置')

        try:
            # 先打开邮件通知
            self.turn_on_email_alert()
            # 点击邮件内容
            self.click_by_text('邮件内容')
            # 验证邮件内容全局文案
            RemoteSetting().scroll_check_funcs2(texts=common_email_content_texts)
            RemoteSetting().scroll_check_funcs2(texts=common_email_content_reotitle,
                                                selector=reo_title_id,
                                                scroll_or_not=False)
            # 返回上一页
            self.back_previous_page_by_xpath()

            if turkey_b194_resolution == device_name and supported_move_track and supported_resolution:
                # 遍历邮件内容并测试点击移动轨迹\分辨率设置
                for i in common_email_content_reotitle:
                    self.click_by_text(text='邮件内容')
                    self.click_by_text(text=i)
                    time.sleep(1)
                    self.is_element_exists(element_value=i)
                    if i in ['图片', '图片和文字', '视频和文字']:
                        handle_move_track()
                        handle_b194_resolution()
                    else:
                        if self.is_element_exists(element_value='移动轨迹') or self.is_element_exists(element_value='分辨率设置'):
                            pytest.fail(f"【{i}】状态下，页面出现了移动轨迹或分辨率设置选项！")

        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_email_interval(self, texts, options):
        """
        点击并遍历邮箱间隔
        :param texts: 需要验证的全局页面内容
        :param options: 需要遍历的邮箱间隔列表
        :return:
        """
        try:
            # 先打开邮件通知开关
            self.turn_on_email_alert()
            # 点击邮箱间隔
            self.click_by_text('邮箱间隔')
            # 验证页面内容
            RemoteSetting().scroll_check_funcs2(texts=texts, scroll_or_not=False)
            RemoteSetting().scroll_check_funcs2(texts=texts, selector=reo_title_id)

            # 返回上一页
            self.back_previous_page_by_xpath()
            # 检测当前邮箱间隔被选中的选项，然后构造一个新的列表
            for i in options:
                if self.is_element_exists(element_value=i):
                    options.remove(i)
                    logger.info(f"【{i}】已被选中，构造新的邮箱间隔列表用于遍历：{options}")

            self.iterate_and_click_popup_text(option_text_list=options, menu_text='邮箱间隔')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")

    def verify_email_not_received_link(self):
        """
        点击未收到邮件？链接
        :return:
        """
        try:
            self.scroll_and_click_by_text('未收到邮件？')
            time.sleep(5)
            RemoteSetting().scroll_check_funcs2(texts='Troubleshooting - Fail to Get Alerts via Emails')
        except Exception as e:
            pytest.fail(f"函数执行出错: {str(e)}")
