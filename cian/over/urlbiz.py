#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
import math
from selenium.webdriver.common.proxy import *
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


#binary = FirefoxBinary("/home/oleg/.local/share/torbrowser/tbb/x86_64/tor-browser_ru/")


myProxy = "185.223.164.218:8085"

proxy = Proxy({
           'proxyType': ProxyType.MANUAL,
           'httpProxy': myProxy,
           'ftpProxy': myProxy,
           'sslProxy': myProxy,
           'noProxy': '' # set this value as desired
})

#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/s5fj2olz.default/') #Gui2
profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/')#Gui1
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
profile.set_preference("javascript.enabled", False)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference('network.proxy.type', 1)
#profile.set_preference('network.proxy.http', '95.181.177.126')
#profile.set_preference('network.proxy.http_port', 8085)
#profile.set_preference('network.proxy.socks_remote_dns', True)
profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)
driver.set_window_position(0,0)
driver.set_window_size(800,500)


#driver.get('https://www.cian.ru/authenticate/')
#raw_input("Press Enter to continue...") 


#time.sleep(2)
#driver.find_element_by_id('page_login_email').send_keys('galatimus@mail.ru')
#driver.find_element_by_id('page_login_pwd').send_keys('walter2005AA')
#time.sleep(3)
#driver.find_element_by_id('page_login_btn_ok').click()
#time.sleep(5)


i = 0
ls= open('Links/biz.txt').read().splitlines()
dc = len(ls)





while i < len(ls):
           print '*********'
           print i+1,'/',dc  
           time.sleep(1)           
           driver.get(ls[i])    
           #print ls[i]
           time.sleep(2)
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
                      #profile.set_preference('permissions.default.image', 1)
                      #profile.set_preference('permissions.default.stylesheet', 1)
                      #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'true')
                      #profile.update_preferences()
                      #driver.refresh()
                      raw_input("Press Enter to continue...") 
                      time.sleep(3)           
                      driver.get(ls[i])    
                      #print ls[i]
                      time.sleep(3)
                      driver.set_window_size(800,500)
           except TimeoutException:
                      print "NEXT!"   
           try:
                      num = re.sub('[^\d]','',driver.find_element_by_xpath(u'//div[@class="totalOffers--yZcBn"]').text)
                      pag = int(math.ceil(float(int(num))/float(25)))
                      if pag > 60:
                                 pag = 60
                      print num
                      print pag           
           except (NoSuchElementException,WebDriverException):
                      num = 1
                      pag = 1
           for page in range(1,pag+1):
                      
                      driver.get(ls[i]+'&p=%s'% page) 
                      time.sleep(1)
                      
                      for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/commercial")]'):
                                 url = link.get_attribute('href')   
                                 print url
                                 lin.append(url)
                      for link in driver.find_elements_by_xpath(u'//a[contains(@href,"rent/commercial")]'):
                                 url = link.get_attribute('href')   
                                 print url
                                 lin.append(url)                                 
                      time.sleep(1)                                 
                      #page = driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').get_attribute('href')
                      
                      #page = driver.find_element_by_xpath(u'//a[@class="list-itemLink--39icE"][contains(text(), "%s")]' % page1).get_attribute('href')
                      print'*********************'
                      print 'Page = '+str(page),'/',str(pag)
                      print '***',len(lin),'****'
                      print i+1,'/',dc
                      print'*********************'
                      #driver.get(page)
                      
                       
                      try:
                                 WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                                 driver.set_window_size(800,700)
                                 raw_input("Press Enter to continue...") 
                                 time.sleep(3)           
                                 driver.get(ls[i]+'&p=%s'% page)     
                                 #print ls[i]
                                 time.sleep(3)
                                 driver.set_window_size(800,500)
                      except TimeoutException:
                                 print "NEXT!"

                     
           lin = list(set(lin))           
           print 'Save...' 
           print '***',len(lin),'****'
           links = open('cian_biz.txt', 'a')
           for item in lin:
                      links.write("%s\n" % item)
           links.close()
           time.sleep(1) 
           driver.get("about:blank")
           driver.delete_all_cookies()
           time.sleep(3)
                                 
                                          
                         
                   
           i=i+1 

driver.close()



