import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os


class Logger:
    def __init__(self, name: str = 'data', log_dir: str = None, level: str = 'logging.INFO') -> None:
        self._name = name
        self._log_dir = log_dir
        self._level = level

    # def get_time_by_fmt(self, fmt: str = '%Y-%m-%d', dt: str = time.localtime()) -> str:
    #     return time.strftime(fmt, dt)
    #
    # p = os.path.join(get_time_by_fmt('%Y%m%d'), 'runtime.log')
    # print(p)

    def setup_logging(self, log_file='./log.txt', log_level=''):
        # 创建日志记录器
        logger = logging.getLogger()
        logger.setLevel(log_level)

        # 设置日志输出格式
        format_log = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        # 创建一个Handler用于将日志写入文件
        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(log_level)
        fh.setFormatter(format_log)
        logger.addHandler(fh)

        # 创建一个Handler用于控制台输出日志
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(format_log)
        logger.addHandler(ch)


# 使用示例
if __name__ == "__main__":
    log = Logger()
    log.setup_logging()
    logging.debug('Debug message')
    logging.info('Info message')
    logging.warning('Warning message')
    logging.error('Error message')
    logging.critical('Critical message')
