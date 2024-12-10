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

workbook = xlsxwriter.Workbook(u'ar/Sochi_Express_Arenda.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Район")
	  self.ws.write(0, 1, u"Улица")
	  self.ws.write(0, 2, u"№ дома")
	  self.ws.write(0, 3, u"Тип дома")
	  self.ws.write(0, 4, u"Потребительский класс")
	  self.ws.write(0, 5, u"Комнат")
	  self.ws.write(0, 6, u"Площадь")
	  self.ws.write(0, 7, u"Тип_аренды")
	  self.ws.write(0, 8, u"Ставка")
	  self.ws.write(0, 9, u"Описание")
	  self.ws.write(0, 10, u"Источник")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  for x in range(1,62):#42
               yield Task ('post',url='http://www.sochi-express.ru/realty/for_rent/secondary/?page=%d'%x,network_try_count=100)
         
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="adv-link"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'.//*[@id="wrap"]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/p[2]/text()[2]').text()
          except DataNotFound:
               ray =''
	  
	  try:
	       uliza = re.sub('[\d\,]','',grab.doc.select(u'.//*[@id="wrap"]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/p[2]/text()[1]').text())
	      
	  except DataNotFound:
               uliza = ''
	       
	  try:
	       dom = re.sub('[^\d]','',grab.doc.select(u'.//*[@id="wrap"]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/p[2]/text()[1]').text())[:2]
	   #print rayon
	  except DataNotFound:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//li[contains(text(),"Тип дома")]').text().split(': ')[1]
          except IndexError:
	       tip = ''
	      
	  try:
	       s = grab.doc.select(u'//div[@class="description"]').text().split(u'Количество просмотров: ')[0]
	       if s.find(u'длительн')>=0:
		    novo = u'долгосрочная'
	       else:
		    novo = u'краткосрочная'
	  except DataNotFound:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//div[@class="address"]/p[1]').number()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//li[contains(text(),"Общая площадь:")]').text().split(': ')[1]
          except DataNotFound:
	       plosh = ''
          try:
               price = grab.doc.select(u'//div[@class="price"]').text()#.split(u'.')[0]
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="description"]').text().split(u'Количество просмотров: ')[0] 
          except DataNotFound:
               opis = ''	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom,
	              'tip': tip,
	              'novo': novo,
	              'plosh': plosh,
	              'cena': price,
	              'opis': opis,
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
	  
    
	  self.ws.write(self.result, 0,task.project['rayon'])
	  self.ws.write(self.result, 1,task.project['ulica'])
	  self.ws.write(self.result, 2,task.project['dom'])
	  self.ws.write(self.result, 3,task.project['tip'])
	  self.ws.write(self.result, 7,task.project['novo'])
	  self.ws.write(self.result, 5,task.project['col_komnat'])
	  self.ws.write(self.result, 6,task.project['plosh'])
	  self.ws.write(self.result, 8,task.project['cena'])
	  self.ws.write(self.result, 9,task.project['opis'])
	  self.ws.write(self.result, 10, u'Sochi-Express.ru')
	  
	  
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

     
     