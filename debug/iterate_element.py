import uiautomator2 as u2


# 初始化设备连接
# d = u2.connect_usb()


def find_element_by_xpath_recursively(d, xpath_prefix, target_id=None, target_text=None):
    """
    递归查找指定的目标元素，遍历同级和子级元素

    :param d: uiautomator2设备对象
    :param xpath_prefix: 当前元素的xpath前缀路径
    :param target_id: 目标元素的resourceId（可选）
    :param target_text: 目标元素的text属性值（可选）
    :return: 返回找到的目标元素对象，如果未找到则返回None
    """
    # 初始化同级元素索引
    sibling_index = 1

    while True:
        # 构建当前同级元素的xpath
        current_xpath = f"{xpath_prefix}[{sibling_index}]"
        current_element = d.xpath(current_xpath)

        # 如果当前同级元素不存在，则退出循环
        if not current_element.exists:
            print('不存在同级元素！')
            break

        # 检查是否匹配目标元素的条件
        if (target_id is None or current_element.info.get('resourceName') == target_id) and \
                (target_text is None or current_element.info.get('text') == target_text):
            return current_element  # 找到目标元素，返回该元素对象

        # 如果没有匹配，递归遍历当前元素的子元素
        child_index = 1
        while True:
            # 构建子元素的xpath路径
            child_xpath = f"{current_xpath}/*[{child_index}]"
            child_element = d.xpath(child_xpath)

            # 如果没有更多子元素，退出子元素循环
            if not child_element.exists:
                break

            # 递归在子元素中查找
            result = find_element_by_xpath_recursively(d, child_xpath, target_id, target_text)
            if result:
                return result  # 找到目标元素，返回该元素对象

            child_index += 1  # 检查下一个子元素

        # 检查下一个同级元素
        sibling_index += 1

    # 如果未找到目标元素，返回None
    return None


# 示例使用
# 连接设备
d = u2.connect()  # 请根据实际情况填写设备IP或序列号

# 定义起始元素的xpath路径
start_xpath = '//*[@resource-id="RNE__Slider_Thumb"]'

ele = d.xpath(xpath=start_xpath)
# print(ele.info)
# 调用方法查找目标元素
target_element = find_element_by_xpath_recursively(d,
                                                   start_xpath,
                                                   target_id="RNE__Slider_Thumb")


def operate_on_element(element):
    # 检查查找结果
    if element:
        print("找到目标元素:", element.info)
        print(element.info.get('text'))
        # element.swipe('right')
    else:
        print("未找到目标元素")


operate_on_element(target_element)
