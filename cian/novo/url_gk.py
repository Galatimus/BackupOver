#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.common.by import By
import time
import re
import math
from datetime import datetime,timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print (sys.version)




#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
###profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
###profile = webdriver.FirefoxProfile()
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)


ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
driver = webdriver.PhantomJS()

time.sleep(3)


driver.set_window_position(0,0)
driver.set_window_size(1500,400)
   

v = 1
ls= open('cian_gk.txt').read().splitlines()

while v < len(ls):           
           time.sleep(1)
           page = ls[v]
           try:
                      driver.set_page_load_timeout(30)
                      driver.get(page) 
           except TimeoutException:
                      driver.execute_script("window.stop();")
           time.sleep(3)
           num = re.sub(u'[^\d]','',driver.find_element_by_xpath(u'//p[@class="pagination__hint"]').text.split(u' из ')[1])
           pag = int(math.ceil(float(int(num))/float(10)))
           print 'Total...',v+1,'/',len(ls)
           print num,pag
           novo = []
           for x in range(1,pag+1):                              
                      try:
                                 driver.set_page_load_timeout(30)
                                 driver.get(page+'&page=%d'%x)
                      except TimeoutException:
                                 driver.execute_script("window.stop();")
                      time.sleep(3)           
                      for link in driver.find_elements_by_xpath(u'//h3/a'):
                                 url = link.get_attribute('href')   
                                 print url
                                 novo.append(url)
                      print '***',len(novo),'/',str(num),'Total...',v+1,'/',len(ls),'***'
                      time.sleep(1)
                      
                      
           links = open('erzrf.txt', 'a')
           for item in novo:
                      links.write("%s\n" % item)
           links.close()            
           time.sleep(1)            
           print'SAVE and NEXT'           
                     
           v += 1
driver.close()