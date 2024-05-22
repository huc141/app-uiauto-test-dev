# -*- coding: utf-8 -*-
import os
import time
import pytest

# 运行pytest测试框架的主函数
if __name__ == '__main__':
    """
    参数说明：
        "-s": 这个标志告诉pytest不捕获标准输出和标准错误流，使得在运行测试时可以直接看到打印信息。
        "./test_case": 指定测试用例的路径。这里的"."表示当前目录，pytest会递归查找当前test_case目录下所有的测试用例（通常是以_test.py结尾的文件）并执行它们。
            "./test_case/test_welcome.py"：执行该目录下的test_welcome.py文件
        "--capture=sys": 配置pytest的输出捕获模式为"sys"，意味着它会按照系统的默认行为来捕获输出，这与-s的作用有些相反，但在这里可能是为了确保某些特定的输出行为。通常，如果希望看到全部输出，仅使用-s就足够了。
        
        
        ./report_allure_temps 临时的json格式报告的路径
        -o 输出output
        ./reports 生成的allure报告的路径
        –clean 清空./reports路径原来的报告
    """
    pytest.main(["-s", "./test_case/test_welcome.py", "--capture=sys"])

    # 调用allure生成报告
    os.system("allure generate ./report_allure_temps -o ./reports/{}.html --clean".format(time.strftime("%Y%m%d-%H%M%S")))

