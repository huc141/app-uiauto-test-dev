import uiautomator2 as u2

d = u2.connect_usb()


def clear_app_cache():
    """
    清除app数据
    :return:
    """
    d.app_clear("com.mcu.reolink")
    print("清除reolink app数据成功···")


clear_app_cache()
