import os

path = '../screen_record/'

abs_path = os.path.abspath('../scrcpy_path')
print(abs_path)

getcwd = os.getcwd()
print(getcwd)

log_dir = os.path.join('common_tools', 'log')
print("log_dir: " + log_dir)

path2 = '../screen_record/'
content = os.listdir(abs_path)
print(content)
