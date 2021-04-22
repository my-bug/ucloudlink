#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
    一、项目名称：S1 S13手机模式下的自动化测试
    二、定制文件：无
    三、涵盖测试模块：
        1、FOTA
'''

import pytest, subprocess, time, os, allure, sys, random
# 获取项目路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASEDIR)
from common import models, logger
from common.ui_operation import G4S_uiOpration
from config import settings, U3_settings
from config.config import global_config
import uiautomator2 as u2
from pywinauto import application
# from openpyxl import xw.Book
import xlwings as xw

# 启动切口工具
subprocess.getstatusoutput(" ".join(["start", settings.Qualcomm_SwitchCom_file]))

# 获取项目名称
project_name = os.path.basename(__file__).split('.')[0]
# 创建log对象
log_name = '.'.join(['_'.join([project_name, time.strftime('%Y%m%d%H%M%S', time.localtime())]), "log"])
log_file = os.path.join(BASEDIR, "logs", log_name)
log = logger.Logger(screen_output=True, log_level='logging.INFO', log_file=log_file).create_logger()

@allure.feature("FOTA")
class Test_Fota:
    def setup_class(self):
        log.info("-" * 20 + "Start Test_Fota" + "-" * 20)
        # 测试截图、视频的保存路径；如果不存在此路径，就创建此路径
        self.test_record_path = '/'.join([BASEDIR, 'TestRecord', project_name, "Test_Fota"])
        if not os.path.exists(self.test_record_path):
            os.makedirs(self.test_record_path)

        # 初始化信息
        self.serialno = global_config.getRaw("S1_S13", "serialno")
        self.source_version = global_config.getRaw("S1_S13", "source_version")
        self.target_version = global_config.getRaw("S1_S13", "target_version")
        self.s1 = models.Glocalme(device_id=self.serialno, log_project=log)
        self.s1.wait_device_connect()
        self.s1.wakey()  # 设置屏幕常亮
        # 执行uiautomator2的init操作，在测试设备端安装uiautomator app，minicap和minitouch，atx-agent
        uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
        self.s1_d = u2.connect(self.serialno)

        # self.g4s_uiOpration = G4S_uiOpration(g4s=self.g4s, d=self.g4s_d, log_project=log)

        # 切换系统语言为中文
        # self.g4s_uiOpration.switch_language(language="中文简体")

        # 打开USB debug模式
        # self.g4s_uiOpration.enable_test_mode()

        self.version = self.s1.get_current_version()  # 获取测试设备的版本
        self.test_result_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'TestResult', project_name)
        if not os.path.exists(self.test_result_path):
            os.makedirs(self.test_result_path)  # 创建测试结果文件夹，并以测试版本命名
        self.test_result_file_path = os.path.join(self.test_result_path, '.'.join([self.version, 'xlsx']))  # 创建一个以测试版本号命名的Excel表
        self.app = xw.App(visible=False, add_book=False)
        # 打开测试用例表
        self.wb = self.app.books.open(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', 'S1_S13自动化测试用例.xlsx'))
        # self.ws = self.wb.active  # 激活表
        self.ws1 = self.wb.sheets['fota']  # 选择表

        # if self.g4s_d(resourceId="com.glocalme.g4home:id/tv_unlock").exists():
        #     self.g4s_d.swipe(0.5, 0.8, 0.5, 0.3, 0.1)


    def setup(self):
        self.s1.wait_network_connect()
        current_version = self.s1.get_current_version()
        if current_version != self.source_version:
            pass

    def test01(self):
        '''测试用例：云卡网络-开机检测'''
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.s1.root()
        self.s1_d.press("home")
        login_type = self.s1.login_type()
        if login_type == 0:
            self.s1_uiOpration.switch_network_to_cloudSIM()
            time.sleep(5)
        self.s1.reboot()
        self.s1.wait_device_connect()
        self.s1.wakey()
        self.s1.wait_network_connect()
        check_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_new_version").exists(timeout=180))
        if check_result:
            self.ws1["F2"].value = "PASS"
        else:
            self.ws1["F2"].value = "FAIL"

    def test02(self):
        """测试用例：云卡网络-周期检测"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 0:
            self.g4s_uiOpration.switch_network_to_cloudSIM()
            time.sleep(5)
        self.g4s.wait_network_connect()
        # 取iport日志，确认下个检测周期时间点
        iportLog_file = self.g4s.pull_iportLog(target_path=self.test_record_path)
        next_check_time = self.g4s.next_check_time(iportLog_file=iportLog_file)
        # 将下次周期检测的时间转换为时间戳
        next_check_timestamp = next_check_time[1]
        # 系统时间设置为下个周期检测时间点前两分钟
        set_system_timestamp = next_check_timestamp - 120
        self.g4s.set_system_time(timestamp=set_system_timestamp)
        time.sleep(120)
        circle_check_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_new_version").exists(timeout=180))
        if circle_check_result:
            self.ws1["F3"].value = "PASS"
        else:
            self.ws1["F3"].value = "FAIL"

    def test03(self):
        """测试用例：云卡网络-手动下载"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 0:
            self.g4s_uiOpration.switch_network_to_cloudSIM()
            time.sleep(5)
        self.g4s.wait_network_connect()
        self.g4s.start_activity(package_name="com.abupdate.fota_demo_iot", activity="com.abupdate.fota_demo_iot.view.activity.MainActivity")
        if self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="下载").exists(30):
            self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="下载").click()
        download_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").exists(timeout=360))
        if download_result:
            self.ws1["F4"].value = "PASS"
        else:
            self.ws1["F4"].value = "FAIL"
        # if self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail").exists():
        #     self.g4s.wait_device_disconnect()

    def test04(self):
        """测试用例：云卡网络-手动升级"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        if self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").exists():
            self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").click()
            self.g4s.wait_device_disconnect()
            self.g4s.wait_device_connect(timeout=480)
            self.g4s.wait_network_connect()
            upgraded_version = self.g4s.get_current_version()
            upgrade_result = pytest.assume(upgraded_version == self.target_version)
            if upgrade_result:
                self.ws1["F5"].value = "PASS"
            else:
                self.ws1["F5"].value = "FAIL"
        else:
            assert False

    def test05(self):
        '''测试用例：实体卡网络-开机检测'''
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 1:
            self.g4s_uiOpration.switch_network_to_SIM()
            time.sleep(5)
        self.g4s.reboot()
        self.g4s.wait_device_connect()
        # self.g4s.wakey()
        self.g4s.wait_network_connect()
        check_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_new_version").exists(timeout=180))
        if check_result:
            self.ws1["F6"].value = "PASS"
        else:
            self.ws1["F6"].value = "FAIL"

    def test06(self):
        """测试用例：实体卡网络-周期检测"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 1:
            self.g4s_uiOpration.switch_network_to_SIM()
            time.sleep(5)
        self.g4s.wait_network_connect()
        # 取iport日志，确认下个检测周期时间点
        iportLog_file = self.g4s.pull_iportLog(target_path=self.test_record_path)
        next_check_time = self.g4s.next_check_time(iportLog_file=iportLog_file)
        # 将下次周期检测的时间转换为时间戳
        next_check_timestamp = next_check_time[1]
        # 系统时间设置为下个周期检测时间点前两分钟
        set_system_timestamp = next_check_timestamp - 120
        self.g4s.set_system_time(timestamp=set_system_timestamp)
        time.sleep(120)
        circle_check_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_new_version").exists(timeout=180))
        if circle_check_result:
            self.ws1["F7"].value = "PASS"
        else:
            self.ws1["F7"].value = "FAIL"

    def test07(self):
        """测试用例：实体卡网络-手动下载"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 1:
            self.g4s_uiOpration.switch_network_to_SIM()
            time.sleep(5)
        self.g4s.wait_network_connect()
        self.g4s.start_activity(package_name="com.abupdate.fota_demo_iot", activity="com.abupdate.fota_demo_iot.view.activity.MainActivity")
        if self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="下载").exists(30):
            self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="下载").click()
        download_result = pytest.assume(self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").exists(timeout=360))
        if download_result:
            self.ws1["F8"].value = "PASS"
        else:
            self.ws1["F8"].value = "FAIL"

    def test08(self):
        """测试用例：实体卡网络-手动升级"""
        log.info("start %s" % sys._getframe().f_code.co_name)
        if self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").exists():
            self.g4s_d(resourceId="com.abupdate.fota_demo_iot:id/tv_update_state_detail", text="点击升级").click()
            self.g4s.wait_device_disconnect()
            self.g4s.wait_device_connect(timeout=480)
            self.g4s.wait_network_connect()
            upgraded_version = self.g4s.get_current_version()
            upgrade_result = pytest.assume(upgraded_version == self.target_version)
            if upgrade_result:
                self.ws1["F5"].value = "PASS"
            else:
                self.ws1["F5"].value = "FAIL"
        else:
            assert False

    def teardown(self):
        # 每条case执行结束保存一下测试结果表
        self.wb.save(self.test_result_file_path)

    def teardown_class(self):
        self.wb.close()
        self.app.quit()
        log.info("-" * 20 + "End Test_Fota" + "-" * 20)
