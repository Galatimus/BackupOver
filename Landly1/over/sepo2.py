#!/usr/bin/python
# -*- coding: utf-8 -*-




import os
import time
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys 
import keyboard
import json
import six
from six.moves.urllib import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


reload(sys)
sys.setdefaultencoding('utf-8')



def get_chrome_drive(driver_path=None):
    
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox') 
    driver = webdriver.Chrome(executable_path='D:\\VMF\\OlegPars\\webshot\\chromedriver\\chromedriver.exe',chrome_options=options,service_args=['--verbose']) 
    return driver

def get_firefox_drive(driver_path=None):
    
    profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/xys9r0ld.default/') #Gui1
    #profile = webdriver.FirefoxProfile()#Gui2
    #profile.set_preference('permissions.default.stylesheet', 2)
    #profile.set_preference('permissions.default.image', 2)
    #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    #profile.set_preference("javascript.enabled", False)

    
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
     "httpProxy":'127.0.0.1:24000',
     "sslProxy":'127.0.0.1:24000',
     "noProxy":[],
     "proxyType":"MANUAL"

    }
    
    profile.native_events_enabled = False
    #options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,service_log_path=None,timeout=90)
    #driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)
    return driver

def take_content(driver, url):
    # get the page
    driver.get(url)
    time.sleep(3)
    #WebDriverWait(driver,10).until(EC.alert_is_present(),"wait for alert pop out")
    #alert_window=driver.switch_to_alert()
    #alert_window.send_keys("User Name")
    #time.sleep(5)
    #alert_window.send_keys(Keys.TAB)
    #time.sleep(5)
    #alert_windows.send_keys("passwd")   
    time.sleep(20)
     


def main(url):
    driver = get_firefox_drive()
    driver.set_window_size(800,800)
    time.sleep(5) 
    try:
        take_content(driver,url)
    except TimeoutException:
        pass
    
    driver.quit()
    time.sleep(1)    
    return


if __name__ == '__main__':
    l= open('shorte.txt').read().splitlines()
    try:
        for p in range(len(l)):
            print '******',p,'/',len(l),'******'
            main(l[p])
    except KeyboardInterrupt:
        pass
    print('Save it...')
    time.sleep(2)
    print('Done')    
    
    
    
