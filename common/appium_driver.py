#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''
from appium import webdriver

class Appium_driver:
    def __init__(self, desired_caps):
        self.desired_caps = desired_caps

    def get_driver(self):
        '''获取driver'''
        try:
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.desired_caps)
            return self.driver
        except Exception as e:
            raise e