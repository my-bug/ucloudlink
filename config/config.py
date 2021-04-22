#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

import configparser
import os


class Config(object):
    def __init__(self, config_file="/".join([os.path.dirname(__file__), "config.ini"])):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


global_config = Config()

if __name__ == '__main__':
    serialno = global_config.get("config-U3", "u3_serialno")
    print(type(serialno))
    print(serialno)
    print(os.path.dirname(__file__))