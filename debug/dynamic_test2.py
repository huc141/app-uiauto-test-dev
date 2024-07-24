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


for page in pages:
    for menu_name in page:
        pass

