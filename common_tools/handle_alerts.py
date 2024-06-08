# -*- coding: utf-8 -*-
from common_tools.app_driver import driver

DEFAULT_SECONDS = 15


class HandleAlerts:
    def __init__(self):
        self.driver = driver.get_actual_driver()

    def handle_alerts(self):
        """
        定义并处理常见弹窗
        """
        alert_buttons = [
            'com.android.permissioncontroller:id/permission_allow_foreground_only_button'  # 系统权限弹窗：仅在使用该应用时允许
        ]

        for button in alert_buttons:
            if self.driver(resourceId=button).exists:
                print(f"识别到相关弹窗按钮: {button}")
                self.driver(resourceId=button).click()
                return True
        return False


handle_alert = HandleAlerts()
