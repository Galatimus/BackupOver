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


profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ymoy2ffu.default/')#Gui1
#profile = webdriver.FirefoxProfile()
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)
driver.set_window_position(0,0)
driver.set_window_size(850,500)


#time.sleep(2)


#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')


i = 21
ls= open('Links/zemm.txt').read().splitlines()
dc = len(ls)

oper = u'Продажа'



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
           #time.sleep(1)   
           #driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//div[@class="c-footer-copyright"]'))
           #time.sleep(1)   
           #driver.find_element_by_xpath(u'//div[@class="c-footer-tomobile"]/a').click()
           #time.sleep(3)           
           
                      
                      
           workbook = xlsxwriter.Workbook(u'zem/Cian_%s' % sub + u'_Земля_'+oper+str(i+1)+'.xlsx')
           ws = workbook.add_worksheet(u'Rosrealt_Земля')
           ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
           ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
           ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
           ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
           ws.write(0, 4, u"УЛИЦА")
           ws.write(0, 5, u"ДОМ")
           ws.write(0, 6, u"ОРИЕНТИР")
           ws.write(0, 7, u"ТРАССА")
           ws.write(0, 8, u"УДАЛЕННОСТЬ")
           ws.write(0, 9, u"ОПЕРАЦИЯ")
           ws.write(0, 10, u"СТОИМОСТЬ")
           ws.write(0, 11, u"ЦЕНА_ЗА_СОТКУ")
           ws.write(0, 12, u"ПЛОЩАДЬ")
           ws.write(0, 13, u"КАТЕГОРИЯ_ЗЕМЛИ")
           ws.write(0, 14, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
           ws.write(0, 15, u"ГАЗОСНАБЖЕНИЕ")
           ws.write(0, 16, u"ВОДОСНАБЖЕНИЕ")
           ws.write(0, 17, u"КАНАЛИЗАЦИЯ")
           ws.write(0, 18, u"ЭЛЕКТРОСНАБЖЕНИЕ")
           ws.write(0, 19, u"ТЕПЛОСНАБЖЕНИЕ")
           ws.write(0, 20, u"ОХРАНА")
           ws.write(0, 21, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
           ws.write(0, 22, u"ОПИСАНИЕ")
           ws.write(0, 23, u"ИСТОЧНИК_ИНФОРМАЦИИ")
           ws.write(0, 24, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
           ws.write(0, 25, u"ТЕЛЕФОН")
           ws.write(0, 26, u"КОНТАКТНОЕ_ЛИЦО")
           ws.write(0, 27, u"КОМПАНИЯ")
           ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
           ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
           ws.write(0, 30, u"ДАТА_ПАРСИНГА")
           ws.write(0, 31, u"ВИД_ПРАВА")
           ws.write(0, 32, u"МЕСТОПОЛОЖЕНИЕ")
           result= 1           
           lin = []





           while True:
                      print '****',len(lin),'****'
                      try:
                                 try:
                                            WebDriverWait(driver, 1000).until_not(lambda driver: driver.find_element_by_xpath(u'//div[@class="preload0verlay--3TfSc"]').is_displayed())
                                            print "Page is ready!"
                                            print i+1,'/',dc 
                                            time.sleep(1)                                            
                                 except TimeoutException:
                                            break
                                 time.sleep(1)
                                 for link in driver.find_elements_by_xpath(u'//a[contains(@href,"sale/suburban")]'):
                                            url = link.get_attribute('href')   
                                            print url
                                            lin.append(url)
                                 time.sleep(1)   
                                 driver.execute_script("arguments[0].scrollIntoView(false);",driver.find_element_by_xpath(u'//ul[@class="list--35Suf"]'))                                 
                                 time.sleep(1)
                                 driver.find_element_by_xpath(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').click()
                                 time.sleep(3)
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
                                                       ray = driver.find_element_by_xpath(u'//address[@class="address--D3O4n"]/a[contains(text(),"р-н ")]').text
                                                       
                                            except NoSuchElementException:
                                                       ray = ''
                                            try:
                                                       punkt= driver.find_element_by_xpath(u'//p[@class="pbig"]/a[1]').text.replace(ray,'')
                                            except NoSuchElementException:
                                                       punkt = ''                                            
                                            try:
                                                       ter = driver.find_element_by_xpath(u'//p[@class="pbig"]/a[contains(@href,"rajon")]/b').text
                                            except NoSuchElementException:
                                                       ter =''
                                            try:
                                                       uliza = driver.find_element_by_xpath(u'//a[contains(@href,"?ul=")]').text
                                            except NoSuchElementException:
                                                       uliza = ''
                                           
                                            try:
                                                       try:
                                                                  price = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Общая стоимость")]/following::p[1]').text
                                                       except NoSuchElementException:
                                                                  price = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Стоимость аренды в месяц")]/following::p[1]').text+u' /мес'
                                            except NoSuchElementException:
                                                       price = ''
                                                       
                                            try:
                                                       try:
                                                                  try:
                                                                             cena_za = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Цена за сотку")]/following::p[1]').text
                                                                  except NoSuchElementException:
                                                                             cena_za = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Цена за гектар")]/following::p[1]').text+u' /Га'
                                                       except NoSuchElementException:
                                                                  cena_za = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Стоимость аренды 1 сотки в месяц")]/following::p[1]').text+u' /мес'
                                            except NoSuchElementException:
                                                       cena_za = ''
                                                       
                                            try: 
                                                       klass = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Класс")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       klass =''
                                            try:
                                                       plosh = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Площадь")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       plosh = ''
                                            try:
                                                       opis = driver.find_element_by_xpath(u'//div[@class="section_right"]/following-sibling::div[1]').text.replace(u'Поделиться…','')  
                                            except NoSuchElementException:
                                                       opis = ''
                                            try:
                                                       phone = re.sub('[^\d]', u'',driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Контакты")]/following::p[1]').text)
                                            except NoSuchElementException:
                                                       phone = ''
                                            try:
                                                       lico = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Контакты")]/following::p[1]').text.split(', ')[1]
                                            except (NoSuchElementException,IndexError):
                                                       lico = ''
                                                       
                                            try:
                                                       comp = driver.find_element_by_xpath(u'//p[contains(text(),"Автор")]/following::p[2]').text
                                            except NoSuchElementException:
                                                       comp = ''
                                            try:
                                                       vid_prava = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Вид собственности")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       vid_prava = ''
                                                       
                                            try:
                                                       vid_iz = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Назначение земли")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       vid_iz = ''                                                       
                                                       
                                            try:
                                                       data = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Обновлено")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       data = ''
                                            try:
                                                       data1 = driver.find_element_by_xpath(u'//p[@class="pbig_gray"][contains(text(),"Добавлено")]/following::p[1]').text
                                            except NoSuchElementException:
                                                       data1=''
                                            try:
                                                       mesto = driver.find_element_by_xpath(u'//h1/following::div[@class="info"][1]/p').text
                                            except NoSuchElementException:
                                                       mesto =''
                                            print('*'*50)
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
                                            print('*'*50)
                                            ws.write(result, 0, sub)
                                            ws.write(result, 1, ray)
                                            ws.write(result, 2, punkt)
                                            ws.write(result, 3, ter)
                                            ws.write(result, 4, uliza)
                                            ws.write(result, 11, cena_za)
                                            ws.write(result, 13, klass)
                                            ws.write(result, 10, price)
                                            ws.write(result, 12, plosh)
                                            ws.write(result, 22, opis)
                                            ws.write(result, 23, u'ЦИАН')
                                            ws.write_string(result, 24, line)                                            
                                            ws.write(result, 25, phone)
                                            ws.write(result, 26, lico)
                                            ws.write(result, 27, comp)
                                            ws.write(result, 29, data)
                                            ws.write(result, 28, data1)
                                            ws.write(result, 9, oper)
                                            ws.write(result, 31, vid_prava)
                                            ws.write(result, 14, vid_iz)
                                            ws.write(result, 30, datetime.today().strftime('%d.%m.%Y'))
                                            ws.write(result, 32, mesto)
                                            result+=1
                                            z=z+1
                                 workbook.close()
                                 time.sleep(1) 
                                 driver.get("about:blank")
                                 driver.delete_all_cookies()
                                 time.sleep(1)                                 
                                 break
           i=i+1 



 

