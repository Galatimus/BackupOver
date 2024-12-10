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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')





profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/46stx7t7.default/')#Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/')#Gui2
#profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',firefox_options=options,service_log_path=None,timeout=90)

#ua = dict(DesiredCapabilities.PHANTOMJS)
#ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
#driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])

driver.set_window_position(0,0)
driver.set_window_size(850,800)

time.sleep(5)

i = 0
l= open('old/comm.txt').read().splitlines()

page ='arenda-pomesheniya/'
   
logging.basicConfig(level=logging.ERROR)

time.sleep(5) 

while True:
    try:
        driver.get(l[i]+page)
        time.sleep(5) 
        driver.find_element_by_xpath(u'//input[@class="select-dropdown"]').click()
        time.sleep(2) 
        driver.find_element_by_xpath(u'//span[contains(text(),"Все")]').click()
        time.sleep(3) 
        driver.find_element_by_xpath(u'//div[@class="input-field col find"]/a').click()
        time.sleep(5) 
        #driver.find_element_by_xpath(u'//a[@class="color-red uderlined-dots"]').click()
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
            break
    time.sleep(1)
    lin = []
    driver.find_element_by_xpath(u'//a[@class="color-red uderlined-dots"]').click()
    time.sleep(5)
    nums = re.sub('[^\d]','',driver.find_element_by_xpath(u'//span[@class="color-red ss"]').text)
    pag = int(math.ceil(float(int(nums))/float(16)))
    print pag
    for x in range(1,pag+1):
        print('*'*10)
        for link in driver.find_elements_by_xpath(u'//a[@itemprop="url"]'):
            url = link.get_attribute('href')   
            print url
            lin.append(url)
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//div[@id="searchText"]'))
        time.sleep(1)
        try:
            url_next = l[i]+page+'?page=%d'%x
            print('*'*10)
            print "Next Page is ..." ,url_next,str(pag)            
            driver.find_element_by_xpath(u'//i[@class="material-icons"][contains(text(),"chevron_right")]/ancestor::a').click()
        except NoSuchElementException:
            pass
        time.sleep(10)        
        
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
    driver.delete_all_cookies()
    i=i+1 
    
#time.sleep(5)
#os.system("/home/oleg/pars/bc/comm.py")




