#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from mesto import ul
import os
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

workbook = xlsxwriter.Workbook(u'Sochi_Domofond_Продажа.xlsx') 

	       
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
	  for x in range(1,1600):#148
               yield Task ('post',url='http://www.domofond.ru/prodazha-kvartiry-sochi-c909?Page=%d'%x,network_try_count=100)
         
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@itemprop="sameAs"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//span[@itemprop="address"]/following-sibling::p').text().replace(u'Сочи','')
          except IndexError:
               ray =''
	  
	  try:
               r1= grab.doc.select(u'//span[@itemprop="address"]').text()
               t2=0
	       for w1 in r1.split(','):
		    t2+=1
		    for x in range(len(ul)):
			 if ul[x] in w1:
			      uliza = r1.split(',')[t2-1].replace(u' д','')
			      break
	       print uliza
	  except (IndexError,UnboundLocalError):
	       uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//span[@itemprop="address"]').text().split(', ')[1]
	       #print rayon
	  except IndexError:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//strong[contains(text(),"Материал здания:")]/following-sibling::text()').text()
          except IndexError:
	       tip = ''
	      
	  try:
	       novo = grab.doc.select(u'//strong[contains(text(),"Тип объекта:")]/following-sibling::text()').text().replace(u'Новостройка',u'Да').replace(u'Вторичная',u'Нет')
	  except IndexError:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//strong[contains(text(),"Комнаты:")]/following-sibling::text()').number()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::text()').text()
          except DataNotFound:
	       plosh = ''
          try:
               price = grab.doc.select(u'//strong[contains(text(),"Цена:")]/following-sibling::text()').text()#.split(u'.')[0]
	       #novo = u'краткосрочная'
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//p[@itemprop="description"]').text()
	       #istoch = u'DOMOFOND.RU'
	       
          except DataNotFound:
               opis = ''
	       
	  try:
	       m2 = grab.doc.select(u'//strong[contains(text(),"Цена за м²:")]/following-sibling::text()').text()
	  except IndexError:
	       m2 =''	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom.replace(ray,'').replace(uliza,''),
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
	  self.ws.write(self.result, 11, u'DOMOFOND.RU')
	  
	  
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

     
     