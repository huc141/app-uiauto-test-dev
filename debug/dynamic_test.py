import yaml
import uiautomator2 as u2
from time import sleep

# 连接到设备
d = u2.connect()

# 读取 YAML 文件，并赋值给pages列表
with open("temp.yml", "r", encoding='utf-8') as file:
    pages = yaml.safe_load(file)["pages"]


# 定义元素操作函数
def perform_action(action, element):
    if action['type'] == 'click':
        sleep(1)
        element.click()
    elif action['type'] == 'input':
        sleep(1)
        element.send_keys(action['value'])


# 根据页面名称从pages列表中获取页面定义
def get_page_by_name(name):
    for pagee in pages:
        if pagee['name'] == name:
            return pagee
    return None


# 执行页面操作
# def execute_page(page_name):
#     # 从pages列表中获取页面名称
#     page = get_page_by_name(page_name)
#     # 如果页面在列表中不存在，则报错
#     if not page:
#         print(f"Page {page_name} not found.")
#         return
#
#     print(f"Testing {page['name']}...")
#
#     for element in page["elements"]:
#         # 获取元素的定位方法
#         locator_method = element["locator"]["method"]
#         # 获取元素的定位值：xpath、文本内容、id
#         locator_value = element["locator"]["value"]
#
#         # 判断元素的定位方法，执行对应的定位策略
#         if locator_method == "text":
#             ui_element = d(text=locator_value)
#         elif locator_method == "id":
#             ui_element = d(resourceId=locator_value)
#         elif locator_method == "xpath":
#             ui_element = d.xpath(locator_value)
#         # Add other locator methods as needed
#
#         # 遍历该元素的操作，执行对应操作
#         for action in element["actions"]:
#             perform_action(action, ui_element)
#             sleep(2)  # Add delays if necessary for the app to respond


# 执行特定页面元素的操作，特别是处理WiFiBandPreference的循环操作
# def execute_element_actions(page_name, element_name):
#     page = get_page_by_name(page_name)
#     if not page:
#         print(f"Page {page_name} not found.")
#         return
#
#     for element in page["elements"]:
#         if element["name"] == element_name:
#             locator_method = element["locator"]["method"]
#             locator_value = element["locator"]["value"]
#
#             if locator_method == "text":
#                 ui_element = d(text=locator_value)
#             elif locator_method == "id":
#                 ui_element = d(resourceId=locator_value)
#             elif locator_method == "xpath":
#                 ui_element = d.xpath(locator_value)
#             # Add other locator methods as needed
#
#             for action in element["actions"]:
#                 perform_action(action, ui_element)
#                 if action['expected_result']['type'] == 'dialog_opened':
#                     dialog_name = action['expected_result']['value']
#                     dialog = get_page_by_name(dialog_name)
#                     if dialog:
#                         for dialog_element in dialog['elements']:
#                             dialog_locator_method = dialog_element["locator"]["method"]
#                             dialog_locator_value = dialog_element["locator"]["value"]
#
#                             if dialog_locator_method == "text":
#                                 dialog_ui_element = d(text=dialog_locator_value)
#                             elif dialog_locator_method == "id":
#                                 dialog_ui_element = d(resourceId=dialog_locator_value)
#                             elif dialog_locator_method == "xpath":
#                                 dialog_ui_element = d.xpath(dialog_locator_value)
#                             # Add other locator methods as needed
#
#                             for dialog_action in dialog_element["actions"]:
#                                 perform_action(dialog_action, dialog_ui_element)
#                                 sleep(1)  # Add delays if necessary for the app to respond
#
#                             # 重新点击 WiFiBandPreference
#                             perform_action(action, ui_element)
#                             sleep(1)


# 获取页面标题
def get_current_page_title():
    page_title = d.xpath('//*[@resource-id="com.mcu.reolink:id/base_navigationbar_title"]')
    return page_title


def execute_page2(element_locator_method, element_locator_value, action):
    # 判断元素的定位方法，执行对应的定位策略
    if element_locator_method == "text":
        ui_element = d(text=element_locator_value)
    elif element_locator_method == "id":
        ui_element = d(resourceId=element_locator_value)
    elif element_locator_method == "xpath":
        ui_element = d.xpath(element_locator_value)

    # 执行元素的对应操作
    perform_action(action, ui_element)
    sleep(2)  # Add delays if necessary for the app to respond


# 遍历pages列表
def pages_iter(name1, name2):
    for element in pages:
        # 获取元素的定位方法和定位的值
        ele = element[name1][name2]
    return ele


# 遍历yaml文件即pages列表中的所有页面
for page in pages:
    print("Testing ...")
    # 获取元素的定位方法和定位的值
    element_locator_method = pages_iter('locator', 'method')
    element_locator_value = pages_iter('locator', 'value')
    expected_result = pages_iter('actions', 'expected_result')
    element_actions = pages_iter('actions', 'type')

    # 执行元素操作
    execute_page2(element_locator_method, element_locator_value, element_actions)

    # 获取当前页面标题
    page_title = get_current_page_title()

    # 将预期页面名称与当前页面名称做比较
    if expected_result['type'] == 'page_loaded' and expected_result['value'] == page_title:
        # 从pages列表里获取指定页面，并执行在该页面下的第一个操作
        page_title = get_page_by_name(page_title)

        # 获取元素的定位方法和定位的值
        element_locator_method = pages_iter('locator', 'method')
        element_locator_value = pages_iter('locator', 'value')
        expected_result = pages_iter('actions', 'expected_result')
        element_actions = pages_iter('actions', 'type')

        # 执行元素操作
        execute_page2(element_locator_method, element_locator_value, element_actions)

        # 获取当前页面标题
        page_title2 = get_current_page_title()

        # 将预期页面名称与当前页面名称做比较
        if expected_result['type'] == 'page_loaded' and expected_result['value'] == page_title:
            # 从pages列表里获取指定页面，并执行在该页面下的第一个操作
            page_title = get_page_by_name(page_title)



# 测试主流程
# def main():
#     execute_page("设置")
#     execute_element_actions("Wi-Fi", "Wi-Fi 频段偏好")
#     execute_page("Wi-Fi")
#     execute_element_actions("Wi-Fi", "Wi-Fi测速")
#     execute_page("Wi-Fi")
#     execute_element_actions("Wi-Fi", "添加其他网络")

#
# if __name__ == "__main__":
#     main()
