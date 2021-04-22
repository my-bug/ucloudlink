#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Curry'
'''
description:
'''

import pytest, os, time, subprocess
from src.test_case.test_project_G4 import project_name

def main():
    # 获取项目路径
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
    # os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
    current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    # # 创建测试记录保存路径
    # test_record_path = '/'.join([BASEDIR, 'TestRecord', project_name, current_time])
    # if not os.path.exists(test_record_path):
    #     os.makedirs(test_record_path)
    # 报告保存路径
    report_path = '/'.join([BASEDIR, 'reports', project_name])
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    report_name = '/'.join([report_path, '.'.join(['__'.join([project_name, current_time]), 'html'])])
    report = ''.join(['--html=', report_name])
    # report = ''.join(['--html-report=', report_name])


    '''生成html报告的运行方式'''
    # test_case_path = '/'.join([os.path.dirname(__file__), 'test_case', 'test_project_U3.py::Test_CloudSimAndPhysicalSimSwitch::test02'])
    test_case_path = '/'.join([os.path.dirname(__file__), 'test_case', 'test_project_G4.py::Test_Fota'])
    # --self_contained-html参数表示生成独立的html报告（即把CSS样式合并到html里）
    pytest.main(['-s', report, "--self-contained-html", test_case_path])

    """
    '''生成定制测试报告的运行方式'''
    result_file = '/'.join([report_path, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))])
    report_file = '/'.join([result_file, 'report'])
    os.makedirs(report_file)
    test_case_path = '/'.join([os.path.dirname(__file__), 'test_case', 'test_project_U3.py::Test_Display::test01'])
    pytest.main(['-s', '-q', '--alluredir', result_file, test_case_path])
    cmd = ' '.join(['allure generate', result_file, '-o', report_file])
    subprocess.getoutput(cmd)
    """

if __name__ == '__main__':
    main()