class AssertUtil:

    def __init__(self, assert_type, assert_text, expected_text=None):
        self.assert_type = assert_type
        self.assert_text = assert_text
        self.expected_text = expected_text

    def text_assert(self):
        """
        检查expected_text是否存在于text中
        使用Python内置的count方法计算text中expected_text出现的次数
        如果expected_text在text中出现，那么其出现次数应大于0
        如果expected_text不在text中，断言将失败，并抛出一个AssertionError异常。异常的错误消息将包含期望的文本和实际的文本。
        """
        if self.expected_text is not None:
            if self.assert_type == 'assert_text_in':
                assert self.assert_text.count(
                    self.expected_text) > 0, f"Expected text '{self.expected_text}' not found in '{self.assert_text}'"

                print("Test passed successfully!!")
            elif self.assert_type == 'assert_equal':
                assert self.assert_text == self.expected_text, "实际值{}与期望值{}不相等".format(self.assert_text,
                                                                                                 self.expected_text)
                print("Test passed successfully!")
            else:
                print("expected_text值不为空时，assert_type类型{}有误".format(self.assert_type))

        elif self.assert_type == 'assert_not_none':
            assert self.assert_text, '期望值{}是None'.find(self.assert_text)
        else:
            print("expected_text值为空时，assert_type类型{}有误".format(self.assert_type))


a = "assert_text_in"
b = "hello world"
c = "hello"

d = AssertUtil(a, b, c)
d.text_assert()
