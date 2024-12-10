#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.common.by import By
import time
import random
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException


profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/v7uwe0l1.default/') #Gui2
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ymoy2ffu.default/')#Gui1
#profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('permissions.default.image', 3)
profile.set_preference("javascript.enabled", False)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)
driver.set_window_position(0,0)
driver.set_window_size(850,500)



i = 3
ls= open('Links/com_p.txt').read().splitlines()
dc = len(ls)

while i < len(ls):
       print '*********'
       print i+1,'/',dc  
       time.sleep(3)           
       driver.get(ls[i])    
       print ls[i]
       time.sleep(3)       


       try:
              WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
              driver.set_window_size(850,700)
              time.sleep(1)
              sitekey = re.findall(u"sitekey': '(.*?)'",driver.page_source)[0]
              print sitekey              
              raw_input('Введите число   ') 
              time.sleep(3)           
              driver.get(ls[i])    
              time.sleep(3)
              driver.set_window_size(850,500)
       except TimeoutException:
              print "NEXT!"
       try:
              driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//div[@class="c-footer-blackstripe"]'))       
              time.sleep(2)
              driver.find_element_by_xpath(u'//div[@class="c-footer-tomobile"]/a').click()
       except (NoSuchElementException,WebDriverException):
              pass
       time.sleep(5)       
       page = 1
       while True:
              try:
                     driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//button[contains(text(),"Полная версия сайта")]'))
                     print "NEXT!"
                     #time.sleep(1)
                     page=page+1
                     print 'Next Page is = '+str(page)
                     time.sleep(2)
                     driver.find_element_by_xpath(u'//button[contains(text(),"Следующие")]').click()
                     time.sleep(1)
                     #driver.page_source().contains("2 страница")
                     WebDriverWait(driver,80).until(EC.presence_of_element_located((By.XPATH,'//div[@class="_2pjsHfdkNjdDeBXI"][contains(text(),"%s")]'% page)))
                     print('Done!') 
                     time.sleep(2)
              except (ElementNotVisibleException,TimeoutException,ElementNotInteractableException,NoSuchElementException):
                     for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/commercial")]'):
                            url = link.get_attribute('href')   
                            print url
                            li = open('cian_com.txt', 'a')
                            li.write(url + '\n')
                            li.close() 
                     for link in driver.find_elements_by_xpath(u'//a[contains(@href,"rent/commercial")]'):
                            url = link.get_attribute('href')   
                            print url
                            li = open('cian_com.txt', 'a')
                            li.write(url + '\n')
                            li.close()                     
                     time.sleep(1) 
                     driver.get("about:blank")
                     driver.delete_all_cookies()
                     time.sleep(3)
                     print('Done All') 
                     break
       i=i+1 
    
   
