#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
import re
import os
import random
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Gdedom_Zem(Spider):
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'GoodsMatrix.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"Наименование магазина")
	  self.ws.write(0, 1, u"Представитель")
	  self.ws.write(0, 2, u"Гост/Ту")
	  self.ws.write(0, 3, u"Раздел")
	  self.ws.write(0, 4, u"Подраздел")
	  self.ws.write(0, 5, u"Подраздел 3й уровень")
	  self.ws.write(0, 6, u"Наименование продукта")
	  self.ws.write(0, 7, u"Вес продукта(нетто)")
	  self.ws.write(0, 8, u"Штрих-код")
	  self.ws.write(0, 9, u"Срок годности")
	  self.ws.write(0, 10, u"Упаковка")
	  self.ws.write(0, 11, u"Количество в коробе (шт.)")
	  self.ws.write(0, 12, u"Продавец")
	  self.ws.write(0, 13, u"Описание")
	  self.ws.write(0, 14, u"Состав")
	  self.ws.write(0, 15, u"Бренд")
	  self.ws.write(0, 16, u"Страна")
	  self.ws.write(0, 17, u"Условия хранения")
	  self.ws.write(0, 18, u"Срок хранения")
	  self.ws.write(0, 19, u"Тип")
	  self.ws.write(0, 20, u"Вес")
	  self.ws.write(0, 21, u"Белки")
	  self.ws.write(0, 22, u"Жиры")
	  self.ws.write(0, 23, u"Углеводы")
	  self.ws.write(0, 24, u"Энергетическая ценность")
	  self.ws.write(0, 25, u"Ссылка")
	  self.result= 1


     def task_generator(self):
	  l= open('doods.txt').read().splitlines()
          self.dc = len(l)
          print self.dc
          for line in l:
	       yield Task ('item',url=line,refresh_cache=True,network_try_count=100)
	     

	
     def task_item(self, grab, task):
	  
	  ln = []
	  for elem in grab.doc.select(u'//span[@id="ctl00_GroupPath_GroupName"]/a'):
	       ur = elem.text()
	       ln.append(ur)	  
	  
	  try:
	       ray = ln[-3]
	  except IndexError:
	       ray = '' 
	  try:
	       punkt = ln[-2]
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//h1/span').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       ter2 = grab.doc.select(u'//span[contains(text(),"ГОСТ/ТУ:")]/following-sibling::span').text()
          except IndexError:
	       ter2 =''     
	       
	  try:
	       uliza = grab.doc.select(u'//span[contains(text(),"Масса нетто:")]/following-sibling::span').text()
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//span[contains(text(),"Срок годности:")]/following-sibling::span').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       trassa = grab.doc.select(u'//span[contains(text(),"Упаковка:")]/following-sibling::span').text()
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//span[contains(text(),"Количество в коробе (шт.):")]/following-sibling::span').text()
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//b[contains(text(),"Продавец:")]/following::a[1]').text()
	  except IndexError:
	       price = ''
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Описание:")]/following-sibling::span').text()
	  except IndexError:
	       plosh = ''

	  try:
	       vid = grab.doc.select(u'//span[contains(text(),"Состав:")]/following-sibling::span').text()
	  except IndexError:
	       vid = '' 
	       
	  try:
	       ohrana = grab.doc.select(u'//span[contains(text(),"Условия хранения:")]/following-sibling::span').text()
	  except IndexError:
	       ohrana =''

	  
	  try:
	       elek = ln[-1]
	  except IndexError:
	       elek =''
	       
	  try:
	       comp = grab.doc.select(u'//strong[contains(text(),"Срок хранения")]/following::div[1]').text()
	  except IndexError:
	       comp = '' 	       
	  try:
	       comp1 = grab.doc.select(u'//strong[contains(text(),"Тип")]/following::div[1]').text()
          except IndexError:
	       comp1 = '' 	       
	  try:
	       comp2 = grab.doc.select(u'//strong[contains(text(),"Вес")]/following::div[1]').text()
	  except IndexError:
	       comp2 = ''
	       
          try:
	       comp3 = grab.doc.select(u'//span[contains(text(),"Энергетический состав:")]/following-sibling::span/text()[1]').text().split(': ')[1]
	  except IndexError:
	       comp3 = '' 
	  try:
	       comp4 = grab.doc.select(u'//span[contains(text(),"Энергетический состав:")]/following-sibling::span/text()[2]').text().split(': ')[1]
	  except IndexError:
	       comp4 = ''        
          try:
	       comp5 = grab.doc.select(u'//span[contains(text(),"Энергетический состав:")]/following-sibling::span/text()[3]').text().split(': ')[1]
          except IndexError:
	       comp5 = ''        
	  try:
	       comp6 = grab.doc.select(u'//span[contains(text(),"Энергетический состав:")]/following-sibling::span/text()[4]').text().split(': ')[1]
	  except IndexError:
               comp6 = ''
	       
	  try:
	       comp7 = grab.doc.select(u'//div[@class="name_block_item"]/span[contains(text(),"(агент)")]').text()
          except IndexError:
	       comp7 = '' 	       
	  try:
	       comp8 = grab.doc.select(u'//div[@class="name_block_item"]/span[contains(text(),"(агент)")]').text()
	  except IndexError:
	       comp8 = '' 	       
	  try:
	       comp9 = grab.doc.select(u'//div[@class="name_block_item"]/span[contains(text(),"(агент)")]').text()
	  except IndexError:
	       comp9 = ''
	       
	  try:
	       comp10 = grab.doc.select(u'//div[@class="name_block_item"]/span[contains(text(),"(агент)")]').text()
	  except IndexError:
	       comp10 = ''	       
	       
	       
	  projects = {'url': task.url,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
	              'gost': ter2,
                      'ulica': uliza,
                      'dom': re.sub('[^\d]','',task.url),
                      'trassa': trassa,
	              'srok': dom,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
                      'vid': vid,
                      'ohrana':ohrana,
	              'company':comp,
	              'company1':comp1,
	              'company2':comp2,
	              'company3':comp3,
	              'company4':comp4,
	              'company5':comp5,
	              'company6':comp6,
	              'company7':comp7,
	              'company8':comp8,
	              'company9':comp9,
	              'company10':comp10,
                      'electr': elek}
                      
	  
	  yield Task('write',project=projects,grab=grab)
	    
     def task_write(self,grab,task):
	  print('*'*50)
	 
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['electr']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['ohrana']
	  print  task.project['vid']
	  print  task.project['gost']
	  print  task.project['srok']
	 
	  
	  
	  self.ws.write(self.result, 0, 'Товарная матрица')
	  self.ws.write(self.result, 1, 'Гудс Матрикс ООО')
	  self.ws.write(self.result, 2, task.project['gost'])
	  self.ws.write(self.result, 3, task.project['rayon'])
	  self.ws.write(self.result, 4, task.project['punkt'])
	  self.ws.write(self.result, 5, task.project['electr'])
	  self.ws.write(self.result, 6, task.project['teritor'])
	  self.ws.write(self.result, 7, task.project['ulica'])
	  self.ws.write(self.result, 8, task.project['dom'])
	  self.ws.write(self.result, 9, task.project['srok'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['vid'])
	  self.ws.write(self.result, 17, task.project['ohrana'])
	  self.ws.write(self.result, 10, task.project['trassa'])
	  self.ws.write(self.result, 11, task.project['udal'])
	  self.ws.write(self.result, 13, task.project['plosh'])
	  self.ws.write(self.result, 18, task.project['company'])
	  self.ws.write(self.result, 19, task.project['company1'])
	  self.ws.write(self.result, 20, task.project['company2'])
	  self.ws.write(self.result, 21, task.project['company3'])
	  self.ws.write(self.result, 22, task.project['company4'])
	  self.ws.write(self.result, 23, task.project['company5'])
	  self.ws.write(self.result, 24, task.project['company6'])
	  self.ws.write_string(self.result, 25, task.project['url'])

	  print('*'*50)
	  print 'Ready - '+str(self.result)+'/'+str(self.dc)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*50) 
	  self.result+= 1
	       

	  #if int(self.result) >= int(self.num)-3:
	       #self.stop()		    

     
bot = Gdedom_Zem(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')  
bot.workbook.close()
print('Done')
    





