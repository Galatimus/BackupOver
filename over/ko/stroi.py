#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
import math
from grab import Grab
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Стройки_Москвы.xlsx')


     
     
class Region_Com(Spider):    
     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"Местоположение")
	  self.ws.write(0, 2, u"Район")
	  self.ws.write(0, 3, u"Населенный пункт")
	  self.ws.write(0, 4, u"Функциональное назначение")
	  self.ws.write(0, 5, u"Вид строительства")
	  self.ws.write(0, 6, u"Срок ввода")
	  self.ws.write(0, 7, u"Этажность")
	  self.ws.write(0, 8, u"Застройщик")
	  self.ws.write(0, 9, u"Источник финансирования")
	  self.ws.write(0, 10, u"Описание")
	  self.ws.write(0, 11, u"Назначение объекта")
	  self.ws.write(0, 12, u"Статус объекта")
	  self.ws.write(0, 13, u"Общая площадь, кв.м.")
	  self.ws.write(0, 14, u"Долгота")
	  self.ws.write(0, 15, u"Широта")
	  self.ws.write(0, 16, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 17, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 18, u"ДАТА_ПАРСИНГА")
	
	  self.result= 1        

     def task_generator(self):
	  for x in range(1,2340):#52
	       yield Task ('item',url='https://stroi.mos.ru/construction/%d'%x,refresh_cache=True,network_try_count=100)
       
       
     def task_item(self, grab, task):
	  try:
	       punkt = grab.doc.select(u'//strong[@class="object-page__position-name"]/following-sibling::text()').text().replace(u'адрес: ','')
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter =  grab.doc.select(u'//span[@class="object-page__position-area"]').text().replace('( ','').replace(' )','')
	  except IndexError:
	       ter =''
	       
	  try:
	       uliza = 'Москва'
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom =  grab.doc.select(u'//span[contains(text(),"Функциональное назначение")]/following::span[2]').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       tip = grab.doc.select(u'//span[contains(text(),"Вид строительства")]/following::span[2]').text()
	  except IndexError:
	       tip = ''
	     
	  try:
	       orentir = grab.doc.select(u'//span[contains(text(),"Срок ввода")]/following::span[2]').text()
	       #print rayon
	  except DataNotFound:
	       orentir = ''
	  try:
	       price = grab.doc.select(u'//span[contains(text(),"Этажность")]/following::span[2]').text()
	  except IndexError:
	       price = ''
	       
	  try:
	       naz = grab.doc.select(u'//span[contains(text(),"Застройщик")]/following::span[2]').text()
	  except IndexError:
	       naz = ''   
	     
	     
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Источник финансирования")]/following::span[2]').text()
	    #print rayon
	  except IndexError:
	       plosh = ''

	  try:
	       ohrana = grab.doc.select(u'//div[@class="object-page__info-content"]').text()
	  except IndexError:
	       ohrana =''
	       
	       
	  try:
	       gaz = grab.doc.select(u'//strong[@class="object-page__position-name"]').text()
	  except IndexError:
	       gaz =''
	  try:
	       try:
	            voda = grab.doc.select(u'//span[@class="object-page__position-status operation"]').text()
	       except IndexError:
		    voda = grab.doc.select(u'//span[@class="object-page__position-status construction"]').text()
	  except IndexError:
	       voda =''
	       
	  try:
	       kanal = grab.doc.select(u'//span[contains(text(),"Общая площадь, кв.м")]/following::span[2]').text()
	  except IndexError:
	       kanal =''
	       
	  try:
	       elek = grab.doc.rex_text(u'data-point="(.*?)"').split(',')[0]
	  except IndexError:
	       elek =''
	       
	  try:
	       teplo =  grab.doc.rex_text(u'data-point="(.*?)"').split(',')[1]
	  except IndexError:
	       teplo =''	 	     
	     
	  try:
	       sub = 'Москва'
          except IndexError:
               sub = ''	       
	       
	       
	  projects = {'sub': sub,
                       'uliza': uliza,
                       'dom': dom,
                       'punkt': punkt,
                       'terit':ter,  
                       'price': price,                     
                       'naz': naz,
                       'url': task.url,
                       'orentir': orentir,
                       'ploshad': plosh,
                       'tip': tip,
                       'gaz': gaz,
                       'voda':voda,
                       'elekt': elek,
                       'ohrana': ohrana,
                       'teplo': teplo,
                       'kanal': kanal}
                      
   
	     
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	 
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['uliza']
	  print  task.project['dom']
	  print  task.project['naz']
	  print  task.project['punkt']
	  print  task.project['terit']	      
	  print task.project['url']
	  print  task.project['price']
	  print  task.project['orentir']	      
	  print  task.project['ploshad']	       
	  print  task.project['tip']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanal']
	  print  task.project['elekt']
	  print  task.project['teplo']
	  print  task.project['ohrana']
	
	 
	  
	  
	  
	  
   
   
   
   
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,3, task.project['uliza'])
	  self.ws.write(self.result,2, task.project['terit'])
	  self.ws.write(self.result,1, task.project['punkt'])
	  self.ws.write(self.result,4, task.project['dom']) 
	  self.ws.write(self.result,6, task.project['orentir'])
	  self.ws.write(self.result,5, task.project['tip'])
	  self.ws.write(self.result,8, task.project['naz'])
	  self.ws.write(self.result,7, task.project['price'])
	  self.ws.write(self.result,9, task.project['ploshad'])
	  self.ws.write(self.result,11, task.project['gaz'])
	  self.ws.write(self.result,12, task.project['voda'])
	  self.ws.write(self.result,13, task.project['kanal'])
	  self.ws.write(self.result,14, task.project['elekt'])
	  self.ws.write(self.result,15, task.project['teplo'])
	  self.ws.write(self.result,10, task.project['ohrana'])	 
	  self.ws.write_string(self.result,17, task.project['url'])  
	  self.ws.write_string(self.result,16, 'stroi.mos.ru')
	  self.ws.write(self.result,18, datetime.today().strftime('%d.%m.%Y'))
	  
	  
          
	  
	  print('*'*100)	
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  
	  #if self.result >50:
	       #self.stop()

bot = Region_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
workbook.close()
print('Done')

