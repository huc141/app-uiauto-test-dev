# -*- coding: utf-8 -*-
import os
import pytest

# 运行pytest测试框架的主函数
if __name__ == '__main__':
    pytest.main()
    # 调用allure生成报告
    os.system("allure generate ./report_allure_temps -o ./reports --clean")
