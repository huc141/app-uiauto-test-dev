import uiautomator2 as u2

d = u2.connect_usb("VOA6AU89B6GAO7U4")

d(resourceId="com.mcu.reolink:id/agree_term_button").click()
