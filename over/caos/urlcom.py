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


try:
    os.remove('/home/oleg/pars/bc/bc_com.txt')
    print 'Удаляем: '
except (IOError, OSError):
    print 'Нет файла'


#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/qgrm1yot.default/')#Gui1
###profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/')#Gui2
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)

ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
#service_args = ['--proxy='+proxy,'--proxy-type=http',]
driver = webdriver.PhantomJS()

driver.set_window_position(0,0)
driver.set_window_size(800,385)

time.sleep(5)


page ='http://arenda-ofisa.caos.ru/'
   
logging.basicConfig(level=logging.ERROR)




driver.get(page)
time.sleep(5)
lin = []
nums = re.sub('[^\d]','',driver.find_element_by_xpath(u'//strong[@class="panel-title_large"]').text)
pag = int(math.ceil(float(int(nums))/float(40)))
#pag = 272
print pag
for x in range(1,pag+1):
    url_next = page+'?page=%d'%x
    print('*'*10)
    print "Next Page is ..." ,url_next,str(pag)
    driver.get(url_next) 
    time.sleep(5)        
    for link in driver.find_elements_by_xpath(u'//div[@class="name_class_and_stars"]/a'):
        url = link.get_attribute('href')   
        print url
        lin.append(url)
time.sleep(1)
links = open('caos.txt', 'a')
for item in lin:
    links.write("%s\n" % item)
links.close()            
time.sleep(1)            
print'DONE_ALL'
driver.close()
    
#time.sleep(5)
#os.system("/home/oleg/pars/bc/comm.py")




