import uiautomator2 as u2

driver_device01 = u2.connect_usb('VOA6AU89B6GAO7U4')

print(driver_device01.info)

# 获取所有包名，返回一个列表
all_pkg_list = driver_device01.app_list()
print(len(all_pkg_list), all_pkg_list)

# 获取正在运行的APP的包名 com.mcu.reolink
running_pkg_list = driver_device01.app_list_running()
print(len(running_pkg_list), running_pkg_list)
