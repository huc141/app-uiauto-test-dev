import uiautomator2 as u2


# 初始化设备连接
d = u2.connect_usb()

scroll_method = d.swipe_ext

# scroll_method('up', scale=0.8)

# 获取屏幕size
win_x, win_y = d.window_size()
# 计算出屏幕宽度的1/10
box = (0, 0, win_x // 10, win_y)
scroll_method('up', box=box)
print(win_x, win_y)
print(box)

