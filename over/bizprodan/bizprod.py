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
from sub import conv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ljpce52l.default/') #Gui2
profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/n1ddsdpx.default/')#Gui1
#profile = webdriver.FirefoxProfile()
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)


time.sleep(3)

driver.set_window_position(0,0)
driver.set_window_size(900,600)

driver.get("http://bizprodan.ru/")
time.sleep(2) 


driver.find_element_by_xpath('//li[@class="logout"]/a').click()
time.sleep(1)
driver.find_element_by_id('user_email').send_keys('galatimus@mail.ru')
driver.find_element_by_id('user_password').send_keys('walter2005')
time.sleep(1)
driver.find_element_by_name('commit').click()

time.sleep(5)

workbook = xlsxwriter.Workbook(u'Bizprodan_Готовый_бизнес.xlsx')
ws = workbook.add_worksheet(u'Bizprodan')
ws.write(0, 0,u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
ws.write(0, 2, u"ОРИЕНТИР")
ws.write(0, 3, u"НАСЕЛЕННЫЙ_ПУНКТ")
ws.write(0, 4, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
ws.write(0, 5, u"УЛИЦА")
ws.write(0, 6, u"ДОМ")
ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
ws.write(0, 10, u"СФЕРА БИЗНЕСА")
ws.write(0, 11, u"ОПЕРАЦИЯ")
ws.write(0, 12, u"СПОСОБ РЕАЛИЗАЦИИ")
ws.write(0, 13, u"ЦЕНА ПРОДАЖИ")
ws.write(0, 14, u"ЭТАЖНОСТЬ")
ws.write(0, 15, u"СОСТОЯНИЕ")
ws.write(0, 16, u"ПРОДАВАЕМАЯ ДОЛЯ В БИЗНЕСЕ")
ws.write(0, 17, u"СРЕДНЕМЕСЯЧНЫЙ ОБОРОТ")
ws.write(0, 18, u"ЕЖЕМЕСЯЧНАЯ ЧИСТАЯ ПРИБЫЛЬ")
ws.write(0, 19, u"ЧИСЛО СОТРУДНИКОВ")
ws.write(0, 20, u"НАЛИЧИЕ ДОЛГОВЫХ ОБЯЗАТЕЛЬСТВ")
ws.write(0, 21, u"СРОК ОКУПАЕМОСТИ")
ws.write(0, 22, u"СРОК СУЩЕСТВОВАНИЯ БИЗНЕСА")
ws.write(0, 23, u"ОСНОВНЫЕ СРЕДСТВА")
ws.write(0, 24, u"ПРИЧИНА ПРОДАЖИ")
ws.write(0, 25, u"ОПИСАНИЕ")
ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
ws.write(0, 28, u"ТЕЛЕФОН ПРОДАВЦА")
ws.write(0, 29, u"ДАТА_ДЕЙСТВИЯ_ПРЕДЛОЖЕНИЯ")
ws.write(0, 30, u"ДАТА ПАРСИНГА")
ws.write(0, 31, u"ЗАГОЛОВОК")
ws.write(0, 32, u"АДРЕС")
ws.write(0, 33, u"ОБОРУДОВАНИЕ")
ws.write(0, 34, u"ОСНОВНЫЕ_ТОВАРЫ_НА_ПРОДАЖУ")
row = 1

lin = open('bizpr.txt').read().splitlines()


v = 1
for line in lin:
        print v,'/',len(lin)
        try:
                driver.set_page_load_timeout(10)
                driver.get(line)
        except TimeoutException:
                driver.execute_script("window.stop();")
        
        print "Page is ready!"
        time.sleep(2)
        
        
        try:
                dt= driver.find_element_by_xpath(u'//div[@class="info"]/span[contains(text(),"г. ")][1]').text.split(', ')[0].replace(u'г. ','')
                sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
                print sub
                ws.write(row, 0, sub)
        except (NoSuchElementException,IndexError):
                sub=''
        try:
                punkt= driver.find_element_by_xpath(u'//div[@class="info"]/span[contains(text(),"г. ")][1]').text.split(', ')[0]
                print punkt
                ws.write(row, 3, punkt)
        except (NoSuchElementException,IndexError):
                punkt=''
        try:
                metro= driver.find_element_by_xpath(u'//div[@class="info"]/span[contains(text(),"г. ")][1]').text.split(', ')[1]
                print metro
                ws.write(row, 7, metro)
        except (NoSuchElementException,IndexError):
                metro=''
        try:
                sfera= driver.find_element_by_xpath(u'//div[@class="info"]/h1').text
                print sfera
                ws.write(row, 10, sfera)
        except (NoSuchElementException,IndexError):
                sfera=''
        try:
                cena= driver.find_element_by_xpath(u'//div[@class="info"]/span[2]').text.replace(u'Цена: ','')
                print cena
                ws.write(row, 13, cena)
        except (NoSuchElementException,IndexError):
                cena=''
        try:
                dolya= driver.find_element_by_xpath(u'//span[contains(text(),"Продаваемая доля:")]').text.split(': ')[1]
                print dolya
                ws.write(row, 16, dolya)
        except (NoSuchElementException,IndexError):
                dolya=''
        try:
                mes= driver.find_element_by_xpath(u'//span[contains(text(),"Выручка в мес.:")]').text.split(': ')[1]
                print mes
                ws.write(row, 17, mes)
        except (NoSuchElementException,IndexError):
                mes=''
        try:
                prib= driver.find_element_by_xpath(u'//span[contains(text(),"Прибыль в мес.:")]').text.split(': ')[1]
                print prib
                ws.write(row, 18, prib)
        except (NoSuchElementException,IndexError):
                prib=''
        try:
                sotr= driver.find_element_by_xpath(u'//span[contains(text(),"Количество сотрудников:")]').text.split(': ')[1]
                print sotr
                ws.write(row, 19, sotr)
        except (NoSuchElementException,IndexError):
                sotr=''
        try:
                vozr= driver.find_element_by_xpath(u'//span[contains(text(),"Возраст бизнеса:")]').text.split(': ')[1]
                print vozr
                ws.write(row, 22, vozr)
        except (NoSuchElementException,IndexError):
                vozr=''
        try:
                sred= driver.find_element_by_xpath(u'//span[contains(text(),"Оборудование:")]/following-sibling::span[1]').text#.split(': ')[1]
                print sred
                ws.write(row, 23, sred)
                ws.write(row, 33, sred)
        except (NoSuchElementException,IndexError):
                sred=''
        try:
                prich= driver.find_element_by_xpath(u'//span[contains(text(),"Причина для продажи:")]').text.split(': ')[1]
                print prich
                ws.write(row, 24, prich)
        except (NoSuchElementException,IndexError):
                prich=''
        try:
                opis= driver.find_element_by_xpath(u'//span[@class="full_description"]/following-sibling::span').text
                print opis
                ws.write(row, 25, opis)
        except (NoSuchElementException,IndexError):
                opis=''
        try:
                phone= re.sub('[^\d]','',driver.find_element_by_xpath(u'//span[contains(text(),"Контактные данные:")]').text.split(': ')[1])[:11]
                print phone
                ws.write(row, 28, phone)
        except (NoSuchElementException,IndexError):
                phone=''
        try:
                data= driver.find_element_by_xpath(u'//span[contains(text(),"Дата обновления:")]').text.split(': ')[1]
                print data
                ws.write(row, 29, data)
        except (NoSuchElementException,IndexError):
                data=''
        try:
                zag = driver.find_element_by_xpath(u'//h1').text
                print zag
                ws.write(row, 31, zag)
        except (NoSuchElementException,IndexError):
                zag =''                
        try:
                web= driver.find_element_by_xpath(u'//span[contains(text(),"Ссылка на сайт:")]/following-sibling::span[1]').text#.split(': ')[1]
                print web
                ws.write_string(row, 31, web)
        except (NoSuchElementException,IndexError):
                web=''
                
        try:
                adr = driver.find_element_by_xpath(u'//span[contains(text(),"Адрес (район, улица, дом):")]/following-sibling::span[1]').text
                print adr
                ws.write(row, 32, adr)
        except (NoSuchElementException,IndexError):
                adr =''
                
        try:
                tov = driver.find_element_by_xpath(u'//span[contains(text(),"Основные товары на продажу:")]/following-sibling::span[1]').text
                print tov
                ws.write(row, 34, tov)
        except (NoSuchElementException,IndexError):
                tov =''                
        
        ws.write(row, 11, 'Продажа')
        ws.write(row, 26, 'Bizprodan.ru')
        ws.write_string(row, 27, driver.current_url)
        ws.write(row, 30, datetime.today().strftime('%d.%m.%Y'))
        
        
        
        
        
        
        
        
        v+=1
        row+=1
        print('*'*100)
        time.sleep(2)
        
        #if v > 10:
             #break          
        
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
#command = 'mount -t cifs //192.168.1.6/e /home/oleg/Pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
##command = 'apt autoremove'
#p = os.system('echo %s|sudo -S %s' % ('1122', command))
#print p
time.sleep(1)
workbook.close()
print('Done!')
