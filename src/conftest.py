# #!/usr/bin/env python
# # _*_ coding:utf-8 _*_
# __author__ = 'Curry'
# '''
# description:
# '''
# import pytest
# from selenium import webdriver
# from py._xmlgen import html
#
# _driver = None
# # 测试失败时添加截图和测试用例描述(用例的注释信息)
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """当测试失败的时候，自动截图，展示到html报告中"""
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_")+".png"
#             screen_img = _capture_screenshot()
#             if file_name:
#                 html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
# def _capture_screenshot():
#     '''截图保存为base64'''
#     return _driver.get_screenshot_as_base64()
#
# @pytest.fixture(scope='module')
# def driver():
#     global _driver
#     print('------------open browser------------')
#     _driver = webdriver.Firefox()
#
#     yield _driver
#     print('------------close browser------------')
#     _driver.quit()
#
# #coding:utf-8
#
# from selenium import webdriver
# import pytest
# driver = None
#
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#     Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_")+".png"
#             _capture_screenshot(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'οnclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#
# def _capture_screenshot(name):
#     driver.get_screenshot_as_file(name)
#
#
# @pytest.fixture(scope='session', autouse=True)
# def browser():
#     global driver
#     if driver is None:
#         driver = webdriver.Chrome()
#     return driver