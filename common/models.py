#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''
import subprocess, time, serial, os, re, logging
from config import settings
import serial.tools.list_ports

def show_casename(testname):
    def inner(func):
        def inner01():
            print("start %s" % testname)
            res = func()
            print("end %s" % testname)
            return res
        return inner01
    return inner

class at_cmd:
    def __init__(self, at_dev, log_project=None):
        self.m_at_dev  = at_dev
        self.m_ser_hdl = None
        if log_project:
            self.log = log_project
        else:
            import logging
            self.log = logging

    def __del__(self):
        self.ser_close()

    def ser_init(self):
        try:
            self.m_ser_hdl = serial.Serial(self.m_at_dev, 115200, timeout=30)
            if self.m_ser_hdl is not None:
                self.log.debug("open serial %s successfully" % self.m_at_dev)
                return True
        except Exception as e:
            print(e)
            return False
        self.log.error("open serial %s failed" % self.m_at_dev)
        print("open serial %s failed" % self.m_at_dev)
        return False

    def ser_close(self):
        if self.m_ser_hdl is not None:
            self.m_ser_hdl.close()
            self.log.debug("close serial " + self.m_at_dev)
            self.m_ser_hdl = None

    def at_cmd_report(self, timeout, *exp):
        line = ""
        cur     = time.time()
        expire  = cur + timeout
        time.sleep(0.1)
        while cur < expire:
            try:
                n = self.m_ser_hdl.inWaiting()
                if n == 0:
                    time.sleep(0.2)
                else:
                    line = self.m_ser_hdl.readline().decode().strip()
                    self.log.info("report: %s",line)
                    for item in exp:
                        if item in line:
                            return line
                        else:
                            pass
                cur = time.time()
            except Exception as e:
                print(e)
                return None
        else:
            return None

    def at_cmd_response(self, timeout):
        line = ""
        cur = time.time()
        expire = cur + timeout
        time.sleep(0.1)
        while cur < expire:
            try:
                n = self.m_ser_hdl.inWaiting()
                if n == 0:
                    time.sleep(0.2)
                else:
                    recv_str = self.m_ser_hdl.read(n)
                    print(recv_str)
                    line += recv_str.decode()
                    if "OK\r\n" in line or "ERROR\r\n" in line or "unknown atcmd\r\n" in line:
                        return line
                cur = time.time()
            except Exception as e:
                print(e)
                return None
        else:
            return None

    def at_cmd_exec(self, cmd, timeout, *exp):
        if not cmd.endswith("\r") and not cmd.endswith("\r\n"):
            cmd += "\r"

        try:
            self.m_ser_hdl.write(cmd.encode())
        except Exception as e:
            print(e)
            return False, None
        response = self.at_cmd_response(timeout)

        if response is None:
            return False, None

        for key in exp:
            if key in response:
                return True, response
        else:
            return False, None

    def at_hexcmd_exec(self, cmd, timeout, *exp):
        try:
            self.m_ser_hdl.write(cmd)
            return True
        except Exception as e:
            print(e)
            return False

# def search_port(dlg_info="SPRD LTE DIAG"):
#     plist = list(serial.tools.list_ports.comports())
#     if len(plist) <= 0:
#         return None
#     else:
#         for portinfo in plist:
#             # print(portinfo.description)
#             if dlg_info in portinfo.description:
#                 # print("port descriptor: %s, port: %s", portinfo.description, portinfo.device)
#                 self.log.info("port descriptor: %s, port: %s", portinfo.description, portinfo.device)
#                 return portinfo.device
#         else:
#             return None
#
#
# def dev_root(port):
#     at = at_cmd(port)
#     if not at.ser_init():
#         return False
#     # result,info = at.at_hexcmd_exec("7e 4c 9f 83 70 16 00 68 00 61 74 2b 73 65 74 61 64 62 72 6f 6f 74 0d 7e", 5, "OK")
#     result = at.at_hexcmd_exec(bytes().fromhex("7e4c9f83701600680061742b736574616462726f6f740d7e"), 5, "OK")
#     if result:
#         return True
#     else:
#         return False

class Glocalme:
    def __init__(self, device_id='', log_project=None):
        self.device_id = device_id
        if self.device_id == '':
            self.adb = 'adb'
        else:
            self.adb = ' '.join(['adb -s', self.device_id])
        if log_project:
            self.log = log_project
        else:
            import logging
            self.log = logging

    def battery_percentage(self):
        """
        获取设备电量百分比
        :return:
        """

        battery_info = subprocess.getoutput(' '.join([self.adb, 'shell "dumpsys battery | grep level"']))
        level = battery_info.split(":")[1].strip()
        return level

    def wakey(self):
        """
        设置当设备插入USB时屏幕常亮
        :return:
        """
        try:
            # 设置当usb接入时屏幕常亮
            subprocess.Popen(' '.join([self.adb, 'shell svc power stayon usb']))
            self.log.debug("wakey successfully.")
        except Exception as e:
            self.log.error("wakey failed:%s" % e)

    # def connect_device(self):
    #     # 检查设备是否连接
    #     # self.log.debug("try to connect device")
    #     try:
    #         # 获取设备列表信息，并用“\r\n”拆分
    #         device_info = subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')
    #         # if device_info is not None and self.device_id in device_info and 'device' in device_info:
    #         if device_info.endswith('device'):
    #             # self.log.debug("device connect success.")
    #             if self.device_id:
    #                 if self.device_id in device_info:
    #                     return True
    #                 else:
    #                     return False
    #             else:
    #                 return True
    #         else:
    #             # self.log.error("device connect failed, device info:%s" % device_info)
    #             return False
    #     except Exception as e:
    #         print(e)
    #         return False

    def connect_device(self):
        """
        判断设备adb端口是否开启
        :return: 布尔值
        """
        device_info = subprocess.check_output("adb devices").decode(r'GBK').strip().split('\r\n')
        device_info.pop(0)
        device_dic = {}
        for i in device_info:
            device_list = i.split('\t')
            device_dic[device_list[0]] = device_list[1]
        if device_info:
            if self.device_id:
                if self.device_id in device_dic.keys() and device_dic[self.device_id]=='device':
                    self.log.debug("device connect success.")
                    return True
                else:
                    self.log.debug('device connect failed')
                    return False
            else:
                if len(device_info) > 1:
                    self.log.error('more than one device connect')
                    return False
                else:
                    if 'device' in device_dic.values():
                        self.log.debug("device connect success.")
                        return True
                    else:
                        self.log.debug('device connect failed')
                        return False
        else:
            self.log.debug('device connect failed')
            return False

    def wait_device_connect(self, timeout=180):
        """
        等待设备adb端口打开
        :param timeout：等待超时时间
        :return 布尔值
        """
        cur = time.time()
        expire = cur + timeout
        fail_time = 1
        while cur < expire:
            if self.connect_device():
                self.log.info("device connect success.")
                return
            else:
                if fail_time > 1:
                    self.log.debug("device connect failed %d times, device info:%s" % (fail_time, subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')))
                else:
                    self.log.info("waitting device connect, device info:%s" % subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', '))
                fail_time += 1
                cur = time.time()
        else:
            raise TimeoutError('device connect timeout.')
            # self.log.error('device connect timeout.')

    def wait_device_disconnect(self, timeout=180):
        """
        等待设备adb端口消失
        :param timeout：等待超时时间
        :return 布尔值
        """
        cur = time.time()
        expire = cur + timeout
        fail_time = 1
        while cur < expire:
            if not self.connect_device():
                self.log.info("device disconnect success.")
                return
            else:
                if fail_time > 1:
                    self.log.debug("device disconnect failed %d times, device info:%s" % (fail_time, subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')))
                else:
                    self.log.info("waitting device disconnect, device info:%s" % subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', '))
                fail_time += 1
                cur = time.time()
        else:
            raise TimeoutError('device disconnect timeout.')

    # def wait_device_disconnect(self, timeout:int=None):
    #     if timeout:
    #         start_time = int(time.time())
    #         while True:
    #             if not self.connect_device():
    #                 self.log.info("device disconnect success.")
    #                 return True
    #             else:
    #                 if start_time + timeout < int(time.time()):
    #                     self.log.error('device disconnet timeout')
    #                     return False
    #     else:
    #         fail_time = 1
    #         while True:
    #             if not self.connect_device():
    #                 self.log.info("device disconnect success.")
    #                 return
    #             else:
    #                 if fail_time > 1:
    #                     self.log.debug("device disconnect failed %d times, device info:%s" % (fail_time, subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')))
    #                 else:
    #                     self.log.error("device disconnect failed, device info:%s" % subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', '))
    #                 fail_time += 1
    #                 time.sleep(2)

    def reboot(self):
        if self.connect_device():
            subprocess.getoutput(' '.join([self.adb, 'reboot']))
        # while not self.connect_device():
        #     device_info = subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')
        #     if 'offline' in device_info:
        #         self.log.error('device offline, restart adb server.')
        #         subprocess.getoutput(' '.join([self.adb, 'kill-server']))
        #         subprocess.getoutput(' '.join([self.adb, 'start-server']))
        #     time.sleep(1)
        # self.log.info('device reboot success.')

    def connect_network(self):
        """
        判断网络是否连接
        :return: 布尔值
        """
        if self.connect_device():
            try:
                # ping = subprocess.getoutput('adb -s ' + self.device_id + ' shell ping -c 4 www.baidu.com')
                ping = subprocess.getoutput(' '.join([self.adb, 'shell ping -c 4 www.baidu.com']))
                if '4 packets transmitted' in ping:
                    # self.log.debug("network connect success.")
                    return True
                else:
                    # self.log.error("network connect failed.")
                    return False
            except Exception as e:
                print(e)
                return False


    def wait_network_connect(self, timeout=180):
        cur = time.time()
        expire = cur + timeout
        fail_time = 1
        while cur < expire:
            if self.connect_network():
                self.log.info("network connect success.")
                return
            else:
                if fail_time > 1:
                    self.log.debug("network connect failed %d times." % fail_time)
                else:
                    self.log.info("waitting network connect.")
                fail_time += 1
                cur = time.time()
        else:
            raise TimeoutError('network connect timeout.')


    def get_current_version(self):
        try:
            ver = subprocess.check_output(' '.join([self.adb, 'shell getprop ro.fota.version'])).decode(r'GBK').strip()
            self.log.info("current version: %s", ver)
            return ver
        except Exception as e:
            print(e)
            return None

    def get_ext_version(self):
        try:
            ver = subprocess.getoutput(' '.join([self.adb, 'shell "cat data/fota/build_ext.prop | grep ro.fota.version"']))
            ret = ver.split('=')
            version = ret[1]
            return version
        except Exception as e:
            print(e)

    def get_built_type(self):
        try:
            ver = subprocess.check_output(' '.join([self.adb, 'shell getprop ro.build.type'])).decode(r'GBK').strip()

            return ver
        except Exception as e:
            print(e)
            return None

    def search_port(self, dlg_info="SPRD LTE DIAG"): # dlg_info="SPRD LTE DIAG"
        plist = list(serial.tools.list_ports.comports())
        print(plist)
        if len(plist) <= 0:
            return None
        else:
            for portinfo in plist:
                print(portinfo.description)
                if dlg_info in portinfo.description:
                    # print("port descriptor: %s, port: %s", portinfo.description, portinfo.device)
                    self.log.info("port descriptor: %s, port: %s", portinfo.description, portinfo.device)
                    return portinfo.device
            else:
                return None

    def dev_root(self, port):
        at = at_cmd(port)
        if not at.ser_init():
            return False
        # result,info = at.at_hexcmd_exec("7e 4c 9f 83 70 16 00 68 00 61 74 2b 73 65 74 61 64 62 72 6f 6f 74 0d 7e", 5, "OK")
        result = at.at_hexcmd_exec(bytes().fromhex("7e4c9f83701600680061742b736574616462726f6f740d7e"), 5, "OK")
        if result:
            self.wait_device_connect()
            return True
        else:
            return False

    def root_by_at(self):
        port = self.search_port()
        if port:
            return self.dev_root(port)
        else:
            self.log.error('Unable to get root permission.')
            return False

    def turnOnAirplaneMode_byAt(self):
        port = self.search_port(dlg_info="SPRD LTE AT")
        if port:
            at = at_cmd(port)
            if not at.ser_init():
                return False
            result = at.at_cmd_exec('at+cgatt=0', 5, "OK")
            if result:
                return True
            else:
                return False
        else:
            self.log.error('Unable to turn on airplane mode.')
            return False

    def turnOffAirplaneMode_byAt(self):
        port = self.search_port(dlg_info="SPRD LTE AT")
        if port:
            at = at_cmd(port)
            if not at.ser_init():
                return False
            result = at.at_cmd_exec('at+cgatt=1', 5, "OK")
            if result:
                return True
            else:
                return False
        else:
            self.log.error('Unable to turn on airplane mode.')
            return False

    def send_at_command(self, dlg_info, cmd, expire_response, timeout:int=5):
        '''
        发送at命令
        :param dlg_info: 1、展讯平台dlg_info="SPRD LTE AT"；2、高通平台直接指定COM端口，如dlg_info="COM373"
        :param cmd: 发送的at命令
        :return:
        '''
        if "COM" in dlg_info:
            port = dlg_info
        else:
            port = self.search_port(dlg_info=dlg_info)
        if port:
            at = at_cmd(port)
            if not at.ser_init():
                return False
            result = at.at_cmd_exec(cmd, timeout, expire_response)
            if result:
                return True
            else:
                return False
        else:
            self.log.error('Unable to send at command.')
            return False

    def root_by_adb(self):
        res = os.system('adb root')
        if res:
            self.log.error('Unable to get root permission.')
            return False
        else:
            return True

    def root_by_broadcast(self):
        res = os.system(' '.join([self.adb, 'shell am broadcast -n com.ukl.factory/.UklRootReceiver -a android.intent.action.OpenRoot']))
        if res:
            self.log.error('Unable to get root permission.')
            return False
        else:
            return True

    def get_product_name(self):
        res = subprocess.getstatusoutput(' '.join([self.adb, 'shell getprop ro.fota.device']))
        if res[0] == 0:
            return res[1]
        else:
            self.log.error('get product name failed,error info:%s' % res)
            return None


    def _is_root(self):
        ver_type = self.get_built_type()
        if ver_type is not None and "userdebug" in ver_type:
            return self.root_by_adb()
        else:
            return self.root_by_at()

    def root(self):
        at_root_list = ['U3C', 'M2S18', 'G4S18', 'P3S18']
        broadcast_root_list = ['U3Q19']
        installApk_root_list = ['G4SQ19']
        product_name = self.get_product_name()
        if product_name in at_root_list:
            return self.root_by_at()
        elif product_name in broadcast_root_list:
            return self.root_by_broadcast()
        elif product_name in installApk_root_list:
            return self.root_by_installAPK()


    def wipe_data(self):
        """
        恢复出厂设置
        :return:
        """
        root = self.root()
        if root:
            cmd = ' '.join([self.adb, 'shell "echo \"--wipe_data\" > /cache/recovery/command"'])
            print(cmd)
            cmd_excute = subprocess.getstatusoutput(cmd)
            res = subprocess.getoutput(' '.join([self.adb, 'reboot recovery']))
            print(cmd_excute)

    def local_update(self, upgradePackage_file):
        # if not self._is_root():
            # return

        self.log.info(' 准备本地升级，请勿关机...')
        # remove = subprocess.getoutput('adb -s ' + device_id + ' shell rm /data/update.zip')  # 删除升级路径原来存在的升级包
        remove = subprocess.getoutput(' '.join([self.adb, 'shell rm /data/update.zip']))  # 删除升级路径原来存在的升级包
        time.sleep(2)
        # push = subprocess.getstatusoutput('adb -s ' + device_id + ' push ./FOTATEST_G4SQ19_TSV2.1.000.006.190919_202549_user.zip /data/update.zip')  # 将目标升级包push到升级路径
        push = subprocess.getstatusoutput(' '.join([self.adb, 'push', upgradePackage_file, '/data/update.zip']))  # 将目标升级包push到升级路径
        self.log.info('push: %s' % push[0])
        time.sleep(2)
        while 0 not in push:
            time.sleep(10)
            push = subprocess.getstatusoutput(' '.join([self.adb, 'push', upgradePackage_file, '/data/update.zip']))  # 将目标升级包push到升级路径
            # push = subprocess.getstatusoutput('adb -s ' + device_id + ' push ./FOTATEST_G4SQ19_TSV2.1.000.006.190919_202549_user.zip /data/update.zip')
        else:
            # cammand = subprocess.getoutput('adb -s ' + device_id + ' shell "echo "--update_package=/data/update.zip" > /cache/recovery/command"')  # 将升级标志位写到cache/command
            cammand = subprocess.getoutput(' '.join([self.adb, 'shell "echo "--update_package=/data/update.zip" > /cache/recovery/command"']))  # 将升级标志位写到cache/command
            time.sleep(1)
            # update = subprocess.getoutput('adb -s ' + device_id + ' reboot recovery')  # 重启设备进入recovery模式升级
            update = subprocess.getoutput(' '.join([self.adb, 'reboot recovery']))  # 重启设备进入recovery模式升级
            self.log.info(' 本地升级中，请等待升级完成...')
            # time.sleep(60)

    def pull_fota_log(self):
        if self.connect_device():
            log_file = ' '.join([self.adb, 'pull', '/sdcard/Android/data/com.abupdate.fota_demo_iot/cache/iport_log.txt'])
            pull_log_result = subprocess.getstatusoutput(log_file)
            time.sleep(2)
            while 0 not in pull_log_result:
                pull_log_result = subprocess.getstatusoutput(log_file)

    def pull_log_by_cmd(self, cmd_01, save_file):
        if self.connect_device():
            cmd = ' '.join([cmd_01, save_file])
            pull_log_result = subprocess.getstatusoutput(cmd)
            time.sleep(2)
            while 0 not in pull_log_result:
                pull_log_result = subprocess.getstatusoutput(cmd)

    def get_pid(self, process_name):
        # self.wait_device_connect()
        cmd = ' '.join([self.adb, 'shell "ps | grep', process_name, '| grep -v grep | cut -c 9-15"'])
        pid_02 = subprocess.getoutput(cmd)
        pid = pid_02.strip()
        return pid

    def kill_process(self, pid):
        result = {}
        if self.connect_device():
            a = isinstance(pid, list) or isinstance(pid, str)
            if a:
                b = isinstance(pid, str)
                if b:
                    # cmd = ''.join(['adb shell "kill ', pid, '"'])
                    cmd = ' '.join([self.adb, 'shell "kill', pid, '"'])
                    kill_result = subprocess.getstatusoutput(cmd)
                    result[pid] = kill_result[0]
                else:
                    for i in pid:
                        # cmd = ''.join(['adb shell "kill ', i, '"'])
                        cmd = ''.join([self.adb, 'shell "kill', i, '"'])
                        kill_result = subprocess.getstatusoutput(cmd)
                        result[i] = kill_result[0]
            else:
                print("参数process不是str或list")
                return
        return result

    def install_apk(self, apk_file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        # cmd_01 = ' '.join(['adb install -i com.glocalme.appstore', apk_file])
        try:
            install_result = subprocess.getstatusoutput(' '.join([self.adb, 'install', apk_file]))
            self.log.info('apk_install_result:%s' % str(install_result))
        except Exception as e:
            print(e)

    def root_by_installAPK(self):
        self.wakey()
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join([self.adb, 'install -i com.glocalme.appstore', settings.G4S_ROOT_APK_FILE])
        install_result = subprocess.getstatusoutput(cmd_01)
        print('apkInstallResult:', install_result)
        self.log.info('apk_install_result:%s' % str(install_result))
        if install_result[0] == 0:
            ui_result = subprocess.getstatusoutput(' '.join([self.adb, 'shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity']))
            print('uiResult:', ui_result)
            time.sleep(1)
            # tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
            tapRootResult = subprocess.getstatusoutput(' '.join([self.adb, 'shell input tap 660 408']))
            print('tapRootResult:', tapRootResult)
            root_state = subprocess.getstatusoutput(' '.join([self.adb, 'shell cd cache']))
            if root_state[0] == 0:
                return True
            else:
                return False
        else:
            self.log.error("root apk install failed.")
            return False

    def push(self, source_file, target_path):
        cmd = ' '.join([self.adb, 'push', source_file, target_path])
        res = subprocess.getstatusoutput(cmd)
        if res[0] == 0:
            return True
        else:
            self.log.error('push error:%s' % str(res))
            return False

    def pull(self, source_file, target_path):
        cmd = ' '.join([self.adb, 'pull', source_file, target_path])
        res = subprocess.getstatusoutput(cmd)
        if res[0] == 0:
            return True
        else:
            self.log.error('pull error:%s' % str(res))
            raise FileNotFoundError()
            return False

    def uiautomator2_init(self):
        self.install_apk(settings.APPUIAUTOMATOR_APK_FILE)
        self.install_apk(settings.APPUIAUTOMATORTEST_APK_FILE)
        self.push(source_file=settings.atx_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_so_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minitouch_file, target_path='/data/local/tmp/')

    def file_exists(self, file):
        '''
        Determine if the file exists.
        :param file: The file path to determine
        :return: bool
        '''
        # cmd =  ' '.join([self.adb, 'shell "[ -f /sdcard/test_fil.zip ] && echo 'found'"'])
        cmd =  ' '.join([self.adb, 'shell "[ -f', file, '] && echo \'found\'"'])
        res = subprocess.getoutput(cmd)
        if res == 'found':
            return True
        else:
            return False

    def ping(self, duration, target):
        '''
        :param
            duration: ping时长，单位：秒
            target：ping的目标
        :return
            transmitted_packets: ping包的总数量
            lost_packets：丢包的数量
            packet_loss：丢包率
        '''
        cur = time.time()
        expire = cur + duration
        transmitted_packets = 0
        lost_packets = 0
        while cur < expire:
            # res = subprocess.getoutput("adb -s 1d2dce87 shell ping -c 1 www.baidu.com")
            res = subprocess.getoutput(' '.join([self.adb, 'shell ping -c 1', target]))
            if "1 packets transmitted, 1 received" in res:
                transmitted_packets += 1
            else:
                lost_packets += 1
                self.log.error(res)
            time.sleep(0.8)
            cur = time.time()
        packet_loss = round((lost_packets / transmitted_packets), 2)    # 丢包率
        self.log.info("%d packets transmitted, %d received, %.2f%% packet loss" % (transmitted_packets, transmitted_packets - lost_packets, packet_loss))
        # print("%d packets transmitted, %d received, %d%% packet loss" % (transmitted_packets, transmitted_packets - lost_packets, int(lost_packets / transmitted_packets)))
        return transmitted_packets, lost_packets, packet_loss

    def wifi_info(self):
        res = subprocess.getoutput(" ".join([self.adb, "shell \"cat productinfo/ucloud/softap_oem.cfg\""]))
        ssid_regex = re.compile("[a-zA-Z]+_[\w]+")
        password_regex = re.compile("\d{8}")
        ssid = ssid_regex.findall(res)[0]
        password = password_regex.findall(res)[0]
        return ssid, password

    def start_activity(self, package_name, activity):
        cmd = "".join([self.adb, " shell \"am start -n ", package_name, "/", activity])
        subprocess.getoutput(cmd)

    def stop_cloudsim(self):
        cmd = " ".join([self.adb, "shell \"am broadcast -a com.ucloudlink.cmd.logout\""])
        subprocess.getoutput(cmd)

class G3(Glocalme):
    def apk_install(self, file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join([self.adb, 'install -r -i com.glocalme.appstore', file])
        try:
            install_result = subprocess.getstatusoutput(cmd_01)
            self.log.debug('apk_install_result:%s' % str(install_result))
            if install_result[0] == 0:
                return True
            else:
                return False
        except Exception as e:
            self.log.debug(e)
            return False

    def uiautomator2_init(self):
        self.apk_install(settings.APPUIAUTOMATOR_APK_FILE)
        self.apk_install(settings.APPUIAUTOMATORTEST_APK_FILE)
        self.push(source_file=settings.atx_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_so_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minitouch_file, target_path='/data/local/tmp/')

class G4S(Glocalme):
    def apk_install(self, file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join([self.adb, 'install -r -i com.glocalme.appstore', file])
        try:
            install_result = subprocess.getstatusoutput(cmd_01)
            self.log.debug('apk_install_result:%s' % str(install_result))
            if install_result[0] == 0:
                return True
            else:
                return False
        except Exception as e:
            self.log.debug(e)
            return False

    def root(self):
        self.apk_install(settings.G4S_ROOT_APK_FILE)
        # ui_result = subprocess.getstatusoutput(r"adb shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity")
        ui_result = subprocess.getstatusoutput(' '.join([self.adb, 'shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity']))
        self.log.debug('open root ui result: %s' % str(ui_result))
        time.sleep(1)
        # 判断设备是否root，如果未root，执行root
        # root_state = subprocess.getstatusoutput(r"adb shell cd cache")
        root_state = subprocess.getstatusoutput(' '.join([self.adb, 'shell cd cache']))
        self.log.debug("root_state:%s" % str(root_state))
        if root_state[0] != 0:
            # tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
            tapRootResult = subprocess.getstatusoutput(' '.join([self.adb, 'shell input tap 660 408']))
            self.log.debug('tap root button result: %s' % str(tapRootResult))
        time.sleep(5)

    def remove_root(self):
        # ui_result = subprocess.getstatusoutput(r"adb shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity")
        ui_result = subprocess.getstatusoutput(' '.join([self.adb, 'shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity']))
        self.log.debug('open root ui result: %s' % str(ui_result))
        time.sleep(1)
        # 判断设备是否root，如果root，去掉root权限
        # root_state = subprocess.getstatusoutput(r"adb shell cd cache")
        root_state = subprocess.getstatusoutput(' '.join([self.adb, 'shell cd cache']))
        self.log.debug("root_state:%s" % str(root_state))
        if root_state[0] == 0:
            # tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
            tapRootResult = subprocess.getstatusoutput(' '.join([self.adb, 'shell input tap 660 408']))
            self.log.debug('tap root button result: %s' % str(tapRootResult))

    def uiautomator2_init(self):
        self.apk_install(settings.APPUIAUTOMATOR_APK_FILE)
        self.apk_install(settings.APPUIAUTOMATORTEST_APK_FILE)
        self.push(source_file=settings.atx_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minicap_so_file, target_path='/data/local/tmp/')
        self.push(source_file=settings.minitouch_file, target_path='/data/local/tmp/')

    def login_type(self):
        '''
                判断设备登陆类型是云卡还是实体卡
                :return:
                    1、return 0或者没有值表示登陆类型是实体卡登陆
                    2、return 1 表示设备登陆类型是云卡登陆
                    3、return 2 表示登陆类型是软种子卡
                '''
        res = subprocess.getstatusoutput(' '.join([self.adb, 'shell getprop gsm.ukelink.cardtype']))
        if res[0] == 0:
            if res[1] == '0,0' or res[1] == ',0':
                return 0
            elif res[1] == '1,0':
                return 1
            elif res[1] == '2,0':
                return 2
            else:
                self.log.error('gsm.ukelink.cardtype:%s' % res[1])
                return None
        else:
            self.log.error("execute cmd to get gsm.ukelink.cardtype failed.")
            return None

    def pull_iportLog(self, target_path):
        """
        导出设备iport日志
        :return：返回iport日志的绝对路径
        """
        self.pull(source_file="/sdcard/Android/data/com.abupdate.fota_demo_iot/cache/iport_log.txt", target_path=target_path)
        if os.path.isfile(target_path):
            return target_path
        else:
            iportLog_file = "/".join([target_path, "iport_log.txt"])
            return iportLog_file

    def next_check_time(self, iportLog_file):
        """
        获取下次fota升级周期检测的时间
        :param:
            iportLog_file：iport日志的绝对路径
        :return：
            next_check_time:下次周期检测的时间
            next_check_timestamp:下次周期检测时间的时间戳
        """
        with open(iportLog_file, "r", encoding="utf-8") as f:
            res = ""
            lines = f.readlines()
            for line in lines:
                if "setAlarm() start time" in line:
                    res = line.strip("\r\n")
            next_check_time = re.findall('(?<=start time:).*$', res)[0]
        # 将下次周期检测的时间转换为时间戳
        next_check_timestamp = time.mktime(time.strptime(next_check_time, "%Y-%m-%d %H:%M:%S"))
        self.log.info("下个周期检测时间：%s" % next_check_time)
        return next_check_time, next_check_timestamp

    def set_system_time(self, timestamp):
        """
        设置设备的系统时间
        :param: timestamp：时间戳
        """
        set_system_time = time.strftime("%m%d%H%M%Y", time.localtime(timestamp))
        cmd = " ".join([self.adb, "shell \"date", set_system_time, "set\""])
        res = subprocess.getstatusoutput(cmd)
        if res[0] == 0:
            self.log.info("set system time success")
            return True
        else:
            self.log.error("set system time failed")
            raise PermissionError("set system time failed, the device may not have root.")
            return False

class U3(Glocalme):
    def root(self):
        return self.root_by_broadcast()

    def login_type(self):
        '''
        判断设备登陆类型是云卡还是实体卡
        :return:
            1、return 0或者没有值表示登陆类型是实体卡登陆
            2、return 1 表示设备登陆类型是云卡登陆
            3、return 2 表示登陆类型是软种子卡
        '''
        res = subprocess.getstatusoutput(' '.join([self.adb, 'shell getprop gsm.ukelink.cardtype']))
        if res[0] == 0:
            if res[1] == '0' or res[1] == '':
                return 0
            elif res[1] == '1':
                return 1
            elif res[1] == '2':
                return 2
        else:
            sim_state = subprocess.getstatusoutput(' '.join([self.adb, 'shell getprop gsm.sim.state']))
            if sim_state[0] == 0 and sim_state[1] == 'LOADED,LOADED':
                return 0
            else:
                self.log.error('sim state：%s' % sim_state[1])
                return None

class G4(Glocalme):
    def pull_iportLog(self, target_path):
        """
        导出设备iport日志
        :return：返回iport日志的绝对路径
        """
        self.pull(source_file="/sdcard/Android/data/com.abupdate.fota_demo_iot/cache/iport_log.txt", target_path=target_path)
        if os.path.isfile(target_path):
            return target_path
        else:
            iportLog_file = "/".join([target_path, "iport_log.txt"])
            return iportLog_file

    def next_check_time(self, iportLog_file):
        """
        获取下次fota升级周期检测的时间
        :param:
            iportLog_file：iport日志的绝对路径
        :return：
            next_check_time:下次周期检测的时间
            next_check_timestamp:下次周期检测时间的时间戳
        """
        with open(iportLog_file, "r", encoding="utf-8") as f:
            res = ""
            lines = f.readlines()
            for line in lines:
                if "setAlarm() start time" in line:
                    res = line.strip("\r\n")
            next_check_time = re.findall('(?<=start time:).*$', res)[0]
        # 将下次周期检测的时间转换为时间戳
        next_check_timestamp = time.mktime(time.strptime(next_check_time, "%Y-%m-%d %H:%M:%S"))
        self.log.info("下个周期检测时间：%s" % next_check_time)
        return next_check_time, next_check_timestamp

    def set_system_time(self, timestamp):
        """
        设置设备的系统时间
        :param: timestamp：时间戳
        """
        set_system_time = time.strftime("%m%d%H%M%Y", time.localtime(timestamp))
        cmd = " ".join([self.adb, "shell \"date", set_system_time, "set\""])
        res = subprocess.getstatusoutput(cmd)
        if res[0] == 0:
            self.log.info("set system time success")
            return True
        else:
            self.log.error("set system time failed")
            raise PermissionError("set system time failed, the device may not have root.")
            return False

class U5(Glocalme):
    def get_version(self):
        res = subprocess.check_output(' '.join([self.adb, 'shell \"grep ro.build.version /etc/build.prop\"'])).decode(r'GBK').strip()
        version = res.split("=")[1]
        return version

    def local_update(self, upgradePackage_file):
        self.push(source_file=upgradePackage_file, target_path="/cache/fota/ipth_package.bin")
        subprocess.getstatusoutput(' '.join([self.adb, 'reboot recovery']))
        self.log.info("本地升级中，请等待升级完成...")


class Logger:
    def __init__(self, file_output=True, screen_output=False, log_level=None, log_file=None):
        self._level_list = ['logging.DEBUG', 'logging.INFO', 'logging.WARNING ', 'logging.ERROR', 'logging.CRITICAL']
        self.file_output = file_output
        self.screen_output = screen_output
        self.log_level = log_level
        if self.log_level:
            if not isinstance(self.log_level, str):
                raise TypeError("log_level is not str")
            if self.log_level not in self._level_list:
                raise ValueError('log_levle must be one of the following lists:%s' % self._level_list)
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
            log_path = '/'.join([os.path.dirname(__file__), time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))])
            log_name = '.'.join([log_path, 'log'])
            # log_path = '/'.join([BASEDIR, 'logs', time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))])
            # log_name = '.'.join([log_path, 'log'])
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

if __name__ == '__main__':
    u3x = U3()
    # wifi = u3x.wifi_info()
    # print(wifi)
    u3x.root_by_at()
    time.sleep(3)
    u3x.local_update(upgradePackage_file='C:\\Users\\xuhong\\Desktop\\update.zip')