#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

import uiautomator2 as u2
from config import U3_settings
from common.models import Glocalme, G4S
import os, subprocess
import sys, time, re

# last_check_time = res[-1]
# print(last_check_time)

# if "setAlarm() start time" in line:
#     print(line)

# print(time.mktime(time.strptime()))
# d = u2.connect()

g4 = Glocalme()
g4.wait_network_connect()
# print(g4.wifi_info())
# g4.wakey()
# g4.root_by_at()
# g4.start_activity(package_name='com.glocalme.g4home', activity='com.glocalme.basic.simcard.SimCardActivity')

# g4.local_update(upgradePackage_file="E:\\2-version\\G4\\FOTA_G4S18_TSV1.4.001.016.210129_104718_user.zip")
# g4.root_by_at()
# g4.start_activity(package_name='com.glocalme.g4home', activity='com.glocalme.basic.simcard.SimCardActivity')
# g4.wait_network_connect()
# g4.wait_device_disconnect()
# g4.root_by_at()
# g4.start_activity(package_name='com.glocalme.g4home', activity='com.glocalme.basic.simcard.SimCardActivity')
# g4.wakey()
# g4.root_by_at()
# print(d.info)
# print(d.app_current())

# package_name='com.glocalme.g4home'
# activity='com.glocalme.launcher.launcher.LauncherActivity'
# 更多界面{'package': 'com.glocalme.g4home', 'activity': 'com.glocalme.basic.more.MoreActivity'}
# g4.start_activity(package_name, activity)