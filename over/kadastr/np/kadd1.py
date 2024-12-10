#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

i = 0
ls= open('np.txt').read().splitlines()
dc = len(ls)

#profile =  webdriver.FirefoxProfile()
profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ljpce52l.default/') #Gui2
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/jcpr7q9q.default/')#Gui1
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,timeout=60)
driver.set_window_position(0,0)
driver.set_window_size(1000,720)

lin = []
while i < len(ls):
    print '********************************************************************************************'
               
    print i+1,'/',dc     
    driver.get('http://pkk5.rosreestr.ru/#x=&y=&z=&type=1&zoomTo=1&app=search&opened=1&text='+ls[i])    
    sub = ls[i]
    print sub
    time.sleep(5)           
    
    while True:
        print '********************',len(lin),'**********************'
        try:
            try:
                WebDriverWait(driver,200).until(EC.presence_of_element_located((By.XPATH,u'//div[@class="featureSet_list"]')))
                print "Page is ready!"
                time.sleep(2)
            except TimeoutException:
                print "Loading took too much time!"
                time.sleep(2)
                driver.find_element_by_xpath(u'//a[contains(@title,"Следующая страница")]').click()                                 

            for link in driver.find_elements_by_xpath(u'//b[@class="pull-left"]'):
                #url = re.sub(r'(?<=:)0*','',link.text).replace(u'::',':0:') 
                url = link.text 
                print url
                lin.append(url)

            driver.find_element_by_xpath(u'//a[contains(@title,"Следующая страница")]').click()
            time.sleep(5)
        except NoSuchElementException:
            break
    time.sleep(3)
    print "Page is Refresh!"
    driver.get("about:blank")
    driver.delete_all_cookies()
    time.sleep(3)
    i=i+1    
links = open('nums_np.txt', 'w')
for item in lin:
    links.write("%s\n" % item)
links.close()





