# 获取预期结果 test_data["expected"]
# 断言
# 如果出现断言失败，需要将失败的用例记录到logger当中
# 如果断言失败，会抛出一个异常，AssertionError
# 如果不手动抛出异常，程序正常走不是走try就是except分支，测试用例都会全部显示通过；
# 抛出异常就意味着程序运行错误，这条用例执行失败
try:
    print(res["msg"])
    self.assertEqual(test_data["expected"], res["code"])
    # 把实际结果写入excel数据，通过case_id获取行号
    self.excel_handler.write(config.data_path,
                             "register",
                             test_data["case_id"] + 1,
                             9,
                             "测试通过")
except AssertionError as e:  # 如果出现错误，就会执行except的代码
    # 记录日志logger
    self.logger.error("测试用例失败：{}".format(e))
    # 把实际结果写入excel数据，通过case_id获取行号
    self.excel_handler.write(config.data_path,
                             "register",
                             test_data["case_id"] + 1,
                             9,
                             "测试失败")
    raise e  # 程序运行错误，抛出异常，就意味着这条用例执行失败
