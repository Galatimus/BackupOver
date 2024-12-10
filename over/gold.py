#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import time
from random import randint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
#profile = webdriver.FirefoxProfile()
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)


time.sleep(5)

driver.set_window_position(0,0)
driver.set_window_size(800,800)

driver.get("http://www.goodsmatrix.ru/GoodsCatalogue.aspx")
time.sleep(2) 

while True:
    
    try:
        try:
            driver.find_element_by_xpath(u'//img[@align="absmiddle"][contains(@src,"http://www.goodsmatrix.ru/Images/CatalogTree/P.gif")]').click()
        except (AttributeError,NoSuchElementException):
            driver.find_element_by_xpath(u'//img[@align="absmiddle"][contains(@src,"http://www.goodsmatrix.ru/Images/CatalogTree/O.gif")]').click()
    except (AttributeError,NoSuchElementException):
        break
    time.sleep(1)
    
linn = []
for link in driver.find_elements_by_xpath(u'//img[@class="wtvicon1"][contains(@src,"/Images/CatalogTree/folder_close.gif")]/following-sibling::span[@class="MyNode"]/a'):
    url = link.get_attribute('href')   
    print url
    linn.append(url)
print '***',len(linn),'**********'

z = 1
for line in linn:
    new = []
    try:
        driver.set_page_load_timeout(15)
        driver.get(line) 
    except TimeoutException:
        driver.execute_script("window.stop();")
        
    time.sleep(1)
         
    try:
        driver.find_element_by_xpath(u'//input[@id="ctl00_ConfirmAge_okBT"]').click()
    except NoSuchElementException:
        pass
    
    while True:        
        try:
            for lin in driver.find_elements_by_xpath(u'//td[@align="center"]/a[contains(@id,"Content")]'):
                urll = lin.get_attribute('href')   
                print urll
                new.append(urll)
            time.sleep(1)
            driver.execute_script("window.scrollTo(400, document.body.scrollHeight);")
            time.sleep(1)
            driver.find_element_by_xpath(u'//span[@style="color:Black;"]/following-sibling::a[1]').click()
            time.sleep(2)            
        except NoSuchElementException:
            print 'Save...',len(new),str(z),'/',len(linn),'**********'
            links = open('doods.txt', 'a')
            for item in new:
                links.write("%s\n" % item)
            links.close()
            break
    time.sleep(2)
    z=z+1
