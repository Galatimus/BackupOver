#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
from lxml import html
from lxml.etree import ParserError
from lxml.etree import XMLSyntaxError
import time
#import signal
import re
from sub import conv
from datetime import datetime,timedelta
import xlsxwriter
import subprocess
reload(sys)
sys.setdefaultencoding('utf-8')

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

l= open('bc_com.txt').read().splitlines()

try:
    for p in range(9935,len(l)):
        print '********************',p+1,'/',len(l),'************************'
        command = "phantomjs --ignore-ssl-errors=true --ssl-protocol=any --load-images=false fetchh.js %s" % l[p]
        #command = "phantomjs fetchh.js %s" % l[p]
        try:
            proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
            #print("Process spawned with PID: %s" % proc.pid)
        except OSError:
            continue
        
        try:
            parsed_body = html.fromstring(proc.communicate()[0].decode('utf-8').strip())
        except (ParserError,XMLSyntaxError):
            time.sleep(2)
            del proc
            continue
        
        try:
            zag = parsed_body.xpath('//title/text()')[0]
        except IndexError:
            zag = ''
        try:
            uliza = parsed_body.xpath('//div[@class="street"]/a/text()')[0]
        except IndexError:
            uliza = ''
        try:
            ray = parsed_body.xpath('//div[@class="district"]/a/text()')[0] 
        except IndexError:
            ray = ''
        try:
            if 'moscow' in l[p]:
                punkt = u'Москва'
            else:        
                punkt = parsed_body.xpath('//ul[@class="breadcrumbs"]/li[2]/span/a/span[1]/text()')[0]
        except IndexError:
            punkt =''
        try:
            cena = parsed_body.xpath('//td[@itemprop="price"][1]/text()')[0]
        except IndexError:
            cena = ''
        try:
            oren = parsed_body.xpath('//span[@class="left"]/a/text()')[0]
        except IndexError:
            oren = ''
        try:
            seg = parsed_body.xpath('//tr[@class="object-id"]/td[2]/text()')[0]
        except IndexError:
            seg =''
        try:
            klass = parsed_body.xpath('//span[@class="white-text badge"]/text()')[0]
        except IndexError:
            klass = ''
        try:
            try:
                plosh = parsed_body.xpath('//ul[@class="breadcrumbs"]/li[4]/descendant::span[2]/text()')[0]
            except IndexError:
                plosh = re.sub('[^\d\.]','',parsed_body.xpath(u'//meta[@name="description"]')[0].attrib['content'].split(': ')[1].split(u' за ')[0].split(u' кв.м')[0])+' м2'
        except IndexError:
            plosh = ''
        try:
            ets = parsed_body.xpath('//tr[@class="object-id"]/td[3]/text()')[0]
        except IndexError:
            ets = ''
        try:
            metro = parsed_body.xpath('//span[@class="metro-line"]/following-sibling::text()')[0].split('(')[0]
        except IndexError:
            metro = ''
        try:
            opis = parsed_body.xpath('//div[@class="extended-body"]/text()')[0]
        except IndexError:
            opis = ''
        try:
            lico = parsed_body.xpath('//div[@class="name"]/text()')[0]
        except IndexError:
            lico = ''
        try:
            phone = parsed_body.xpath('//div[@class="phone"]')[0].attrib['data-phone']
        except IndexError:
            phone =''
        try:
            data = parsed_body.xpath('//div[@class="row"]/div[contains(@class,"lastModify")]/text()')[0]
        except IndexError:
            data = ''
        try:
            #oper = parsed_body.xpath('//ul[@class="breadcrumbs"]/li[3]/descendant::span[2]/text()')[0].split(' ')[0]
            oper = parsed_body.xpath(u'//meta[@name="description"]')[0].attrib['content'].split(': ')[1].split(' ')[0]
        except IndexError:
            oper = ''
        sub = reduce(lambda punkt, r: punkt.replace(r[0], r[1]), conv, punkt)
        
        ray = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", ray)
        ray = re.sub(u"[.,\-\s]{3,}", " ", ray) 
        
        oren = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", oren)
        oren = re.sub(u"[.,\-\s]{3,}", " ", oren)
        
        cena = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", cena)
        cena = re.sub(u"[.,\-\s]{3,}", " ", cena)
        
        opis = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", opis)
        opis = re.sub(u"[.,\-\s]{3,}", " ", opis)
        
        
        lico = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", lico)
        lico = re.sub(u"[.,\-\s]{3,}", " ", lico)
        
        
        metro = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", metro)
        metro = re.sub(u"[.,\-\s]{3,}", " ", metro)        
        
        data = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", data)
        data = re.sub(u"[.,\-\s]{3,}", " ", data).replace(u'Данные обновлены ','').replace('-','.')[1:].split(' ')[0]    
        
    
        print sub 
        print punkt 
        print ray 
        print uliza
        print oren
        print seg
        print klass
        print cena
        print plosh
        print ets
        print opis
        print phone
        print lico
        print oper
        print data
        print metro
        print zag
    
        ws.write(result, 0, sub)
        ws.write(result, 1, ray)
        ws.write(result, 2, punkt)
        ws.write(result, 4, uliza)
        ws.write(result, 6, oren)
        ws.write(result, 7, seg)
        ws.write(result, 10, klass)
        ws.write(result, 11, cena)
        ws.write(result, 14, plosh)
        ws.write(result, 16, ets)
        ws.write(result, 18, opis)
        ws.write(result, 19, u'БЦИнформ')
        ws.write_string(result, 20, l[p])
        ws.write(result, 21, phone)
        ws.write(result, 22, lico)
        ws.write(result, 26, metro)
        ws.write(result, 28, oper)
        ws.write(result, 30, data)
        ws.write(result, 31, datetime.today().strftime('%d.%m.%Y'))
        ws.write(result, 33, zag)
        result+=1
        #try:
            #os.killpg(proc.pid, signal.SIGKILL)
        #except OSError:
            #del proc
        time.sleep(1)
except KeyboardInterrupt:
    pass

print('Save it...')
time.sleep(2)
workbook.close()
time.sleep(1)
print('Done')