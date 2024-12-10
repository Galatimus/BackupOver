#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException,NoSuchWindowException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
from datetime import datetime,timedelta
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/')
##profile.set_preference('permissions.default.stylesheet', 2)
##profile.set_preference('permissions.default.image', 2)
#profile.set_preference('javascript.enabled', False)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)

ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
driver = webdriver.PhantomJS()
time.sleep(3)
driver.set_window_position(0,0)
driver.set_window_size(800,500)


          
workbook = xlsxwriter.Workbook(u'ERZRF_Новостройки.xlsx')


ws = workbook.add_worksheet()
ws.write(0, 0, u"СУБЪЕКТ РОССИЙСКОЙ ФЕДЕРАЦИИ")
ws.write(0, 1, u"ОКРУГ")
ws.write(0, 2, u"РАЙОН")
ws.write(0, 3, u"НАСЕЛЕННЫЙ ПУНКТ")
ws.write(0, 4, u"МИКРОРАЙОН")
ws.write(0, 5, u"КВАРТАЛ")
ws.write(0, 6, u"АДРЕС")
ws.write(0, 7, u"МЕТРО")
ws.write(0, 8, u"БРЕНД")
ws.write(0, 9, u"ЗАСТРОЙЩИК")
ws.write(0, 10, u"СТАДИЯ СТРОИТЕЛЬСТВА")
ws.write(0, 11, u"СРОК СДАЧИ")
ws.write(0, 12, u"ДАТА ВВОДА")
ws.write(0, 13, u"КЛАСС ОБЪЕКТА")
ws.write(0, 14, u"СЕРИЯ ОБЪЕКТА")
ws.write(0, 15, u"ТИП ОБЪЕКТА")
ws.write(0, 16, u"ЭТАЖНОСТЬ")	
ws.write(0, 17, u"ЖИЛАЯ ПЛОЩАДЬ ОБЪЕКТА")
ws.write(0, 18, u"ОТДЕЛКА")
ws.write(0, 19, u"МАТЕРИАЛ НАРУЖНЫХ СТЕН")
ws.write(0, 20, u"ВСЕГО КВАРТИР")
ws.write(0, 21, u"ПРОДАЕТСЯ КВАРТИР")
ws.write(0, 22, u"ПОДХОДИТ КВАРТИР")
ws.write(0, 23, u"ПЛОЩАДЬ ЗАСТРОЙКИ")
ws.write(0, 24, u"ПЛОЩАДЬ СТРОЯЩИХСЯ ОБЪЕКТОВ")
ws.write(0, 25, u"ПЛОЩАДЬ ЖИЛЫХ ПОМЕЩЕНИЙ")
ws.write(0, 26, u"ПРИВЛЕЧЕНИЕ СРЕДСТВ")
ws.write(0, 27, u"ОПИСАНИЕ ОБЪЕКТА")
ws.write(0, 28, u"ОПИСАНИЕ ПО ЭЛЕМЕНТАМ")
ws.write(0, 29, u"ИПОТЕКА ПО ДДУ")
ws.write(0, 30, u"САЙТ ЗАСТРОЙЩИКА")
ws.write(0, 31, u"ССЫЛКА")
ws.write(0, 32, u"НАИМЕНОВАНИЕ ЖК")
ws.write(0, 33, u"ДАТА ПАРСИНГА")
ws.write(0, 34, u"СОЦИАЛЬНЫЕ СЕТИ")

result= 1           
           


z=0
lin= open('erzrf2.txt').read().splitlines()


           
while z < len(lin): 
           print z+1,'/',str(len(lin))
           
           try:
                      driver.set_page_load_timeout(30)
                      driver.get(lin[z]) 
           except TimeoutException:
                      driver.execute_script("window.stop();")
           time.sleep(1)
                               
           
           try:
                      sub = driver.find_element_by_xpath(u'//b[contains(text(),"Регион")]/following::td[1]').text.replace(u'г.','')
           except (NoSuchElementException,WebDriverException):
                      sub = ''                                            
           
           try:
                      ray = driver.find_element_by_xpath(u'//b[contains(text(),"Округ")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      ray = ''
           try:
                      punkt= driver.find_element_by_xpath(u'//b[contains(text(),"Населенный пункт")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      punkt = ''                                            
           try:
                      ter = driver.find_element_by_xpath(u'//b[contains(text(),"Район")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      ter =''
           
                      
           try:
                      dom = driver.find_element_by_xpath(u'//b[contains(text(),"Квартал")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      dom = ''                                                       
                      
           try:                                                             
                      try:
                                 seg = driver.find_element_by_xpath(u'//b[contains(text(),"Адрес")]/following::td[1]').text
                      except (NoSuchElementException,WebDriverException):
                                 seg = driver.find_element_by_xpath(u'//b[contains(text(),"Улица")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):                      
                      seg = ''                                            
           try:
                      naz = driver.find_element_by_xpath(u'//b[contains(text(),"Метро")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      naz = ''                                                       
           try:
                      price = driver.find_element_by_xpath(u'//b[contains(text(),"Бренд")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      price = ''
                      
           try:
                      elek = driver.find_element_by_xpath(u'//b[contains(text(),"Площадь застройки")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      elek =''
                      
           try:
                      park = driver.find_element_by_xpath(u'//b[contains(text(),"Площадь строющихся объектов")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      park =''                      
                      
           try:
                      cena_za = driver.find_element_by_xpath(u'//b[contains(text(),"Застройщик")]/following::td[1]').text 
           except (NoSuchElementException,IndexError,WebDriverException):
                      cena_za = ''
                      
           try:
                      vent4 = driver.find_element_by_xpath(u'//b[contains(text(),"Сайт")]/following::td[1]/a').get_attribute('href').replace(u'http://','')
           except (NoSuchElementException,WebDriverException):
                      vent4 =''                      
           try:
                      vent5 = driver.find_element_by_xpath(u'//h1').text
           except (NoSuchElementException,WebDriverException):
                      vent5 =''                      
           try:
                      vent6 = driver.find_element_by_xpath(u'//b[contains(text(),"Соц. сети")]/following::td[1]/a').get_attribute('href')
           except (NoSuchElementException,WebDriverException):
                      vent6 =''                      
                      
           try:
                      plosh = driver.find_element_by_xpath(u'//b[contains(text(),"Срок сдачи")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      plosh = ''
                      
           try:
                      vent3 = driver.find_element_by_xpath(u'//tab-header[contains(text(),"Ипотека ДДУ")]/following::div[@class="content"]/tab-content[@class="tab-pane wysiwyg active"]').text
           except (NoSuchElementException,WebDriverException):
                      vent3 =''
                      
           try:
                      vent2 = driver.find_element_by_xpath(u'//tab-header[contains(text(),"Описание по элементам")]/following::div[@class="content"]/tab-content[@class="tab-pane wysiwyg active"]').text
           except (NoSuchElementException,WebDriverException):
                      vent2 =''                      
                      
           #try:
                      #driver.find_element_by_xpath(u'//tab-header[contains(@class,"active")]/following-sibling::tab-header').click()
                      #print 'Klik-OK'
           #except (NoSuchElementException,WebDriverException):
                      #pass
           #time.sleep(2)           
                      
           try: 
                      klass = driver.find_element_by_xpath(u'//b[contains(text(),"Стадия строительства")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      klass =''
          
           try:
                      uliza = driver.find_element_by_xpath(u'//b[contains(text(),"Микрорайон")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      uliza = ''           
           try:
                      et = driver.find_element_by_xpath(u'//b[contains(text(),"Дата ввода")]/following::td[1]').text
           except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                      et = ''
           
           try:
                      et2 = driver.find_element_by_xpath(u'//b[contains(text(),"Класс объекта")]/following::td[1]').text
           except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                      et2 = ''
                      
           try:
                      god = driver.find_element_by_xpath(u'//b[contains(text(),"Серия объекта")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      god =''
                      
           try:
                      zag = driver.find_element_by_xpath(u'//b[contains(text(),"Вид объекта")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      zag =''
                      
           try:
                      do_m = driver.find_element_by_xpath(u'//b[contains(text(),"Этажность")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      do_m =''                                                       
                      
           try:
                      opis = driver.find_element_by_xpath('//b[contains(text(),"Жилая площадь объекта")]/following::td[1]').text
           except (NoSuchElementException,IndexError,WebDriverException):
                      opis = ''
           try:
                      phone = driver.find_element_by_xpath('//b[contains(text(),"Отделка")]/following::td[1]').text
           except (NoSuchElementException,IndexError,WebDriverException):
                      phone = ''
           try:
                      lico = driver.find_element_by_xpath(u'//b[contains(text(),"Материал наружных стен")]/following::td[1]').text
           except (NoSuchElementException,IndexError,WebDriverException):
                      lico = ''
                      
           try:
                      comp = driver.find_element_by_xpath(u'//b[contains(text(),"Всего квартир")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      comp = ''
                      

           try:
                      data1 = driver.find_element_by_xpath(u'//b[contains(text(),"Продается квартир")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      data1=''
           try:
                      mesto = driver.find_element_by_xpath(u'//b[contains(text(),"Подходит квартир")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      mesto =''
           try:
                      vent = driver.find_element_by_xpath(u'//b[contains(text(),"Привлечение средств")]/following::td[1]').text
           except (NoSuchElementException,WebDriverException):
                      vent =''
                      
           try:
                      vent1 = driver.find_element_by_xpath(u'//tab-header[contains(text(),"Описание объекта")]/following::div[@class="content"]/tab-content[@class="tab-pane wysiwyg active"]').text
           except (NoSuchElementException,WebDriverException):
                      vent1 =''                      
           print('*'*50)
           print sub
           print ray 
           print punkt 
           print ter 
           print uliza
           print dom
           print seg
           print naz
           print price
           print klass
           print plosh
           print opis
           print phone
           print lico
           print comp
           print data1
           print mesto
           print et2
           print('*'*50)
           ws.write(result, 0, sub)
           ws.write(result, 1, ray)
           ws.write(result, 2, ter)
           ws.write(result, 3, punkt)
           ws.write(result, 4, uliza)
           ws.write(result, 5, dom)
           ws.write(result, 6, seg)
           ws.write(result, 7, naz)
           ws.write(result, 8, price)
           ws.write(result, 9, cena_za)
           ws.write(result, 10, klass)
           ws.write(result, 11, plosh)
           ws.write(result, 12, et)
           ws.write(result, 13, et2)
           ws.write(result, 14, god)
           ws.write_string(result, 31, lin[z])                                            
           ws.write(result, 15, zag)
           ws.write(result, 16, do_m)
           ws.write(result, 17, opis)
           ws.write(result, 18, phone)
           ws.write(result, 19, lico)
           ws.write(result, 20, comp)
           ws.write(result, 21, data1)
           ws.write(result, 22, mesto)
           ws.write(result, 23, elek)
           ws.write(result, 24, park)
           #ws.write(result, 25, vent)
           ws.write(result, 26, vent)
           ws.write(result, 27, vent1)
           ws.write(result, 28, vent2)
           ws.write(result, 29, vent3)
           ws.write_string(result, 30, vent4)
           ws.write(result, 33, datetime.today().strftime('%d.%m.%Y'))
           ws.write(result, 32, vent5)
           #ws.write(result, 33, vent)
           ws.write_string(result, 34, vent6)
           result+=1
           time.sleep(1)
           z=z+1
           #if result >= 10:
                      #break
                                
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')    
#command = 'mount -a'
#os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
workbook.close()
print('Done')
driver.close()


          


 

