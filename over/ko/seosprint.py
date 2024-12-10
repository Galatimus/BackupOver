#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import Select,WebDriverWait

profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/xoyfz7kv.default/')
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,timeout=60)
driver.get('http://www.seosprint.net/')

time.sleep(2)


#password = driver.find_element_by_name('password')
#password.send_keys('Walter2005')


driver.find_element_by_id('mnu302').click()
driver.add_cookie
time.sleep(2) 
driver.find_element_by_xpath('//input[@type="text"]').send_keys('galatimus@mail.ru')
driver.find_element_by_xpath('//input[@type="password"]').send_keys('tdoJgyOvbl')
#time.sleep(3)
#driver.find_element_by_xpath('//input[@class="auth-enter"]').click()



for i in range(40):
     print  i
     time.sleep(1)
     
print 'GO!'






driver.find_element_by_xpath('//a[@class="button-green"]').click()
for i in range(5):
     print  i
     time.sleep(1)
     


while True:
     try:
          driver.find_element_by_xpath('//table[@class="work-serf"]/tbody/tr[1]/td[@class="normalm"]').click()
          time.sleep(1)
          driver.find_element_by_partial_link_text('Просмотреть сайт рекламодателя').click()
          time.sleep(2)
          
          print driver.window_handles[0]
          print driver.window_handles[1]
          time.sleep(1)
          driver.switch_to_window(driver.window_handles[1])
          #driver.switch_to().window(driver.window_handles[1])
          time.sleep(1)
          driver.set_window_position(0,0)
          #try:
               #print "about to look for element"
               #element = WebDriverWait(driver, 80).until(lambda driver : driver.find_element_by_id("blockverify"))
               #print "still looking?"
          #finally:
               #print 'yowp'          
          for i in range(80):
               print  i
               time.sleep(1)
          driver.close()
          driver.switch_to_window(driver.window_handles[0])
          driver.refresh()
          time.sleep(5)
     except NoSuchElementException:
          for i in range(300):
               print  i
               time.sleep(1)
          driver.refresh()
          time.sleep(1)
          driver.find_element_by_xpath('//a[contains(text(),"Cepфинг caйтoв")]').click()
          continue
                  
         
    
          
       



 

