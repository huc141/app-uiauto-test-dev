# @Fuction  :主要是页面的一些操作

import allure
from datetime import datetime
from appium import webdriver
from commons.deal_log import Logs
from configs.config import ImagePath

class Operates():
    # 初始化页面的操作
    def __init__(self):
        """
        构造函数，创建必要的实例变量
        """
        self.log = Logs().get_log()  # 初始化一个log对象

    # def init_driver(self):
    #     """
    #     告诉appium自动化测试相关的配置项
    #     :return: 返回驱动
    #     """

        caps = {
            # 被测APP所处平台-操作系统
            'platformName': 'Android',
            # 操作系统版本
            'platformVersion': '10',
            # 设备明后才能——可以随表填写，但是必须要有
            'deviceName': 'reolink',
            # 被测APP的信息————打开某个APP后输入命令：adb shell dumpsys activity recents | findstr intent
            # cmd上展示的第一行命令：com.android.mediacenter/.PageActivity
            # 包名——代表被测app在设备上的地址
            'appPackage': 'com.mcu.reolink',
            # 入口信息——被测app入口
            'appActivity': 'com.android.bc.MainActivity',
            # 禁止app在自动化后重置
            'noReset': True,
            # 设置命令超时时间,超过后driver会关闭
            'newCommandTimeout': 3600,
            # 指定驱动——UI2,安卓5以下用uiautomator1，以上用uiautomator2
            'automationName': 'UiAutomator2',
            # 支持中文
            'unicodeKeyboard': True,  # 使用 Unicode 输入法
            'resetKeyboard': True,  # 在设定了 `unicodeKeyboard` 关键字的 Unicode 测试结束后，重置输入法到原有状态
        }

        # 启动被测试app,启动之前打开appium server
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)  # 如果访问的是本机就用localhost或127.0.0.1, wd/hub是固定的
        self.driver.implicitly_wait(10)  # 设置隐士等待10s
        # return driver

    def click(self, *locator):
        """
        找到元素，并点击
        :param locator: 定位器
        :return:
        """
        try:
            self.driver.find_element(*locator).click()
        except Exception:
            self.log.error("定位点击元素失败！")

    def click_ele_exist(self, *locator):
        """
        当定为元素出现时，定位元素，并点击
        :param locator: 定位器
        :return:
        """
        try:
            self.driver.find_element(*locator)
            btns = self.driver.find_elements(*locator)
            # 如果出现用户协议弹出按钮
            if btns:
                btns[0].click()
        except Exception:
            self.log.error("定位有时出现的点击元素失败！")

    def input_text(self, value, *locator):
        """
        定位元素，并完成输入
        :param text:
        :param locator:
        :return:
        """
        try:
            self.driver.find_element(*locator).send_keys(str(value))
        except Exception:
            self.log.info("定位输入元素失败！")


    def get_text(self, *locator):
        """
        获取文本元素
        :param locator:
        :return:
        """
        try:
            ele = self.driver.find_element(*locator)
        except Exception:
            self.log.error("获取元素文本失败！")
        else:
            return ele.text

    def getImage(self, image_name):
        """
        生成用例失败的截图,并将截图展示到allure报告中
        :param image_name: 截图的名称
        :return:
        """
        try:
            nowTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            NewPicture = ImagePath + '\\' + nowTime + '_' + image_name + '.png'   # 保存图片为png格式
            self.driver.get_screenshot_as_file(NewPicture)
            allure.attach.file(NewPicture, attachment_type=allure.attachment_type.PNG)  # 将截图作为附件上传到allure测试报告中
        except Exception:
            self.log.error(u'截图失败！')

    def getElements(self, *locator):
        """
        根据某种方式定位到多个元素
        :return:
        """
        try:
            eles = self.driver.find_elements(*locator)
        except Exception:
            self.log.error("定位多个元素失败！")
        else:
            return eles

    def new_swap(self, start_x, start_y, end_x, end_y):
        """
        重新疯转swap()函数
        滑动页面
        :param start_x: 当前位置的横坐标
        :param start_y: 当前位置的竖坐标
        :param end_x: 滑动后位置的横坐标
        :param end_y: 滑动后位置的竖坐标
        :return:
        """
        try:
            self.driver.swap(start_x, start_y, end_x, end_y)
        except Exception:
            self.log.error("滑动页面失败！")

    def new_keyEvent(self, key):
        """
        重新封装keyEvent()函数
        根据不同的键值，来确定系统的操作
        :param key:
        :return:
        """
        try:
            self.driver.keyevent(key)
        except Exception:
            self.log.error("系统键操作失败！")

    def quit(self):
        """
        退出浏览器
        :return:
        """
        try:
            self.driver.quit()
        except Exception:
            self.log.error("退出浏览器失败！")


