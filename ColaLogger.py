import os
import logging
import ColoryChar as ccc


class ColaLogger(logging.Logger):
    def __init__(self, name: str, log_dir="./ColaLog", is_just_info=False) -> None:
        super().__init__(name)

        self.dir_log = log_dir
        if not os.path.exists(self.dir_log):
            os.makedirs(self.dir_log)

        self.level = logging.DEBUG
        self.setLevel(self.level)

        # 日志文件
        self.name_log = "log_cola_{}".format(name)
        self.path_log = os.path.join(self.dir_log, self.name_log)
        self.handler = logging.FileHandler(self.path_log)
        self.handler.setLevel(self.level)

        # 日志输出格式
        if is_just_info:
            self.formatter = logging.Formatter("%(asctime)s:%(message)s")
        else:
            self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - ' + ccc.colory("%(message)s", ccc.RED))
        self.handler.setFormatter(self.formatter)

        self.addHandler(self.handler)

    def info(self, msg, is_print=False) -> None:
        if is_print:
            print(msg)
        return super().info(msg)

if __name__ == "__main__":
    logger = ColaLogger("实验测试")
    logger.debug("Cola debug.")
    logger.info("Cola info.")

"""
python ColaLogger.py
"""