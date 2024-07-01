# -*- coding: utf-8 -*-
import os
import subprocess
import console_ctrl
from datetime import datetime
from common_tools.logger import logger


class ScreenRecord:
    def __init__(self):
        self.record_proc = None
        self.v_name = None

    @staticmethod
    def read_shared_v_name():
        try:
            with open("shared_v_name.txt", "r") as f:
                v_name = f.read().strip()
                return v_name
        except FileNotFoundError:
            return None

    def take_screenrecord(self, is_record: bool):
        """
        录屏
        :param is_record: 开启或停止录屏
        :return:
        """
        working_directory = os.path.join(os.getcwd(), 'scrcpy_path')  # 获取scrcpy的路径，让cmd在scrcpy应用程序路径下执行
        logger.info("scrcpy的执行路径： " + working_directory)

        if is_record:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.v_name = f"{timestamp}.mp4"
            screen_record_path = os.path.join(os.getcwd(), 'screen_record')  # 录像的保存路径
            cmd_start_record = f'scrcpy -m 1024 -r --no-audio --record {screen_record_path}\\{self.v_name}'
            cmd_start_ios_record = f't3 screenrecord {screen_record_path}\\{self.v_name}'
            logger.info("这是输出的录像保存路径：" + screen_record_path)

            try:
                from common_tools.app_driver import driver  # 延迟导入，消除循环导入driver产生报错
                platform = driver.get_platform()  # 获取当前被测系统(iOS/Android/web)
                logger.info("录屏开始···")

                if platform == 'android':
                    self.record_proc = subprocess.Popen(
                        cmd_start_record, cwd=working_directory,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                        shell=True
                    )
                    logger.info("输出安卓录像执行命令： " + cmd_start_record)

                elif platform == 'ios':
                    self.record_proc = subprocess.Popen(
                        cmd_start_ios_record,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                        shell=True
                    )
                    logger.info("输出iOS录像执行命令： " + cmd_start_ios_record)
                logger.info("录屏进程已启动")

                # 将 v_name 写入共享文件
                with open("shared_v_name.txt", "w") as f:
                    f.write(self.v_name)

            except Exception as err:
                logger.error("录屏失败，原因可能是：{}".format(err))
                raise err
        else:
            if self.record_proc:
                try:
                    if self.record_proc.poll() is None:
                        console_ctrl.send_ctrl_c(self.record_proc.pid)
                        self.record_proc.wait(timeout=10)  # 等待子进程结束
                        test_name = self.read_shared_v_name()
                        logger.info("录屏结束···")
                        return test_name
                except subprocess.TimeoutExpired:
                    self.record_proc.kill()
                    logger.warning("录屏进程超时，已强制终止")
                self.record_proc = None
            else:
                logger.warning("没有录屏进程正在运行")

        return self.v_name if is_record else None


scr = ScreenRecord()
