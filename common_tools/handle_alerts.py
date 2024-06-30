# -*- coding: utf-8 -*-
from common_tools.app_driver import driver
import time

from common_tools.logger import logger

DEFAULT_SECONDS = 15


class HandleAlerts:
    def __init__(self):
        self.driver = driver.get_actual_driver()
        self.platform = driver.get_platform()

    def handle_alerts(self):
        """
        定义并处理安卓/iOS常见弹窗
        """
        alert_buttons = [
            'com.android.permissioncontroller:id/permission_allow_foreground_only_button'  # 系统权限弹窗：仅在使用该应用时允许
        ]
        ios_alert_buttons = [
            "使用App时允许", "好", "稍后", "稍后提醒", "确定", "允许", "以后"
        ]
        try:
            if self.platform == 'android':
                for button in alert_buttons:
                    if self.driver(resourceId=button).exists:
                        print(f"识别到安卓相关弹窗按钮: {button}")
                        self.driver(resourceId=button).click()
                        return True
            elif self.platform == 'ios':
                session = self.driver.session()
                for button in ios_alert_buttons:
                    if session(label=button).exists:
                        print(f"识别到iOS相关弹窗按钮: {button}")
                        time.sleep(2)
                        session(label=button).tap()
                        logger.info(f"点击权限弹窗按钮: {button}")
                        return True
            return False
        except Exception as err:
            logger.error(f"处理权限弹窗失败，原因为：{err}")
            return False


handle_alert = HandleAlerts()
