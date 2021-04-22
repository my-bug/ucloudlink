#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''
import subprocess, time, serial, os
from config import settings
import serial.tools.list_ports

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
            self.cmd_01 = 'adb'
        else:
            self.cmd_01 = 'adb -s'
        if log_project:
            self.log = log_project
        else:
            import logging
            self.log = logging

    def wakey(self):
        try:
            # 设置当usb接入时屏幕常亮
            subprocess.Popen(' '.join([self.cmd_01, self.device_id, 'shell svc power stayon usb']))
            self.log.debug("wakey successfully.")
        except Exception as e:
            self.log.error("wakey failed:%s" % e)

    def connect_device(self):
        # 检查设备是否连接
        # self.log.debug("try to connect device")
        try:
            # 获取设备列表信息，并用“\r\n”拆分
            device_info = subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ', ')
            # if device_info is not None and self.device_id in device_info and 'device' in device_info:
            if device_info.endswith('device'):
                self.log.debug("device connect success.")
                return True
            else:
                self.log.error("device connect failed, device info:%s" % device_info)
                return False
        except Exception as e:
            print(e)
            return False


    def wait_device_connect(self):
        while True:
            if self.connect_device():
                self.log.info("device connect success.")
                return
            else:
                time.sleep(5)

    def wait_device_disconnect(self):
        while True:
            if not self.connect_device():
                self.log.info("device disconnect success.")
                return
            else:
                time.sleep(2)

    def device_reboot(self):
        if self.connect_device():
            subprocess.getoutput(' '.join([self.cmd_01, self.device_id, 'reboot']))

    def connect_network(self):
        # 检查设备网络是否连接
        self.log.debug("try to connect network.")
        while True:
            if self.connect_device():
                try:
                    # ping = subprocess.getoutput('adb -s ' + self.device_id + ' shell ping -c 4 www.baidu.com')
                    ping = subprocess.getoutput(' '.join([self.cmd_01, self.device_id, 'shell ping -c 4 www.baidu.com']))
                    if '4 packets transmitted' in ping:
                        self.log.debug("network connect success.")
                        return True
                    else:
                        self.log.error("network connect failed.")
                        return False
                except Exception as e:
                    print(e)
                    return False
            else:
                time.sleep(2)

    def wait_network_connect(self):
        while True:
            if self.connect_network():
                self.log.info("network connect success.")
                return
            else:
                time.sleep(1)


    def get_current_version(self):
        try:
            # ver = subprocess.check_output("adb shell getprop ro.fota.version").decode(r'GBK').strip()
            ver = subprocess.check_output(' '.join([self.cmd_01, self.device_id, 'shell getprop ro.fota.version'])).decode(r'GBK').strip()
            self.log.info("current version: %s", ver)
            return ver
        except Exception as e:
            print(e)
            return None

    def get_built_type(self):
        try:
            # ver = subprocess.check_output("adb shell getprop ro.build.type").decode(r'GBK').strip()
            ver = subprocess.check_output(' '.join([self.cmd_01, self.device_id, 'shell getprop ro.build.type'])).decode(r'GBK').strip()

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
            return True
        else:
            return False

    def get_root_by_at(self):
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

    def send_at_command(self, dlg_info, cmd):
        '''

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
            result = at.at_cmd_exec(cmd, 5, "OK")
            if result:
                return True
            else:
                return False
        else:
            self.log.error('Unable to send at command.')
            return False

    def get_root_by_adb(self):
        res = os.system('adb root')
        if res:
            self.log.error('Unable to get root permission.')
            return False
        else:
            return True

    def get_root_for_U3(self):
        res = os.system('adb shell am broadcast -n com.ukl.factory/.UklRootReceiver -a android.intent.action.OpenRoot')
        if res:
            self.log.error('Unable to get root permission.')
            return False
        else:
            return True


    def _is_root(self):
        ver_type = self.get_built_type()
        if ver_type is not None and "userdebug" in ver_type:
            return self.get_root_by_adb()
        else:
            return self.get_root_by_at()

    def local_update(self, upgradePackage_file):
        # if not self._is_root():
            # return

        self.log.info(' 准备本地升级，请勿关机...')
        # remove = subprocess.getoutput('adb -s ' + device_id + ' shell rm /data/update.zip')  # 删除升级路径原来存在的升级包
        remove = subprocess.getoutput(' '.join([self.cmd_01, self.device_id, 'shell rm /data/update.zip']))  # 删除升级路径原来存在的升级包
        time.sleep(2)
        # push = subprocess.getstatusoutput('adb -s ' + device_id + ' push ./FOTATEST_G4SQ19_TSV2.1.000.006.190919_202549_user.zip /data/update.zip')  # 将目标升级包push到升级路径
        push = subprocess.getstatusoutput(' '.join([self.cmd_01, self.device_id, 'push', upgradePackage_file, '/data/update.zip']))  # 将目标升级包push到升级路径
        self.log.info('push: %s' % push[0])
        time.sleep(2)
        while 0 not in push:
            time.sleep(10)
            push = subprocess.getstatusoutput(' '.join([self.cmd_01, self.device_id, 'push', upgradePackage_file, '/data/update.zip']))  # 将目标升级包push到升级路径
            # push = subprocess.getstatusoutput('adb -s ' + device_id + ' push ./FOTATEST_G4SQ19_TSV2.1.000.006.190919_202549_user.zip /data/update.zip')
        else:
            # cammand = subprocess.getoutput('adb -s ' + device_id + ' shell "echo "--update_package=/data/update.zip" > /cache/recovery/command"')  # 将升级标志位写到cache/command
            cammand = subprocess.getoutput(' '.join([self.cmd_01, self.device_id, 'shell "echo "--update_package=/data/update.zip" > /cache/recovery/command"']))  # 将升级标志位写到cache/command
            time.sleep(1)
            # update = subprocess.getoutput('adb -s ' + device_id + ' reboot recovery')  # 重启设备进入recovery模式升级
            update = subprocess.getoutput(' '.join([self.cmd_01, self.device_id, 'reboot recovery']))  # 重启设备进入recovery模式升级
            self.log.info(' 本地升级中，请等待升级完成...')
            # time.sleep(60)

    def pull_fota_log(self):
        if self.connect_device():
            log_file = ' '.join([self.cmd_01, self.device_id, 'pull', '/sdcard/Android/data/com.abupdate.fota_demo_iot/cache/iport_log.txt'])
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

    # def get_pid(self, process):
    #     process_dic = {}
    #     if self.connect_device():
    #         # 判断process类型是否为str或者list
    #         a = isinstance(process, str) or isinstance(process, list)
    #         if a:
    #             b = isinstance(process, str)
    #             if b:
    #                 self.wait_device_connect()
    #                 cmd = ''.join(['adb shell "ps | grep ', process, ' | grep -v grep | cut -c 9-15"'])
    #                 pid_01 = subprocess.getoutput(cmd)
    #                 pid = pid_01.strip()
    #                 process_dic[process] = pid
    #             else:
    #                 for i in process:
    #                     self.wait_device_connect()
    #                     cmd = ''.join(['adb shell "ps | grep ', i, ' | grep -v grep | cut -c 9-15"'])
    #                     pid_02 = subprocess.getoutput(cmd)
    #                     pid = pid_02.strip()
    #                     process_dic[i] = pid
    #         else:
    #             print("参数process不是str或list")
    #             return
    #     return process_dic

    def get_pid(self, process):
        process_dic = {}
        for i in process:
            self.wait_device_connect()
            cmd = ''.join(['adb shell "ps | grep ', i, ' | grep -v grep | cut -c 9-15"'])
            pid_02 = subprocess.getoutput(cmd)
            pid = pid_02.strip()
            process_dic[i] = pid
        return process_dic

    def kill_process(self, process_pid):
        result = {}
        if self.connect_device():
            a = isinstance(process_pid, list) or isinstance(process_pid, str)
            if a:
                b = isinstance(process_pid, str)
                if b:
                    cmd = ''.join(['adb shell "kill ', process_pid, '"'])
                    kill_result = subprocess.getstatusoutput(cmd)
                    result[process_pid] = kill_result[0]
                else:
                    for i in process_pid:
                        cmd = ''.join(['adb shell "kill ', i, '"'])
                        kill_result = subprocess.getstatusoutput(cmd)
                        result[i] = kill_result[0]
            else:
                print("参数process不是str或list")
                return
        return result

    def glocalme_install_apk(self, file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join(['adb install -i com.glocalme.appstore', file])
        try:
            install_result = subprocess.getstatusoutput(cmd_01)
            self.log.info('apk_install_result:%s' % str(install_result))
        except Exception as e:
            print(e)

    def g4s_root(self, file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join(['adb install -i com.glocalme.appstore', file])
        install_result = subprocess.getstatusoutput(cmd_01)
        print('apkInstallResult:',install_result)
        self.log.info('apk_install_result:%s' % str(install_result))
        # root_result = subprocess.getstatusoutput(cmd_02)
        ui_result = subprocess.getstatusoutput(r"adb shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity")
        print('uiResult:',ui_result)
        time.sleep(1)
        tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
        print('tapRootResult:', tapRootResult)


class G4S(Glocalme):
    def apk_install(self, file):
        '''explanation:some glocalme devices need "-i com.glocalme.appstore" to install apk'''
        cmd_01 = ' '.join(['adb install -i com.glocalme.appstore', file])
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
        ui_result = subprocess.getstatusoutput(r"adb shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity")
        self.log.debug('open root ui result: %s' % str(ui_result))
        time.sleep(1)
        # 判断设备是否root，如果未root，执行root
        root_state = subprocess.getstatusoutput(r"adb shell cd cache")
        self.log.debug("root_state:%s" % str(root_state))
        if root_state[0] != 0:
            tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
            self.log.debug('tap root button result: %s' % str(tapRootResult))

    def remove_root(self):
        ui_result = subprocess.getstatusoutput(r"adb shell am start com.ukl.factory/com.ukl.factory.UklFacMainActivity")
        self.log.debug('open root ui result: %s' % str(ui_result))
        time.sleep(1)
        # 判断设备是否root，如果root，去掉root权限
        root_state = subprocess.getstatusoutput(r"adb shell cd cache")
        self.log.debug("root_state:%s" % str(root_state))
        if root_state[0] == 0:
            tapRootResult = subprocess.getstatusoutput(r"adb shell input tap 660 408")
            self.log.debug('tap root button result: %s' % str(tapRootResult))


if __name__ == '__main__':
    from common.logger import Logger
    log = Logger(screen_output=True).create_logger()
    g4s = G4S(log_project=log)
    # g4s = G4S()
    # time.sleep(180)
    # g4s.device_reboot()
    g4s.root()

    # device_info = subprocess.check_output("adb devices").decode(r'GBK').strip().replace('\r\n', ' ')
    # print(device_info)
    # print(type(device_info))
    # if device_info is not None and '' in device_info and 're' in device_info:
    #     print('ok')


