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

workbook = xlsxwriter.Workbook(u'Sochi_realinvest.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Район")
	  self.ws.write(0, 1, u"Улица")
	  self.ws.write(0, 2, u"№ дома")
	  self.ws.write(0, 3, u"Тип дома")
	  self.ws.write(0, 4, u"Потребительский_класс")
	  self.ws.write(0, 5, u"Новостройка(да/нет)")
	  self.ws.write(0, 6, u"Комнат")
	  self.ws.write(0, 7, u"Площадь")
	  self.ws.write(0, 8, u"Стоимость общая")
	  self.ws.write(0, 9, u"Цена кв.м")
	  self.ws.write(0, 10, u"Описание")
	  self.ws.write(0, 11, u"Источник")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  for x in range(1,32):#22
               yield Task ('post',url='https://sochi-realinvest.ru/catalog/novostroyki/?PAGEN_1=%d'%x,network_try_count=100)
          for x1 in range(1,28):#17
               yield Task ('post',url='https://sochi-realinvest.ru/catalog/kvartiry-bez-remonta/?PAGEN_1=%d'%x1,network_try_count=100)
	  for x2 in range(1,77):#44
	       yield Task ('post',url='https://sochi-realinvest.ru/catalog/kvartiry/?PAGEN_1=%d'%x2,network_try_count=100)  
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="row"]/div/a[contains(@target,"blank")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Район")]/following::div[@class="column"]/p[2]').text()
          except IndexError:
               ray =''
	  
	  try:
	       uliza = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Улица")]/following::div[@class="column"]/p[3]').text()
	      
	  except IndexError:
               uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//div[@class="bx-breadcrumb"]/div[3]').text().split(', ')[1]
	   #print rayon
	  except IndexError:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//li[contains(text(),"Тип здания")]').text().split(': ')[1]
          except IndexError:
	       tip = ''
	      
	  try:
               novo = grab.doc.select(u'//div[@class="bx-breadcrumb"]/div[2]').text().replace(u'Квартиры без ремонта',u'Нет').replace(u'Квартиры c ремонтом',u'Нет').replace(u'Новостройки',u'Да')
	  except IndexError:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//div[@class="bx-breadcrumb"]/div[3]').text().split(u'-комнатная')[0]
          except IndexError:
               kol_komnat = ''
          try:
	       try:
                    plosh = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Общая площадь")]/following::div[@class="column"]/p[3]').text()+u' м2'
	       except IndexError:
		    plosh = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Максимальная площадь")]/following::div[@class="column"]/p[5]').text()+u' м2'
          except IndexError:
	       plosh = ''
          try:
	       try:
                    price = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Цена")]/following::div[@class="column"]/p[3]/following-sibling::text()').text()+u' р.'
	       except IndexError:
		    price = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Минимальная цена за квартиру")]/following::div[@class="column"]/p[7]').text()+u' р.'
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="description-product"]').text().split(u'Технические характеристики')[0] 
          except IndexError:
               opis = ''
	       
	  try:
	       m2 = grab.doc.select(u'//div[@class="column"]/p[contains(text(),"Минимальная цена за 1 кв.м")]/following::div[@class="column"]/p[5]').text()+u' р.'
	  except IndexError:
	       m2 =''	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom,
	              'tip': tip,
	              'novo': novo,
	              'plosh': plosh,
	              'cena': price,
	              'opis': opis,
	              'metr': m2,
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
	  print  task.project['metr']
	  
    
	  self.ws.write(self.result, 0,task.project['rayon'])
	  self.ws.write(self.result, 1,task.project['ulica'])
	  self.ws.write(self.result, 2,task.project['dom'])
	  self.ws.write(self.result, 3,task.project['tip'])
	  self.ws.write(self.result, 5,task.project['novo'])
	  #self.ws.write(self.result, 6,task.project['col_komnat'])
	  self.ws.write(self.result, 7,task.project['plosh'])
	  self.ws.write(self.result, 8,task.project['cena'])
	  self.ws.write(self.result, 9,task.project['metr'])
	  self.ws.write(self.result, 10,task.project['opis'])
	  self.ws.write(self.result, 11, u'Sochi-Realinvest.ru')
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result > 10:
	       #self.stop()

     
bot = Cian_Kv(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')

     
     