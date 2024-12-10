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

workbook = xlsxwriter.Workbook(u'ar/Arendash.xlsx') 

	       
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
	  yield Task ('post',url='http://arendash.ru/kvartiry.html',network_try_count=100)
         
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="section-on-index"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100,use_proxylist=False)
	    
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//a[@class="ditto_next_link"]')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*100)
	       print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!','NO PAGE NEXT','!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	       print('*'*100)
	       logger.debug('%s taskq size' % self.task_queue.size())        
        
     
     def task_item(self, grab, task):
	  
	  try:
	       try:
                    ray = grab.doc.rex_text(u' улице (.*?) районе.').split(u' в ')[1]
	       except IndexError:
		    ray = grab.doc.rex_text(u'микрорайоне (.*?) Сочи') 
          except IndexError:
               ray =''
	  
	  try:
	       uliza = grab.doc.rex_text(u'улице (.*?) в ')
	      
	  except IndexError:
               uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//h3').text().split('-')[0]
	   #print rayon
	  except IndexError:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//li[contains(text(),"Тип дома")]').text().split(': ')[1]
          except IndexError:
	       tip = ''
	      
	  try:
	       s = grab.doc.select(u'//div[@class="row"]/div[@class="col-md-12 content"]').text()#.split(u'Количество просмотров: ')[0]
	       if s.find(u'длительн')>=0:
		    novo = u'долгосрочная'
	       else:
		    novo = u'краткосрочная'
	  except IndexError:
	       novo = ''
          try:
               kol_komnat = re.sub('[^\d]','',grab.doc.rex_text(u'аренду (.*?)-'))
          except IndexError:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//strong[contains(text(),"Общая площадь ")]/following-sibling::text()').text()
          except IndexError:
	       plosh = ''
          try:
               price = re.sub('[^\d]','',grab.doc.rex_text(u'квартира (.*?)рублей'))+u' руб.'
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="row"]/div[@class="col-md-12 content"]').text() 
          except IndexError:
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
	  self.ws.write(self.result, 5,task.project['dom'])
	  self.ws.write(self.result, 3,task.project['tip'])
	  self.ws.write(self.result, 7,task.project['novo'])
	  #self.ws.write(self.result, 4,task.project['col_komnat'])
	  self.ws.write(self.result, 6,task.project['plosh'])
	  self.ws.write(self.result, 8,task.project['cena'])
	  self.ws.write(self.result, 9,task.project['opis'])
	  self.ws.write(self.result, 10, u'Arendash.ru')
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result > 10:
	       #self.stop()

bot = Cian_Kv(thread_number=2,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')

     
     