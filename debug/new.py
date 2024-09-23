# import time
#
# from common_tools.read_yaml import read_yaml
# from pages.rn_device_setting_page.remote_setting import RemoteSetting

# import wda
#
# c = wda.Client('http://localhost:8100')
#
# s = c.session()
#
#
# # 使用类名定位元素
#
# def get_all_texts():
#     my_set = set()
#     temp = set()
#
#     # 将元素存储在列表中
#     # def get_elements_texts():
#     elements = c(className='XCUIElementTypeStaticText', index=0).find_elements()
#     static_text_elements = {element.text for element in elements}
#     # print(static_text_elements)
#
#     for element in static_text_elements:
#         x, y, w, h = element.bounds
#         if x == 31 and element.label is not None:
#             temp.update(element.text)
#             print(element)
#             print(element.text)
#             print(temp)
#
#         # return temp
#
#     # 获取当前页面所有元素的文本内容
#     # for _ in range(1):
#     #     # 获取当前页面所有元素的文本内容
#     #     new_texts = get_elements_texts()
#     #     my_set.update(new_texts)
#     #
#     #     c.swipe_up()
#     #     time.sleep(0.5)
#     #
#     #     # 检查滑动后页面是否有变化
#     #     new_texts = get_elements_texts()
#     #     if not new_texts - my_set:
#     #         break  # 如果滑动后没有新内容，退出循环
#     #
#     #     # 添加新获取的文本内容
#     #     my_set.update(new_texts)
#     #
#     # print(my_set)
#
#
# get_all_texts()


# 定义列表
# list1 = ['显示', '音频', '报警', '鸣笛']
# list2 = ['显示', '音频']
#
# # 验证list2中的元素是否都在list1中
# all_elements_in_list1 = all(element in list1 for element in list2)
#
# # 比较两个列表的元素数量是否一致
# same_length = len(list1) == len(list2)
#
# print(all_elements_in_list1)
# print(same_length)


# list1 = ['显示', '音频', '报警', '鸣笛']
# list2 = ['显示', '音频', '视频', 'pp', 'qq', 'aa']  # '视频' 不存在于 list1
#
# # 逐个检查list2中的元素是否在list1中
# elements_in_list1 = []
# for element in list2:
#     is_in_list1 = element in list1
#     elements_in_list1.append(is_in_list1)
#
#     # 如果元素不在list1中，则打印该元素
#     if not is_in_list1:
#         print(f"元素 '{element}' 不存在于 list1 中")
#
# # 检查是否list2中的所有元素都在list1中
# all_elements_exist = all(elements_in_list1)
#
# # 检查两个列表的长度是否相同
# lengths_are_equal = len(list1) == len(list2)
#
# print(f"所有元素都在list1中: {all_elements_exist}")
# print(f"两个列表的长度是否一致: {lengths_are_equal}")

# devices_config = read_yaml.load_device_config()  # 读取参数化文件
# element_config = read_yaml.load_device_config(device_dir='../config/global_config', yaml_file_name='')
# # idd = element_config['android']
# page_fun_list = ['音频', '显示']
# idd = RemoteSetting().extract_yaml_names(element_config, "setting")
#
# page_fun2 = RemoteSetting().scroll_check_funcs2(texts=page_fun_list, selector='Cell_Title')
#
# print(devices_config)
# print('-----------------------------')
# print(element_config)
# print(page_fun_list)
# print(page_fun2)


# import random
#
# lucky_er = ['黄sir', '曾银', '刘娜', '何建祥', '罗少', '罗玉隆']
# module_list = ['预览1', '预览2', '预览3', '回放', '添加设备2+灯+WiFi配网', '初始化']
#
# # 打乱列表元素顺序
# random.shuffle(lucky_er)
# random.shuffle(module_list)
#
# # 开始匹配
# pairings = {lucky_er[i]: module_list[i] for i in range(min(len(lucky_er), len(module_list)))}
#
# # 输出结果
# formatted_output = "\n".join([f"{name}：【{module}】" for name, module in pairings.items()])
# print(formatted_output)


import wda
import uiautomator2 as u2
from uiautomator2 import Direction

d = u2.connect_usb()

# d.swipe_ext(Direction.HORIZ_FORWARD)  # 页面水平右翻
# d.swipe_ext(Direction.HORIZ_BACKWARD)  # 页面水平左翻
e = d.xpath(xpath='//*[@resource-id="com.mcu.reolink:id/options1"]')
e.scroll('up')

# c = wda.Client('http://localhost:8100')
# s = c.session()
# s.swipe_right()