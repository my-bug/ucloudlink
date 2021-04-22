#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

'''
参数详解：
    1、platformName:设备系统（指的是用的那种平台系统，如Android、iOS、orFirefoxOS）

    2、platformVersion:指平台系统的版本
    
    3、deviceName:设备名称，指启动的那个设备
    
    4、appActivity:待测app的activity的名字
    
    5、appPackage:待测app的包名
    
    6、noReset:在此会话之前要不要重制应用状态
    
    7、unicodeKeyboard:启动软键盘输入，默认flase
    
    8、appWaitActivity:活动名称/名称，逗号分隔，您想要等待的Android活动（SplashActivity，SplashActivity,OtherActivity）
    
    9、appWaitPackage:您想等待的Android应用程序的app包
    
    10、appWaitDuration:用于等待appWaitActivity启动的超时（以毫秒为单位20000）（默认）
'''

G4S_CONFIG = {
    'platformName': 'Android',
    'platformVersion': '8.1.0',
    'appPackage': 'com.android.settings',
    'appActivity': 'com.android.settings.Settings',
    'newCommandTimeout': '360',
    'deviceName': '11c9b534',
    'noReset': False
}
