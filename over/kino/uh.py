#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
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











       
class Ners_zem(Spider):
     def prepare(self):
       
	       
	  self.workbook = xlsxwriter.Workbook(u'UchebaRu_Школы.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"Название школы")
	  self.ws.write(0, 1, u"Город, в котором расположена школа")
	  self.ws.write(0, 2, u"Район школы")
	  self.ws.write(0, 3, u"Ближайшая к школе станция метро")
	  self.ws.write(0, 4, u"Полный адрес школы")
	  self.ws.write(0, 5, u"Тип школы")
	  self.ws.write(0, 6, u"Классы")
	  self.ws.write(0, 7, u"Стоимость обучения")
	  self.ws.write(0, 8, u"Профили обучения")
	  self.ws.write(0, 9, u"Виды спорта")
	  self.ws.write(0, 10, u"Кружки и секции")
	  self.ws.write(0, 11, u"Факультативы")
	  self.ws.write(0, 12, u"Дополнительно")
	  self.ws.write(0, 13, u"Адрес сайта школы")
	  self.ws.write(0, 14, u"Контактный имейл школы")
	  self.ws.write(0, 15, u"Контактный телефон школы")
	  self.ws.write(0, 16, u"Текстовое описание школы")
	  self.ws.write(0, 17, u"Адрес страницы школы")
	  self.ws.write(0, 18, u"Номер страницы школы")
	  self.result= 1
	  
	   
	   
	   
	   
     def task_generator(self):
	  for x in range(51):
	       yield Task ('post',url='https://www.ucheba.ru/for-kids/schools?s='+str(x*30),refresh_cache=True,network_try_count=100)
     
   
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//h2/a[1]'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)
	 
       
    
   
     def task_item(self, grab, task):
	  try:
	       mesto = grab.doc.select(u'//h1').text()
	  except IndexError:
	       mesto =''
	       
	  try:
	       punkt = grab.doc.select(u'//span[@class="address-panel-title"]/i[@class="fa fa-map-marker"]/following::text()[1]').text().split(', ')[0].split(' (')[0]
	  except IndexError:
	       punkt = ''	       
	   
	  try:
	       ter = grab.doc.rex_text(u', (.*?)р-н')
	  except IndexError:
	       ter =''
	  try:
	       uliza = grab.doc.select(u'//span[@class="address-panel-title"]/i[@class="fa fa-map-marker"]/following::text()[1]').text()
	  except IndexError:
	       uliza = ''
	      
	  try:
	       dom = grab.doc.select(u'//dt[contains(text(),"Тип школы")]/following-sibling::dd').text()
	  except IndexError:
	       dom = ''
	       
	  
	  try:
	       naz = grab.doc.select(u'//dt[contains(text(),"Классы")]/following-sibling::dd').text()
	  except IndexError:
	       naz =''
	  try:
	       klass =  grab.doc.select(u'//dt[contains(text(),"Стоимость обучения")]/following-sibling::dd').text()
	  except IndexError:
	       klass = ''
	  try:
	       price = grab.doc.select(u'//dt[contains(text(),"Профили обучения")]/following-sibling::dd').text()
	  except IndexError:
	       price =''
	  try: 
	       plosh = grab.doc.select(u'//dt[contains(text(),"Виды спорта")]/following-sibling::dd').text()
	  except IndexError:
	       plosh=''
	  try:
	       ohrana = grab.doc.select(u'//dt[contains(text(),"Кружки и секции")]/following-sibling::dd').text()
	  except IndexError:
	       ohrana =''
	  try:
	       gaz =  grab.doc.select(u'//dt[contains(text(),"Факультативы")]/following-sibling::dd').text()
	  except IndexError:
	       gaz =''
	  try:
	       voda =  grab.doc.select(u'//dt[contains(text(),"Дополнительно")]/following-sibling::dd').text()
	  except IndexError:
	       voda =''
	  try:
	       kanal = grab.doc.select(u'//span[@class="address-panel-title"]/i[@class="fa fa-newspaper-o"]/following::text()[1]').text()
	  except IndexError:
	       kanal =''
	  try:
	       elek = grab.doc.select(u'//span[@class="address-panel-title"]/i[@class="fa fa-at"]/following::text()[1]').text()
	  except IndexError:
	       elek =''
	  try:
	       teplo = re.sub(u'[^\d\,\(\)\-]','',grab.doc.select(u'//span[@class="address-panel-title"]/i[@class="fa fa-phone"]/following::text()[1]').text()).replace('(4','+7(4')
	  except IndexError:
	       teplo =''
	  #time.sleep(1)
	  try:
	       opis = grab.doc.select(u'//div[@class="head-announce__lead"]').text() 
	  except IndexError:
	       opis = ''
	  
	  
	   
	  projects = {'adress': mesto,
                      'terit':ter, 
                      'punkt':punkt, 
                      'ulica':uliza,
                      'dom':dom,
                      'naz':naz,
                      'klass': klass,
                      'cena': price,
                      'plosh': plosh,
                      'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal,
                      'electr': elek,
                      'teplo': teplo,
                      'opis': opis,
                      'url': task.url}
                     
	  
	  try:
	       link = task.url+'/contacts'
	       yield Task('metro',url=link,project=projects,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       yield Task('metro',grab=grab,project=projects)
	       
	       
     def task_metro(self, grab, task):
	  try:
	       metro = grab.doc.select(u'//span[@class="address-panel-title mr-5"]/following-sibling::text()').text()
	  except IndexError:
	       metro = ''
	    
	  yield Task('write',project=task.project,metro=metro,grab=grab)
     
     
     
     def task_write(self,grab,task):
	  #time.sleep(1)
	  print('*'*100)	       
	  print  task.project['adress']
	  print  task.project['punkt']
	  
	  print  task.project['terit']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['naz']
	  print  task.project['klass']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['ohrana']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.metro
	  
	 
     
	  
	  

	  self.ws.write(self.result, 0, task.project['adress'])
	  self.ws.write(self.result, 1, task.project['punkt'])
	  self.ws.write(self.result, 2, task.project['terit'])
	  self.ws.write(self.result, 3, task.metro)
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 6, task.project['naz'])
	  self.ws.write(self.result, 7, task.project['klass'])
	  self.ws.write(self.result, 8, task.project['cena'])
	  self.ws.write(self.result, 9, task.project['plosh'])
	  self.ws.write(self.result, 10, task.project['ohrana'])
	  self.ws.write(self.result, 11, task.project['gaz'])
	  self.ws.write(self.result, 12, task.project['voda'])
	  self.ws.write_string(self.result, 13, task.project['kanaliz'])
	  self.ws.write_string(self.result, 14, task.project['electr'])
	  self.ws.write(self.result, 15, task.project['teplo'])
	  self.ws.write(self.result, 16, task.project['opis'])
	  self.ws.write_string(self.result, 17, task.project['url'])
	  self.ws.write(self.result, 18, re.sub(u'[^\d]','',task.project['url']))
	 
	  
	  print('*'*100)
	  
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	 
	 
	  print('*'*100)
	  self.result+= 1

	  #if self.result > 50:
	       #self.stop()	       


bot = Ners_zem(thread_number=2, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
print('Спим 1 сек...')
time.sleep(1)
print('Сохранение...')
bot.workbook.close()
print('Done!')

       
     
     
     