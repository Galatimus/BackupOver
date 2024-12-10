#! /usr/bin/env python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.common.by import By
import time
import re
from datetime import datetime,timedelta
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import xlsxwriter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#print (sys.version)
#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
##profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
##profile = webdriver.FirefoxProfile()
##profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)

ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
#driver = webdriver.PhantomJS(service_args=["--load-images=no","--ignore-ssl-errors=true"])
driver = webdriver.PhantomJS()

time.sleep(2)

driver.set_window_position(0,0)
driver.set_window_size(800,750)


driver.get("https://msk.igooods.ru/")
time.sleep(3) 
driver.get("https://igooods.ru/select_address")

time.sleep(10) 

driver.find_element_by_id(u'place_street').send_keys(u'проезд Кадомцева, 23')
time.sleep(15)
driver.find_element_by_xpath(u'//button[@class="btn search-btn"]').click()
time.sleep(5)
driver.find_element_by_xpath(u'//div[@class="logo-metro sa-delivery-zone__head"]').click()
#driver.find_element_by_xpath(u'//div[@class="logo-lenta sa-delivery-zone__head"]').click()
time.sleep(20)

          
workbook = xlsxwriter.Workbook(u'Igooods_metro.xlsx')


ws = workbook.add_worksheet()
ws.write(0, 0, u"Наименование магазина")
ws.write(0, 1, u"Город")
ws.write(0, 2, u"Адрес Магазина")
ws.write(0, 3, u"Раздел")
ws.write(0, 4, u"Подраздел")
ws.write(0, 5, u"Наименование продукта")
ws.write(0, 6, u"Вес продукта(фасовка)")
ws.write(0, 7, u"Стоимость")
ws.write(0, 8, u"Стоимость за ед. измерения")
ws.write(0, 9, u"Акция/регулярная цена")
ws.write(0, 10, u"Единица измерения")
ws.write(0, 11, u"Изготовитель")
ws.write(0, 12, u"Описание")
ws.write(0, 13, u"Состав")
ws.write(0, 14, u"Ссылка")

result= 1           
           


z = 0
lin= open('mag1.txt').read().splitlines()

g = Grab(timeout=20, connect_timeout=50)

try:
           while z < len(lin): 
                     
                      try:
                                 print z+1,'/',str(len(lin)),' ',lin[z]
                                 driver.set_page_load_timeout(15)
                                 driver.get(lin[z]) 
                                 g.go(lin[z])
                      except TimeoutException:
                                 driver.execute_script("window.stop();")
                                 time.sleep(0.5)
                                 driver.execute_script("window.stop();")
                      except(GrabTimeoutError,GrabNetworkError,GrabConnectionError):
                                 continue
                      time.sleep(0.5)                      
                     
                      try:
                                 ray = driver.find_element_by_xpath(u'//div[@class="b-breadcrumbs"]/ul/li[1]/a').text
                      except (NoSuchElementException,WebDriverException):
                                 ray = ''
                     
                      try:
                                 uliza = driver.find_element_by_xpath(u'//div[@class="b-breadcrumbs"]/ul/li[2]/a').text
                      except (NoSuchElementException,WebDriverException):
                                 uliza = ''
           
                      try:
                                 dom = driver.find_element_by_xpath(u'//div[@class="b-product__title"]').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 dom = ''                                                       
           
                      try:
                                 seg = driver.find_element_by_xpath(u'//div[@class="b-product__weight"]').text
                      except (NoSuchElementException,WebDriverException):
                                 seg = ''                                            
                      try:
                                 naz = driver.find_element_by_xpath(u'//span[@class="total-price"]').text[:-1]+'р.'
                      except (NoSuchElementException,WebDriverException):
                                 naz = ''                                                       
                      try:
                                 price = driver.find_element_by_xpath(u'//div[@class="price-per-kg"]').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 price = ''
           
                      try:
                                 cena_za = driver.find_element_by_xpath(u'//div[@class="label-stock"]').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 cena_za = u'Регулярная цена'
                      try: 
                                 klass = driver.find_element_by_xpath(u'//div[@class="total-price-for"]').text
                      except (NoSuchElementException,WebDriverException):
                                 klass =''
                      try:
                                 plosh = g.doc.select(u'//div[contains(text(),"Описание:")]/following-sibling::div').text()
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 plosh = ''
                                 
                      try:
                                 et = g.doc.select(u'//div[contains(text(),"Состав:")]/following-sibling::div').text()
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 et = ''
           
                      try:
                                 god = g.doc.select(u'//div[contains(text(),"Изготовитель:")]/following-sibling::div').text()
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 god =''
           
                    
                      print('*'*50)
                      print ray 
                      print uliza
                      print dom
                      print seg
                      print naz
                      print cena_za
                      print price
                      print klass
                      print plosh
                      print et
                      print god
                      print('*'*50)
                      ws.write(result, 0, 'Метро')
                      ws.write(result, 1, 'Москва')
                      ws.write(result, 2, 'проспект Мира, 211к1')
                      ws.write(result, 3, ray)
                      ws.write(result, 4, uliza)
                      ws.write(result, 5, dom)
                      ws.write(result, 6, seg)
                      ws.write(result, 7, naz)
                      ws.write(result, 8, price)
                      ws.write(result, 9, cena_za)
                      ws.write(result, 10, klass)
                      ws.write(result, 12, plosh)
                      ws.write(result, 13, et)
                      ws.write(result, 11, god)
                      ws.write_string(result, 14, lin[z])
                      result+=1
                      #driver.delete_all_cookies()                      
                      time.sleep(2)
                      z=z+1
except KeyboardInterrupt:
           pass
           
print('Save it...')
time.sleep(2)
workbook.close()
print('Done')
driver.close()




          


 

