import uiautomator2 as u2


d = u2.connect_usb()

d.xpath('//*[@resource-id="ReoIcon-Left"]').click()

