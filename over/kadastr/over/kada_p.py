#!/usr/bin/python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import time
#from pyvirtualdisplay import Display
import xlsxwriter
from datetime import datetime
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#display = Display(visible=0, size= (800, 600)) 
#display.start() 


profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/jcpr7q9q.default/')
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,timeout=600)

#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

driver.set_window_position(0,0)
driver.set_window_size(1000,720)

time.sleep(3)

workbook = xlsxwriter.Workbook(u'Кадастровые номера_Готово.xlsx')
ws = workbook.add_worksheet(u'Kadastr_numbers')
ws.write(0,0, u"Кадастровый номер")
ws.write(0,1, u"Статус объекта")
ws.write(0,2, u"Дата постановки на кадастровый учет")
ws.write(0,3, u"Категория земель")
ws.write(0,4, u"Площадь")
ws.write(0,5, u"Тип")
ws.write(0,6, u"Кадастровая стоимость")
ws.write(0,7, u"Кадастровый квартал")
ws.write(0,8, u"Адрес (местоположение)")
ws.write(0,9, u"Разрешенное использование")
ws.write(0,10, u"ФИО кадастрового инженера")
ws.write(0,11, u"Разрешенное использование по документу")
ws.write(0,12, u"Форма собственности")
ws.write(0,13, u"Широта")
ws.write(0,14, u"Долгота")
ws.write(0,15, u"Ссылка на сайт")
ws.write(0,16, u"Дата парсинга")
row = 1

lin = open('nums.txt').read().splitlines()

v = 1
#r = 1
for line in lin:
    print v,'/',len(lin)
    print('*'*50)
   
    driver.get("http://pkk5.rosreestr.ru/#x=&y=&z=&type=1&zoomTo=1&app=search&opened=1&text="+line)
    
    
    time.sleep(2) 
    
    try:
        WebDriverWait(driver,7).until(EC.visibility_of_element_located((By.XPATH,u'//div[contains(text(),"Дата постановки на учет:")]/following-sibling::div')))
        print "Page is ready!"    
        ##time.sleep(2) 
    except TimeoutException:
        time.sleep(1) 
        driver.get("about:blank")
        driver.delete_all_cookies()
        time.sleep(2)
        continue
    try:
        tip= driver.find_element_by_xpath(u'//div[contains(text(),"Тип:")]/following-sibling::div').text
        print tip
        #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        tip='' 
    try:
        num= driver.find_element_by_xpath(u'//div[contains(text(),"Кад. номер:")]/following-sibling::div[2]').text
        print num
                #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        num=''
    try:
        kvartal= driver.find_element_by_xpath(u'//div[contains(text(),"Кад. квартал:")]/following-sibling::div').text
        print kvartal
        #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        kvartal='' 
    try:
        status= driver.find_element_by_xpath(u'//div[contains(text(),"Статус:")]/following-sibling::div').text
        print status
                #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        status=''
    try:
        adres= driver.find_element_by_xpath(u'//div[contains(text(),"Адрес:")]/following-sibling::div').text
        print adres
                        #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        adres=''
    try:
        cat= driver.find_element_by_xpath(u'//div[contains(text(),"Категория земель:")]/following-sibling::div').text
        print cat
                       #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        cat=''
    try:
        forma= driver.find_element_by_xpath(u'//div[contains(text(),"Форма собственности:")]/following-sibling::div').text
        print forma
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        forma=''
    try:
        cena= driver.find_element_by_xpath(u'//div[contains(text(),"Кадастровая стоимость:")]/following-sibling::div').text
        print cena
                       #ws.write(row, 3, punkt)
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        cena=''
    try:
        plosh= driver.find_element_by_xpath(u'//div[contains(text()," площадь:")]/following-sibling::div').text
        print plosh
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        plosh=''
    try:
        vid= driver.find_element_by_xpath(u'//div[contains(text(),"Разрешенное использование:")]/following-sibling::div').text
        print vid
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        vid=''
    try:
        doc= driver.find_element_by_xpath(u'//div[contains(text(),"по документу:")]/following-sibling::div').text
        print doc
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        doc=''
    try:
        ingener= driver.find_element_by_xpath(u'//div[contains(text(),"Кадастровый инженер:")]/following-sibling::div').text
        print ingener
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        ingener=''
    try:
        data= driver.find_element_by_xpath(u'//div[contains(text(),"Дата постановки на учет:")]/following-sibling::div').text
        print data
    except (NoSuchElementException,StaleElementReferenceException,IndexError):
        data=''        
   
    
    #time.sleep(1) 
    driver.find_element_by_xpath('//*[@id="map-map_gc"]').click()
    time.sleep(2)
     
    
   
    try:
        p= driver.find_element_by_xpath(u'//input[@id="search-text"]').get_attribute('value').split(' ')[0]
        p1= driver.find_element_by_xpath(u'//input[@id="search-text"]').get_attribute('value').split(' ')[1]
        print p
        print p1
    except (NoSuchElementException,IndexError):
        p=''
        p1=''
    print('*'*50)
    
    ws.write(row, 0, num)
    ws.write(row, 1, status)
    ws.write(row, 2, data)
    ws.write(row, 3, cat)
    ws.write(row, 4, plosh)
    ws.write(row, 5, tip)    
    ws.write(row, 6, cena)
    ws.write(row, 7, kvartal)    
    ws.write(row, 8, adres)
    ws.write(row, 9, vid)    
    ws.write(row, 10, ingener)
    ws.write(row, 11, doc)
    ws.write(row, 12, forma)
    ws.write(row, 13, p)
    ws.write(row, 14, p1)
    ws.write_string(row, 15, driver.current_url)
    ws.write(row, 16, datetime.today().strftime('%d.%m.%Y'))
    
    
    v+=1
    row+=1
    #r+=1

    
    #if r == 5:
    #time.sleep(1) 
    print "Page is Refresh!"
    driver.get("about:blank")
    driver.delete_all_cookies()
    #driver.refresh()
    print('+'*5)
    #r = 1
    time.sleep(1) 

workbook.close()
driver.close() 
#display.stop()
