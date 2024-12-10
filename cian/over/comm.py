#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
import xlsxwriter
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime


#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ymoy2ffu.default/')#Gui1
profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/v7uwe0l1.default/')#Gui2
#profile = webdriver.FirefoxProfile()
#profile.set_preference('permissions.default.stylesheet', 2)
#profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)
driver.set_window_position(0,0)
driver.set_window_size(850,500)


#time.sleep(2)


#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')


i = 0
ls= open('Links/com_p.txt').read().splitlines()
dc = len(ls)





while i < len(ls):
           print '********'
           print i+1,'/',dc
           
           time.sleep(3)
           driver.get(ls[i])    
           #print ls[i]
           time.sleep(2)
           try:
                      time.sleep(2)
                      driver.find_element_by_xpath(u'//div[@class="c-app-banner__close"]/button').click()
                      time.sleep(2)
           except (NoSuchElementException,WebDriverException):
                      pass
           
           try:
                      WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                      driver.set_window_size(850,700)
                      #driver.refresh()
                      time.sleep(1) 
                      # find iframe
                      captcha_iframe = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                      ActionChains(driver).move_to_element(captcha_iframe).click().perform()
                      # click im not robot
                      #captcha_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response')))
                      #driver.execute_script("arguments[0].click()", captcha_box)
                      time.sleep(1) 
                      sitekey = re.findall(u"sitekey': '(.*?)'",driver.page_source)[0]
                      print sitekey                      
                      raw_input('Введите число пять  ') 
                      time.sleep(1)           
                      driver.get(ls[i])    
                      #print ls[i]
                      time.sleep(1)
                      driver.set_window_size(850,500)                      
           except TimeoutException:
                      print "NEXT!"           
           
           
           sub = driver.find_element_by_xpath(u'//button[@data-mark="location"]').text
           print sub
           
           
                      
                      
           workbook = xlsxwriter.Workbook(u'com/Cian_%s' % sub + '_'+str(i+1)+'.xlsx')
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
                      print '****',len(lin),'****'
                      try:
                                 try:
                                            #WebDriverWait(driver, 1000).until_not(lambda driver: driver.find_element_by_xpath(u'//div[@class="preload0verlay--3TfSc"]').is_displayed())
                                            WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,u'//ul[@class="list--35Suf"]')))
                                            #WebDriverWait(driver, 10).until(ajax_complete,  "Timeout waiting for page to load")
                                            #WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//ul[@class="list--35Suf"]'))
                                            print "Page is ready!"
                                            print i+1,'/',dc 
                                            time.sleep(1)                                            
                                 except TimeoutException:
                                            break
                                 time.sleep(1)
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/commercial")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"rent/commercial")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)
                                 time.sleep(1)   
                                 driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//ul[@class="list--35Suf"]'))                                 
                                 time.sleep(1)
                                 driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').click()
                                 time.sleep(3)
                                 #raw_input('Введите число пять  ')
                                 try:
                                            time.sleep(3)
                                            driver.find_element_by_xpath(u'//div[@class="button--3JzvW"]').click()
                                            time.sleep(3)
                                 except (NoSuchElementException,WebDriverException):
                                            pass                                 
                      except (NoSuchElementException,WebDriverException):
                                 lin = list(set(lin))
                                 z=0
                                 time.sleep(1) 
                                 driver.get("about:blank")
                                 driver.delete_all_cookies()
                                 time.sleep(1)                                 
                                 for line in lin:
                                            print z+1,'/',str(len(lin))+' - '+ sub+' '+str(i+1),'/',str(dc)     
                                            driver.get(line)
                                            time.sleep(2)
                                            try:
                                                       WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                                                       driver.set_window_size(850,700)
                                                       #driver.refresh()
                                                       time.sleep(1) 
                                                       # find iframe
                                                       captcha_iframe = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                                                       time.sleep(1) 
                                                       ActionChains(driver).move_to_element(captcha_iframe).click().perform()
                                                       # click im not robot
                                                       #captcha_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response')))
                                                       #time.sleep(1) 
                                                       #driver.execute_script("arguments[0].click()", captcha_box)
                                                       time.sleep(1) 
                                                       raw_input('Введите число пять  ') 
                                                       time.sleep(1)
                                                       driver.set_window_size(850,500)                      
                                            except TimeoutException:
                                                       print "NEXT!"                                                       
                                            print line
                                            
                                            try:
                                                       try:
                                                                  ray = driver.find_element_by_xpath(u'//address[@class="address--D3O4n"]/a[contains(text(),"р-н ")]').text
                                                       except NoSuchElementException:
                                                                  ray = driver.find_element_by_xpath(u'//address[@class="address--D3O4n"]/a[contains(text(),"район")]').text
                                            except NoSuchElementException:
                                                       ray = ''
                                            try:
                                                       if sub == u'Москва':
                                                                  punkt= u'Москва'
                                                       elif sub == u'Санкт-Петербург':
                                                                  punkt= u'Санкт-Петербург'
                                                       elif sub == u'Севастополь':
                                                                  punkt= u'Севастополь'
                                                       else:
                                                                  punkt= re.findall(u'fbCity":"(.*?)"',driver.page_source)[0]
                                            except NoSuchElementException:
                                                       punkt = ''                                            
                                            try:
                                                       ter = re.findall(u'house","fullName":"(.*?)"',driver.page_source)[0]
                                            except (NoSuchElementException,IndexError):
                                                       ter =''
                                            try:
                                                       uliza = re.findall(u'street","fullName":"(.*?)"',driver.page_source)[0]
                                            except (NoSuchElementException,IndexError):
                                                       uliza = ''
                                           
                                            try:
                                                       price = driver.find_element_by_xpath(u'//div[@class="price--xQiE6"]').text
                                            except NoSuchElementException:
                                                       price = ''
                                                       
                                            try:
                                                       cena_za = driver.find_element_by_xpath(u'//h1').text.split(', ')[0]
                                            except NoSuchElementException:
                                                       cena_za = ''
                                                       
                                            try: 
                                                       klass = driver.find_element_by_xpath(u'//div[contains(text(),"Класс")]/following-sibling::div[1]').text
                                            except NoSuchElementException:
                                                       klass =''
                                            try:
                                                       plosh = driver.find_element_by_xpath(u'//div[contains(text(),"Площадь")]/following-sibling::div[1]').text
                                            except NoSuchElementException:
                                                       plosh = ''
                                            try:
                                                       opis = driver.find_element_by_xpath(u'//p[@class="description-text--3SshI"]').text  
                                            except NoSuchElementException:
                                                       opis = ''
                                            try:
                                                       phone = re.findall(u'href="tel:(.*?)"',driver.page_source)[0]
                                            except (NoSuchElementException,IndexError):
                                                       phone = ''
                                            try:
                                                       lico = driver.find_element_by_xpath(u'//div[@class="link-wrapper--EDwrd"]/a[contains(@href,"agents")][1]/h2').text
                                            except (NoSuchElementException,IndexError):
                                                       lico = ''
                                                       
                                            try:
                                                       comp = driver.find_element_by_xpath(u'//div[@class="link-wrapper--EDwrd"]/a[contains(@href,"company")][1]/h2').text
                                            except NoSuchElementException:
                                                       comp = ''
                                            try:
                                                       vid_prava = re.findall(u'center=(.*?)&',driver.page_source)[0].split('%2C')[0]
                                            except (NoSuchElementException,IndexError):
                                                       vid_prava = ''
                                                       
                                            try:
                                                       vid_iz = re.findall(u'center=(.*?)&',driver.page_source)[0].split('%2C')[1]
                                            except (NoSuchElementException,IndexError):
                                                       vid_iz = ''                                                       
                                                       
                                            try:
                                                       data = re.sub(u'[^\d\-]','',re.findall(u'editDate(.*?)T',driver.page_source)[0]).replace('-','.')
                                            except (NoSuchElementException,IndexError):
                                                       data = ''
                                            try:
                                                       data1 = driver.title
                                            except NoSuchElementException:
                                                       data1=''
                                            try:
                                                       mesto = driver.find_element_by_xpath(u'//div[@class="address--2T-DP"]').text
                                            except NoSuchElementException:
                                                       mesto =''
                                                       
                                            try:
                                                       kad = re.findall(u'cadastralNumber":"(.*?)"',driver.page_source)[0]
                                            except (NoSuchElementException,IndexError):
                                                       kad =''                                                       
                                                       
                                            try:
                                                       if 'sale' in line:
                                                                  oper = u'Продажа' 
                                                       elif 'rent' in line:
                                                                  oper = u'Аренда'     
                                            except (NoSuchElementException,IndexError):
                                                       oper = '' 
                                                       
                                            print('*'*10)
                                            print ray 
                                            print punkt 
                                            print ter 
                                            print uliza
                                            print cena_za
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
                                            print kad
                                            print('*'*10)
                                            ws.write(result, 0, sub)
                                            ws.write(result, 1, ray)
                                            ws.write(result, 2, punkt)
                                            ws.write(result, 5, ter)
                                            ws.write(result, 4, uliza)
                                            ws.write(result, 9, cena_za)
                                            ws.write(result, 10, klass)
                                            ws.write(result, 11, price)
                                            ws.write(result, 14, plosh)
                                            ws.write(result, 18, opis)
                                            ws.write(result, 19, u'ЦИАН')
                                            ws.write_string(result, 20, line)                                            
                                            ws.write(result, 21, phone)
                                            ws.write(result, 22, lico)
                                            ws.write(result, 23, comp)
                                            ws.write(result, 29, data)
                                            ws.write(result, 33, data1)
                                            ws.write(result, 28, oper)
                                            ws.write(result, 32, kad)
                                            ws.write(result, 35, vid_prava)
                                            ws.write(result, 34, vid_iz)
                                            ws.write(result, 30, datetime.today().strftime('%d.%m.%Y'))
                                            ws.write(result, 24, mesto)
                                            result+=1
                                            z=z+1
                                 workbook.close()
                                 time.sleep(1) 
                                 driver.get("about:blank")
                                 driver.delete_all_cookies()
                                 time.sleep(1)                                 
                                 break
           i=i+1 



 

