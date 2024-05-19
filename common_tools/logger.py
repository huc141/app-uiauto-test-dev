import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os

log_dir = os.path.join(os.getcwd(), 'log')
level = logging.DEBUG

# 创建日志记录文件
logger = logging.getLogger('running_log')
logger.setLevel(level)

# 设置日志输出格式
format_log = logging.Formatter(
    '%(name)s  %(asctime)s %(filename)s[line:%(lineno)d]  %(levelname)s  [%(module)s - %(funcName)s]: %(message)s')

# 创建一个Handler用于将日志写入文件
# when 参数设置为 'midnight'，表示每天的午夜会生成一个新的日志文件。
# interval 参数设置为 1，表示每天生成一个新的日志文件。
# backupCount 参数设置为 7，表示保留最近的 7 个日志文件备份
log_file = os.path.join(log_dir, 'log')
print("log_file: " + log_file)
fh = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
fh.setLevel(level)
fh.setFormatter(format_log)
fh.suffix = "%Y-%m-%d.log"  # 设置日志文件名后缀格式
logger.addHandler(fh)

# 创建一个Handler用于控制台输出日志
ch = logging.StreamHandler()
ch.setLevel(level)
ch.setFormatter(format_log)
logger.addHandler(ch)

"""
控制台日志输出命令：
debug级别的日志：pytest --log-cli-level=debug
info级别的日志：pytest --log-cli-level=info
"""
