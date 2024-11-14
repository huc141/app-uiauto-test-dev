# import time
#
# from common_tools.read_yaml import read_yaml
# from pages.rn_device_setting_page.remote_setting import RemoteSetting
import time

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


import uiautomator2 as u2

d = u2.connect_usb()


# d.swipe_ext(Direction.FORWARD) # 页面下翻, 等价于 d.swipe_ext("up"), 只是更好理解
# d.swipe_ext(Direction.BACKWARD) # 页面上翻

# a = d(text='切换Wi-Fi').exists
# e = d.xpath(xpath='//android.widget.TextView[@text=""]')
# e.click()
# d.swipe_ext(Direction.HORIZ_FORWARD)  # 页面水平右翻
# d.swipe_ext(Direction.HORIZ_BACKWARD)  # 页面水平左翻
# e = d.xpath(xpath='//*[@text="开始测速"]')
# e.click()
# e.scroll('up')

# c = wda.Client('http://localhost:8100')
# s = c.session()
# s.swipe_right()

# 使用 press() 方法在元素上按住一段时间后再执行操作
# elem = s(xpath='image_id')
# elem.press(duration=5000)

# 确定合法功能的ID集合（这取决于你的APP，这里只是示例）
# legal_function_ids = ['音频', '录制声音', '关闭后，将不会录制声音到回放文件中', '设备音量',
#                       '报警音量和对讲音量', '试听', '音频降噪', '降噪强度', '自动回复', '低', '高']
#
# # 获取当前界面上所有的可见UI元素,
# #                  '//*[@resource-id="com.android.systemui:id/battery_digit"]',
# #                  '//*[@resource-id="com.android.systemui:id/wifi_standard"]'
# exclude_xpath = ['//*[@resource-id="com.android.systemui:id/clock"]',
#                  '//*[@resource-id="com.android.systemui:id/operator_name"]',
#                  '//*[@resource-id="RNE__ICON__Component"]',
#                  '//*[@resource-id="storageText"]',
#                  '//*[@resource-id="name"]',
#                  '//*[@resource-id="ReoValue"]']
#
# exclude_elements = []
# all_elements = []
#
# # 先获取需要排除的文本内容
# for i in exclude_xpath:
#     try:
#         text = d.xpath(i).all()
#         for t in text:
#             element_text = t.text
#             exclude_elements.append(element_text)
#         print("需要排除的内容：" + str(exclude_elements))
#     except Exception as err:
#         print(err)
#
# # 再获取全屏文本
# text2 = d.xpath('//android.widget.TextView').all()
# for i in text2:
#     # 获取元素的text属性，假设合法功能的ID就是UI元素的text
#     element_text = i.text
#     all_elements.append(element_text)
# print('全屏文本：' + str(all_elements))
#
#
# # 从全屏文本中排除掉需要排除的文本内容,构建出最终的文本
# excluded_text = []
# for i in exclude_elements:
#     if i in all_elements:
#         all_elements.remove(i)
#         excluded_text.append(i)
# print('本次移除的文本：' + str(excluded_text))
#
#
# # 检查非法功能
# illegal_functions = []
#
# for element in all_elements:
#     # 如果元素的text不在合法功能列表中，则标记为非法功能
#     if element not in legal_function_ids:
#         illegal_functions.append(element)
#
# # 输出非法功能
# if illegal_functions:
#     print("检测到以下非法功能：")
#     for func in illegal_functions:
#         print(func)
# else:
#     print("没有检测到非法功能。")

# 注意：这里使用的是XPath表达式`//android.widget.TextView`，它假设所有的功能文本都是TextView类型。
# 实际应用中，你可能需要根据APP的实际情况调整XPath表达式或使用其他属性进行筛选。


def detect_illegal_functions(legal_function_ids):
    """
    检查页面非法功能，需要事先定义排除的元素xpath列表
    :param legal_function_ids: 预期的合法功能名称列表
    :return:
    """
    try:
        if isinstance(legal_function_ids, list):
            # 定义需要排除的元素xpath列表
            exclude_xpath = ['//*[@resource-id="com.android.systemui:id/clock"]',
                             '//*[@resource-id="com.android.systemui:id/operator_name"]',
                             '//*[@resource-id="RNE__ICON__Component"]',
                             '//*[@resource-id="storageText"]',
                             '//*[@resource-id="name"]',
                             '//*[@resource-id="ReoValue"]'
                             ]

            exclude_elements = set()  # 定义需要排除的文案集合
            illegal_functions = []  # 定义非法功能列表
            all_elements = set()  # 定义全屏文案集合

            def get_exclude_texts():  # 获取当前页面需要排除的文本内容
                for i in exclude_xpath:
                    try:
                        exclude_text = d.xpath(i).all()
                        for t in exclude_text:
                            element_text = t.text  # 获取元素的text属性
                            exclude_elements.update(element_text)  # 添加至exclude_elements列表
                        print("需排除的内容有：")
                        print(exclude_elements)
                        return exclude_elements
                    except Exception as err:
                        print(f'排除的文本内容时出错：{err}')

            def get_fullscreen_text():  # 获取当前页面全屏文本
                fullscreen_text = d.xpath('//android.widget.TextView').all()  # 获取当前页面所有元素的文本内容
                for s in fullscreen_text:
                    element_texts = s.text  # 获取元素的text属性
                    all_elements.update(element_texts)
                return all_elements

            for _ in range(3):
                # 先获取当前页面需要排除的文本内容
                new_exclude_texts = get_exclude_texts()
                exclude_elements.update(new_exclude_texts)

                # 再获取当前页面所有元素的文本内容
                new_all_texts = get_fullscreen_text()
                all_elements.update(new_all_texts)  # 添加至all_elements集合

                d.swipe_ext(direction='up')
                time.sleep(0.5)

                # 检查滑动后页面是否有变化:
                # 1.排除的文本:
                new_exclude_texts = get_exclude_texts()
                new_all_texts = get_fullscreen_text()
                if not new_exclude_texts - exclude_elements and not new_all_texts - all_elements:
                    break  # 如果滑动后没有新内容，退出循环
                # 2.全屏文本：
                # new_all_texts = get_fullscreen_text()
                # if not new_all_texts - all_elements:
                #     break

                # 添加新获取的文本内容:
                # 1.排除的文本:
                exclude_elements.update(new_exclude_texts)
                all_elements.update(new_all_texts)

            # 从全屏文本中删掉需要排除的文本内容,构建出最终文本
            excluded_text = list(set(exclude_elements))
            print("需要排除的文案列表：")
            print(exclude_elements)
            all_texts = list(set(all_elements))
            print("全屏文案列表：")
            print(all_texts)
            for e in excluded_text:
                if e in all_texts:
                    all_texts.remove(e)
                    excluded_text.append(e)
                print('本次移除的文本：' + str(excluded_text))

            # 检查非法功能
            for element in all_texts:
                # 如果元素的text不在合法功能列表中，则标记为非法功能，添加到illegal_functions列表中
                if element not in legal_function_ids:
                    illegal_functions.append(element)

            # 输出非法功能
            if illegal_functions:
                print(f"存在非法功能：{illegal_functions}")
            else:
                print("没有检测到非法功能。")
                return True

    except Exception as err:
        print(f"函数执行出错: {str(err)}")


# legal_function_ids = ['音频', '录制声音', '关闭后，将不会录制声音到回放文件中', '设备音量',
#                       '报警音量和对讲音量', '试听', '音频降噪', '降噪强度', '自动回复', '低', '高']
legal_function_ids = ['Wi-Fi', '显示', '音频', '灯', '报警设置', '侦测报警', '摄像机录像', '报警通知',
                      '手机推送', '邮件通知', 'FTP', '鸣笛', '设备联动', '延时摄影', '安装方式', '更多设置',
                      '设备分享', '更多', '高级设置', '退出登录', '删除设备']
detect_illegal_functions(legal_function_ids)
