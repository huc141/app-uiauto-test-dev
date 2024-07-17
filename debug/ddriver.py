import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
from common_tools.logger import logger

driver = u2.connect_usb("28131FDH2000K1")

driver(text="显示").click()





# 使用示例
# if __name__ == "__main__":
#     driver = u2.connect_usb("28131FDH2000K1")