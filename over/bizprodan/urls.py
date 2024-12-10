#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
#profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.stylesheet', 1)
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)

time.sleep(3)

driver.set_window_position(0,0)
driver.set_window_size(900,600)

i = 0
l= ['https://pandao.ru/category/krasota-i-zdorove',
    'https://pandao.ru/category/zhenskaya-odezhda',
    'https://pandao.ru/category/dom-i-interer',
    'https://pandao.ru/category/telefony-i-planshety',
    'https://pandao.ru/category/sad-i-ogorod',
    'https://pandao.ru/category/avtotovary',
    'https://pandao.ru/category/sport-i-otdyh',
    'https://pandao.ru/category/igry-i-igrushki',
    'https://pandao.ru/category/tovary-dlya-detej',
    'https://pandao.ru/category/kanctovary',
    'https://pandao.ru/category/elektronika',
    'https://pandao.ru/category/tovary-dlya-hobbi',
    'https://pandao.ru/category/muzhskaya-odezhda',
    'https://pandao.ru/category/chasy',
    'https://pandao.ru/category/kompyutery-i-ofis',
    'https://pandao.ru/category/tovary-dlya-remonta',
    'https://pandao.ru/category/tovary-dlya-jivotnyh',
    'https://pandao.ru/category/bytovaya-tehnika',
    'https://pandao.ru/category/obuv',
    'https://pandao.ru/category/mototovary',
    'https://pandao.ru/category/mebel',
    'https://pandao.ru/category/chaj-i-prinadlezhnosti']

page = l[i]

while True:
       print '********************************************',i+1,'/',len(l),'*******************************************'       
       driver.get(page)       
       time.sleep(3)       
       for p in range(1,51):
              driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              time.sleep(1)
              print 'Page is '+str(p)
              #time.sleep(1)
       else:
              for link in driver.find_elements_by_xpath(u'//a[@class="product-item"]'):
                     url = link.get_attribute('href')   
                     print url
                     links = open('pandao.txt', 'a')
                     links.write("%s\n" % url)
                     links.close()
                     
              print('Done!')    
              time.sleep(2)
       i=i+1
       try:
              page = l[i]
       except IndexError:
              break    
   
driver.close()