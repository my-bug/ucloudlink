#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
    1、用于test_project_U3自动化项目配置测试相关的信息；
'''

# 测试设备信息配置
test_device_info = {
    'id': '1d2dce87',
    'ssid': 'GlocalMe_799626',
    'password': '08077628',
}

# 辅助机信息配置
auxiliary_device_info = {
    'id': 'c58790e3',
}

# G4设备信息
G4_info = {
    'id': '11c9b534',
}

# pin码
pin = '1234'

if __name__ == '__main__':
    # import uiautomator2 as u2
    # d = u2.connect(auxiliary_device_info['id'])
    # d.app_start("com.android.settings", "com.android.settings.SubSettings")
    # d.swipe(0.5, 0.8, 0.5, 0.5)
    test = all([True, True, False])
    print(test)