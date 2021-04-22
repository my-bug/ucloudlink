#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

import os, time

# 获取项目路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(BASEDIR)

VERSION_01 = 'G4S18_TSV1.4.001.014.190923_204454'
VERSION_02 = 'G4S18_TSV1.4.001.015.191231_180211'
VERSION_03 = 'G4S18_T_TSV1.4.001.015.200102_142119'
LOCAL_UPGRADE_PACKAGE = os.path.join(BASEDIR, 'upgradePackage', 'FOTA_U2sS18_TSV2.0.001.009.200212_153610_user.zip')
U3_LOCAL_UPGRADE_PACKAGE = os.path.join(BASEDIR, 'upgradePackage', 'FOTATEST_U3Q19_TSV3.2.004.003.200226_172621_user.zip')
G4S_LOCAL_UPGRADE_PACKAGE = os.path.join(BASEDIR, 'upgradePackage', 'FOTATEST_G4SQ19_TSV3.1.003.036.200312_102909_user.zip')

# root权限apk路径
G4S_ROOT_APK_FILE = os.path.join(BASEDIR, 'application', 'UklFactory.apk')

# appium自动化测试需要安装的apk
APPIUM_APK_FILE = os.path.join(BASEDIR, 'application', 'appium_settings.apk')
UIAUTOMATOR2_APK_FILE_01 = os.path.join(BASEDIR, 'application', 'appium.uiautomator2.server.apk')
UIAUTOMATOR2_APK_FILE_02 = os.path.join(BASEDIR, 'application', 'appium-uiautomator2-server-debug-androidTest.apk')
GC00_APK_FILE = os.path.join(BASEDIR, 'application', 'applicationGC00_TSV3.2.001.999.0703_defaultFlavor_sprd_persistent_2999.apk')

# uiautomator2自动化测试需要安装的apk和文件
APPUIAUTOMATOR_APK_FILE = os.path.join(BASEDIR, 'application', 'uiautomator2', 'app-uiautomator.apk')
APPUIAUTOMATORTEST_APK_FILE = os.path.join(BASEDIR, 'application', 'uiautomator2', 'app-uiautomator-test.apk')
atx_file = os.path.join(BASEDIR, 'application', 'uiautomator2', 'atx-agent')
minicap_file = os.path.join(BASEDIR, 'application', 'uiautomator2', 'minicap')
minicap_so_file = os.path.join(BASEDIR, 'application', 'uiautomator2', 'minicap.so')
minitouch_file = os.path.join(BASEDIR, 'application', 'uiautomator2', 'minitouch')



# 测试设备连接是wifi信息
WIFI_SSID = "James"
WIFI_PWD = "55667788"

# 测试用例代码存放路径（用于构建suite,注意该文件夹下的文件都应该以test开头命名）
test_case_path = BASEDIR+"\\src\\test_case"

# print u'日志路径：'+log_path
# 测试报告存储路径，并以当前时间作为报告名称前缀
report_path = BASEDIR+"\\report\\"
report_name = report_path+time.strftime('%Y%m%d%H%M%S', time.localtime())

# 设置发送测试报告的公共邮箱、用户名和密码
smtp_sever = 'smtp.ukelink.com'  # 邮箱SMTP服务，各大运营商的smtp服务可以在网上找，然后可以在foxmail这些工具中验正
email_name = "xuhong@ukelink.com"  # 发件人名称
email_password = "520@lixianghe"  # 发件人登录密码
# email_To = 'xuhong@ukelink.com;fanweigang@ukelink.com;guoge@ukelink.com;wuqingdao@ukelink.com;lvpeifang@ukelink.com;heguifeng@ukelink.com'  # 收件人
email_To = 'xuhong@ukelink.com'  # 收件人

# 高通切口工具路径
Qualcomm_SwitchCom_file = os.path.join(BASEDIR, 'config', 'kit', 'Qualcomm_Switch_Com.exe')

# 迅捷录屏大师APK路径
xunjielupingdashi_apk_file = os.path.join(BASEDIR, 'application', 'com.jy.recorder_1.8.5_185.apk')


if __name__ == '__main__':
    print(Qualcomm_SwitchCom_file)
    # cmd = " ".join(["start", Qualcomm_SwitchCom_file])
    # import subprocess
    # subprocess.getstatusoutput(cmd)
