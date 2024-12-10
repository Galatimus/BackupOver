#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
import re
import time
import math
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

i = 0
l= open('gos.txt').read().splitlines()
page = l[i]




    
while True:
     class Gosgkh(Spider):
	  def prepare(self):
	       self.f = page
	       #self.link =l[i]	  
	       while True:
		    try:
			 time.sleep(2)
			 g = Grab(timeout=20, connect_timeout=20)
			 g.go(self.f)
			 self.sub = g.doc.select(u'//ul[@class="breadcrumb"]/li[2]/a/span').text()
			 print self.sub
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,IndexError,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 del g
			 continue	  
	       self.workbook = xlsxwriter.Workbook(u'gosgkh/Gosjkh_%s' % bot.sub + u'.xlsx')
	       self.ws = self.workbook.add_worksheet()
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 2, u"УЛИЦА")
	       self.ws.write(0, 3, u"ДОМ")
	       self.ws.write(0, 4, u"ГОД_ВВОДА_В_ЭКСПЛУАТАЦИЮ")
	       self.ws.write(0, 5, u"ПЛОЩАДЬ М2")
	       self.ws.write(0, 6, u"ЗАРЕГИСТРИРОВАНО_ЖИТЕЛЕЙ")
	       self.ws.write(0, 7, u"УПРАВЛЯЮЩАЯ_КОМПАНИЯ")
	       self.ws.write(0, 8, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 9, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 10, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 11, u"МЕСТОПОЛОЖЕНИЕ")
		    
		    
	       self.result= 1
	     
		    
	 
	  def task_generator(self):
	       yield Task ('next',url=self.f,refresh_cache=True,network_try_count=100)
		    
     
	  def task_next(self,grab,task):
	       for ele in grab.doc.select(u'//ul[@class="col-md-3 list-unstyled"]/li/a'):
		    urs = grab.make_url_absolute(ele.attr('href'))  
		    #print urs
		    yield Task('dom',url=urs,refresh_cache=True,network_try_count=100)
		    
	  def task_dom(self,grab,task):
	       try:
		    num = re.sub('[^\d]','',grab.doc.rex_text(u'составляет более(.*?)домов'))
		    pag = int(math.ceil(float(int(num))/float(10)))
		    for x in range(1,pag+1):
			 yield Task ('poisk',url=task.url+'?page=%d'%x,refresh_cache=True,network_try_count=100) 
	       except IndexError:
		    yield Task ('poisk',url=task.url,refresh_cache=True,network_try_count=100)
		    
	  def task_poisk(self,grab,task):
	       for em in grab.doc.select(u'//td/a[contains(@href,"houses")]'):
		    urr = grab.make_url_absolute(em.attr('href'))
		    #print urr
		    yield Task('item', url=urr,refresh_cache=True, network_try_count=100)
		    
		    
	  def task_item(self, grab, task):
     
	       try:
		    punkt= grab.doc.select(u'//dt[contains(text(),"Населенный пункт")]/following-sibling::dd[1]').text()
	       except IndexError:
		    punkt = ''
		    
	       try:
		    uliza = grab.doc.select(u'//dt[contains(text(),"Адрес")]/following-sibling::dd[1]').text().split(', д.')[0]
	       except IndexError:
		    uliza = ''
	       try:
		    dom = grab.doc.select(u'//dt[contains(text(),"Адрес")]/following-sibling::dd[1]').text().split(', д.')[1]
	       except IndexError:
		    dom = ''       
		    
	       try:
		    price = grab.doc.select(u'//dt[contains(text(),"Год ввода в эксплуатацию")]/following-sibling::dd[1]').number()
	       except DataNotFound:
		    price = ''   
	       try:
		    plosh = grab.doc.select(u'//dt[contains(text(),"Площадь")]/following-sibling::dd[1]').text()
	       except DataNotFound:
		    plosh = ''
	       
	       try:
		    mat = grab.doc.select(u'//dt[contains(text(),"Зарегистрировано жителей")]/following-sibling::dd[1]').number()
	       except IndexError:
		    mat = ''
	       try:
		    godp = grab.doc.select(u'//dt[contains(text(),"Управляющая компания")]/following-sibling::dd[1]/a').text()
	       except IndexError:
		    godp = ''	       
	       try:
		    vid = grab.doc.select(u'//dt[contains(text(),"Полный адрес")]/following-sibling::dd[1]').text()
	       except DataNotFound:
		    vid = '' 	       
			 
	       
							
		    
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'punkt': punkt,
		           'ulica': uliza.replace(punkt,''),
		           'dom': dom,
		           'cena': price,
		           'plosh':plosh,
		           'mat': mat,
		           'god':godp,
		           'vid': vid}
	       
	       yield Task('write',project=projects,grab=grab,refresh_cache=True)
		 
	  def task_write(self,grab,task):
	       print('*'*50)
	       
	       print  task.project['punkt']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['cena']
	       print  task.project['plosh']
	       print  task.project['mat']
	       print  task.project['god']
	       print  task.project['vid']
	       print task.project['url']
	      
	       
	       #global result
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['punkt'])
	       self.ws.write(self.result, 2, task.project['ulica'])
	       self.ws.write(self.result, 3, task.project['dom'])
	       self.ws.write(self.result, 4, task.project['cena'])
	       self.ws.write(self.result, 5, task.project['plosh'])
	       self.ws.write(self.result, 6, task.project['mat'])
	       self.ws.write(self.result, 7, task.project['god'])
	       self.ws.write(self.result, 8, u'ГОСЖКХ.РУ')	  
	       self.ws.write_string(self.result, 9, task.project['url'])
	       self.ws.write(self.result, 10, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result, 11, task.project['vid'])
	       print('*'*50)
	       print 'Ready - '+str(self.result)
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print '***',i+1,'/',len(l),'***'
	       print  task.project['sub']
	       print('*'*50)	       
	       self.result+= 1
		    
	       #if self.result >= 10:
		    #self.stop()	       	       
     
     bot = Gosgkh(thread_number=5,network_try_limit=5000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     bot.run()
     print('Спим 1 сек...')
     time.sleep(1)
     print('Сохранение...')
     bot.workbook.close()
     print('Done!')
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  break







