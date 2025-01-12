import time

import uiautomator2 as u2


driver = u2.connect_usb()

element = driver(resourceId='RNE__Slider_Thumb_One')

for i in range(1, 10):
    time.sleep(2)
    element.swipe('left')

