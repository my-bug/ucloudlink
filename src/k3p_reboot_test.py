#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''
from common.logger import Logger
from common.models import Glocalme
import os, time, subprocess

BASEDIR = os.path.dirname(os.path.dirname(__file__))
# 获取项目名称
project_name = os.path.basename(__file__).split('.')[0]
# 创建log对象
log_name = '.'.join(['_'.join([project_name, time.strftime('%Y%m%d%H%M%S', time.localtime())]), "log"])
log_file = os.path.join(BASEDIR, "logs", log_name)
log = Logger(screen_output=True, log_level='logging.INFO', log_file=log_file).create_logger()

def reboot():
    k3p = Glocalme()
    for i in range(400):
        log.info('第%d次重启' % (i+1))
        current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        k3p.reboot()
        k3p.wait_device_disconnect()
        time.sleep(3)
        k3p.wait_device_connect()
        k3p.wakey()
        logcat_file = '\\'.join(['F:\\logcat', '.'.join([current_time, 'log'])])
        os.system(' '.join(["adb logcat -b all -v time >> ", logcat_file]))
        time.sleep(30)
        while not k3p.connect_network():
            pid = k3p.get_pid(process_name="hostapd")
            log.info(pid)
            if not pid:
                log.error("pid is null.")
                time.sleep(2)
                continue
            time.sleep(2)

        start = time.time()
        expire = start + 60
        while start < expire:
            pid = k3p.get_pid(process_name="hostapd")
            log.info(pid)
            if not pid:
                log.error("pid is null.")
                time.sleep(1)
                start = time.time()
                expire = start + 60
                continue
            time.sleep(2)
            start = time.time()

if __name__ == '__main__':
    reboot()
