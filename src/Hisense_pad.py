#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
    一、项目名称：海信平板自动化
    二、涵盖测试模块：
        脚本流程：PPT播放25分钟---视频播放20分钟---待机10分钟（循环）
        
'''

from common.models import Glocalme, G4S
from config import settings
import subprocess, time
import uiautomator2 as u2
from appium import webdriver

def main():
    # uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
    # device = PyQt_Glocalme()
    d = u2.connect()
    d.press("home")
    # 杀掉所有后台程序
    d(resourceId="com.android.systemui:id/recent_apps").click()
    d(resourceId="com.hmct.recents:id/fallback_clear_all").click()
    # 打开文件管理
    # device.start_activity(package_name='com.hmct.FileManager.Activity', activity=".FileManagerTab")
    d.app_start(package_name='com.hmct.FileManager.Activity')
    # 点击进入文档
    d(resourceId="com.hmct.FileManager.Activity:id/category_document").click()
    d(resourceId="com.hmct.FileManager.Activity:id/title", text="终端测试部项目测试人力规划（2019年下半年）.pptx").click()
    d(resourceId="cn.wps.moffice_eng:id/ppt_menuitem_text", text="播放").click()
    d(resourceId="cn.wps.moffice_eng:drawable/public_play_autoplay").click()


if __name__ == '__main__':
    # d = u2.connect()
    # d.press("home")
    # print(d.app_current())
    # main()
    g4s = G4S()
    g4s.root()
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.1.0',
        'appPackage': 'com.android.settings',
        'appActivity': 'com.android.settings.Settings',
        'newCommandTimeout': '360',
        'deviceName': '11c9b534',
        'noReset': False,
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(3)
    # driver.press_keycode(3)
    # time.sleep(3)
    # driver.start_activity(app_package='com.glocalme.g4home', app_activity='com.glocalme.basic.simcard.SimCardActivity')
    driver.start_activity(app_package='com.glocalme.g4home', app_activity='com.glocalme.basic.simcardmanager.SimCardActivityG4P')
    sim_status = driver.find_element_by_id("com.glocalme.g4home:id/st_sim_net").text
    print(sim_status)
