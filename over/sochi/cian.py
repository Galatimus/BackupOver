#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Cian_Сочи.xlsx') 

	       
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
          yield Task ('post',url='https://www.yelp.com/city',refresh_cache=True,network_try_count=100)

	       
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[contains(@href,"city")]'):
	       ur = elem.text()  
	       print ur
	       #yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').text()
          except DataNotFound:
               ray =''
	  
	  try:
	       try:
		    try:
			 try:
			      try:
				   try:
					try:
					     try:
						  uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ул.")]').text()
					     except IndexError:
						  uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пер.")]').text()
					except IndexError:
					     uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"просп.")]').text()
				   except IndexError:
					uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ш.")]').text()
			      except IndexError:
				   uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"бул.")]').text()
			 except IndexError:
			      uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"проезд")]').text()
		    except IndexError:
			 uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"наб.")]').text()
	       except IndexError:
		    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пл.")]').text()
	  except IndexError:
	       uliza =''
	       
	  try:
	       if uliza == '':
		    dom =''
	       else:	       
	            dom = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(@href,"house")]').text()
	   #print rayon
	  except DataNotFound:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//th[contains(text(),"Тип дома:")]/following-sibling::td').text().split(', ')[1]
          except IndexError:
	       tip = ''
	      
	  try:
	       novo = grab.doc.select(u'//th[contains(text(),"Тип дома:")]/following-sibling::td').text().split(', ')[0].replace(u'новостройка',u'да').replace(u'вторичка',u'нет')
	  except DataNotFound:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//div[@class="object_descr_title"]').number()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//th[contains(text(),"Общая площадь:")]/following-sibling::td').text().replace(u'–','')
          except DataNotFound:
	       plosh = ''
          try:
               price = grab.doc.select(u'//div[@class="object_descr_price"]').text().split(u'.')[0]
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="object_descr_text"]/text()').text() 
          except DataNotFound:
               opis = ''
	       
	  try:
	       m2 = grab.doc.select(u'//div[@id="price_rur"]/following-sibling::div').text()#.split(u'включая')[0]
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
	  self.ws.write(self.result, 6,task.project['col_komnat'])
	  self.ws.write(self.result, 7,task.project['plosh'])
	  self.ws.write(self.result, 8,task.project['cena'])
	  self.ws.write(self.result, 9,task.project['metr'])
	  self.ws.write(self.result, 10,task.project['opis'])
	  self.ws.write(self.result, 11, u'ЦИАН')
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result > 20:
	       #self.stop()

     
bot = Cian_Kv(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
command = 'mount -t cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
#command = 'apt autoremove'
p = os.system('echo %s|sudo -S %s' % ('1122', command))
print p
time.sleep(1)
#bot.workbook.close()
workbook.close()
print('Done!')

     
     