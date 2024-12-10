#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
from datetime import datetime,timedelta
import xlsxwriter
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'IRR_Сочи_Квартиры_Продажа.xlsx') 

	       
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
	  for x in range(1,764):
               link = 'http://sochi.irr.ru/real-estate/apartments-sale/secondary/'+'page'+str(x)+'/'
               yield Task ('post',url=link.replace(u'page1/',''),refresh_cache=True,network_try_count=100)
	  for x1 in range(1,997):
	       link1 = 'http://sochi.irr.ru/real-estate/apartments-sale/new/'+'page'+str(x1)+'/'
	       yield Task ('post',url=link1.replace(u'page1/',''),refresh_cache=True,network_try_count=100)	   
	       
     def task_post(self,grab,task):
	  if grab.doc.select(u'//h4[contains(text(),"Предложения рядом")]').exists()==True:
	       links = grab.doc.select(u'//h4[contains(text(),"Предложения рядом")]/preceding::a[contains(@class,"listing")]')
	  else:
	       links = grab.doc.select(u'//a[@class="listing__itemTitle"]')
	  for elem in links:
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//li[contains(text(),"Район города:")]').text().split(': ')[1]
          except IndexError:
               ray =''
	  
	  try:
	       uliza = grab.doc.select(u'//li[contains(text(),"Улица:")]').text().split(': ')[1]
	  except IndexError:
	       uliza =''
	       
	  try:
               dom = grab.doc.select(u'//li[contains(text(),"Дом:")]').text().split(': ')[1]
	   #print rayon
	  except IndexError:
	       dom = ''
		
	    
	  try:
               tip = grab.doc.select(u'//li[contains(text(),"Материал стен:")]').text().split(': ')[1]
          except IndexError:
	       tip = ''
	      
	  try:
	       #nv = re.sub('[^\d]', '',grab.doc.select(u'//li[contains(text(),"Год постройки/сдачи:")]').text().split(': ')[1])
	       if 'secondary'in task.url:
		    novo ='Нет'
	       else:
		    novo = 'Да'
	  except IndexError:
	       novo = ''
          try:
               kol_komnat = grab.doc.select(u'//li[contains(text(),"Комнат в квартире:")]').number()
          except IndexError:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//li[contains(text(),"Общая площадь:")]').text().split(': ')[1]
          except IndexError:
	       plosh = ''
          try:
               price = grab.doc.select(u'//div[@class="productPage__price js-contentPrice"]').text()
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//h4[contains(text(),"Описание")]/following-sibling::p').text() 
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
	  self.ws.write(self.result, 11, u'Из рук в руки')
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result > 10:
	       #self.stop()

     
bot = Cian_Kv(thread_number=5,network_try_limit=1000)
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

     
     