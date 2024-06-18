# -*- coding: utf-8 -*-
import os
from os.path import exists

from common_tools.logger import logger

path = '../screen_record/'

abs_path = os.path.join(os.getcwd(), 'scrcpy_path')
print("scrcpy的执行路径： " + abs_path)


v_name = "1111111.mp4"
screen_record_path = os.path.join(os.getcwd(), 'screen_record')  # 录像的保存路径
cmd = f'scrcpy -m 1024 -r --no-audio --record {screen_record_path}/{v_name}'
print("这是输出的录像执行命令： " + cmd)
print("这是输出的录像保存路径：" + screen_record_path)

getcwd = os.getcwd()
print(getcwd)


v_name = '2020202.mp4'
screen_record_path = os.path.join(os.getcwd(), 'screen_record')
print("录像的保存路径: " + screen_record_path)

cmd = f'scrcpy -m 1024 -r --no-audio --record {screen_record_path}\\{v_name}'

print("cmd: " + cmd)


# path2 = '../screen_record/'
# content = os.listdir(abs_path)
# print(content)
