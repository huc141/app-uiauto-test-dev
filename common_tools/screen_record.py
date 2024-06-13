# -*- coding: utf-8 -*-
import os
import subprocess
from datetime import datetime
from common_tools.logger import logger


class ScreenRecord:
    def __init__(self):
        self.record_proc = None
        self.v_name = None

    def take_screenrecord(self, is_record: bool):
        """
        录屏
        :param is_record: 开启或停止录屏
        :return:
        """
        working_directory = os.path.abspath('../scrcpy_path')  # 获取scrcpy的路径，让cmd在scrcpy应用程序路径下执行
        print("scrcpy的执行路径： " + working_directory)
        if is_record:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.v_name = f"{timestamp}.mp4"
            screen_record_path = os.path.abspath('../screen_record/')  # 录像的保存路径
            cmd = f'scrcpy -m 1024 -r --no-audio --record {screen_record_path}/{self.v_name}'
            print("这是输出的录像执行命令： " + cmd)
            print("这是输出的录像保存路径：" + screen_record_path)
            try:
                logger.info("录屏开始···")
                self.record_proc = subprocess.Popen(
                    cmd, cwd=working_directory,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True
                )
                logger.info("录屏进程启动")
            except Exception as err:
                logger.error("录屏失败，原因可能是：{}".format(err))
                raise err
        else:
            if self.record_proc:
                self.record_proc.terminate()
                try:
                    stdout, stderr = self.record_proc.communicate(timeout=10)  # 等待子进程结束
                    if self.record_proc.returncode != 0:
                        logger.error(f"录屏停止失败，原因可能是：{stderr.decode()}")
                        raise Exception(stderr.decode())
                    logger.info("录屏结束···")
                except subprocess.TimeoutExpired:
                    self.record_proc.kill()
                    logger.warning("录屏进程超时，已强制终止")
                self.record_proc = None
            else:
                logger.warning("没有录屏进程正在运行")

        return self.v_name if is_record else None


scr = ScreenRecord()
