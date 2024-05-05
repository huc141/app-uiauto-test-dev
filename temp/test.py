
DEFAULT_SECONDS = 10


class BasePage(object):
    """
    第一层：对uiAutomator2进行二次封装，定义一个所有页面都继承的BasePage
    封装uiAutomator2基本方法，如：元素定位，元素等待，导航页面等
    不需要全部封装，用到多少就封装多少
    """

    def __init__(self, device):
        self.d = device

    def by_id(self, id_name):
        """通过id定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(resourceId=id_name)
        except Exception as e:
            print("页面中没有找到id为%s的元素" % id_name)
            raise e