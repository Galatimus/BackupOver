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
    profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/s352ajck.default/') #Gui1
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
    driver.get(url)
    time.sleep(10)
    try:
        uliza = driver.title
    except (NoSuchElementException,WebDriverException):
        uliza = ''

    try:
        try:
            dom = driver.find_element_by_xpath(u'//button[contains(text(),"Показать телефоны")]/preceding-sibling::a').get_attribute('href').replace('tel:','')
        except (NoSuchElementException,IndexError,WebDriverException):
            dom = re.findall(u'tel:(.*?)"',driver.page_source)[0]
    except (NoSuchElementException,IndexError,WebDriverException):
        dom = ''
    try:
        side = driver.find_element_by_xpath(u'//a[contains(@href,"link")][contains(text(),".")]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        side = ''    
        
    print('*'*10)
    print uliza
    print dom
    print side
    print('*'*10)
    ws.write_string(result, 0, uliza)
    ws.write_string(result, 1, dom)
    ws.write_string(result, 2, side)
    time.sleep(2)


def main(url):
    try:
        take_content(driver,url)
    except (TimeoutException,WebDriverException):
        pass
      
    


if __name__ == '__main__':
    l= open('gis_new.txt').read().splitlines()
    workbook = xlsxwriter.Workbook(u'0001-0002_00_C_001-0217_GIS_P4.xlsx')    
    ws = workbook.add_worksheet()
    ws.write(0, 0, u"НАЗВАНИЕ_ОРГАНИЗАЦИИ МЕСТОПОЛОЖЕНИЕ")
    ws.write(0, 1, u"ТЕЛЕФОН")
    ws.write(0, 2, u"ВЕБ_САЙТ_ОРГАНИЗАЦИИ")
    result= 1
    driver = get_firefox_drive()
    driver.set_window_size(800,800)
    time.sleep(5)
    try:
        for p in range(len(l)):
            print '**',p,'/',len(l),'**'
            main(l[p])
            result+=1  
    except KeyboardInterrupt:
        pass
    print('Save it...')
    time.sleep(1)
    workbook.close()
    time.sleep(2)
    driver.close()
    print('Done')    
    
    
    
