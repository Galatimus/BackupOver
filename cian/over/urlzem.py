#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
import math
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/v7uwe0l1.default/') #Gui2
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ymoy2ffu.default/')#Gui11
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
profile.set_preference("javascript.enabled", False)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)
driver.set_window_position(0,0)
driver.set_window_size(800,500)


#driver.get('https://whoer.net/ru')
#time.sleep(30)
#driver.close()



i = 0
ls= open('Links/zemm.txt').read().splitlines()
dc = len(ls)





while i < len(ls):
           print '*********'
           print i+1,'/',dc  
           time.sleep(3)           
           driver.get(ls[i])    
           #print ls[i]
           time.sleep(3)
           lin = []
           try:
                      time.sleep(2)
                      driver.find_element_by_xpath(u'//div[@class="c-app-banner__close"]/button').click()
                      time.sleep(2)
           except (NoSuchElementException,WebDriverException):
                      pass
           
           try:
                      WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                      driver.set_window_size(800,700)
                      raw_input("Press Enter to continue...") 
                      time.sleep(3)           
                      driver.get(ls[i])    
                      #print ls[i]
                      time.sleep(3)
                      driver.set_window_size(800,500)
           except TimeoutException:
                      print "NEXT!"   
           #page = 2
           while True:
                      
                      try:
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/suburban")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"rent/suburban")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)                                 
                                 time.sleep(1)                                 
                                 page = driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').text
                                 print'*********************'
                                 print 'Next Page = '+str(page)
                                 print '***',len(lin),'****'
                                 print i+1,'/',dc
                                 print'*********************'
                                 driver.get(ls[i]+'&p=%s'% page) 
                                 time.sleep(2)                                 
                      except (NoSuchElementException,WebDriverException):
                                 lin = list(set(lin))
                                 print '***',len(lin),'****'
                                 print 'Save...' 
                                 links = open('cian_zem.txt', 'a')
                                 for item in lin:
                                            links.write("%s\n" % item)
                                 links.close()
                                 time.sleep(1) 
                                 driver.get("about:blank")
                                 driver.delete_all_cookies()
                                 time.sleep(3)
                                 #driver.close()
                                 break
                                          
                         
                   
           i=i+1 

driver.close()



