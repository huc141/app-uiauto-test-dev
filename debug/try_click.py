import uiautomator2 as u2


d = u2.connect_usb()


# 在新坐标处进行点击操作
d.xpath('//*[@text="清空所有"]').click()

