#!/usr/bin/python
# -*- coding: utf-8 -*-




import os
import time
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException
from selenium.webdriver.common.proxy import *


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
    
    
    #PROXY_HOST = "46.17.47.134"    
    #PROXY_PORT = 8080    
    #USERNAME = "Ivan"     
    #PASSWORD = "tempuvefy"
    myProxy = "46.17.47.134:8080"
    
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy, # set this value as desired
        'ftpProxy': myProxy,  # set this value as desired
        'sslProxy': myProxy,  # set this value as desired
        'noProxy': '',        # set this value as desired
        'socksUsername': 'Ivan',
        'socksPassword': 'tempuvefy',
        })    

    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    #profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/s352ajck.default/') #Gui1
    profile = webdriver.FirefoxProfile()#Gui2
    #profile.set_preference('permissions.default.stylesheet', 2)
    #profile.set_preference('permissions.default.image', 2)
    #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    #profile.set_preference("javascript.enabled", False)
    profile.set_preference("network.proxy.type", 1)    
    #profile.set_preference("network.proxy.http", PROXY_HOST)
    profile.set_preference("network.proxy.http", "http://Ivan:tempuvefy@46.17.47.134:8080")
    #profile.set_preference("network.proxy.http_port", PROXY_PORT)    
    #profile.set_preference("network.proxy.socks_username", USERNAME)    
    #profile.set_preference("network.proxy.socks_password", PASSWORD)    
    profile.native_events_enabled = False
    #profile.update_preferences()
    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,service_log_path=None,timeout=90)
    return driver

def take_content(driver, url):
    # get the page
    driver.get(url)
    time.sleep(100)
     


def main(url):
    driver = get_firefox_drive()
    driver.set_window_size(800,800)
    time.sleep(5) 
    try:
        take_content(driver,url)
    except (TimeoutException,WebDriverException):
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
    
    
    
