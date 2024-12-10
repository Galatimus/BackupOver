#! /usr/bin/env python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.common.by import By
import time
import re
from datetime import datetime,timedelta
import xlsxwriter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#display = Display(visible=0, size=(800, 600))
#display.start()

#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/')#Gui1
####profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/')#Gui2
#profile.set_preference('permissions.default.stylesheet',2)
#profile.set_preference('permissions.default.image',2)
#profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#profile.set_preference("javascript.enabled", False)
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=90)

ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
driver = webdriver.PhantomJS()

time.sleep(5)

driver.set_window_position(0,0)
driver.set_window_size(800,750)

          
workbook = xlsxwriter.Workbook(u'0001-0002_00_C_001-0217_BCINF.xlsx')


ws = workbook.add_worksheet()
ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
ws.write(0, 4, u"УЛИЦА")
ws.write(0, 5, u"ДОМ")
ws.write(0, 6, u"ОРИЕНТИР")
ws.write(0, 7, u"СЕГМЕНТ")
ws.write(0, 8, u"ТИП_ПОСТРОЙКИ")
ws.write(0, 9, u"НАЗНАЧЕНИЕ_ОБЪЕКТА")
ws.write(0, 10, u"ПОТРЕБИТЕЛЬСКИЙ_КЛАСС")
ws.write(0, 11, u"СТОИМОСТЬ")
ws.write(0, 12, u"ИЗМЕНЕНИЕ_СТОИМОСТИ")
ws.write(0, 13, u"ДОПОЛНИТЕЛЬНЫЕ_КОММЕРЧЕСКИЕ_УСЛОВИЯ")
ws.write(0, 14, u"ПЛОЩАДЬ")
ws.write(0, 15, u"ЭТАЖ")
ws.write(0, 16, u"ЭТАЖНОСТЬ")
ws.write(0, 17, u"ГОД_ПОСТРОЙКИ")
ws.write(0, 18, u"ОПИСАНИЕ")
ws.write(0, 19, u"ИСТОЧНИК_ИНФОРМАЦИИ")
ws.write(0, 20, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
ws.write(0, 21, u"ТЕЛЕФОН")
ws.write(0, 22, u"КОНТАКТНОЕ_ЛИЦО")
ws.write(0, 23, u"КОМПАНИЯ")
ws.write(0, 24, u"МЕСТОПОЛОЖЕНИЕ")
ws.write(0, 25, u"МЕСТОРАСПОЛОЖЕНИЕ")
ws.write(0, 26, u"БЛИЖАЙШАЯ_СТАНЦИЯ_МЕТРО")
ws.write(0, 27, u"РАССТОЯНИЕ_ДО_БЛИЖАЙШЕЙ_СТАНЦИИ_МЕТРО")
ws.write(0, 28, u"ОПЕРАЦИЯ")
ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ")
ws.write(0, 31, u"ДАТА_ПАРСИНГА")
ws.write(0, 32, u"КАДАСТРОВЫЙ_НОМЕР")
ws.write(0, 33, u"ЗАГОЛОВОК")
ws.write(0, 34, u"ШИРОТА_ИСХ")
ws.write(0, 35, u"ДОЛГОТА_ИСХ")
result= 1           
           


z = 4973
lin= open('caos.txt').read().splitlines()


time.sleep(3)

try:
           while z < len(lin): 
                     
                      try:
                                 print z+1,'/',str(len(lin)),' ',lin[z]
                                 driver.set_page_load_timeout(15)
                                 driver.get(lin[z]) 
                      except TimeoutException:
                                 driver.execute_script("window.stop();")
                                 time.sleep(0.5)
                                 driver.execute_script("window.stop();")
                      time.sleep(5)                      
                     
                      try:
                                 ray = driver.find_element_by_xpath(u'//ul[@class="breadcrumbs-items"]/li[3]/a/span').text
                      except (NoSuchElementException,WebDriverException):
                                 ray = ''
                      try:
                                 punkt=u'Москва'#driver.find_element_by_xpath(u'//ul[@class="breadcrumbs"]/li[2]/span/a/span[1]').text
                      except (NoSuchElementException,WebDriverException):
                                 punkt = ''                                            
                      try:
                                 sub = u'Москва'#reduce(lambda punkt, r: punkt.replace(r[0], r[1]), conv, punkt)
                      except (NoSuchElementException,WebDriverException):
                                 sub =''
                      try:
                                 uliza = driver.find_element_by_xpath(u'//ul[@class="breadcrumbs-items"]/li[6]/a/span').text
                      except (NoSuchElementException,WebDriverException):
                                 uliza = ''
           
                      try:
                                 dom = driver.find_element_by_xpath(u'//ul[@class="breadcrumbs-items"]/li[4]/a/span').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 dom = ''                                                       
           
                      try:
                                 seg = driver.find_element_by_xpath(u'//div[@class="commercial--terms"]/ul').text
                      except (NoSuchElementException,WebDriverException):
                                 seg = ''                                            
                      try:
                                 naz = driver.find_element_by_xpath(u'//ul[@class="breadcrumbs-items"]/li[7]/a/span').text
                      except (NoSuchElementException,WebDriverException):
                                 naz = ''                                                       
                      try:
                                 price = driver.find_element_by_xpath(u'//div[@class="commercial--terms"]/ul/li[1]/p').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 price = ''
           
                      try:
                                 cena_za = driver.find_element_by_xpath(u'//meta[@name="description"]').get_attribute('content').split(': ')[1].split(' ')[0]
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 cena_za = ''
                      try: 
                                 klass = driver.find_element_by_xpath(u'//p[contains(text(),"Класс здания")]').text
                      except (NoSuchElementException,WebDriverException):
                                 klass =''
                      try:
                                 plosh = driver.find_element_by_xpath(u'//p[contains(text(),"Общая площадь")]').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 plosh = ''
           
                      try:
                                 et = driver.find_element_by_xpath(u'//p[contains(text(),"Кол-во этажей")]').text.split(': ')[1]
                      except (NoSuchElementException,WebDriverException):
                                 et = ''
           
                      try:
                                 et2 = driver.title
                      except (NoSuchElementException,WebDriverException):
                                 et2 = ''
           
                      try:
                                 god = driver.find_element_by_xpath(u'//ul[@class="breadcrumbs-items"]/li[5]/a/span').text
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 god =''
           
                      try:
                                 zag = driver.find_element_by_xpath(u'//span[contains(text(),"Площадь комнат")]/following-sibling::span[1]').text
                      except (NoSuchElementException,WebDriverException):
                                 zag =''
           
                      try:
                                 do_m = driver.find_element_by_xpath(u'//span[contains(text(),"Вид из окон")]/following-sibling::span[1]').text
                      except (NoSuchElementException,WebDriverException):
                                 do_m =''                                                       
           
                      try:
                                 opis = driver.find_element_by_xpath(u'//div[@id="full-description"]').text
                      except (NoSuchElementException,WebDriverException):
                                 opis = ''
                      try:
                                 phone = driver.find_element_by_xpath('//div[@class="phone"]').get_attribute('data-phone')
                      except (NoSuchElementException,WebDriverException):
                                 phone = ''
                      try:
                                 lico = driver.find_element_by_xpath(u'//div[@class="name"]').text
                      except (NoSuchElementException,WebDriverException):
                                 lico = ''
           
                      try:
                                 comp = driver.find_element_by_xpath(u'//li[contains(text(),"Пассажирский лифт")]').text.replace(u' лифт','')
                      except (NoSuchElementException,WebDriverException):
                                 comp = ''
           
           
                      try:
                                 data = driver.find_element_by_xpath(u'//div[@class="row"]/div[contains(text(),"Данные ")]').text
                                 data1 = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", data)
                                 data1 = re.sub(u"[.,\-\s]{3,}", " ", data1).replace(u'Данные обновлены ','').split(' ')[0].replace('-','.')
                      except (NoSuchElementException,IndexError,WebDriverException):
                                 data1=''
                      try:
                                 mesto = sub+', '+punkt+', '+ray+', '+uliza
                      except (NoSuchElementException,WebDriverException):
                                 mesto =''
                      try:
                                 park = driver.find_element_by_xpath(u'//div[contains(text(),"Срок сдачи")]/following-sibling::div[1]').text
                      except (NoSuchElementException,WebDriverException):
                                 park =''
                      try:
                                 vent = driver.find_element_by_xpath(u'//div[@class="main-slider-map__location"]').text
                      except (NoSuchElementException,WebDriverException):
                                 vent =''
                      print('*'*50)
                      print ray 
                      print punkt 
                      print sub 
                      print uliza
                      print dom
                      print seg
                      print naz
                      print price
                      print klass
                      print plosh
                      print et
                      print opis
                      print phone
                      print lico
                      print cena_za
                      print data1
                      print mesto
                      print vent
                      print('*'*50)
                      ws.write(result, 0, sub)
                      ws.write(result, 1, ray)
                      ws.write(result, 2, punkt)
                      ws.write(result, 4, uliza)
                      ws.write(result, 3, dom)
                      ws.write(result, 13, seg)
                      ws.write(result, 8, naz)
                      ws.write(result, 11, price)
                      ws.write(result, 28, cena_za)
                      ws.write(result, 10, klass)
                      ws.write(result, 14, plosh)
                      ws.write(result, 16, et)
                      ws.write(result, 33, et2)
                      ws.write(result, 26, god)
                      #ws.write(result, 14, zag)
                      ws.write_string(result, 20, lin[z])
                      ws.write(result, 30, data1)
                      ws.write(result, 18, opis)
                      ws.write(result, 21, phone)
                      ws.write(result, 22, lico)
                      ws.write(result, 19, u'Officescanner')
                      ws.write(result, 31, datetime.today().strftime('%d.%m.%Y'))
                      ws.write(result, 25, mesto)
                      ws.write(result, 5, vent)
                      result+=1
                      #driver.delete_all_cookies()                      
                      time.sleep(2)
                      z=z+1
except KeyboardInterrupt:
           pass
           
print('Save it...')
time.sleep(2)
workbook.close()
time.sleep(2)
driver.close()
#display.stop()
print('Done')




          


 

