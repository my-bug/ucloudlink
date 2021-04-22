#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
    一、项目名称：G4S项目自动化测试
    二、定制文件：GCBU个人版
    三、涵盖测试模块：
        1、云卡和实体卡切换
        2、Flash
        3、显示
        4、加入云卡后的稳定性
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

# def screenShot(d, title):
#     '''
#     在uiautomator2的截图函数上封装的截图方法
#     :param
#         d:uiautomator2对象
#         title: 自定义截图的名称
#     :return: 返回截图的路径
#     '''
#     screenShot_file = '/'.join([test_record_path, '.'.join([title, 'png'])])
#     d.screenshot(screenShot_file)
#     return screenShot_file
#
# def pull_ScreenRecord(d, title):
#     list = d.adb_shell('ls /sdcard/ScreenRecord/record/')
#     ScreenRecord_list = list.strip().split('\n')
#     file = '/'.join(['/sdcard/ScreenRecord/record', ScreenRecord_list[-1]])
#     save_file = '/'.join([test_record_path, '.'.join([title, 'mp4'])])
#     d.pull(src=file, dst=save_file)
#     return save_file

class Test_Flash:
    def setup_class(self):
        log.info("-" * 20 + "Start Test_Flash" + "-" * 20)
        # 初始化信息
        self.serialno = global_config.getRaw("config-G4S", "serialno")
        self.g4s = models.G4S(device_id=self.serialno, log_project=log)
        self.g4s.wait_device_connect()
        self.g4s.wakey()  # 设置辅助机屏幕常亮
        # 执行uiautomator2的init操作，在测试设备端安装uiautomator app，minicap和minitouch，atx-agent
        # uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
        # self.g4s_d = u2.connect(self.serialno)

        self.version = self.g4s.get_current_version()  # 获取测试设备的版本
        self.test_result_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'TestResult', project_name)
        if not os.path.exists(self.test_result_path):
            os.makedirs(self.test_result_path)  # 创建测试结果文件夹，并以测试版本命名
        self.test_result_file_path = os.path.join(self.test_result_path,
                                                  '.'.join([self.version, 'xlsx']))  # 创建一个以测试版本号命名的Excel表
        if os.path.exists(self.test_result_file_path):
            self.wb = xw.Book(self.test_result_file_path)
        else:
            # 打开测试用例表
            self.wb = xw.Book(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', '整机测试内容_有屏MIFI_V1.0.xlsx'))
        self.ws = self.wb.active  # 激活表
        self.ws1 = self.wb["Flash"]  # 选择表
        self._test_file = os.path.join(BASEDIR, 'config', 'test_file.zip')  # 测试文件路径
        self._test_storage_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'test_storage_path')  # 测试pull时文件的存放路径
        if not os.path.exists(self._test_storage_path):
            os.makedirs(self._test_storage_path)
        # self._test_file_size = os.path.getsize(self._test_file)
        self._test_file_size = round((os.path.getsize(self._test_file) / 1000000), 2)  # 获取测试文件大小（字节），将单位转换为MB，并保留小数点2位
        log.info("测试文件大小：%s MB" % self._test_file_size)
        # 判断G4设备是否锁屏，锁屏的话向上滑动解锁
        # if self.g4s_d(resourceId="com.glocalme.g4home:id/tv_unlock").exists():
        #     self.g4s_d.swipe(0.5, 0.8, 0.5, 0.3, 0.1)
        # self.g4s.root()
        # self.g4s_d.app_start(package_name="com.glocalme.g4home", activity="com.glocalme.basic.more.MoreActivity")

    def test01_push(self):
        log.info("start %s" % sys._getframe().f_code.co_name)
        # u3_push_avg_result_list = []
        # u3_push_duration_result_list = []
        g4s_push_avg_result_list = []
        for i in range(50):
            # log.info("-"*20 + "U3设备第%d次push" % (i+1) + "-"*20)
            # u3_push_start_time = time.time()
            # u3_push = self.u3.push(source_file=self._test_file, target_path='/sdcard/')
            # u3_push_end_time = time.time()
            # if u3_push:
            #     u3_push_duration = round((u3_push_end_time - u3_push_start_time), 2)    # 计算push时长
            #     u3_push_duration_result_list.append(u3_push_duration)
            #     log.info("push duration:%s" % u3_push_duration)
            #     u3_push_speed = round((self._test_file_size / u3_push_duration), 2)
            #     log.info("push speed:%s MB/S" % u3_push_speed)    # 计算push速率
            #     u3_push_avg_result_list.append(u3_push_speed)
            # else:
            #     log.error("push faild.")
            #     u3_push_avg_result_list.append(0)
            # time.sleep(1)
            log.info("-" * 20 + "G4S设备第%d次push" % (i + 1) + "-" * 20)
            g4s_start_time = time.time()
            g4s_push = self.g4s.push(source_file=self._test_file, target_path='/sdcard/')    # 将测试文件push到设备sdcard目录下，返回push结果
            g4s_end_time = time.time()
            if g4s_push:
                g4s_push_duration = round((g4s_end_time - g4s_start_time), 2)  # 计算push时长
                log.info("push duration:%s" % g4s_push_duration)
                g4s_push_speed = round((self._test_file_size / g4s_push_duration), 2)
                log.info("push speed:%s MB/S" % g4s_push_speed)  # 计算push速率
                g4s_push_avg_result_list.append(g4s_push_speed)
            else:
                log.error("push faild.")
                g4s_push_avg_result_list.append(0)
            time.sleep(1)
        # log.info('u3_push_avg_result_list:%s' % str(u3_push_avg_result_list))
        log.info('g4s_push_avg_result_list:%s' % str(g4s_push_avg_result_list))
        # u3_push_success_list = self._remove_value_from_list(u3_push_avg_result_list, 0)
        g4s_push_success_list = self._remove_value_from_list(g4s_push_avg_result_list, 0)
        # if len(u3_push_success_list) != len(u3_push_avg_result_list):
        #     u3_push_fail_times = len(u3_push_avg_result_list) - len(u3_push_success_list)
        #     log.error("u3 push fail times: %d" % u3_push_fail_times)
        #     self.ws1['H17'] = "u3 push fail times: %d" % u3_push_fail_times
        if len(g4s_push_success_list) != len(g4s_push_avg_result_list):
            g4s_push_fail_times = len(g4s_push_avg_result_list) - len(g4s_push_success_list)
            log.error("g4s push fail times: %d" % g4s_push_fail_times)
            self.ws1['H18'] = "g4s push fail times: %d" % g4s_push_fail_times
        # u3_push_avg = sum(u3_push_success_list) / len(u3_push_success_list)
        g4s_push_avg = sum(g4s_push_success_list) / len(g4s_push_success_list)
        # self.ws1['F17'] = round(u3_push_avg, 2)
        self.ws1['F18'] = round(g4s_push_avg, 2)
        # self.ws1['F32'] = len(u3_push_duration_result_list)
        # self.ws1['G32'] = round((sum(u3_push_duration_result_list) / len(u3_push_duration_result_list)), 2)

    def test02_pull(self):
        log.info("start %s" % sys._getframe().f_code.co_name)
        # u3_pull_result_list = []
        g4s_pull_result_list = []
        # u3_pull_duration_result_list = []
        """
        # 判断U3设备/sdcard路径下是否存在test_file.zip文件，如果不存在就push一个进去
        if not self.u3.file_exists(file='/sdcard/test_file.zip'):
            u3_push = self.u3.push(source_file=self._test_file, target_path='/sdcard/')
            while not u3_push:
                u3_push = self.u3.push(source_file=self._test_file, target_path='/sdcard/')
        for i in range(50):
            log.info("-"*20 + "U3设备第%d次pull" % (i+1) + "-"*20)
            u3_pull_start_time = time.time()
            u3_pull = self.u3.pull(source_file="/sdcard/test_file.zip", target_path=self._test_storage_path)
            u3_pull_end_time = time.time()
            if u3_pull:
                u3_pull_duration = round((u3_pull_end_time - u3_pull_start_time), 2)    # 计算pull时长，保留小数点后2位
                u3_pull_duration_result_list.append(u3_pull_duration)
                log.info("pull duration:%s" % u3_pull_duration)
                u3_pull_speed = round((self._test_file_size / u3_pull_duration), 2)    # 计算pull速度，保留小数点后2位
                log.info("pull speed:%s" % u3_pull_speed)
                u3_pull_result_list.append(u3_pull_speed)
            else:
                log.error("pull failed.")
                u3_pull_result_list.append(0)
            time.sleep(1)
        log.info("u3_pull_result_list:%s" % str(u3_pull_result_list))
        u3_pull_success_list = self._remove_value_from_list(u3_pull_result_list, 0)    # 去除u3 pull结果集中为0的结果
        if len(u3_pull_success_list) != len(u3_pull_result_list):
            u3_pull_fail_times = len(u3_pull_result_list) - len(u3_pull_success_list)    # pull 失败次数
            log.error("u3 pull failed times: %d" % u3_pull_fail_times)
            self.ws1['H12'] = "u3 pull failed times: %d" % u3_pull_fail_times
        u3_pull_avg = round((sum(u3_pull_success_list) / len(u3_pull_success_list)), 2)
        self.ws1['F12'] = u3_pull_avg
        self.ws1['F31'] = len(u3_pull_duration_result_list)
        self.ws1['G31'] = round((sum(u3_pull_duration_result_list) / len(u3_pull_duration_result_list)), 2)
        """
        # 判断G4S设备/sdcard路径下是否存在test_file.zip文件，如果不存在就push一个进去
        if not self.g4s.file_exists(file='/sdcard/test_file.zip'):
            g4s_push = self.g4s.push(source_file=self._test_file, target_path='/sdcard/')
            while not g4s_push:
                g4s_push = self.g4s.push(source_file=self._test_file, target_path='/sdcard/')
        for i in range(50):
            log.info("-" * 20 + "G4S设备第%d次pull" % (i + 1) + "-" * 20)
            g4s_pull_start_time = time.time()
            g4s_pull = self.g4s.pull(source_file="/sdcard/test_file.zip", target_path=self._test_storage_path)
            g4s_pull_end_time = time.time()
            if g4s_pull:
                g4s_pull_duration = round((g4s_pull_end_time - g4s_pull_start_time), 2)  # 计算pull时长，保留小数点后2位
                log.info("pull duration:%s" % g4s_pull_duration)
                g4s_pull_speed = round((self._test_file_size / g4s_pull_duration), 2)  # 计算pull速度，保留小数点后2位
                log.info("pull speed:%s" % g4s_pull_speed)
                g4s_pull_result_list.append(g4s_pull_speed)
            else:
                log.error("pull failed.")
                g4s_pull_result_list.append(0)
            time.sleep(1)
        log.info("g4s_pull_result_list:%s" % str(g4s_pull_result_list))
        g4s_pull_success_list = self._remove_value_from_list(g4s_pull_result_list, 0)  # 去除g4s pull结果集中为0的结果
        if len(g4s_pull_success_list) != len(g4s_pull_result_list):
            g4s_pull_fail_times = len(g4s_pull_result_list) - len(g4s_pull_success_list)  # pull 失败次数
            log.error("g4s pull failed times: %d" % g4s_pull_fail_times)
            self.ws1['H13'] = "g4s pull failed times: %d" % g4s_pull_fail_times
        g4s_pull_avg = round((sum(g4s_pull_success_list) / len(g4s_pull_success_list)), 2)    # 计算pull成功结果的平均值，保留小数点2位
        self.ws1['F13'] = g4s_pull_avg

    def test03(self):
        print("OK")

    def teardown(self):
        # 每条case执行结束保存一下测试结果表
        self.wb.save(self.test_result_file_path)

    def teardown_class(self):
        log.info("-" * 20 + "End Test_Flash" + "-" * 20)

    def _remove_value_from_list(self, list, value):
        for i in list:
            if i == value:
                list.remove(i)
        return list

@allure.feature("显示")
class Test_Display:
    def setup_class(self):
        log.info("-" * 20 + "Start Test_Display" + "-" * 20)
        # 测试截图、视频的保存路径；如果不存在此路径，就创建此路径
        self.test_record_path = '/'.join([BASEDIR, 'TestRecord', project_name, "Test_Display"])
        if not os.path.exists(self.test_record_path):
            os.makedirs(self.test_record_path)

        # 初始化信息
        self.serialno = global_config.getRaw("config-G4S", "serialno")
        self.g4s = models.Glocalme(device_id=self.serialno, log_project=log)
        self.g4s.wait_device_connect()
        self.g4s.wakey()  # 设置辅助机屏幕常亮
        # 执行uiautomator2的init操作，在测试设备端安装uiautomator app，minicap和minitouch，atx-agent
        uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
        self.g4s_d = u2.connect(self.serialno)

        self.version = self.g4s.get_current_version()  # 获取测试设备的版本
        self.test_result_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'TestResult', project_name)
        if not os.path.exists(self.test_result_path):
            os.makedirs(self.test_result_path)  # 创建测试结果文件夹，并以测试版本命名
        self.test_result_file_path = os.path.join(self.test_result_path, '.'.join([self.version, 'xlsx']))  # 创建一个以测试版本号命名的Excel表
        if os.path.exists(self.test_result_file_path):
            self.wb = xw.Book(self.test_result_file_path)
        else:
            # 打开测试用例表
            self.wb = xw.Book(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', '整机测试内容_有屏MIFI_V1.0.xlsx'))
        self.ws = self.wb.active  # 激活表
        self.ws1 = self.wb["显示及设置"]  # 选择表
        if self.g4s_d(resourceId="com.glocalme.g4home:id/tv_unlock").exists():
            self.g4s_d.swipe(0.5, 0.8, 0.5, 0.3, 0.1)


    def test01(self):
        '''测试用例：卡状态'''
        log.info("start %s" % sys._getframe().f_code.co_name)
        log.info(self.g4s_d.device_info)
        assert True

    def teardown(self):
        # 每条case执行结束保存一下测试结果表
        self.wb.save(self.test_result_file_path)

    def teardown_class(self):
        log.info("-" * 20 + "End Test_Display" + "-" * 20)

@allure.feature("FOTA")
class Test_Fota:
    def setup_class(self):
        log.info("-" * 20 + "Start Test_Fota" + "-" * 20)
        # 测试截图、视频的保存路径；如果不存在此路径，就创建此路径
        self.test_record_path = '/'.join([BASEDIR, 'TestRecord', project_name, "Test_Fota"])
        if not os.path.exists(self.test_record_path):
            os.makedirs(self.test_record_path)

        # 初始化信息
        self.serialno = global_config.getRaw("config-G4S", "serialno")
        self.source_version = global_config.getRaw("config-G4S", "source_version")
        self.target_version = global_config.getRaw("config-G4S", "target_version")
        self.g4s = models.G4S(device_id=self.serialno, log_project=log)
        self.g4s.wait_device_connect()
        self.g4s.wakey()  # 设置屏幕常亮
        # 执行uiautomator2的init操作，在测试设备端安装uiautomator app，minicap和minitouch，atx-agent
        # uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
        self.g4s.uiautomator2_init()
        self.g4s_d = u2.connect(self.serialno)
        self.g4s_uiOpration = G4S_uiOpration(g4s=self.g4s, d=self.g4s_d, log_project=log)

        # 切换系统语言为中文
        self.g4s_uiOpration.switch_language(language="中文简体")

        # 打开USB debug模式
        # self.g4s_uiOpration.enable_test_mode()

        self.version = self.g4s.get_current_version()  # 获取测试设备的版本
        self.test_result_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'TestResult', project_name)
        if not os.path.exists(self.test_result_path):
            os.makedirs(self.test_result_path)  # 创建测试结果文件夹，并以测试版本命名
        self.test_result_file_path = os.path.join(self.test_result_path, '.'.join([self.version, 'xlsx']))  # 创建一个以测试版本号命名的Excel表
        self.app = xw.App(visible=False, add_book=False)
        # 打开测试用例表
        self.wb = self.app.books.open(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', 'G4自动化测试用例.xlsx'))
        # self.ws = self.wb.active  # 激活表
        self.ws1 = self.wb.sheets['fota']  # 选择表

        # if self.g4s_d(resourceId="com.glocalme.g4home:id/tv_unlock").exists():
        #     self.g4s_d.swipe(0.5, 0.8, 0.5, 0.3, 0.1)


    def setup(self):
        self.g4s.wait_network_connect()
        current_version = self.g4s.get_current_version()
        if current_version != self.source_version:
            pass

    def test01(self):
        '''测试用例：云卡网络-开机检测'''
        log.info("start %s" % sys._getframe().f_code.co_name)
        self.g4s.root()
        self.g4s_d.press("home")
        login_type = self.g4s.login_type()
        if login_type == 0:
            self.g4s_uiOpration.switch_network_to_cloudSIM()
            time.sleep(5)
        self.g4s.reboot()
        self.g4s.wait_device_connect()
        self.g4s.wakey()
        self.g4s.wait_network_connect()
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
