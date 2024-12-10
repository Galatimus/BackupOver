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


workbook = xlsxwriter.Workbook(u'Incity_Склады.xlsx')


     
     
class Region_Com(Spider):    
     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"Округ")
	  self.ws.write(0, 2, u"Местоположение")
	  self.ws.write(0, 3, u"Подъездные пути")
	  self.ws.write(0, 4, u"Шоссе")
	  self.ws.write(0, 5, u"Удаленность")
	  self.ws.write(0, 6, u"Класс")
	  self.ws.write(0, 7, u"Цена аренды")
	  self.ws.write(0, 8, u"Общая площадь")
	  self.ws.write(0, 9, u"Этаж")
	  self.ws.write(0, 10, u"Год постройки")
	  self.ws.write(0, 11, u"Описание")
	  self.ws.write(0, 12, u"Режим работы")
	  self.ws.write(0, 13, u"Высота потолков")
	  self.ws.write(0, 14, u"Ворота")
	  self.ws.write(0, 15, u"Благоустройство")
	  self.ws.write(0, 16, u"Полы")
	  self.ws.write(0, 17, u"Метро")
	  self.ws.write(0, 18, u"Удаленность от метро")
	  self.ws.write(0, 19, u"Паркинг")
	  self.ws.write(0, 20, u"Электроснабжение")
	  self.ws.write(0, 21, u"Площадь аренды")
	  self.ws.write(0, 22, u"Налогооблажение")
	  self.ws.write(0, 23, u"Тип договора аренды")
	  self.ws.write(0, 24, u"Срок договора аренды")
	  self.ws.write(0, 25, u"Заголовок")
	  self.ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 28, u"ДАТА_ПАРСИНГА")
	
	  self.result= 1        

     def task_generator(self):
	  for x in range(1,11):#52
	       yield Task ('post',url='http://www.incity.su/krupnye_skladskie_kompleksy.php?page_11=%d'%x,refresh_cache=True,network_try_count=100)
       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//td[@class="border"]/a'):
	       ur = elem.attr('href')  
	       #print ur	      
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
  
   
     def task_item(self, grab, task):
	  try:
	       punkt = grab.doc.select(u'//td[contains(text(),"Округ")]/following-sibling::td').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter =  grab.doc.select(u'//td[contains(text(),"Подъездные пути")]/following-sibling::td').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
		    #uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
	       #else:    
	       uliza = grab.doc.select(u'//td[contains(text(),"Шоссе")]/following-sibling::td').text()
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom =  grab.doc.select(u'//td[contains(text(),"Удаленность")]/following-sibling::td[contains(text(),"МКАД")]').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       tip = grab.doc.select(u'//td[contains(text(),"Класс")]/following-sibling::td').text()
	  except IndexError:
	       tip = ''
	     
	  try:
	       orentir = grab.doc.select(u'//td[contains(text(),"Цена аренды")]/following-sibling::td').text()
	       #print rayon
	  except DataNotFound:
	       orentir = ''
	  try:
	       price = grab.doc.select(u'//td[contains(text(),"Общая площадь")]/following-sibling::td').text()
	  except IndexError:
	       price = ''
	       
	  try:
	       naz = grab.doc.select(u'//td[contains(text(),"Этаж")]/following-sibling::td').text()
	  except IndexError:
	       naz = ''   
	     
	     
	  try:
	       plosh = grab.doc.select(u'//td[contains(text(),"Год постройки")]/following-sibling::td').text()
	    #print rayon
	  except IndexError:
	       plosh = ''

	  try:
	       ohrana = grab.doc.select(u'//td[@class="type"]').text()
	  except IndexError:
	       ohrana =''
	       
	       
	  try:
	       gaz = grab.doc.select(u'//td[contains(text(),"Режим работы")]/following-sibling::td').text()
	  except IndexError:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//td[contains(text(),"Высота потолков")]/following-sibling::td').text()
	  except IndexError:
	       voda =''
	       
	  try:
	       kanal = grab.doc.select(u'//td[contains(text(),"Ворота")]/following-sibling::td').text()
	  except IndexError:
	       kanal =''
	       
	  try:
	       elek = grab.doc.select(u'//td[contains(text(),"Благоустройство")]/following-sibling::td').text()
	  except IndexError:
	       elek =''
	       
	  try:
	       teplo =  grab.doc.select(u'//td[contains(text(),"Полы")]/following-sibling::td').text()
	  except IndexError:
	       teplo =''	 	     
	     
	  
	     
	  try:
	       opis = grab.doc.select(u'//td[contains(text(),"Метро")]/following-sibling::td').text() 
	  except IndexError:
	       opis = ''
	     
	  try:
	       lico = grab.doc.select(u'//td[contains(text(),"Удаленность от метро")]/following-sibling::td').text()
	   #print rayon
	  except IndexError:
	       lico = ''
	     
	  try:
	       com = grab.doc.select(u'//td[contains(text(),"Паркинг")]/following-sibling::td').text()
	   #print rayon
	  except IndexError:
	       com = ''
	     
	     
	  try:
	       data = grab.doc.select(u'//td[contains(text(),"Электроснабжение")]/following-sibling::td').text()
	  except IndexError:
	       data = ''
	       
	  try:
	       data1 = grab.doc.select(u'//td[contains(text(),"Площадь аренды")]/following-sibling::td').text()
	  except IndexError:
	       data1 = ''
	 
	  try:
	       data2 = grab.doc.select(u'//td[contains(text(),"Налогооблажение")]/following-sibling::td').text()
	  except IndexError:
	       data2 = ''
	   
	  try:
	       data3 = grab.doc.select(u'//td[contains(text(),"Тип договора аренды")]/following-sibling::td').text()
	  except IndexError:
	       data3 = ''
	     
	  try:
	       data4 = grab.doc.select(u'//td[contains(text(),"Срок договора аренды")]/following-sibling::td').text()
	  except IndexError:
	       data4 = '' 
	       
	  try:
	       zagol = grab.doc.select(u'//h1').text()
	  except IndexError:
	       zagol = ''	  
	       
	  try:
	       if 'МО'in punkt:
		    sub = 'Московская область'
	       else:
		    sub = 'Москва'
          except IndexError:
               sub = ''	       
	       
	       
	  projects = {'sub': sub,
                       'uliza': uliza,
                       'dom': dom,
                       'punkt': punkt,
                       'terit':ter,  
                       'price': price,
                       'opis': opis,
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
                       'kanal': kanal,
                       'lico':lico,
                       'com':com,
	               'zagolovok': zagol,
                       'dataraz': data,
	               'datara': data1,
	               'datar': data2,
	               'datarz': data3,
	               'daaraz': data4 }
   
	  try:
	  
	       #linkk = task.url.replace('http://www.incity.su/commercial_real_estate/','')
	       link = 'http://www.incity.su/commercial_real_estate/contacts/'+task.url.replace('http://www.incity.su/commercial_real_estate/','')
	       #print link
	       yield Task('subject',url=link,project=projects,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       yield Task('subject',grab=grab,project=projects)  
	       
     def task_subject(self, grab, task):
	  
          try:
	       try:
	            adress = grab.doc.select(u'//td[contains(text(),"Адрес МО")]/following-sibling::td').text()
	       except IndexError:
		    adress = grab.doc.select(u'//td[contains(text(),"Улица")]/following-sibling::td').text()
          except IndexError:
	       adress = ''	     
   
	  yield Task('write',project=task.project,adress=adress,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	 
	  print('*'*100)
	  print  task.project['sub']
	  print  task.adress
	  print  task.project['uliza']
	  print task.project['zagolovok']
	  print  task.project['dom']
	  print  task.project['naz']
	  print  task.project['punkt']
	  print  task.project['terit']	      
	  print task.project['url']
	
	  print  task.project['opis']
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
	  print  task.project['lico']
	  print  task.project['com']
	  print  task.project['dataraz']
	  print  task.project['datara']
	  print  task.project['datar']
	  print  task.project['datarz']
	  print  task.project['daaraz']
	  
	  
	  
   
   
   
   
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,2, task.adress)
	  self.ws.write(self.result,4, task.project['uliza'])
	  self.ws.write(self.result,3, task.project['terit'])
	  self.ws.write(self.result,1, task.project['punkt'])
	  self.ws.write(self.result,5, task.project['dom']) 
	  self.ws.write(self.result,7, task.project['orentir'])
	  self.ws.write(self.result,6, task.project['tip'])
	  self.ws.write(self.result,9, task.project['naz'])
	  self.ws.write(self.result,8, task.project['price'])
	  self.ws.write(self.result,10, task.project['ploshad'])
	  self.ws.write(self.result,12, task.project['gaz'])
	  self.ws.write(self.result,13, task.project['voda'])
	  self.ws.write(self.result,14, task.project['kanal'])
	  self.ws.write(self.result,15, task.project['elekt'])
	  self.ws.write(self.result,16, task.project['teplo'])
	  self.ws.write(self.result,11, task.project['ohrana'])
	  self.ws.write(self.result,17, task.project['opis'])
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,18, task.project['lico'])
	  self.ws.write(self.result,19, task.project['com'])
	  self.ws.write(self.result,20, task.project['dataraz'])
	  self.ws.write(self.result,26, 'INCITY.SU')
	  self.ws.write(self.result,28, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,21, task.project['datara'])
          self.ws.write(self.result,22, task.project['datar']) 
          self.ws.write(self.result,23, task.project['datarz'])
          self.ws.write(self.result,24, task.project['daaraz'])
	  self.ws.write(self.result,25, task.project['zagolovok'])
          
	  
	  print('*'*100)	
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  
	  #if self.result >10:
	       #self.stop()

bot = Region_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
workbook.close()
print('Done')

