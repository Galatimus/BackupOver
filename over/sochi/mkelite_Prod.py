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

workbook = xlsxwriter.Workbook(u'Mkelite.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet('mkelite')
	  self.ws.write(0, 0, u"№")
	  self.ws.write(0, 1, u"Район")
	  self.ws.write(0, 2, u"Метро")
	  self.ws.write(0, 3, u"Адрес")
	  self.ws.write(0, 4, u"Название_ЖК")
	  self.ws.write(0, 5, u"Этаж")
	  self.ws.write(0, 6, u"Фонд")
	  self.ws.write(0, 7, u"Кол-во комнат")
	  self.ws.write(0, 8, u"Площадь")
	  self.ws.write(0, 9, u"Цена")
	  self.ws.write(0, 10, u"Бюджет")
	  self.ws.write(0, 11, u"Описание")
	  self.ws.write(0, 12, u"Источник")
	  self.ws.write(0, 13, u"Ссылка")	  
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  for line in open('mk.txt').read().splitlines():
               yield Task ('item',url=line.strip(),refresh_cache=True,network_try_count=100)
         
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="object_img"]/ancestor::div[1]'):
	       ur = grab.make_url_absolute(elem.attr('data-href'))  
	       print ur
	       #yield Task('item', url=ur,refresh_cache=True,network_try_count=1000)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//span[@id="btnDistrict"]').text()
          except IndexError:
               ray =''
	  
	  try:
	       uliza = grab.doc.select(u'//div[@class="big"]/a').text()
	      
	  except IndexError:
               uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//div[@class="first"]/div').text()
	   #print rayon
	  except IndexError:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//div[@class="area"]').text()
          except IndexError:
	       tip = ''
	      
	  #try:
	       ##s = grab.doc.select(u'//div[@class="description"]').text().split(u'Количество просмотров: ')[0]
	       ##if s.find(u'длительн')>=0:
		    ##novo = u'долгосрочная'
	       ##else:
	       #novo = u'краткосрочная'
	  #except DataNotFound:
	       #novo = ''
          try:
               kol_komnat = grab.doc.select(u'//div[@class="amount"]').text()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//div[@class="aside"]/following-sibling::div[@class="text"]').text()
          except DataNotFound:
	       plosh = ''
          try:
               price = grab.doc.select(u'//strong[contains(text(),"Цена:")]/following-sibling::text()').text()#.split(u'.')[0]
	       #novo = u'краткосрочная'
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//p[@class="df_listingDescription"]').text()
	       #istoch = u'DOMOFOND.RU'
	       
          except DataNotFound:
               opis = ''	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom,
	              'tip': tip,
	              'plosh': plosh,
	              'cena': price,
	              'istoh':u'MKELITE.RU',
	              'opis': opis,
	              'col_komnat': kol_komnat}
	
	
	
	  yield Task('write',project=projects,grab=grab)
	
	
	
	
	
	
     def task_write(self,grab,task):
	  
	  print('*'*50)	       
	 
	  print  task.project['rayon']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['tip']
	  #print  task.project['novo']
	  print  task.project['plosh']
	  print  task.project['cena']
	  print  task.project['opis']
	  print  task.project['col_komnat']
	  
    
	  self.ws.write(self.result, 1,task.project['rayon'])
	  self.ws.write(self.result, 3,task.project['ulica'])
	  self.ws.write(self.result, 5,task.project['dom'])
	  self.ws.write(self.result, 8,task.project['tip'])
	  #self.ws.write(self.result, 6,task.project['novo'])
	  self.ws.write(self.result, 9,task.project['col_komnat'])
	  self.ws.write(self.result, 11,task.project['plosh'])
	  self.ws.write(self.result, 0,self.result)
	  self.ws.write_string(self.result, 13,task.url)
	  self.ws.write(self.result, 12,task.project['istoh'])
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result >= 10:
	       #self.stop()
	

bot = Cian_Kv(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')

     
     