import os
import logging

from logging import handlers

from common.helper import time_without_hour, get_execution



__author__ = "Jackey"



class Logger:

    levels = {
        "debug":logging.DEBUG,
        "info":logging.INFO,
        "warning":logging.WARNING,
        "error":logging.ERROR,
        "crit":logging.CRITICAL
    }

    def __init__(self, filename, level="info", count=3, 
                    format_type="[%(asctime)s][%(levelname)s] %(message)s"):
        self.logger = logging.getLogger(filename)
        # 设置log的等级
        self.logger.setLevel(self.levels.get(level))
        self.filename = filename
        self.count = count
        # 设置log的格式
        self.formatter = logging.Formatter(format_type)
        self.init_stream_handler()
        self.init_file_handler()

    def init_stream_handler(self):
        """cmd显示log打印"""
        shandler = logging.StreamHandler()
        # 将log格式同步到cmd显示
        shandler.setFormatter(self.formatter)
        self.logger.addHandler(shandler)

    def init_file_handler(self):
        """将log写入到log文件中""" 
        # backupCount: 当log文件数量大于count时, 就开始删除
        handler = handlers.TimedRotatingFileHandler(self.filename, backupCount=self.count, encoding="utf-8")
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)



filename = os.path.join(get_execution(), "%s.log" % time_without_hour())
logger = Logger(filename).logger