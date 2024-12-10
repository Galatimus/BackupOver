#!/usr/bin/python
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

print (sys.version)




profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/cqryyjra.default/') #Gui1
##profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/o5wsi6o1.default/')#Gui2
##profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("javascript.enabled", False)
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,capabilities={"marionette": False},timeout=90)



#ua = dict(DesiredCapabilities.PHANTOMJS)
#ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
#driver = webdriver.PhantomJS(service_args=["--load-images=no","--ignore-ssl-errors=true"])
####driver = webdriver.PhantomJS()
#driver.set_window_position(0,0)
#driver.set_window_size(800,800)

time.sleep(2)

driver.set_window_position(0,0)
driver.set_window_size(800,400)
          
workbook = xlsxwriter.Workbook(u'CIAN_НовостройкиНАО.xlsx')


ws = workbook.add_worksheet()
ws.write(0, 0, u"ID")
ws.write(0, 1, u"КОЛИЧЕСТВО_КОМНАТ")
ws.write(0, 2, u"МЕТРО")
ws.write(0, 3, u"АДРЕС")
ws.write(0, 4, u"ПЛОЩАДЬ_ОБЩАЯ,м2")
ws.write(0, 5, u"ПЛОЩАДЬ_ЖИЛАЯ,м2")
ws.write(0, 6, u"ПЛОЩАДЬ_КУХНЯ,м2")
ws.write(0, 7, u"ЭТАЖ")
ws.write(0, 8, u"ЭТАЖНОСТЬ")
ws.write(0, 9, u"ТИП_ДОМА")
ws.write(0, 10, u"ПАРКОВКА")
ws.write(0, 11, u"ЦЕНА")
ws.write(0, 12, u"ТЕЛЕФОН")
ws.write(0, 13, u"ОТДЕЛКА")
ws.write(0, 14, u"ПЛОЩАДЬ_КОМНАТ")
ws.write(0, 15, u"ОКНА")
ws.write(0, 16, u"САНУЗЕЛ")	
ws.write(0, 17, u"НАЗВАНИЕ_ЖК")
ws.write(0, 18, u"ВЫСОТА_ПОТОЛКОВ,м")
ws.write(0, 19, u"ЛИФТ")
ws.write(0, 20, u"ССЫЛКА_НА_ОБЪЯВЛЕНИЕ")
ws.write(0, 21, u"ОПИСАНИЕ")
ws.write(0, 22, u"СРОК_СДАЧИ")
ws.write(0, 23, u"ЗАСТРОЙЩИК")
result= 1           
           
my_url = 'https://erzrf.ru/novostroyki?regionKey=143245001&region=kurskaya-oblast&costType=1&sortType=rating&viewMode=list&scrollTo=viewMode'
driver.get(my_url)
time.sleep(2)

lin = []
for x in range(1,34):
           try:
                      driver.set_page_load_timeout(30)
                      driver.get(my_url+'&page=%d'%x)
           except TimeoutException:
                      driver.execute_script("window.stop();")
           time.sleep(3)           
           for link in driver.find_elements_by_xpath(u'//h3/a'):
                      url = link.get_attribute('href')   
                      print url
                      lin.append(url)
           print '***',len(lin),'****'
           time.sleep(1)

           
links = open('erzrf.txt', 'w')
for item in lin:
           links.write("%s\n" % item)
links.close()            
time.sleep(1)            
print'SAVE and NEXT'
time.sleep(3) 
z=0
lin= open('erzrf.txt').read().splitlines()


           
while z < len(lin): 
           print z+1,'/',str(len(lin))
           try:
                      driver.set_page_load_timeout(30)
                      driver.get(lin[z]) 
           except TimeoutException:
                      driver.execute_script("window.stop();")
           time.sleep(1)           
           
           try:
                      WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,u'//div[@id="captcha"]')))
                      driver.set_window_size(800,700)
                      raw_input("Press Enter to continue ...") 
                      time.sleep(3)
                      driver.set_window_size(800,500)
           except TimeoutException:
                      print "NEXT!"           
           
           print lin[z]
           
           
           try:
                      driver.find_element_by_xpath(u'//button[@class="cui-modal__close"]').click()
           except (NoSuchElementException,WebDriverException):
                      pass                                            
           
           try:
                      ray = re.sub(u'[^\d]','',lin[z])
                      
           except (NoSuchElementException,WebDriverException):
                      ray = ''
           try:
                      punkt=driver.find_element_by_xpath(u'//h1').text.split('-')[0].split(', ')[0]
           except (NoSuchElementException,WebDriverException):
                      punkt = ''                                            
           try:
                      ter = driver.find_element_by_xpath(u'//ul[@class="undergrounds--3OsCQ"]/li').text
           except (NoSuchElementException,WebDriverException):
                      ter =''
           try:
                      uliza = driver.find_element_by_xpath(u'//address[@class="address--D3O4n"]').text.replace(u'На карте','')
           except (NoSuchElementException,WebDriverException):
                      uliza = ''
                      
           try:
                      dom = driver.find_element_by_xpath(u'//div[contains(text(),"Общая")]/following-sibling::div[1]').text
           except (NoSuchElementException,WebDriverException):
                      dom = ''                                                       
                      
           try:
                      seg = driver.find_element_by_xpath(u'//div[contains(text(),"Жилая")]/following-sibling::div[1]').text
           except (NoSuchElementException,WebDriverException):
                      seg = ''                                            
           try:
                      naz = driver.find_element_by_xpath(u'//div[contains(text(),"Кухня")]/following-sibling::div[1]').text
           except (NoSuchElementException,WebDriverException):
                      naz = ''                                                       
           try:
                      price = driver.find_element_by_xpath(u'//div[contains(text(),"Этаж")]/following-sibling::div[1]').text.split(u' из ')[0]
           except (NoSuchElementException,WebDriverException):
                      price = ''
                      
           try:
                      cena_za = driver.find_element_by_xpath(u'//div[contains(text(),"Этаж")]/following-sibling::div[1]').text.split(u' из ')[1] 
           except (NoSuchElementException,IndexError,WebDriverException):
                      cena_za = ''
           try: 
                      klass = driver.find_element_by_xpath(u'//span[contains(text(),"Тип дома")]/following-sibling::span[1]').text
           except (NoSuchElementException,WebDriverException):
                      klass =''
           try:
                      plosh = driver.find_element_by_xpath(u'//li[contains(text(),"Паркинг")]').text.replace(u'Паркинг',u'Открытая')
           except (NoSuchElementException,WebDriverException):
                      plosh = ''
                      
           try:
                      et = driver.find_element_by_xpath(u'//span[@class="price_value--XlUfS"]').text
           except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                      et = ''
           
           try:
                      et2 = re.findall(u'tel:(.*?)"',driver.page_source)[0]
           except (NoSuchElementException,IndexError,NoSuchWindowException,WebDriverException):
                      et2 = ''
                      
           try:
                      god = driver.find_element_by_xpath(u'//span[contains(text(),"Отделка")]/following-sibling::span[1]').text
           except (NoSuchElementException,WebDriverException):
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
                      opis = u'Совмещённый'+' '+driver.find_element_by_xpath('//span[contains(text(),"Совмещённый санузел")]/following-sibling::span[1]').text
           except (NoSuchElementException,IndexError,WebDriverException):
                      opis = ''
           try:
                      phone = driver.find_element_by_xpath('//div[@class="container--dcMOP"]/a').text.replace(u'в ','')
           except (NoSuchElementException,IndexError,WebDriverException):
                      phone = ''
           try:
                      lico = driver.find_element_by_xpath(u'//span[contains(text(),"Высота потолков")]/following-sibling::span[1]').text
           except (NoSuchElementException,IndexError,WebDriverException):
                      lico = ''
                      
           try:
                      comp = driver.find_element_by_xpath(u'//li[contains(text(),"Пассажирский лифт")]').text.replace(u' лифт','')
           except (NoSuchElementException,WebDriverException):
                      comp = ''
                      

           try:
                      data1 = driver.find_element_by_xpath(u'//li[contains(text(),"Грузовой лифт")]').text.replace(u' лифт','')
           except (NoSuchElementException,WebDriverException):
                      data1=''
           try:
                      mesto = driver.find_element_by_xpath(u'//p[@class="description-text--3SshI"]').text
           except (NoSuchElementException,WebDriverException):
                      mesto =''
           #try:
                      #elek = re.findall(u'tel:(.*?)"',driver.page_source)[0]
                      #print elek
           #except (NoSuchElementException,WebDriverException):
                      #elek =''
                      
           try:
                      park = driver.find_element_by_xpath(u'//div[contains(text(),"Срок сдачи")]/following-sibling::div[1]').text
           except (NoSuchElementException,WebDriverException):
                      park =''
                      

                      
           try:
                      vent = driver.find_element_by_xpath(u'//h2[@class="title--3rget"]').text
           except (NoSuchElementException,WebDriverException):
                      vent =''
                      
                                                       
                      
                      
           print('*'*50)
           #print ray 
           #print punkt 
           #print ter 
           #print uliza
           #print dom
           #print seg
           #print naz
           #print price
           #print klass
           #print plosh
           #print opis
           #print phone
           #print lico
           #print comp
           #print data1
           #print mesto
           print et2
           print('*'*50)
           ws.write(result, 0, ray)
           ws.write(result, 1, punkt)
           ws.write(result, 2, ter)
           ws.write(result, 3, uliza)
           ws.write(result, 4, dom)
           ws.write(result, 5, seg)
           ws.write(result, 6, naz)
           ws.write(result, 7, price)
           ws.write(result, 8, cena_za)
           ws.write(result, 9, klass)
           ws.write(result, 10, plosh)
           ws.write(result, 11, et)
           ws.write(result, 12, et2)
           ws.write(result, 13, god)
           ws.write(result, 14, zag)
           ws.write_string(result, 20, lin[z])                                            
           ws.write(result, 15, do_m)
           ws.write(result, 16, opis)
           ws.write(result, 17, phone)
           ws.write(result, 18, lico)
           ws.write(result, 19, comp+', '+data1)
           ws.write(result, 21, mesto)
           ws.write(result, 22, park)
           ws.write(result, 23, vent)
           result+=1
           #time.sleep(1) 
           #driver.get("about:blank")
           #driver.delete_all_cookies()
           time.sleep(1)
           z=z+1
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')    
#command = 'mount -a'
#os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
workbook.close()
print('Done')
driver.close()


          


 

