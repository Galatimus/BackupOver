#!/usr/bin/python
# -*- coding: utf-8 -*-



import math
import os
import re
import time
from datetime import datetime,timedelta
#from sub import conv
import sys
import xlsxwriter
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException


reload(sys)
sys.setdefaultencoding('utf-8')



def get_chrome_drive(driver_path=None):
    
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox') 
    driver = webdriver.Chrome(executable_path='D:\\VMF\\OlegPars\\webshot\\chromedriver\\chromedriver.exe',chrome_options=options,service_args=['--verbose']) 
    return driver

def get_firefox_drive(driver_path=None):

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    #profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/yaun5l28.default/') #Gui1
    profile = webdriver.FirefoxProfile()#Gui2
    profile.set_preference('permissions.default.stylesheet', 2)
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    profile.set_preference("javascript.enabled", False)
    profile.native_events_enabled = False
    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)
    return driver

def take_content(driver, url):
    # get the page
    driver.get(url)
    time.sleep(5)
    try:
        zag = driver.find_element_by_xpath(u'//h1[@id="registry-item-heading"]').text
    except (NoSuchElementException,WebDriverException):
        zag = ''
    try:
        uliza = re.findall(u'Полное наименование: (.*?)<br>',driver.page_source)[0]
    except (NoSuchElementException,IndexError,WebDriverException):
        uliza = ''
    try:
        ray = driver.find_element_by_xpath('//div[contains(text(),"Направление")]/following::tr[1]/td[4]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        ray = ''
    try:
        punkt = driver.find_element_by_xpath('//td[@id="itemPhone"]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        punkt =''
    try:
        cena = driver.find_element_by_xpath('//td[@id="itemPostAddress"]').text.split(', ')[0]
    except (NoSuchElementException,IndexError,WebDriverException):
        cena = ''
    try:
        oren = driver.find_element_by_xpath('//td[@id="itemStatus"]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        oren = ''
    try:
        seg = driver.find_element_by_xpath('//tr[@class="object-id"]/td[2]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        seg =''
    try:
        klass = driver.find_element_by_xpath('//span[@class="white-text badge"]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        klass = ''
    try:
        try:
            plosh = driver.find_element_by_xpath('//ul[@class="breadcrumbs"]/li[4]/descendant::span[2]').text
        except (NoSuchElementException,IndexError,WebDriverException):
            plosh = re.sub('[^\d\.]','',driver.find_element_by_xpath(u'//meta[@name="description"]').get_attribute('content').split(': ')[1].split(u' за ')[0].split(u' кв.м')[0])+' м2'
    except (NoSuchElementException,IndexError,WebDriverException):
        plosh = ''
    try:
        ets = driver.find_element_by_xpath('//tr[@class="object-id"]/td[3]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        ets = ''
    try:
        metro = driver.find_element_by_xpath('//span[@class="metro-line"]/following-sibling::text()').text.split('(')[0]
    except (NoSuchElementException,IndexError,WebDriverException):
        metro = ''
    try:
        opis = driver.find_element_by_xpath('//div[@class="extended-body"]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        opis = ''
    try:
        lico = driver.find_element_by_xpath('//div[@class="name"]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        lico = ''
    try:
        phone = driver.find_element_by_xpath('//div[@class="phone"]').get_attribute('data-phone')
    except (NoSuchElementException,IndexError,WebDriverException):
        phone =''
    try:
        data = driver.find_element_by_xpath('//div[@class="row"]/div[contains(@class,"lastModify")]').text
    except (NoSuchElementException,IndexError,WebDriverException):
        data = ''
    try:
        #oper = driver.find_element_by_xpath('//ul[@class="breadcrumbs"]/li[3]/descendant::span[2]/text()')[0].split(' ')[0]
        oper = driver.find_element_by_xpath(u'//meta[@name="description"]').get_attribute('content').split(': ')[1].split(' ')[0]
    except (NoSuchElementException,IndexError,WebDriverException):
        oper = ''
        
    #sub = reduce(lambda punkt, r: punkt.replace(r[0], r[1]), conv, punkt)
    
    data = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", data)
    data = re.sub(u"[.,\-\s]{3,}", " ", data).replace(u'Данные обновлены ','').replace('-','.')[1:].split(' ')[0]    
        
    print('*'*50)
    print zag
    print punkt 
    print ray 
    print uliza
    print oren
    print cena
    #print seg
    #print klass    
    #print plosh
    #print ets
    #print opis
    #print phone
    #print lico
    #print oper
    #print data
    #print metro    
    print('*'*50)
    ws.write(result, 0, zag)   
    ws.write(result, 3, ray)
    ws.write(result, 5, punkt)
    ws.write(result, 2, uliza)
    ws.write(result, 10, oren)
    ws.write(result, 8, cena)
    ws.write(result, 11, u'НП СРО «АРМО»')
    ws.write(result, 12, datetime.today().strftime('%d.%m.%Y'))
    
    #ws.write(result, 7, seg)
    #ws.write(result, 10, klass)
    
    #ws.write(result, 14, plosh)
    #ws.write(result, 16, ets)
    #ws.write(result, 18, opis)
    
    #ws.write_string(result, 20, url)
    #ws.write(result, 21, phone)
    #ws.write(result, 22, lico)
    #ws.write(result, 26, metro)
    #ws.write(result, 28, oper)
    #ws.write(result, 30, data)
    
    


def main(url):
    driver = get_firefox_drive()
    #driver = get_chrome_drive()
    driver.set_window_position(0,0)
    driver.set_window_size(800,800)
    try:
        take_content(driver,url)
    except (TimeoutException,WebDriverException):
        driver.quit()
    
    driver.quit()
    time.sleep(1)    
    return


if __name__ == '__main__':
    l= open('reestr.txt').read().splitlines()
    workbook = xlsxwriter.Workbook(u'Sroarmo.xlsx')    
    ws = workbook.add_worksheet()
    ws.write(0, 0, u"ФИО")
    ws.write(0, 1, u"Должность")
    ws.write(0, 2, u"Место работы")
    ws.write(0, 3, u"Направление")
    ws.write(0, 4, u"Сайт компании")
    ws.write(0, 5, u"Номер телефона")
    ws.write(0, 6, u"E-mail")
    ws.write(0, 7, u"E-mail (личный)")
    ws.write(0, 8, u"Субъект РФ")
    ws.write(0, 9, u"Название СРО")
    ws.write(0, 10, u"Статус членства")
    ws.write(0, 11, u"Источник")
    ws.write(0, 12, u"Дата сбора информации")
    ws.write(0, 13, u"Дата обновления")
    result= 1
    try:
        for p in range(len(l)):
            print '******',p,'/',len(l),'******'
            main(l[p])
            result+=1  
    except KeyboardInterrupt:
        pass
    print('Save it...')
    time.sleep(1)
    workbook.close()
    time.sleep(2)
    print('Done')    
    
    
    
