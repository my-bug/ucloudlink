#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

import logging
import os.path
import time

BASEDIR = os.path.dirname(os.path.dirname(__file__))
level_list = ['logging.DEBUG', 'logging.INFO', 'logging.WARNING ', 'logging.ERROR', 'logging.CRITICAL']
class Logger:
    def __init__(self, file_output=True, screen_output=False, log_level=None, log_file=None):
        self.file_output = file_output
        self.screen_output = screen_output
        self.log_level = log_level
        if self.log_level:
            if not isinstance(self.log_level, str):
                raise TypeError("log_level is not str")
            if self.log_level not in level_list:
                raise ValueError('log_levle must be one of the following lists:%s' % level_list)
            self._log_level = eval(self.log_level)
        else:
            self._log_level = logging.DEBUG
        self.log_file = log_file
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    def createFileHandler(self):
        if self.log_file:
            log_name = self.log_file
        else:
            # 定义日志输出路径
            log_path = '/'.join([BASEDIR, 'logs', time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))])
            log_name = '.'.join([log_path, 'log'])
        # 创建日志文件输出对象
        fh = logging.FileHandler(log_name, mode='w')
        # 定义日志文件的输出格式
        fh.setFormatter(self.formatter)
        return fh

    def createScreenHandler(self):
        # 创建日志屏幕输出对象
        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        return ch

    def create_logger(self):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(self._log_level)
        if self.file_output and self.screen_output:
            fh = self.createFileHandler()
            ch = self.createScreenHandler()
            logger.addHandler(fh)
            logger.addHandler(ch)
        elif self.file_output==True and self.screen_output==False:
            fh = self.createFileHandler()
            logger.addHandler(fh)
        elif self.file_output==False and self.screen_output==True:
            ch = self.createScreenHandler()
            logger.addHandler(ch)
        else:
            raise Exception('One of the parameters "file_outpue" and "screen_output" must be True.')
        return logger
