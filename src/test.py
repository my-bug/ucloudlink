
"""
def sim(sim:"bool"):
    if sim:
        print("ok")
    else:
        print("not ok")

from common.models import G4S
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time

g4s = G4S()
# g4s.root()
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '8.1.0',
    # 'appPackage': 'com.android.settings',
    # 'appActivity': 'com.android.settings.Settings',
    'newCommandTimeout': '360',
    'deviceName': '11c9b534',
    'noReset': False,
}
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
time.sleep(1)
# g4s.reboot()
g4s.wait_network_connect()
res = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id("com.abupdate.fota_demo_iot:id/tv_new_version"))
# res = driver.find_element_by_id("com.abupdate.fota_demo_iot:id/tv_new_version")
print(res)
# driver.press_keycode(4)
# time.sleep(3)
# driver.press_keycode(3)
# time.sleep(3)
# driver.start_activity(app_package='com.glocalme.g4home', app_activity='com.glocalme.basic.simcard.SimCardActivity')
# driver.start_activity(app_package='com.glocalme.g4home', app_activity='com.glocalme.basic.simcardmanager.SimCardActivityG4P')
# sim_status = driver.find_element_by_id("com.glocalme.g4home:id/st_sim_net").text
# print(sim_status)
"""

import uiautomator2 as u2
from common.models import G3

g3 = G3()
g3.wait_device_connect()
g3.uiautomator2_init()

d = u2.connect()
print(d.info)






