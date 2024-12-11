import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import subprocess
import tidevice
from tidevice import Device
import wda

import importlib
import os

from common_tools.logger import logger

driver = u2.connect_usb()


driver.xpath(xpath='//com.horcrux.svg.SvgView').drag_to(text='显示', duration=0.5)
