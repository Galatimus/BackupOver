#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
from sub import conv
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Kartarf_Dostoprimechatelnosti.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Название объекта")
	  self.ws.write(0, 1, u"Регистрационный номер")
	  self.ws.write(0, 2, u"Категория историко-культурного значения")
	  self.ws.write(0, 3, u"Вид объекта")
	  self.ws.write(0, 4, u"Основная типология")
	  self.ws.write(0, 5, u"Сведения о дате создания")
	  self.ws.write(0, 6, u"Адрес объекта (местонахождение)")
	  self.ws.write(0, 7, u"Наименование, дата и номер решения органа государственной власти о постановке объекта на государственную охрану")
	  self.ws.write(0, 8, u"GPS Координаты")
	  self.ws.write(0, 9, u"Описание предмета охраны")
	  self.ws.write(0, 10, u"Гиперссылка")
	  self.ws.write(0, 11, u"Дата сбора информации")
	  self.ws.write(0, 12, u"Источник")
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(1,2873):
               yield Task ('post',url='https://kartarf.ru/dostoprimechatelnosti?page=%d'%x,refresh_cache=True,network_try_count=100)

	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//tbody/tr/td/a[contains(@href,"dostoprimechatelnosti")]'):
	       ur = elem.attr('href')
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)	       
                
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h1').text()
	  except IndexError:
	       sub = ''
	  try:
	       ray =  grab.doc.select(u'//h4[contains(text(),"Регистрационный номер")]/following-sibling::p[1]').text()
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//h4[contains(text(),"Категория историко-культурного значения")]/following-sibling::p[1]').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//h4[contains(text(),"Вид объекта")]/following-sibling::p[1]').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       uliza = grab.doc.select(u'//h4[contains(text(),"Основная типология")]/following-sibling::p[1]').text()
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//h4[contains(text(),"Сведения о дате создания")]/following-sibling::p[1]').text()#.split(', ')[0]
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//h4[contains(text(),"Адрес объекта (местонахождение)")]/following-sibling::p[1]').text()#.split(', ')[1]
	  except IndexError:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//h4[contains(text(),"Наименование, дата и номер решения органа государственной власти о постановке объекта на государственную охрану")]/following-sibling::p[1]').text()#.split(', ')[1].replace(u'г.','')
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//h4[contains(text(),"GPS Координаты")]/following-sibling::p[1]').text()
	  except IndexError:
	       price = '' 
	       
	  try:
	       opis = grab.doc.select(u'//h4[contains(text(),"Описание предмета охраны")]/following-sibling::p[1]').text()
          except IndexError:
	       opis = ''     
	
          #udal = reduce(lambda udal, r: udal.replace(r[0], r[1]), conv, udal).replace(u' областьская ',' ') 
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
	              'opis': opis,
                      'cena': price }
          
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['cena']
	  print  task.project['opis']

	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 6, task.project['trassa'])
	  self.ws.write(self.result, 7, task.project['udal'])
	  self.ws.write(self.result, 8, task.project['cena'])
	  self.ws.write(self.result, 9, task.project['opis'])
	  self.ws.write_string(self.result, 12, u'kartarf.ru')
	  self.ws.write(self.result, 11, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write_string(self.result, 10, task.project['url'])
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	  #if self.result >= 10:
	       #self.stop()	       	       
	 

     
bot = Cian_Zem(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
try:
     bot.run()
except KeyboardInterrupt:
     pass
workbook.close()
print('Done!') 







