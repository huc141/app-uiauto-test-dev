# -*- coding: utf-8 -*-
import os
import time
from os.path import exists

from common_tools.app_driver import driver
from common_tools.logger import logger
from pages.device_list_page import DeviceListPage
import wda

c = wda.Client('http://localhost:8100')  # 8100为启动WDA设置的端口号
# c.app_current()  # 显示当前应用信息，主要用于获取bundleId，也可以使用tidevice ps 命令
c.session().app_activate("com.apple.Preferences")  # 打开设置
