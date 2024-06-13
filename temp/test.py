# -*- coding: utf-8 -*-
import os

path = '../screen_record/'

abs_path = os.path.join(os.getcwd(), 'scrcpy_path')
print("scrcpy的执行路径： " + abs_path)

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
