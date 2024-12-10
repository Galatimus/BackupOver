#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException,NoSuchWindowException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
import random
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



##profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
###profile = webdriver.FirefoxProfile()
##profile.set_preference('permissions.default.stylesheet', 2)
##profile.set_preference('permissions.default.image', 2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)

proxy = random.choice(list(open('../../tipa.txt').read().splitlines()))
print proxy



ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
driver = webdriver.PhantomJS(service_args = ['--proxy='+proxy,'--proxy-type=http'])

driver.set_window_position(0,0)
driver.set_window_size(800,500)

time.sleep(3)           
driver.get('https://www.cian.ru/novostroyki/')    
time.sleep(3)
print driver.title
lin = []

while True:
           
           try:
                      
                      try:
                                 WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                                 driver.set_window_size(800,700)
                                 raw_input("Press Enter to continue ...") 
                                 time.sleep(3)
                                 driver.set_window_size(800,500)
                      except TimeoutException:
                                 print "NEXT!"
                                 
                      for link in driver.find_elements_by_xpath(u'//div[@class="serp-item__content__bottom__left"]/a[contains(text(),"застройщика")]'):
                                 url = link.get_attribute('href')   
                                 print url
                                 lin.append(url)
                      time.sleep(1)                                 
                      page = driver.find_element_by_xpath(u'//div[@class="pager_pages"]/span/following-sibling::a[1]').text
                      print'*********************'
                      print 'Next Page = '+str(page)
                      print '***',len(lin),'****'
                      print'*********************'
                      driver.get('https://www.cian.ru/newobjects/list/?deal_type=sale&engine_version=2&offer_type=newobject'+'&p=%s'% page+'&region=-1') 
                      time.sleep(2)
           except (NoSuchElementException,WebDriverException):
                      time.sleep(1) 
                      driver.get("about:blank")
                      driver.delete_all_cookies()
                      time.sleep(3)                                 
                      break
          
                                 

v = 1
for line in lin:
           
           driver.get(line)
           time.sleep(3)
           novo = []
           while True:
                              
                      try:
           
                                 try:
                                            WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                                            driver.set_window_size(800,700)
                                            raw_input("Press Enter to continue ...") 
                                            driver.get(line+'&p=%s'% nextpage)
                                            time.sleep(3)
                                            driver.set_window_size(800,500)
                                 except TimeoutException:
                                            print "NEXT!"
                                            
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/flat")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            novo.append(url)
                                 time.sleep(1)                                 
                                 nextpage = driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').text
                                 print'*********************'
                                 print 'Next Page = '+str(nextpage)
                                 print '***',len(novo),'****'
                                 print 'GK',v,'/',len(lin)
                                 print'*********************'
                                 driver.get(line+'&p=%s'% nextpage) 
                                 time.sleep(2) 
                      except (NoSuchElementException,WebDriverException):
                                 novo = list(set(novo))
                                 print '***',len(novo),'****'
                                 print 'Save...'                                  
                                 links = open('cian_novo.txt', 'a')
                                 for item in novo:
                                            links.write("%s\n" % item)
                                 links.close()
                                 time.sleep(1) 
                                 driver.get("about:blank")
                                 driver.delete_all_cookies()
                                 time.sleep(3)                                 
                                 break
                     
           v += 1