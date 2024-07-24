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
    sleep(1)
    if action['type'] == 'click':
        element.click()
    elif action['type'] == 'input':
        element.send_keys(action['value'])


# 根据页面名称从pages列表中获取页面定义
def get_page_by_name(name):
    for page in pages:
        if page['name'] == name:
            return page
    return None


# 获取当前页面标题
def get_current_page_title():
    return d.xpath('//*[@resource-id="com.mcu.reolink:id/base_navigationbar_title"]').get_text()


# 执行页面中的所有元素操作
def execute_page(page):
    for element in page["elements"]:
        locator_method = element["locator"]["method"]
        locator_value = element["locator"]["value"]

        if locator_method == "text":
            ui_element = d(text=locator_value)
        elif locator_method == "id":
            ui_element = d(resourceId=locator_value)
        elif locator_method == "xpath":
            ui_element = d.xpath(locator_value)

        for action in element["actions"]:
            perform_action(action, ui_element)
            sleep(1)  # Add delays if necessary for the app to respond


# 遍历 YAML 文件中的所有页面并执行操作
for page in pages:
    print(f"Testing {page['name']}...")

    execute_page(page)
    current_page_title = get_current_page_title()

    # 将预期页面名称与当前页面名称做比较
    for element in page["elements"]:
        for action in element["actions"]:
            expected_result = action.get('expected_result')
            if expected_result and expected_result['type'] == 'page_loaded' and expected_result[
                'value'] == current_page_title:
                next_page = get_page_by_name(current_page_title)
                if next_page:
                    execute_page(next_page)
                    break
