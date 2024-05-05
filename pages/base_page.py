import re
from common_tools.app_driver import driver as app_driver

DEFAULT_SECONDS = 10


class BasePage:
    # 构造函数
    def __init__(self, driver):
        self.driver = driver

    def click(self, element):  # 点击
        self.driver.implicitly_wait(DEFAULT_SECONDS)
        try:
            if str(element).startswith("com"):  # 若开头是com则使用ID定位
                self.driver(resourceId=element).click()  # 点击定位元素
            elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
                self.driver.xpath(element).click()  # 点击定位元素
            else:  # 若以上两种情况都不是，则使用描述定位
                self.driver(description=element).click()  # 点击定位元素
        except Exception as e:
            raise e

    def click_text(self, element):  # 点击，根据文本定位
        self.driver(text=element).click()  # 点击定位元素

    def clear(self, element):  # 清空输入框中的内容
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).clear_text()  # 清除文本
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).clear_text()  # 清除文本
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).clear_text()  # 清除文本

    def find_elements(self, element, timeout=5):  # 找元素
        is_exited = False
        try:
            while timeout > 0:
                xml = self.driver.dump_hierarchy()  # 获取网页层次结构
                if re.findall(element, xml):
                    is_exited = True
                    break
                else:
                    timeout -= 1
        except:
            print("元素未找到!")
        finally:
            return is_exited

    def assert_exited(self, element):  # 断言元素是否存在
        assert self.find_elements(element) == True, "断言失败，{}元素不存在!".format(element)
