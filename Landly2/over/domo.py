#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException




def get_firefox_drive(driver_path=None):

    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/s352ajck.default/') #Gui1
    #profile = webdriver.FirefoxProfile()#Gui2
    #profile.set_preference('permissions.default.stylesheet', 2)
    #profile.set_preference('permissions.default.image', 2)
    #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    #profile.set_preference("javascript.enabled", False)
    profile.native_events_enabled = False
    #driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)
    driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',service_log_path=None,timeout=90)
    return driver

def take_content(driver, url):
    lin = []
    driver.get(url)
    time.sleep(5)
    l= open('../city.txt').read().splitlines()
    for p in range(len(l)):
        print '**',p,'/',len(l),'**'
        time.sleep(1)
        driver.find_element_by_name('searchInputBox').send_keys(l[p]+', USA')
        time.sleep(1)
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="expanded-row-content"]/div')))
            print "Page is ready!"
            time.sleep(1)
            my_ulrs = driver.find_element_by_xpath(u'//a[@class="item-title block"][contains(@href,"city")]').get_attribute('href')
            time.sleep(1)
            print my_ulrs
            lin.append(my_ulrs)
            time.sleep(1)
            driver.find_element_by_name('searchInputBox').clear()
        except (TimeoutException,WebDriverException,UnicodeDecodeError):
            time.sleep(1)
            driver.find_element_by_name('searchInputBox').clear()
            continue
    write_urls(lin)
    
    
def write_urls(lin):
    lin = list(set(lin))
    print '*Save*',len(lin),'*'
    links = open('redfin.txt', 'a')
    for item in lin:
        links.write("%s\n" % item)
    links.close()
    time.sleep(1)
    
  


def main(url): 
    driver = get_firefox_drive()
    driver.set_window_size(800,800)    
    time.sleep(5)    
    try:
        take_content(driver,url)
    except (TimeoutException,WebDriverException):
        pass
    #driver.quit()
    


if __name__ == '__main__':    
    main('https://www.redfin.com/')
    time.sleep(2)
    print('Done') 
        
