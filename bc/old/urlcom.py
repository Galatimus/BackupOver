#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import logging
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import re
import math
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException





profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/46stx7t7.default/')#Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/')#Gui2
profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)



driver.set_window_position(0,0)
driver.set_window_size(800,385)

time.sleep(5)

i = 0
l= open('old/comm.txt').read().splitlines()

page ='arenda-pomesheniya/'
   
logging.basicConfig(level=logging.ERROR)



while True:
    try:
        driver.get(l[i]+page)
    except IndexError:
        if page =='arenda-pomesheniya/':
            i = 0
            l= open('old/comm.txt').read().splitlines()
            page ='prodazha-pomesheniya/'
            time.sleep(2)
            continue
        else:
            print'DONE_ALL'
            driver.close()
            time.sleep(2)
            #os.remove('/home/oleg/pars/bc/geckodriver.log')
            #time.sleep(2)
            break
    time.sleep(1)
    lin = []
    driver.find_element_by_xpath(u'//a[@class="color-red uderlined-dots"]').click()
    time.sleep(5)
    nums = re.sub('[^\d]','',driver.find_element_by_xpath(u'//span[@class="color-red ss"]').text)
    pag = int(math.ceil(float(int(nums))/float(16)))
    print pag
    for x in range(1,pag+1):
        url_next = l[i]+page+'?page=%d'%x
        print('*'*10)
        print "Next Page is ..." ,url_next,str(pag)
        driver.get(url_next) 
        time.sleep(2)        
        for link in driver.find_elements_by_xpath(u'//a[@itemprop="url"]'):
            url = link.get_attribute('href')   
            print url
            lin.append(url)
    print '***',len(lin),'/',str(nums),'**********',i+1,'/',len(l),'********'
    time.sleep(1)
    links = open('bc_com.txt', 'a')
    for item in lin:
        links.write("%s\n" % item)
    links.close()            
    time.sleep(1)            
    print'SAVE...',len(lin),' and NEXT'
    print('*'*10)
    time.sleep(3)
    #driver.delete_all_cookies()
    i=i+1 
    
#time.sleep(5)
#os.system("/home/oleg/pars/bc/comm.py")




