#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import math
import re
import os
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)



workbook = xlsxwriter.Workbook(u'Cian_Новостройки_НАО'+'.xlsx')



class Cian_Com(Spider):
    def prepare(self):
	self.ws = workbook.add_worksheet()
	self.ws.write(0, 0, u"ID")
	self.ws.write(0, 1, u"КОЛИЧЕСТВО_КОМНАТ")
	self.ws.write(0, 2, u"МЕТРО")
	self.ws.write(0, 3, u"АДРЕС")
	self.ws.write(0, 4, u"ПЛОЩАДЬ_ОБЩАЯ,м2")
	self.ws.write(0, 5, u"ПЛОЩАДЬ_ЖИЛАЯ,м2")
	self.ws.write(0, 6, u"ПЛОЩАДЬ_КУХНЯ,м2")
	self.ws.write(0, 7, u"ЭТАЖ")
	self.ws.write(0, 8, u"ЭТАЖНОСТЬ")
	self.ws.write(0, 9, u"ТИП_ДОМА")
	self.ws.write(0, 10, u"ПАРКОВКА")
	self.ws.write(0, 11, u"ЦЕНА")
	self.ws.write(0, 12, u"ТЕЛЕФОН")
	self.ws.write(0, 13, u"ОТДЕЛКА")
	self.ws.write(0, 14, u"ПЛОЩАДЬ_КОМНАТ")
	self.ws.write(0, 15, u"ОКНА")
	self.ws.write(0, 16, u"САНУЗЕЛ")	
	self.ws.write(0, 17, u"НАЗВАНИЕ_ЖК")
	self.ws.write(0, 18, u"ВЫСОТА_ПОТОЛКОВ,м")
	self.ws.write(0, 19, u"ЛИФТ")
	self.ws.write(0, 20, u"ССЫЛКА_НА_ОБЪЯВЛЕНИЕ")
	self.ws.write(0, 21, u"ОПИСАНИЕ")
	self.ws.write(0, 22, u"СРОК_СДАЧИ")
	self.ws.write(0, 23, u"ЗАСТРОЙЩИК")
	self.ws.write(0, 24, u"КОРПУС")

	self.result= 1
	#self.count = 2
	
	    
	    
	    
	      
    
    def task_generator(self):
	l= open('novo3.txt').read().splitlines()
	self.dc = len(l)
	print self.dc
	for line in l:
	    #time.sleep(3)
	    yield Task ('item',url=line,refresh_cache=True,network_try_count=100)

    def task_item(self, grab, task):
	#time.sleep(5)
	
	try:
	    sub = re.sub(u'[^\d]','',task.url)
	except IndexError:
	    sub = ''	
	try:
	    usl = grab.doc.select(u'//h1').text().split('-')[0]
	except IndexError:
	    usl = ''	
	try:
	    ray = grab.doc.select(u'//ul[@class="undergrounds--3OsCQ"]/li').text()
	except IndexError:
	    ray =''
	try:
	    punkt=grab.doc.select(u'//address[@class="address--D3O4n"]').text().replace(u'На карте','')
	except IndexError:
	    punkt = ''
	try:
	    ter=  grab.doc.select(u'//div[contains(text(),"Общая")]/following-sibling::div[1]').text()
	except IndexError:
	    ter =''
	try:
	    uliza = grab.doc.select(u'//div[contains(text(),"Жилая")]/following-sibling::div[1]').text()
	except IndexError:
	    uliza =''
	
	try:
	    dom = grab.doc.select(u'//div[contains(text(),"Кухня")]/following-sibling::div[1]').text()
	except IndexError:
	    dom = ''
	    
	try:
	    seg = grab.doc.select(u'//div[contains(text(),"Этаж")]/following-sibling::div[1]').text().split(u' из ')[0]
	  #print oren
	except DataNotFound:
	    seg = '' 
	    
	try:
	    naz = grab.doc.select(u'//div[contains(text(),"Этаж")]/following-sibling::div[1]').text().split(u' из ')[1]
	  #print naz
	except IndexError:
	    naz = '' 
	    
	try:
	    klass = grab.doc.select(u'//span[contains(text(),"Тип дома")]/following-sibling::span[1]').text()
	except IndexError:
	    klass = ''
	    
	try:
	    price = grab.doc.select(u'//span[@class="price_value--XlUfS"]').text()
	  #print price
	except IndexError:
	    price = ''
	    
	try:
	    plosh = grab.doc.select(u'//span[contains(text(),"Отделка")]/following-sibling::span[1]').text()#.replace(u'м',u'м2')
	  #print plosh
	except IndexError:
	    plosh = '' 
	    
	try:
	    et = grab.doc.select(u'//span[contains(text(),"Площадь комнат")]/following-sibling::span[1]').text()
	except IndexError:
	    et = ''
	    
	try:
	    et2 = grab.doc.select(u'//div[@class="container--dcMOP"]/a').text().replace(u'в ','')
	except IndexError:
	    et2 = ''
	    
	try:
	    opis = grab.doc.select(u'//p[@class="description-text--3SshI"]').text()
	  #print opis
	except IndexError:
	    opis = ''
	    
	try:
		try:
		    phone = re.sub(u'[^\d\+]','',grab.doc.select(u'//a[@class="phone--1OSCA"]').text())
		except IndexError:
		    phone = re.sub(u'[^\d\+]','',grab.doc.rex_text(u'offerPhone(.*?),'))
	except IndexError:
	    phone = '' 
	    
	try:
	    lico = grab.doc.select(u'//span[contains(text(),"Высота потолков")]/following-sibling::span[1]').text() 
	except IndexError:
	    lico = ''
	    
	try:
	    comp = grab.doc.select(u'//li[contains(text(),"Паркинг")]').text().replace(u'Паркинг',u'Открытая')
	except IndexError:
	    comp = '' 
	try:
	    ohrana = grab.doc.select(u'//span[contains(text(),"Вид из окон")]/following-sibling::span[1]').text()
	except IndexError:
	    ohrana =''
	try:
	    gaz = u'Совмещённый'+' '+grab.doc.select(u'//span[contains(text(),"Совмещённый санузел")]/following-sibling::span[1]').text()
	except IndexError:
	    gaz =''
	try:
	    voda =  grab.doc.select(u'//li[contains(text(),"Пассажирский лифт")]').text().replace(u' лифт','')
	except IndexError:
	    voda =''
	try:
	    kanal = grab.doc.select(u'//li[contains(text(),"Грузовой лифт")]').text().replace(u' лифт','')
	except IndexError:
	    kanal =''
	try:
	    elek = grab.doc.select(u'//div[contains(text(),"Срок сдачи")]/following-sibling::div[1]').text()
	except IndexError:
	    elek =''
	try:
	    teplo = grab.doc.select(u'//h2[@class="title--3rget"]').text()
	except IndexError:
	    teplo =''
	    
	try:
	    korpus = grab.doc.select(u'//span[contains(text(),"Корпус")]').text().replace(u', Корпус ','')
	except IndexError:
	    korpus =''		    
	
	
	projects = {'url': task.url,
                    'sub': sub,
                    'ray': ray,
                    'punkt': punkt,
                    'teritor': ter,
                    'uliza': uliza,
                    'dom': dom,
                    'seg': seg,
                    'naznachenie': naz,
                    'klass': klass,
                    'uslovi': usl.split(', ')[0],
                    'cena': price,
                    'ploshad': plosh,
                    'et': et,
                    'ets': et2,
                    'opisanie': opis,
                    'phone':phone,
                    'company':comp,
                    'lico':lico,
	            'kor':korpus,
                    'ohrana':ohrana,
                    'gaz': gaz,
                    'voda': voda,
                    'kanaliz': kanal,
                    'electr': elek,
                    'teplo': teplo }
	
	
	
	
	yield Task('write',project=projects,grab=grab)
	
	
	
	
    def task_write(self,grab,task):
	if task.project['punkt'] <> '':    
	    print('*'*50)
	    print  task.project['sub']
	    print  task.project['ray']
	    print  task.project['punkt']
	    print  task.project['teritor']
	    print  task.project['uliza']
	    print  task.project['dom']
	    print  task.project['seg']
	    print  task.project['naznachenie']
	    print  task.project['uslovi'] 
	    print  task.project['klass']
	    print  task.project['cena']
	    print  task.project['ploshad']
	    print  task.project['et']
	    print  task.project['ets']
	    print  task.project['opisanie']
	    print  task.project['url']
	    print  task.project['phone']
	    print  task.project['lico']
	    print  task.project['company']
	    print  task.project['ohrana']
	    print  task.project['gaz']
	    print  task.project['voda']
	    print  task.project['kanaliz']
	    print  task.project['electr']
	    print  task.project['teplo']
	    print  task.project['kor']
	    
	    
	    self.ws.write(self.result, 0, task.project['sub'])
	    self.ws.write(self.result, 1, task.project['uslovi'])
	    self.ws.write(self.result, 2, task.project['ray'])
	    self.ws.write(self.result, 3, task.project['punkt'])
	    self.ws.write(self.result, 4, task.project['teritor'])
	    self.ws.write(self.result, 5, task.project['uliza'])
	    self.ws.write(self.result, 6, task.project['dom'])
	    self.ws.write(self.result, 7, task.project['seg'])
	    self.ws.write(self.result, 8, task.project['naznachenie'])
	    self.ws.write(self.result, 9, task.project['klass'])
	    self.ws.write(self.result, 10, task.project['company'])
	    self.ws.write(self.result, 11, task.project['cena'])
	    self.ws.write(self.result, 12, task.project['phone'])	
	    self.ws.write(self.result, 13, task.project['ploshad'])
	    self.ws.write(self.result, 14, task.project['et'])
	    self.ws.write(self.result, 15, task.project['ohrana'])
	    self.ws.write(self.result, 16, task.project['gaz'])
	    self.ws.write(self.result, 17, task.project['ets'])
	    self.ws.write(self.result, 18, task.project['lico'])
	    self.ws.write(self.result, 19, task.project['voda']+','+task.project['kanaliz'])
	    self.ws.write_string(self.result, 20, task.project['url'])
	    self.ws.write(self.result, 21, task.project['opisanie'])
	    self.ws.write(self.result, 22, task.project['electr'])
	    self.ws.write(self.result, 23, task.project['teplo'])
	    self.ws.write(self.result, 24, task.project['kor'])
	  
	    
	    
	    print('*'*50)
	    print 'Ready - '+str(self.result)+'/'+str(self.dc)
	    print 'Tasks - %s' % self.task_queue.size()
	    print('*'*50)
	    
	    self.result+= 1
	    
	    
	    
	    #if self.result > 20:
		#self.stop()	
	    
	    
	   
bot = Cian_Com(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../../ivan.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
workbook.close()
print('Done')


