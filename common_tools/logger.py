import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os


class Logger:
    def __init__(self, name: str = 'data', level=logging.INFO) -> None:
        self._name = name
        os.chdir("..")  # 注意：修改pycharm运行配置后，注销该行代码。
        self._log_dir = os.path.join(os.getcwd(), 'log')
        print(self._log_dir)
        self._level = level
        self.here = os.path.abspath(os.path.dirname(__file__))

    # def get_time_by_fmt(self, fmt: str = '%Y-%m-%d', dt: str = time.localtime()) -> str:
    #     return time.strftime(fmt, dt)
    #
    # p = os.path.join(get_time_by_fmt('%Y%m%d'), 'runtime.log')
    # print(p)

    def setup_logging(self):
        # 创建日志记录器
        logger = logging.getLogger()
        logger.setLevel(self._level)

        # 设置日志输出格式
        # format_log = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        format_log = logging.Formatter('%(name)s  %(asctime)s %(filename)s[line:%(lineno)d]  %(levelname)s  [%(module)s - %(funcName)s]: %(message)s')

        # 创建一个Handler用于将日志写入文件
        # fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        # when 参数设置为 'midnight'，表示每天的午夜会生成一个新的日志文件。
        # interval 参数设置为 1，表示每天生成一个新的日志文件。
        # backupCount 参数设置为 7，表示保留最近的 7 个日志文件备份
        log_file = os.path.join(self._log_dir, 'running_log')
        fh = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        fh.setLevel(self._level)
        fh.setFormatter(format_log)
        fh.suffix = "%Y-%m-%d.log"  # 设置日志文件名后缀格式
        logger.addHandler(fh)

        # 创建一个Handler用于控制台输出日志
        ch = logging.StreamHandler()
        ch.setLevel(self._level)
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
