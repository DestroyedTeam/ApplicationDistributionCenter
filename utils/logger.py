import os
from datetime import datetime

from loguru import logger as loguru_logger

from ApplicationDistributionCenter import settings


class CustomLogger:
    def __init__(self):
        self.log_cache = []
        self.project_name = settings.BASE_DIR.name
        self.log_dir = os.path.abspath(settings.LOG_DIR)
        self.log_file = self.get_log_file()
        self.configure_logger()

    def get_log_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        file_prefix, log_dir = self.project_name, self.log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"{file_prefix}.log")
        if os.path.exists(log_file):
            file_creation_date = datetime.fromtimestamp(os.path.getctime(log_file)).strftime("%Y-%m-%d")
            if file_creation_date != today:
                new_log_file = os.path.join(log_dir, f"{file_prefix}:{file_creation_date}.log")
                os.rename(log_file, new_log_file)
        return log_file

    def configure_logger(self):
        log_format = "[{time:DD-MMM-YYYY HH:mm:ss}] | {level} | {name}:{function}:{line} - {message}"
        # 配置文件输出，按大小（3MB）和日期分隔
        loguru_logger.add(
            self.log_file,
            rotation="10 MB",
            retention="10 days",
            level="DEBUG",
            colorize=True,
            format=log_format,
            delay=True,
        )

    @staticmethod
    def log(level, message):
        # 非本文件调用需要额外将日志输出到控制台
        loguru_logger.opt(depth=2, colors=True).log(level, message)

    def debug(self, message):
        self.log("DEBUG", message)
        return self

    def info(self, message):
        self.log("INFO", message)
        return self

    def warning(self, message):
        self.log("WARNING", message)
        return self

    def error(self, message):
        self.log("ERROR", message)
        return self

    def critical(self, message):
        self.log("CRITICAL", message)
        return self


# 创建 CustomLogger 实例
logger = CustomLogger()

# 使用示例
if __name__ == "__main__":
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
    logger.critical("This is a critical message.")
