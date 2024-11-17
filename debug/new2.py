import time

import uiautomator2 as u2

d = u2.connect_usb()


def detect_illegal_functions(legal_function_ids):
    """
    检查页面非法功能，需要事先定义排除的元素xpath列表
    :param legal_function_ids: 预期的合法功能名称列表
    :return:
    """
    try:
        if isinstance(legal_function_ids, list):
            # 定义需要排除的元素xpath列表
            exclude_xpath = [
                '//*[@resource-id="com.android.systemui:id/wifi_standard"]',
                '//*[@resource-id="com.android.systemui:id/clock"]',
                '//*[@resource-id="com.android.systemui:id/operator_name"]',
                '//*[@resource-id="RNE__ICON__Component"]',
                '//*[@resource-id="storageText"]',
                '//*[@resource-id="name"]',
                '//*[@resource-id="ReoValue"]',
                '//*[@resource-id="com.android.systemui:id/battery_digit"]',
                '//*[@resource-id="com.mcu.reolink:id/device_name_tv"]',
                '//*[@resource-id="com.mcu.reolink:id/device_type_tv"]',
                '//*[@resource-id="com.mcu.reolink:id/device_storage_tv"]',
                '//*[@resource-id="com.mcu.reolink:id/tv_sub_right"]'
            ]

            exclude_elements = []  # 定义需要排除的文案集合
            illegal_functions = []  # 定义非法功能列表
            all_elements = []  # 定义全屏文案集合

            def get_exclude_texts():  # 获取当前页面需要排除的文本内容
                for i in exclude_xpath:
                    try:
                        exclude_text = d.xpath(i).all()
                        for t in exclude_text:
                            element_text = t.text  # 获取元素的text属性
                            exclude_elements.append(element_text)  # 添加至exclude_elements列表
                            dr_exclude_elements = list(set(exclude_elements))  # 将列表转集合再转列表，去除重复元素
                    except Exception as err:
                        print(f'排除的文本内容时出错：{err}')
                print("需排除的内容有：")
                print(dr_exclude_elements)
                return dr_exclude_elements

            def get_fullscreen_text():  # 获取当前页面全屏文本
                fullscreen_text = d.xpath('//android.widget.TextView').all()  # 获取当前页面所有元素的文本内容
                for s in fullscreen_text:
                    element_texts = s.text  # 获取元素的text属性
                    all_elements.append(element_texts)
                    dr_all_elements = list(set(all_elements))  # 将列表转集合再转列表，去除重复元素
                print("当前页面全屏文本有：")
                print(dr_all_elements)
                return dr_all_elements

            for _ in range(3):
                # 先获取当前页面需要排除的文本内容
                new_exclude_texts = get_exclude_texts()
                exclude_elements.extend(new_exclude_texts)

                # 再获取当前页面所有元素的文本内容
                new_all_texts = get_fullscreen_text()
                all_elements.extend(new_all_texts)  # 添加至all_elements列表

                d.swipe_ext(direction='up')
                time.sleep(0.5)

            whole_page_exclude_elements = list(set(exclude_elements))
            whole_page_all_elements = list(set(all_elements))

            print("两轮循环后需要排除的内容：")
            print(whole_page_exclude_elements)
            print("两轮循环后全屏的内容：")
            print(whole_page_all_elements)

            # 从全屏文本中删掉需要排除的文本内容,构建出最终文本
            for e in whole_page_exclude_elements:
                if e in whole_page_all_elements:
                    whole_page_all_elements.remove(e)
                    whole_page_exclude_elements.append(e)
            print('本次移除的文本：')
            print(whole_page_exclude_elements)

            # 检查非法功能
            for element in whole_page_all_elements:
                if element not in legal_function_ids:
                    illegal_functions.append(element)

            # 将当前页面滑动回顶部
            print('尝试返回页面顶部...')
            d(scrollable=True).fling.vert.toBeginning(max_swipes=10)

            # 输出非法功能
            if illegal_functions:
                print(f"存在非法功能：{illegal_functions}")
            else:
                print("没有检测到非法功能。")
                return True

    except Exception as err:
        print(f"函数执行出错: {str(err)}")


# legal_function_ids = ['音频', '录制声音', '可设置设备报警音量及对讲音量', '试听', '音频降噪', '低', '高']
legal_function_ids = ['设置', 'Wi-Fi', '显示', '音频', '灯', '报警设置', '侦测报警', '摄像机录像', '报警通知',
                      '手机推送', '邮件通知', 'FTP', '鸣笛', '已联动的设备', '更多', '分享摄像机', '延时摄影', '高级设置',
                      '退出登录设备', '删除']
detect_illegal_functions(legal_function_ids)
















# print(remote_setting_page)


# def extract_value(yaml_content, keys):
#     def get_value(data, keys):
#         if not keys or data is None:
#             return data
#         key = keys[0]
#         if isinstance(data, dict):
#             return get_value(data.get(key), keys[1:])
#         elif isinstance(data, list) and isinstance(key, int):
#             return get_value(data[key], keys[1:])
#         return None
#
#     data = yaml.safe_load(yaml_content)
#     return get_value(data, keys)


# def extract_value(data, keys):
#     def get_value(data, keys):
#         if not keys or data is None:
#             return data
#         key = keys[0]
#         if isinstance(data, dict):
#             return get_value(data.get(key), keys[1:])
#         elif isinstance(data, list) and isinstance(key, int):
#             return get_value(data[key], keys[1:])
#         return None
#
#     return get_value(data, keys)


# 示例用法
# yaml_content = '''
# ipc:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
#
#     - name: 'Wi-Fi测速'
#       key: 'wifi_speed_test'
#       desc: '设置>Wi-Fi>Wi-Fi测速'
#       type: 'navigation'
#       subpage:
#         name: 'Wi-Fi测速'
#         desc: '设置>Wi-Fi>Wi-Fi测速>Wi-Fi测速'
#         type: 'button'
#         options:
#           - '开始测速'
#
#     - name: '未连接'
#       key: 'disconnect'
#       desc: '设置>Wi-Fi>未连接'
#       type: 'text'
#
#     - name: '添加其他网络'
#       key: 'add_other_network'
#       desc: '设置>Wi-Fi>添加其他网络'
#       type: 'navigation'
#       subpage:
#         name: '输入密码'
#         key: 'input_password'
#         desc: '设置>Wi-Fi>添加其他网络>输入密码'
#         type: 'page'
#         options:
#           - 'wifi名称'
#           - 'wifi密码'
#           - '取消'
#           - '保存'
#
# hub:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
#
# nvr:
#   name: 'Wi-Fi'
#   desc: '设置>Wi-Fi'
#   type: 'page'
#   items:
#     - name: 'Wi-Fi 频段偏好'
#       key: 'wifi_band_preference'
#       desc: '设置>Wi-Fi>Wi-Fi 频段偏好'
#       type: 'popup'
#       options:
#         - '自动'
#         - '仅 5G'
#         - '仅 2.4G'
#         - '取消'
# '''
# keys = ['ipc', 'items', 0]
# value = extract_value(devices_config, keys)
# print(value)


# path = 'H:\\app-uiauto-test-dev\\config'
#
# for item in os.listdir(path):
#     if os.path.isdir(os.path.join(path, item)):
#         print(item)  # 输出每一个文件夹的名字
