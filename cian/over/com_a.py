#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException,NoSuchWindowException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ljpce52l.default/') #Gui2
profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/tmxg2mqd.default/')#Gui1
#profile = webdriver.FirefoxProfile()
profile.native_events_enabled = False


#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)
#driver.set_window_position(0,0)
#driver.set_window_size(1000,420)
#time.sleep(3)


i = 49
ls= open('Links/com_a.txt').read().splitlines()
dc = len(ls)

oper = u'Аренда'



while i < len(ls):
           print '********************************************************************************************'
           print i+1,'/',dc
           driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)
           driver.set_window_position(0,0)
           driver.set_window_size(1000,700)
           time.sleep(3)
           driver.get(ls[i])    
           print ls[i]
           time.sleep(2)
           sub = driver.find_element_by_xpath(u'//div[@data-mark="locationSwitcher"]/button').text
           print sub
          
           workbook = xlsxwriter.Workbook(u'com/Cian_%s' % sub + u'_Коммерческая_'+oper+str(i+1)+'.xlsx')
           ws = workbook.add_worksheet(u'Cian_Коммерческая')
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
           ws.write(0, 36, u"ТРАССА")
           ws.write(0, 37, u"ПАРКОВКА")
           ws.write(0, 38, u"ОХРАНА")
           ws.write(0, 39, u"КОНДИЦИОНИРОВАНИЕ")
           ws.write(0, 40, u"ИНТЕРНЕТ")
           ws.write(0, 41, u"ТЕЛЕФОН (КОЛИЧЕСТВО ЛИНИЙ)")
           ws.write(0, 42, u"УСЛУГИ")
           ws.write(0, 43, u"СИСТЕМА ВЕНТИЛЯЦИИ")
           result= 1           
           lin = []





           while True:
                      print '********************',len(lin),'**********************'
                      try:
                                 try:
                                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,u'//h3/a')))
                                            print "Page is ready!"
                                 except TimeoutException:
                                            driver.find_element_by_xpath(u'//button[@class="cui-modal__close"]').click()
                                 time.sleep(1)
                                 for link in driver.find_elements_by_xpath(u'//h3/a'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)
                                 time.sleep(1)   
                                 driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//ul[@class="list--35Suf"]'))                                 
                                 time.sleep(1)
                                 driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').click()
                                 time.sleep(2)
                      except (NoSuchElementException,WebDriverException):
                                 z=0
                                 for line in lin:
                                            print z+1,'/',str(len(lin))+' - '+ sub+' '+str(i+1),'/',str(dc)     
                                            driver.get(line)
                                            time.sleep(3)
                                            print line
                                            try:
                                                       driver.find_element_by_xpath(u'//button[@class="cui-modal__close"]').click()
                                            except (NoSuchElementException,WebDriverException):
                                                       pass                                            
                                            
                                            try:
                                                       ray = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').text
                                                       
                                            except (NoSuchElementException,WebDriverException):
                                                       ray = ''
                                            try:
                                                       if sub == u'Москва':
                                                                  punkt= u'Москва'
                                                       elif sub == u'Санкт-Петербург':
                                                                  punkt= u'Санкт-Петербург'
                                                       elif sub == u'Севастополь':
                                                                  punkt= u'Севастополь'
                                                       else:
                                                                  if  driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[2][contains(text(),"район")]').is_displayed():
                                                                             punkt= driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[3]').text
                                                                  elif driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[3][contains(text(),"район")]').is_displayed():
                                                                             punkt= driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[2]').text
                                                                  else:
                                                                             punkt=driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[2]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       punkt = ''                                            
                                            try:
                                                       ter = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район ")]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       ter =''
                                            try:
                                                       try:
                                                                  try:
                                                                             try:
                                                                                        try:
                                                                                                   try:
                                                                                                              try:
                                                                                                                         try:
                                                                                                                                    uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ул.")]').text
                                                                                                                         except (NoSuchElementException,WebDriverException):
                                                                                                                                    uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пер.")]').text
                                                                                                              except (NoSuchElementException,WebDriverException):
                                                                                                                         uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"просп.")]').text
                                                                                                   except (NoSuchElementException,WebDriverException):
                                                                                                              uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ш.")]').text
                                                                                        except (NoSuchElementException,WebDriverException):
                                                                                                   uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"бул.")]').text
                                                                             except (NoSuchElementException,WebDriverException):
                                                                                        uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"проезд")]').text
                                                                  except (NoSuchElementException,WebDriverException):
                                                                             uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"наб.")]').text
                                                       except (NoSuchElementException,WebDriverException):
                                                                  uliza = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пл.")]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       uliza = ''
                                                       
                                            try:
                                                       if uliza == '':
                                                                  dom =''
                                                       else:
                                                                  dom = driver.find_element_by_xpath(u'//h1[@class="object_descr_addr"]/a[contains(@href,"house")]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       dom = ''                                                       
                                                       
                                            try:
                                                       seg = driver.find_element_by_xpath(u'//dt[contains(text(),"Тип здания:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       seg = ''                                            
                                            try:
                                                       naz = driver.find_element_by_xpath(u'//div[@class="object_descr_title"]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       naz = ''                                                       
                                            try:
                                                       price = driver.find_element_by_xpath(u'//div[@class="object_descr_price"]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       price = ''
                                                       
                                            try:
                                                       cena_za = driver.find_element_by_xpath(u'//p[@class="pbig"]/b[contains(text(),"руб.")]/preceding::p[1]').text.replace(u'Цена за ','').replace(u'Стоимость аренды ','').replace(u'кв.м.',u'м2').replace(u' в ',u'/').replace(u'Общая стоимость','') 
                                            except (NoSuchElementException,WebDriverException):
                                                       cena_za = ''
                                            try: 
                                                       klass = driver.find_element_by_xpath(u'//dt[contains(text(),"Класс:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       klass =''
                                            try:
                                                       plosh = driver.find_element_by_xpath(u'//dt[contains(text(),"Площадь:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       plosh = ''
                                                       
                                            try:
                                                       et = driver.find_element_by_xpath(u'//dt[contains(text(),"Этаж:")]/following-sibling::dd[1]').text.split(u' из ')[0]
                                            except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                                                       et = ''
                                            
                                            try:
                                                       et2 = driver.find_element_by_xpath(u'//dt[contains(text(),"Этаж:")]/following-sibling::dd[1]').text.split(u' из ')[1]
                                            except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                                                       et2 = ''
                                                       
                                            try:
                                                       god = driver.find_element_by_xpath(u'//dt[contains(text(),"Год постройки:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       god =''
                                                       
                                            try:
                                                       zag = driver.find_element_by_xpath(u'//p[@class="objects_item_metro_prg"]/a').text
                                            except (NoSuchElementException,WebDriverException):
                                                       zag =''
                                                       
                                            try:
                                                       do_m = driver.find_element_by_xpath(u'//p[@class="objects_item_metro_prg"]/span[2]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       do_m =''                                                       
                                                       
                                            try:
                                                       #ln = []
                                                       #for m in driver.find_elements_by_xpath(u'//div[@class="object_descr_text"]/text()'):
                                                                  #urr = m.text
                                                                  #ln.append(urr)
                                                       #opis = "".join(ln)
                                                       opis = driver.find_element_by_xpath('//div[@class="object_descr_text"]').text.split(u'Показать ')[0]
                                            except (NoSuchElementException,IndexError,WebDriverException):
                                                       opis = ''
                                            try:
                                                       #phone = re.sub('[^\d]', '',driver.find_element_by_xpath('//div[@class="cf_offer_show_phone-number"]/a').text)
                                                       phone = re.findall(u'tel:(.*?)">',driver.page_source)[0]
                                            except (NoSuchElementException,IndexError,WebDriverException):
                                                       phone = ''
                                            try:
                                                       try:
                                                                  lico = driver.find_element_by_xpath(u'//h3[@class="realtor-card__title"][contains(text(),"Представитель: ")]').text.replace(u'Представитель: ','')
                                                       except (NoSuchElementException,IndexError):
                                                                  lico = driver.find_element_by_xpath(u'//h3[@class="realtor-card__title"]/a[contains(@href,"agents")]').text
                                            except (NoSuchElementException,IndexError,WebDriverException):
                                                       lico = ''
                                                       
                                            try:
                                                       try:
                                                                  comp = driver.find_element_by_xpath(u'//h3[@class="realtor-card__title"]/a[contains(@href,"company")]').text
                                                       except (NoSuchElementException,WebDriverException):
                                                                  comp = driver.find_element_by_xpath(u'//h4[@class="realtor-card__subtitle"]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       comp = ''
                                                       
                                            try:
                                                       conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
                                                       (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
                                                       (u'Окт', '.10.2017'),(u'окт', '.10.2017'),
                                                       (u'Сен', '.09.2017'),(u'сен', '.09.2017'),
                                                       (u'Авг', '.08.2017'),(u'авг', '.08.2017'),
                                                       (u'Июл', '.07.2017'),(u'июл', '.07.2017'),
                                                       (u'Июн', '.06.2017'),(u'июн', '.06.2017'),
                                                       (u'Фев', '.02.2017'),(u'фев', '.02.2017'),
                                                       (u'Мар', '.03.2017'),(u'мар', '.03.2017'),
                                                       (u'Апр', '.04.2017'),(u'апр', '.04.2017'), 
                                                       (u'Янв', '.01.2017'),(u'янв', '.01.2017'),
                                                       (u'Ноя', '.11.2017'),(u'ноя', '.11.2017'),
                                                       (u'Дек', '.12.2017'),(u'дек', '.12.2017'),
                                                       (u'Май', '.05.2017'),(u'май', '.05.2017')]
                                                       dt= driver.find_element_by_xpath(u'//ul[@class="offerStatuses"]/following-sibling::span[@class="object_descr_dt_added"]').text.split(', ')[0]
                                                       data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
                                            except (NoSuchElementException,WebDriverException):
                                                       data = ''
                                            try:
                                                       data1 = driver.find_element_by_xpath(u'//dt[contains(text(),"Кондиционирование:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       data1=''
                                            try:
                                                       mesto = driver.find_element_by_xpath(u'//h1').text
                                            except (NoSuchElementException,WebDriverException):
                                                       mesto =''
                                            try:
                                                       elek = driver.title
                                            except (NoSuchElementException,WebDriverException):
                                                       elek =''
                                                       
                                            try:
                                                       park = driver.find_element_by_xpath(u'//dt[contains(text(),"Парковка:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       park =''
                                                       
                                            try:
                                                       lat = re.findall(u"center: (.*?)],",driver.page_source)[0].split(',')[0].replace('[','')
                                            except (NoSuchElementException,IndexError):
                                                       lat =''
                                                       
                                            try:
                                                       lng = re.findall(u"center: (.*?)],",driver.page_source)[0].split(',')[1]
                                            except (NoSuchElementException,IndexError):
                                                       lng =''
                                                       
                                            try:
                                                       vent = driver.find_element_by_xpath(u'//dt[contains(text(),"Вентиляция:")]/following-sibling::dd[1]').text
                                            except (NoSuchElementException,WebDriverException):
                                                       vent =''
                                                       
                                            try:
                                                       li = []
                                                       for e in driver.find_elements_by_xpath(u'//ul[@class="cf-comm-offer-detail__infrastructure"]/li'):
                                                                  ur = e.text
                                                                  li.append(ur)		
                                                       uslu = ",".join(li)
                                            except (NoSuchElementException,WebDriverException):
                                                       uslu = ''                                                       
                                                       
                                                       
                                            print('*'*50)
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
                                            print data
                                            print data1
                                            print mesto
                                            print lat
                                            print lng
                                            print elek
                                            print('*'*50)
                                            ws.write(result, 0, sub)
                                            ws.write(result, 1, ray)
                                            ws.write(result, 2, punkt)
                                            ws.write(result, 3, ter)
                                            ws.write(result, 4, uliza)
                                            ws.write(result, 5, dom)
                                            ws.write(result, 7, seg)
                                            ws.write(result, 9, naz)
                                            ws.write(result, 10, klass)
                                            ws.write(result, 11, price)
                                            ws.write(result, 14, plosh)
                                            ws.write(result, 15, et)
                                            ws.write(result, 16, et2)
                                            ws.write(result, 17, god)
                                            ws.write(result, 18, opis)
                                            ws.write(result, 19, u'ЦИАН')
                                            ws.write_string(result, 20, driver.current_url)                                            
                                            ws.write(result, 21, phone)
                                            ws.write(result, 22, lico)
                                            ws.write(result, 23, comp)
                                            ws.write(result, 29, data)
                                            ws.write(result, 39, data1)
                                            ws.write(result, 28, oper)
                                            ws.write(result, 31, datetime.today().strftime('%d.%m.%Y'))
                                            ws.write(result, 24, mesto)
                                            ws.write(result, 26, zag)
                                            ws.write(result, 27, do_m)
                                            ws.write(result, 33, elek)
                                            ws.write(result, 34, lng)
                                            ws.write(result, 35, lat)
                                            ws.write(result, 37, park)
                                            ws.write(result, 42, uslu)
                                            ws.write(result, 43, vent)
                                            result+=1
                                            driver.delete_cookie
                                            z=z+1
                                 workbook.close()
                                 driver.close()
                                 time.sleep(3)
                                 break
           i=i+1 



 

