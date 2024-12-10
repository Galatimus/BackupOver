#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import time
import os
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
#profile = webdriver.FirefoxProfile()
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)


time.sleep(2)

driver.set_window_position(0,0)
driver.set_window_size(900,600)

driver.get("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type[0]=10&region=4557")
time.sleep(2) 



#driver.find_element_by_xpath(u'//span[@class="_1dk9MlY93wWdfDVN"]/input').send_keys(u'Новгородская область')
##driver.find_element_by_name('strPasswAuth').send_keys('PVk3TKF')
#time.sleep(2)
#driver.find_element_by_xpath(u'//div[@data-mark="searchButton"]/button').click()

#time.sleep(5)


#driver.find_element_by_id('estateType8').click()
#time.sleep(1)
#driver.find_element_by_id('estateType2').click()
#time.sleep(1)
#driver.find_element_by_id('estateType5').click()
#time.sleep(1)
#driver.find_element_by_id('estateType1').click()
#time.sleep(1)
#driver.find_element_by_id('estateType6').click()
#time.sleep(1)
#driver.find_element_by_id('estateType3').click()
#time.sleep(1)
#driver.find_element_by_id('estateType9').click()
#time.sleep(1)
#driver.find_element_by_id('estateType11').click()
##time.sleep(2)
##driver.find_element_by_xpath(u'//a[@class="link-dy"][contains(text(),"расширенный поиск")]').click()
#time.sleep(1)
#driver.find_element_by_id('cbxRegion3').click()
#time.sleep(1)
#driver.find_element_by_id('cbxRegion4').click()
#time.sleep(2)
#driver.find_element_by_xpath(u'//input[@name="submit"]').click()

#time.sleep(3)

#lin = []
#for x in range(1,61):
        #try:
                #driver.set_page_load_timeout(30)
                #line='http://www.petrostroybaza.ru/search?stPage=%d'%x
                #driver.get(line)
        #except TimeoutException:
                #driver.execute_script("window.stop();")
                
        #time.sleep(2)
        #print "Page is ready!"
        
       
        #for link in driver.find_elements_by_xpath(u'//a[@class="link-blue"][contains(@href,"Page")]'):
                #url = link.get_attribute('href')   
                #print url
                #lin.append(url)
        #time.sleep(2)
        #print x,'/',len(lin)
#print('Wait 2 sec...')
#time.sleep(1)
#driver.find_element_by_name('strLoginAuth').send_keys('ooo2018')
#driver.find_element_by_name('strPasswAuth').send_keys('K3Z6iMk')
#time.sleep(2)
#driver.find_element_by_name('submitAuth').click()
#time.sleep(3)
#workbook = xlsxwriter.Workbook(u'Petrostroybaza_Demo.xlsx')
#ws = workbook.add_worksheet()
#ws.write(0, 0,u"Компания")
#ws.write(0, 1, u"Контакт")
#ws.write(0, 2, u"E-mail")
#row = 1
#row1 = 1
#row2 = 1




#v = 1
#for line in lin:
        #print v,'/',len(lin)
        #try:
                #driver.set_page_load_timeout(30)
                #driver.get(line)
        #except TimeoutException:
                #driver.execute_script("window.stop();")
        
        #print "Page is ready!"
        #time.sleep(2)
        #for punkt in driver.find_elements_by_xpath(u'//td[contains(text(),"Компания")]/following-sibling::td/a'):
                #com = punkt.text
                #print com
                #ws.write(row, 0, com)
                #row+=1

        #for metro in driver.find_elements_by_xpath(u'//td[contains(text(),"Контакт")]/following-sibling::td'):
                #tel = re.sub('[^\d\,\(\)\;]','',metro.text).replace('(','+7(').replace(';',',+7')
                #print tel
                #ws.write_string(row1, 1, tel)
                #row1+=1

        #for sfera in driver.find_elements_by_xpath(u'//td[contains(text(),"E-mail")]/following-sibling::td'):
                #print sfera.text
                #ws.write_string(row2, 2, sfera.text)
                #row2+=1
        #v+=1
        #print('*'*5)
        #time.sleep(2)
#print('Wait 2 sec...')
#time.sleep(2)
#print('Save it...')    
#time.sleep(1)
#workbook.close()
#driver.close()
#print('Done!')
