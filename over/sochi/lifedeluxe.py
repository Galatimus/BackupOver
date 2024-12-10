#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Lifedeluxe_Продажа2.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet('lifedeluxe')
	  self.ws.write(0, 0, u"№")
	  self.ws.write(0, 1, u"Район")
	  self.ws.write(0, 2, u"Метро")
	  self.ws.write(0, 3, u"Адрес")
	  self.ws.write(0, 4, u"Название_ЖК")
	  self.ws.write(0, 5, u"Тип дома / Здание")
	  self.ws.write(0, 6, u"Тип сделки")
	  self.ws.write(0, 7, u"Этаж/Этажность")
	  self.ws.write(0, 8, u"Фонд")
	  self.ws.write(0, 9, u"Кол-во комнат")
	  self.ws.write(0, 10, u"Площадь общая")
	  self.ws.write(0, 11, u"Цена")
	  self.ws.write(0, 12, u"Бюджет")
	  self.ws.write(0, 13, u"Описание")
	  self.ws.write(0, 14, u"Источник")
	  self.ws.write(0, 15, u"Ссылка")
	  self.ws.write(0, 16, u"Дата размещения")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  #for x in range(1,37):#230
               #yield Task ('post',url='http://lifedeluxe.ru/catalog/flats/operation_type/sale/page/%d'%x,network_try_count=100)
          for x in range(1,21):#92
               yield Task ('post',url='http://lifedeluxe.ru/catalog/flats/operation_type/rent/page/%d'%x,network_try_count=100)
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="catalog_item_list"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//td[@class="even"][contains(text(),"Район")]/following-sibling::td').text()
          except DataNotFound:
               ray =''
	  
	  try:
	       uliza = grab.doc.select(u'//td[@class="even"][contains(text(),"Метро")]/following-sibling::td').text()
	      
	  except DataNotFound:
               uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//h1').text()
	   #print rayon
	  except DataNotFound:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//div[@class="breadcrumbs"]/a[3]').text()
          except IndexError:
	       tip = ''
	      
	  try:
	       novo = grab.doc.select(u'//td[@class="even"][contains(text(),"Этаж")]/following-sibling::td[1]').number()
	  except DataNotFound:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//td[@class="even"][contains(text(),"Число комнат")]/following-sibling::td[1]').number()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//em[contains(text(),"Площадь:")]/following-sibling::a').text()#.split(': ')[1]
          except DataNotFound:
	       plosh = ''
          try:
               price = grab.doc.select(u'//em[contains(text(),"Цена:")]/ancestor::div[1]').text().replace(u'Цена:','')
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="ld_description mobile_padding"]/p').text() 
          except DataNotFound:
               opis = ''
	  try:
	       data = grab.doc.select(u'//div[@class="detail_date_add"]').text().replace(u'Дата размещения: ','')
          except IndexError:
	       data = ''
	       
	  try:
	       meb = grab.doc.rex_text(u'operation_type/sale">(.*?) фонд') 
	  except IndexError:
	       meb = '' 	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom,
	              'tip': tip,
	              'novo': novo,
	              'plosh': plosh,
	              'cena': price,
	              'opis': opis,
	              'data': data,
	              'fond': meb,
	              'col_komnat': kol_komnat}
	
	
	
	  yield Task('write',project=projects,grab=grab)
	
	
	
	
	
	
     def task_write(self,grab,task):
	  
	  print('*'*50)	       
	 
	  print  task.project['rayon']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['tip']
	  print  task.project['novo']
	  print  task.project['plosh']
	  print  task.project['cena']
	  print  task.project['opis']
	  print  task.project['col_komnat']
	  
    
	  self.ws.write(self.result, 1,task.project['rayon'])
	  self.ws.write(self.result, 2,task.project['ulica'])
	  self.ws.write(self.result, 3,task.project['dom'])
	  self.ws.write(self.result, 4,task.project['tip'])
	  self.ws.write(self.result, 6,u'Аренда')
	  self.ws.write(self.result, 7,task.project['novo'])
	  self.ws.write(self.result, 8,task.project['fond'])
	  self.ws.write(self.result, 9,task.project['col_komnat'])
	  self.ws.write(self.result, 10,task.project['plosh'])
	  self.ws.write(self.result, 11,task.project['cena'])
	  self.ws.write(self.result, 13,task.project['opis'])
	  self.ws.write(self.result, 14, u'lifedeluxe.ru')
	  self.ws.write_string(self.result, 15,task.url)
	  self.ws.write(self.result, 0,self.result)
	  self.ws.write(self.result, 16,task.project['data'])
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result >= 10:
	       #self.stop()

bot = Cian_Kv(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')

     
     