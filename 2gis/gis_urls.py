#!/usr/bin/python
# -*- coding: utf-8 -*-



import math
import os
import re
import time
from datetime import datetime,timedelta
import xlsxwriter
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException


def get_firefox_drive(driver_path=None):

    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/6om1w25z.default-esr/') #Gui1
    #profile = webdriver.FirefoxProfile()#Gui2
    #profile.set_preference('permissions.default.stylesheet', 2)
    profile.set_preference('permissions.default.image', 2)
    #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    #profile.set_preference("javascript.enabled", False)
    profile.native_events_enabled = False
    #driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)
    driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',service_log_path=None,timeout=90)
    return driver

def take_content(driver, url):
    # get the page
    lin = []
    driver.get(url)
    time.sleep(10)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #time.sleep(1)
    for link in driver.find_elements_by_xpath(u'//a[contains(@href,"firm")]'):
        url = link.get_attribute('href').split('?')[0]   
        print url
        lin.append(url)
    write_urls(lin)
        
        
  
def write_urls(lin):
    lin = list(set(lin))
    print '*Save*',len(lin),'*'
    links = open('gis_new.txt', 'a')
    for item in lin:
        links.write("%s\n" % item)
    links.close()
    time.sleep(1)

def main(url):
    
    try:
        take_content(driver,url)
    except (TimeoutException,WebDriverException):
        pass

if __name__ == '__main__':
    driver = get_firefox_drive()
    driver.set_window_size(800,800)
    for x in range(1,188):#185
        url = 'https://2gis.ru/moscow/search/Бухгалтерские услуги/rubricId/653/page/'+str(x)
        main(url)
    time.sleep(2)
    driver.close()
    print('Done')    
    
    
    
