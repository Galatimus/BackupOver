#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import time
from selenium.webdriver import ActionChains
from random import randint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
#profile = webdriver.FirefoxProfile()
#profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)


time.sleep(2)

driver.set_window_position(0,0)
driver.set_window_size(800,750)

driver.get("https://msk.igooods.ru/")
time.sleep(3) 
driver.get("https://igooods.ru/select_address")

time.sleep(3) 

driver.find_element_by_id(u'place_street').send_keys(u'проезд Кадомцева, 23')
time.sleep(5)
driver.find_element_by_xpath(u'//button[@class="btn search-btn"]').click()
time.sleep(5)
driver.find_element_by_xpath(u'//div[@class="logo-metro sa-delivery-zone__head"]').click()
#driver.find_element_by_xpath(u'//div[@class="logo-lenta sa-delivery-zone__head"]').click()
time.sleep(15)

lin = []
for link in driver.find_elements_by_xpath(u'//div[@class="b-side-menu__item small"]/a'):
    url = link.get_attribute('href')   
    print url
    lin.append(url)
    
z = 0
red = []
while z < len(lin): 
    try:
        print z+1,'/',str(len(lin)),' ',lin[z]
        driver.set_page_load_timeout(15)
        driver.get(lin[z]) 
        for p in range(1,100):
            #time.sleep(0.2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
            try:
                current = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,'//div[@class="b-not-found__card-wrap"]')))
                print current
                break
            except TimeoutException:
                print p
            #time.sleep(0.5)
        for lik in driver.find_elements_by_xpath(u'//div[@class="name-weight"]/a'):
            url1 = lik.get_attribute('href')   
            print url1
            red.append(url1)
        
    except TimeoutException:
        driver.execute_script("window.stop();")
        time.sleep(0.5)
        driver.execute_script("window.stop();")
    #driver.delete_all_cookies()                      
    time.sleep(1.5)    
    z=z+1
    print '**',str(len(red)),'***'
links = open('mag1.txt', 'a')
for item in red:
    links.write("%s\n" % item)
links.close()            
time.sleep(1)            
print'DONE'
driver.close()

#captcha_iframe = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
#time.sleep(2)
#ActionChains(driver).move_to_element(captcha_iframe).click().perform()

#captcha = raw_input("captcha?:  ")
#print "captcha, %s." % captcha
#time.sleep(1)
#driver.find_element_by_name('captcha').send_keys(captcha)
#time.sleep(2)
#driver.find_element_by_xpath(u'//button[@class="btn"][contains(@onclick,"login")]').click()
#time.sleep(randint(5,14))
#driver.execute_script("window.scrollTo(800, document.body.scrollHeight-5000);")
#time.sleep(randint(3,10))
#while True:
    #print 'Wait Bonus...'
    ##WebDriverWait(driver,3700).until(EC.presence_of_element_located((By.XPATH,'//a[@class="btn-small"][contains(@onclick,"hourly")]')))
    #WebDriverWait(driver,3700).until_not(EC.presence_of_element_located((By.XPATH,'//b[@id="deptimer2"]')))
    ##WebDriverWait(driver,3700).until_not(lambda driver: driver.find_element_by_xpath('//b[@id="deptimer2"]').is_displayed())
    #print "Bonus is ready!"
    #time.sleep(randint(10,100))
    #driver.find_element_by_xpath(u'//a[@class="btn-small"][contains(@onclick,"hourly")]').click()    
    #time.sleep(randint(10,100))