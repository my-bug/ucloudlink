#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:基于uiautomator2模块的模拟操控UI的方法
'''
import time
from config import U3_settings
from config.settings import BASEDIR, G4S_ROOT_APK_FILE

class Base_uiOpration:
    def __init__(self, d, log_project=None):
        '''
        :param
            d:uiautomator2对象
            log_project:log对象
        '''
        self.d = d
        if log_project:
            self.log = log_project
        else:
            import logging
            self.log = logging

    def screenShot(self, path, title):
        '''在uiautomator2的截图函数上封装的截图方法
        :param path:截图保存的路径
        :param title: 自定义截图的名称
        :return: 返回截图的路径
        '''
        screenShot_file = '/'.join([path, '.'.join([title, 'png'])])
        self.d.screenshot(screenShot_file)
        return screenShot_file

    '''()
    def pull_ScreenRecord(self, file_path, sava_path, title, format):
        """将设备本地视频pull出来到自定义的path路径
        :param file_path：视频的原始路径
        :param sava_path：视频保存的路径
        :param title: 自定义视频的名称
        :param format：文件保存的格式（如文本格式txt、视频格式mp4等）
        :return: 返回视频的路径
        """
        list = self.d.adb_shell('ls /sdcard/ScreenRecord/record/')
        ScreenRecord_list = list.strip().split('\n')
        file = '/'.join(['/sdcard/ScreenRecord/record', ScreenRecord_list[-1]])
        save_file = '/'.join([sava_path, '.'.join([title, format])])
        self.d.pull(src=file, dst=save_file)
        return save_file
    '''

class S20i_uiOpration(Base_uiOpration):
    """
    def __init__(self, d, log_project=None):
        '''
        :param
            d:uiautomator2对象
            log_project:log对象
        '''
        self.d = d
        if log_project:
            self.log = log_project
        else:
            import logging
            self.log = logging

    def screenShot(self, path, title):
        '''
        在uiautomator2的截图函数上封装的截图方法
        :param
            path:截图保存的路径
            title: 自定义截图的名称
        :return: 返回截图的路径
        '''
        screenShot_file = '/'.join([path, '.'.join([title, 'png'])])
        self.d.screenshot(screenShot_file)
        return screenShot_file
    """

    def search_wifi(self, wifi_name, timeout=180):
        cur = time.time()
        expire = cur + timeout
        while cur < expire:
            if not self.d(resourceId="android:id/title", text=wifi_name).exists(2):  # 判断当前界面是否存在所查找的wifi
                while not self.d(resourceId="android:id/title", text="添加网络").exists(1):
                    if self.d(resourceId="android:id/title", text=wifi_name).exists(1):
                        break
                    else:
                        self.d.swipe(0.5, 0.8, 0.5, 0.3)
                else:
                    while not self.d(resourceId="android:id/title", text="WLAN 偏好设置").exists(1):
                        if self.d(resourceId="android:id/title", text=wifi_name).exists(1):
                            break
                        else:
                            self.d.swipe(0.5, 0.3, 0.5, 0.8)
                cur = time.time()
            else:
                break
        else:
            raise TimeoutError("wifi connect timeout.")

    def connect_wifi(self, wifi_name, password):
        for i in range(2):
            self.d.press('home')
        self.d(resourceId="com.android.systemui:id/recent_apps").click()
        if self.d(resourceId="com.android.systemui:id/clear_all_button").exists(3):
            self.d(resourceId="com.android.systemui:id/clear_all_button").click()
            self.log.info("cleared background app success.")
        else:
            self.log.info('no background app running.')
        for i in range(2):
            self.d.press('home')
        self.d(text="设置").click()
        self.d(resourceId="android:id/title", text="网络和互联网").click()
        self.d(resourceId="android:id/title", text="WLAN").click()
        if self.d(resourceId="com.android.settings:id/switch_widget").get_text() == "关闭":  # 判断wifi是否开启
            self.d(resourceId="com.android.settings:id/switch_widget").click()
        time.sleep(3)
        self.search_wifi(wifi_name)
        if self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="登录到网络").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:登录到网络")
            return
        elif self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="已连接").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:已连接")
            return
        elif self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="已连接，但无法访问互联网").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:已连接，但无法访问互联网")
            return
        self.d(resourceId="android:id/title", text=wifi_name).click()  # 点击名称为“GlocalMe”的wifi
        if self.d(resourceId="com.android.settings:id/password").exists(3):  # 判断是否弹出输入password的弹窗
            self.d.send_keys(password, clear=True)  # 输入password
            self.d(resourceId="android:id/button1").click()
        elif self.d(text="取消保存").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully")
            return
        if self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="登录到网络").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:登录到网络")
        elif self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="已连接").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:已连接")
        elif self.d(resourceId="android:id/title", text=wifi_name).sibling(resourceId="android:id/summary", text="已连接，但无法访问互联网").exists(3):
            self.log.info("auxiliary device connect test device wifi successfully, text:已连接，但无法访问互联网")
        else:
            self.log.error("auxiliary device connect test device wifi failed.")
            # self.screenShot(title="wifi_connect_fail")
            raise ConnectionError("wifi connect error.")

    def open_webui(self):
        # self.connect_wifi()
        self.d(resourceId="com.android.systemui:id/center_group").click()  # 返回主界面
        self.d(text="Chrome").click()  # 点击打开浏览器
        # 判断浏览器是否第一次打开，如果第一次打开就点击设置欢迎页弹窗
        if self.d(resourceId="com.android.chrome:id/terms_accept").exists(5):
            try:
                self.d(resourceId="com.android.chrome:id/terms_accept").click()
                self.d(resourceId="com.android.chrome:id/negative_button").click()
                self.d(resourceId="com.android.chrome:id/button_secondary").click()
            except Exception as e:
                self.log.error(e)
                # self.log.info('浏览器不是第一次启动，不需要设置欢迎页')
        # self.d(resourceId="com.android.chrome:id/home_button").click()  # 点击浏览器主页按钮进入主页
        # 浏览器弹窗是否继续使用Google浏览器，或改用搜狗搜索
        if self.d(resourceId="com.android.chrome:id/button_secondary", text="继续使用 Google").exists(5):
            self.d(resourceId="com.android.chrome:id/button_secondary", text="继续使用 Google").click()
        try:
            self.d(resourceId="com.android.chrome:id/url_bar").click()  # 点击浏览器搜索框
        except:
            self.d(resourceId="com.android.chrome:id/search_box").click()  # 点击浏览器搜索框
        self.d.send_keys("192.168.43.1", clear=True)  # 在搜索框中输入192.168.43.1
        self.d.xpath('//android.widget.ListView/android.view.ViewGroup[1]').click()  # 点击进入webui界面

    def login_webui(self):
        if self.d(resourceId="tr_manage_my_device").exists(5):
            self.d(resourceId="tr_manage_my_device").click()  # 点击管理我的设备
        elif self.d(text="Manage My Device").exists(5):
            self.d(text="Manage My Device").click()
        # 输入账号密码登陆管理界面
        self.d(resourceId="username").click()
        time.sleep(2)
        self.d.click(0.342, 0.303)
        self.d.send_keys("admin", clear=True)
        for i in range(2):
            self.d(resourceId="passWord").click()
        self.d.send_keys("admin", clear=True)
        self.d(text="Login").click()
        time.sleep(1)

    def wipe_data(self):
        self.open_webui()
        self.login_webui()
        self.d(text="Settings").click()
        self.d(text="Restore to factory defaults").click()
        self.d(resourceId="confirm_btn_ok").click()

class G4S_uiOpration(Base_uiOpration):
    def __init__(self, g4s, d, log_project):
        self.g4s = g4s
        super().__init__(d, log_project)

    def switch_language(self, language):
        self.g4s.root()
        self.d.app_start(package_name="com.glocalme.g4home", activity="com.glocalme.basic.language.LanguageActivity")
        self.d(resourceId="com.glocalme.g4home:id/tv_language", text=language).click()
        time.sleep(2)
        self.d.press("home")

    def enable_test_mode(self):
        self.d.app_start(package_name="com.android.settings", activity="com.android.settings.Settings")
        self.d.swipe_ext("up", 1.0)  # 向上滑动100%
        self.d(resourceId="android:id/title", text="系统").click()
        self.d(resourceId="android:id/title", text="关于手机").click()
        for i in range(6):
            self.d(resourceId="android:id/title", text="版本号").click()
            time.sleep(0.5)
        self.d(description="向上导航").click()
        self.d(resourceId="android:id/title", text="开发者选项").click()
        usb_test = self.d(resourceId="android:id/title", text="USB 调试").exists(3)
        while not usb_test:
            self.d.swipe_ext("up", 0.8)    # 向上滑动80%
            usb_test = self.d(resourceId="android:id/title", text="USB 调试").exists(3)
        # 获取USB 调试开关的状态
        status = self.d.xpath('//*[@resource-id="com.android.settings:id/list"]/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.Switch[1]').get_text()
        if status == "OFF":
            self.d.xpath('//*[@resource-id="com.android.settings:id/list"]/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.Switch[1]').click()
            self.d(resourceId="android:id/button1", text="确定").click()
        time.sleep(2)
        self.d.press("home")



    def switch_network_to_cloudSIM(self, retry_num: "int" = 2):
        self.d.app_start(package_name='com.ukl.factory', activity='com.ukl.factory.UklFacMainActivity')
        self.d.app_start(package_name='com.glocalme.g4home', activity='com.glocalme.basic.simcardmanager.SimCardActivityG4P')
        for i in range(retry_num):
            sim_status = self.d(resourceId="com.glocalme.g4home:id/st_sim_net").get_text()
            if sim_status == "开启":
                self.d(resourceId="com.glocalme.g4home:id/st_sim_net").click()
                time.sleep(5)
                self.g4s.wait_network_connect()
                login_type = self.g4s.login_type()
                if login_type == 1:
                    self.log.info("switch to cloudSIM success")
                    return
                else:
                    self.log.error("switch to cloudSIM failed, the number of remaining attempts:%d" % (retry_num-i-1))
                    continue
            else:
                self.log.info("current network is cloudSIM, no need to switch")
                return
        raise Exception("switch to cloudSIM failed")


    def switch_network_to_SIM(self, retry_num: "int" = 2):
        self.d.app_start(package_name='com.glocalme.g4home', activity='com.glocalme.basic.simcardmanager.SimCardActivityG4P')
        for i in range(retry_num):
            sim_status = self.d(resourceId="com.glocalme.g4home:id/st_sim_net").get_text()
            if sim_status == "关闭":
                self.d(resourceId="com.glocalme.g4home:id/st_sim_net").click()
                self.d(text="确定").click()
                time.sleep(5)
                self.g4s.wait_network_connect()
                login_type = self.g4s.login_type()
                if login_type == 0:
                    self.log.info("switch to SIM success")
                    return
                else:
                    self.log.error("switch to SIM failed, the number of remaining attempts:%d" % (retry_num-i-1))
                    continue
            else:
                self.log.info("current network is SIM, no need to switch")
                return
        raise Exception("switch to SIM failed")



    """
    def swith_network(self, swith_to_sim: "bool", retry_num: "int = 2"):
        # 进入SIM卡管理界面
        self.driver.start_activity(app_package='com.glocalme.g4home', app_activity='com.glocalme.basic.simcardmanager.SimCardActivityG4P')
        for i in range(retry_num):
            # 获取SIM卡网络开关状态
            sim_status = self.sim_switch_element.text
            if not swith_to_sim and sim_status == "开启":
                self.log.info("当前网络为SIM卡网络，切换为云卡网络")
                # 关闭SIM卡网络
                self.sim_switch_element.click()
                self.g4s.wait_network_connect()
                sim_status = self.sim_switch_element.text
                if sim_status == "关闭":
                    self.log.info("网络切换成功")
                    return
                else:
                    self.log.error("网络切换失败，第%d次" % i + 1)
                    continue
            elif swith_to_sim and sim_status == "关闭":
                self.log.info("当前网络为云卡网络，切换为SIM卡网络")
                # 开启SIM卡网络
                self.sim_switch_element.click()
                self.g4s.wait_network_connect()
                sim_status = self.sim_switch_element.text
                if sim_status == "开启":
                    self.log.info("网络切换成功")
                    return
                else:
                    self.log.error("网络切换失败，第%d次" % i + 1)
                    continue
            elif not swith_to_sim and sim_status == "关闭":
                self.log.info("当前网络为云卡网络，无需切换")
                return
            else:
                self.log.info("当前网络为SIM卡网络，无需切换")
                return
        self.log.error("网络切换失败，重试次数：%d" % retry_num)
        raise Exception("网络切换失败")
        """
