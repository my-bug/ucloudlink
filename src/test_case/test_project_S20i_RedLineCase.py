#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
    1、脚本目的：S20i项目红线用例自动化测试
    2、涵盖测试模块：
        - 多媒体模块红线包用例
'''

import pytest, subprocess, time, os, allure, random
from common import  models, logger
from config import settings
import uiautomator2 as u2
from pywinauto import application
from openpyxl import load_workbook

os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
# 创建log对象
log = logger.Logger(screen_output=True, log_level='logging.INFO').create_logger()
# 获取项目路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
# 创建测试记录保存路径
test_record_path = '/'.join([BASEDIR, 'TestRecord', 'test_project_S20i_RedLineCase', current_time])
if not os.path.exists(test_record_path):
    os.makedirs(test_record_path)
# 报告保存路径
report_path = '/'.join([BASEDIR, 'reports', 'test_project_S20i_RedLineCase'])
if not os.path.exists(report_path):
    make_report_path = os.makedirs(report_path)
report_name = '/'.join([report_path, '.'.join([current_time, 'html'])])
report = ''.join(['--html=', report_name])


def screenShot(d, title):
    '''
    在uiautomator2的截图函数上封装的截图方法
    :param title: 自定义截图的名称
    :return: 返回截图的路径
    '''
    screenShot_file = '/'.join([test_record_path, '.'.join([title, 'png'])])
    d.screenshot(screenShot_file)
    return screenShot_file


def pull_ScreenRecord(d, title):
    list = d.adb_shell('ls /sdcard/ScreenRecord/record/')
    ScreenRecord_list = list.strip().split('\n')
    file = '/'.join(['/sdcard/ScreenRecord/record', ScreenRecord_list[-1]])
    save_file = '/'.join([test_record_path, '.'.join([title, 'mp4'])])
    d.pull(src=file, dst=save_file)
    return save_file

# 相机类测试用例
@allure.feature('S20i红线用例-相机测试')
class Test_Camera:
    # 测试类起始函数
    def setup_class(self):
        # 启动高通自动切口工具
        self.start_SwitchComTool = application.Application().start(settings.Qualcomm_SwitchCom_file)
        # 创建测试设备对象
        self.test_device = models.Glocalme(log_project=log)
        self.test_device.wait_device_connect()  # 等待设备连接
        # 执行uiautomator2的init操作，在测试设备端安装uiautomator app，minicap和minitouch，atx-agent
        uiautomator2_init = subprocess.getoutput("python -m uiautomator2 init")
        self.d = u2.connect()
        # 设置屏幕常亮
        self.test_device.wakey()
        # 将测试用例copy到存放测试结果的文件夹中并以版本号命名测试结果文件
        version = self.test_device.get_current_version()
        self.test_result_file_path = os.path.join(BASEDIR, 'TestCaseAndResult', 'TestResult', '.'.join([version, 'xlsx']))
        # shutil.copy(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', '整机红线用例.xlsx'), test_result_file_path)
        # 打开测试用例表
        self.wb = load_workbook(os.path.join(BASEDIR, 'TestCaseAndResult', 'TestCase', '整机红线用例.xlsx'))
        self.ws = self.wb.active # 激活表
        self.ws1 = self.wb["多媒体模块红线包用例"]    # 选择表
        # 判断屏幕是否锁屏状态，如果锁屏就给设备解锁（仅适用滑动解锁）
        if self.d(resourceId="com.android.systemui:id/lock_icon").exists():
            self.d(resourceId="com.android.systemui:id/lock_icon").click()
        '''安装录屏软件，并开启录屏'''
        try:
            self.d.app_uninstall(pkg_name='com.jy.recorder')
        except Exception as e:
            log.error(e)
        self.test_device.install_apk(settings.xunjielupingdashi_apk_file)   #安装录屏软件
        try:
            self.d.app_start(package_name='com.jy.recorder')
            self.d(resourceId="com.jy.recorder:id/dlg_top_btn").click()
            self.d(resourceId="com.jy.recorder:id/tv_ensure").click()
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            self.d(resourceId="com.jy.recorder:id/tv_ensure").click()
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            self.d(resourceId="com.jy.recorder:id/dlg_right_btn").click()
            self.d(resourceId="android:id/switch_widget").click()
            self.d(resourceId="com.android.systemui:id/back").click()
            self.d(resourceId="android:id/button1").click()
            self.d(resourceId="com.android.systemui:id/center_group").click()
            # self.d.open_notification()  # 打开设备下拉通知栏
            # self.d(resourceId="com.jy.recorder:id/tv_notify_start").click()     # 点击开始录屏
        except Exception as e:
            log.error('开启录屏失败，失败原因：%s' % e)
        for i in range(2):
            self.d.press('home')

    def setup(self):
        self.d.open_notification()  # 打开设备下拉通知栏
        self.d(resourceId="com.jy.recorder:id/tv_notify_start").click()  # 点击开始录屏
        time.sleep(5)

    @allure.title('启动相机')
    def test01_CameraStart(self):
        '''测试用例标题：启动相机'''
        with allure.step('第一步：灭屏-亮屏-从锁屏界面打开相机'):
            # 灭屏重新亮屏
            self.d.screen_off()
            time.sleep(1)
            self.d.screen_on()
            # 测试从锁屏界面打开相机
            self.d(resourceId="com.android.systemui:id/camera_button").drag_to(0.5, 0.5)
            time.sleep(5)
        with allure.step('第二步：检验从锁屏界面打开相机是否成功'):
            current_app_package_01 = self.d.app_current().get('package')
            # 检验从锁屏界面打开相机的测试结果
            # result01 = pytest.assume(current_app_01 == {'package': 'org.codeaurora.snapcam', 'activity': 'com.android.camera.PermissionsActivity'})
            result01 = pytest.assume(current_app_package_01== 'org.codeaurora.snapcam')
        with allure.step('第三步：杀掉相机应用-从主界面打开相机'):
            # 杀掉相机
            self.d.press('home')
            self.d.app_clear(pkg_name='org.codeaurora.snapcam')
            # 将手机界面切换到主界面
            for i in range(2):
                self.d.press("home")
            time.sleep(1)
            # 测试从主界面打开相机
            self.d(text="相机").click()
            # self.d.wait_activity(activity='com.android.camera.CameraActivity', timeout=10)
            time.sleep(5)
        with allure.step('第四步：检验从主界面打开相机是否成功'):
            current_app_package_02 = self.d.app_current().get('package')
            # 检验从主界面打开相机的测试结果
            result02 = pytest.assume(current_app_package_02 == 'org.codeaurora.snapcam')
        # 杀掉相机
        self.d.press('home')
        self.d.app_clear(pkg_name='org.codeaurora.snapcam')
        if result01 and result02:
            self.ws1['H2'] = "PASS"
        else:
            self.ws1['H2'] = "FAIL"
        # 下拉通知栏，并点击停止录屏按钮
        self.d.open_notification()
        self.d(resourceId="com.jy.recorder:id/tv_notify_stop").click()
        time.sleep(3)
        # 将测试录制的视屏pull出来，并附到测试报告中
        test_video = pull_ScreenRecord(d=self.d, title='test01_CameraStart')
        test_video_read = open(test_video, 'rb').read()
        allure.attach(test_video_read, '测试视频', allure.attachment_type.MP4)


    @allure.title('退出相机')
    def test02_CameraExit(self):
        with allure.step('第一步：从主界面打开相机'):
            # 从主界面打开相机
            self.d(text="相机").click()
            time.sleep(5)
            # 判断相机是否打开成功
            start_camera_result =  pytest.assume(self.d.app_current().get('package') == 'org.codeaurora.snapcam')
            assert self.d.app_current().get('package') == 'org.codeaurora.snapcam'
        # if start_camera_result:
        with allure.step('第二步：点击主页键退出相机'):
            self.d(resourceId="com.android.systemui:id/center_group").click()    #点击主页键退出相机
            time.sleep(3)
            current_app_package_01 = self.d.app_current().get('package')
            # 检验点击主页键退出相机的测试结果
            test_result01 = pytest.assume(current_app_package_01 != 'org.codeaurora.snapcam')
        with allure.step('第三步：杀掉相机-进入相机-进入相机设置-点击主页键退出相机'):
            self.d.app_clear(pkg_name='org.codeaurora.snapcam')  # 杀掉相机
            time.sleep(3)
            self.d(text="相机").click()
            self.d(resourceId="org.codeaurora.snapcam:id/setting_button").click()   # 点击相机中的设置选项
            time.sleep(3)
            self.d(resourceId="com.android.systemui:id/center_group").click()  # 点击主页键退出相机
            time.sleep(3)
            current_app_package_02 = self.d.app_current().get('package')
            # 检验从相机设置界面点击主页键退出相机的测试结果
            test_result02 = pytest.assume(current_app_package_02 != 'org.codeaurora.snapcam')
        self.d.app_clear(pkg_name='org.codeaurora.snapcam')  # 杀掉相机
        if test_result01 and test_result02:
            self.ws1['H3'] = "PASS"
        else:
            self.ws1['H3'] = "FAIL"
        # 下拉通知栏，并点击停止录屏按钮
        self.d.open_notification()
        self.d(resourceId="com.jy.recorder:id/tv_notify_stop").click()
        time.sleep(3)
        # 将测试录制的视屏pull出来，并附到测试报告中
        test_video = pull_ScreenRecord(d=self.d, title='test02_CameraExit')
        test_video_read = open(test_video, 'rb').read()
        allure.attach(test_video_read, '测试视频', allure.attachment_type.MP4)

    @allure.title('菜单选项图标')
    def test03_MenuOptionsIcon(self):
        '''测试用例标题：菜单选项图标'''
        with allure.step('第一步:打开相机'):
            self.d(text="相机").click()
            time.sleep(5)
            assert self.d.app_current().get('package') == 'org.codeaurora.snapcam'
        with allure.step('第二步:检查菜单选项图标是否正常'):
            icon_exits_list = [
                self.d(resourceId="org.codeaurora.snapcam:id/setting_button").exists(5),   # 判断设置图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/scene_mode_switcher").exists(5),  # 判断场景图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/flash_button").exists(5),     # 判断闪光灯图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/face_button").exists(5),      # 判断人脸图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/filter_mode_switcher").exists(5),     # 判断滤镜切换图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_time_lapse").exists(5),      # 判断“延时摄影”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_slow_motion").exists(5),     # 判断“慢动作”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_video").exists(5),       # 判断“视频”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_photo").exists(5),       # 判断“照片”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_square_photo").exists(5),        # 判断“正方形”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_bokeh").exists(5),       # 判断“人像”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/text_panorama").exists(5),        # 判断“全景”是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/preview_thumb").exists(5),        # 判断图库图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").exists(5),       # 判断快门图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/front_back_switcher").exists(5),      # 判断摄像头切换图标是否存在
                self.d(resourceId="org.codeaurora.snapcam:id/mdp_preview_content").exists(5)    # 判断取景框是否存在
            ]
            for icon_exit_result in icon_exits_list:
                pytest.assume(icon_exit_result is True)
        if False in icon_exits_list:
            self.ws1['H4'] = 'FAIL'
            log.error('case：test03_MenuOptionsIcon，error：菜单选项图标不符合预期，图标检测结果：%s' % str(icon_exits_list))
            FailScreenShot_file = screenShot(d=self.d, title='MenuOptionsIcon_fail')
            file = open(FailScreenShot_file, 'rb').read()
            allure.attach(file, '菜单选项图标检测试失败的截图', allure.attachment_type.PNG)
        else:
            self.ws1['H4'] = 'PASS'
        # 下拉通知栏，并点击停止录屏按钮
        self.d.open_notification()
        self.d(resourceId="com.jy.recorder:id/tv_notify_stop").click()
        time.sleep(3)
        # 将测试录制的视屏pull出来，并附到测试报告中
        test_video = pull_ScreenRecord(d=self.d, title='test03_MenuOptionsIcon')
        test_video_read = open(test_video, 'rb').read()
        allure.attach(test_video_read, '测试视频', allure.attachment_type.MP4)

    @allure.title('取景框')
    def test04_CameraAperture(self):
        '''测试用例标题：取景框'''
        with allure.step('第一步：打开相机'):
            self.d(text="相机").click()
            time.sleep(5)
            assert self.d.app_current().get('package') == 'org.codeaurora.snapcam'
        with allure.step('第二步：获取取景框大小，并检验取景框与窗体之间是否有间隙'):
            # 获取取景框大小
            CameraAperture_bounds = self.d(resourceId="org.codeaurora.snapcam:id/mdp_preview_content").info['bounds']
            test_result = pytest.assume(CameraAperture_bounds == {'bottom': 1659, 'left': 0, 'right': 1080, 'top': 219})
        if test_result:
            self.ws1['H5'] = 'PASS'
        else:
            self.ws1['H5'] = 'FAIL'
            log.error('case：test04_CameraAperture，error：取景框大小不符合预期，获取的取景框大小为：%s' % str(CameraAperture_bounds))
            FailScreenShot_file = screenShot(d=self.d, title='CameraAperture_fail')
            file = open(FailScreenShot_file, 'rb').read()
            allure.attach(file, '取景框测试失败的截图', allure.attachment_type.PNG)
        # 杀掉相机
        self.d.press('home')
        self.d.app_clear(pkg_name='org.codeaurora.snapcam')
        # 下拉通知栏，并点击停止录屏按钮
        self.d.open_notification()
        self.d(resourceId="com.jy.recorder:id/tv_notify_stop").click()
        time.sleep(3)
        # 将测试录制的视屏pull出来，并附到测试报告中
        test_video = pull_ScreenRecord(d=self.d, title='test04_CameraAperture')
        test_video_read = open(test_video, 'rb').read()
        allure.attach(test_video_read, '测试视频', allure.attachment_type.MP4)

    @allure.title('预览界面')
    def test05_PreviewInterface(self):
        '''测试用例标题：预览界面'''
        pass

    @allure.title('手动对焦')
    def test06_ddd(self):
        with allure.step('第一步：在主界面打开相机'):
            self.d(text="相机").click()
            time.sleep(5)
            assert self.d.app_current().get('package') == 'org.codeaurora.snapcam'
        with allure.step('第二步：将焦点移到预览页面不同位置上'):
            try:
                for i in range(3):
                    # 在预览框随机生成一个坐标点x, y
                    x = random.random()
                    y = random.uniform(0.18, 0.645)
                    # 点击随机生成的坐标点
                    self.d.click(x, y)
                    time.sleep(3)
            except Exception as e:
                log.error('test06')



    def teardown(self):
        # 每条case执行结束保存一下测试结果表
        self.wb.save(self.test_result_file_path)
        # 测试设备返回主界面
        for i in range(2):
            self.d.press('home')
        time.sleep(1)

    def teardown_class(self):
        # self.d.open_notification()
        # self.d(resourceId="com.jy.recorder:id/tv_notify_stop").click()
        self.start_SwitchComTool.kill()


class Test_Fota:
    def setup_class(self):
        pass



if __name__ == '__main__':
    # pytest.main(['-s', report, 'test_project_S20i_RedLineCase.py::Test_Camera'])
    # result_file = '/'.join([report_path, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))])
    # report_file = '/'.join([result_file, 'report'])
    # os.makedirs(report_file)
    # pytest.main(['-s', '-q', '--alluredir', result_file, 'test_project_S20i_RedLineCase.py::Test_Camera'])
    # cmd = ' '.join(['allure generate', result_file, '-o', report_file])
    # subprocess.getoutput(cmd)

    x = random.random()
    y = random.uniform(0.18, 0.645)
    print(x, y)
    d = u2.connect()
    d.click(x, y)