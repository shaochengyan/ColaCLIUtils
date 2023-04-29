import os
import logging
import datetime
import utils.ColoryChar as ccc

class ColaMarkdownLogger:
    def __init__(self, name:str, dir_log="./ColaLog") -> None:
        time_today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.filename = os.path.join(
            dir_log, "log_{}_{}.md".format(name, time_today)
        )
    
    def log(self, key, value):
        """
        不需要一直保存，否则意外退出才能保存好文件
        """
        message = "**{}**: {}\n\n".format(key, value)
        with open(self.filename, "a") as fp:
            fp.write(message)


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
    if False:
        logger = ColaLogger("实验测试")
        logger.debug("Cola debug.")
        logger.info("Cola info.")
    
    if True:
        logger = ColaMarkdownLogger("test")
        logger.log("cola", "你好")
        logger.log("gpt", "您好")

"""
python -m utils.ColaLogger
"""