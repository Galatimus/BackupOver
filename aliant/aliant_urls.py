#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException






#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/n1ddsdpx.default/') #Gui2
##profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/3missjz0.default/')#Gui1
##profile = webdriver.FirefoxProfile()
#profile.set_preference("network.proxy.type", 1)
#profile.set_preference("network.proxy.http", proxy)
#profile.set_preference("network.proxy.http_port", port)
#profile.set_preference("network.proxy.ssl", proxy)
#profile.set_preference("network.proxy.ssl_port", port)
#profile.update_preferences()
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)



ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
#service_args = ['--proxy='+proxy,'--proxy-type=http',]
driver = webdriver.PhantomJS()
driver.set_window_position(0,0)
driver.set_window_size(900,600)


driver.get("http://aliant.pro/catalog/commercial/")

time.sleep(5)

while True:
       try:
              driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//div[@class="contactUsLeft"]'))
              #WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH,'//div[@id="preloader"][contains(@style,"none")]')))
              print "Page is ready!"
              time.sleep(1)
              driver.find_element_by_xpath(u'//button[@class="waves-effect waves-light btn btn-more"]').click()
              time.sleep(1)
              print('Done!') 
       except (ElementNotVisibleException,ElementNotInteractableException):
              for link in driver.find_elements_by_xpath(u'//a[@class="item"]'):
                     url = link.get_attribute('href')   
                     print url
                     li = open('aliant.txt', 'a')
                     li.write(url + '\n')
                     li.close()                     
              driver.close()
              print('Done All') 
              break
              
              
              
       time.sleep(2)       
                   
 
    
   
