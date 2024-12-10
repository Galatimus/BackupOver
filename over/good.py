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
	  self.workbook = xlsxwriter.Workbook(u'Instamart_Metro.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"Наименование магазина")
	  self.ws.write(0, 1, u"Город")
	  self.ws.write(0, 2, u"Адрес Магазина")
	  self.ws.write(0, 3, u"Раздел")
	  self.ws.write(0, 4, u"Подраздел")
	  self.ws.write(0, 5, u"Подраздел 3й уровень")
	  self.ws.write(0, 6, u"Наименование продукта")
	  self.ws.write(0, 7, u"Вес продукта(фасовка)")
	  self.ws.write(0, 8, u"Стоимость")
	  self.ws.write(0, 9, u"Стоимость за ед. измерения")
	  self.ws.write(0, 10, u"Акция/регулярная цена")
	  self.ws.write(0, 11, u"Единица измерения")
	  self.ws.write(0, 12, u"Изготовитель")
	  self.ws.write(0, 13, u"Описание")
	  self.ws.write(0, 14, u"Состав")
	  self.ws.write(0, 15, u"Бренд")
	  self.ws.write(0, 16, u"Страна")
	  self.ws.write(0, 17, u"Условия хранения")
	  self.ws.write(0, 18, u"Срок хранения")
	  self.ws.write(0, 19, u"Тип")
	  self.ws.write(0, 20, u"Вес")
	  self.ws.write(0, 21, u"Пищевая ценность на 100 г Белки")
	  self.ws.write(0, 22, u"Пищевая ценность на 100 г Жиры")
	  self.ws.write(0, 23, u"Пищевая ценность на 100 г Углеводы")
	  self.ws.write(0, 24, u"Пищевая ценность на 100 г Калорийность")
	  self.ws.write(0, 25, u"Ссылка")
	  self.result= 1


     def task_generator(self):
	  yield Task ('next',url='http://www.goodsmatrix.ru/GoodsCatalogue.aspx',refresh_cache=True,network_try_count=100)
	     
   
   
   
     def task_next(self,grab,task):
	  for el in grab.doc.select(u'//a[@class="show-all"]'):
	       urr = grab.make_url_absolute(el.attr('href'))  
	       #print urr
	       yield Task('goto', url=urr,refresh_cache=True,network_try_count=100)
	  
   
     def task_goto(self,grab,task):
	  for li in grab.doc.select(u'//a[@class="show-all"]'):
	       urlgo = grab.make_url_absolute(li.attr('href'))
	       #print urlgo
	       yield Task('post', url=urlgo,refresh_cache=True,network_try_count=100)
	  
       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="product__link"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  yield Task('page', grab=grab,refresh_cache=True,network_try_count=100)
	
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//div[@class="js-load-more"]')
	       u = grab.make_url_absolute(pg.attr('data-url'))
	       yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       print 'no_page'

	
     def task_item(self, grab, task):
	  
	  try:
	       ray = grab.doc.select(u'//div[@class="product-popup__breadcrumbs"]/span[1]/a/span').text()
	  except IndexError:
	       ray = '' 
	  try:
	       punkt = grab.doc.select(u'//div[@class="product-popup__breadcrumbs"]/span[2]/a/span').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//h1').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       uliza = grab.doc.select(u'//p[@class="product-popup__volume"]').text()
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//meta[@itemprop="price"]').attr('content')
	  except IndexError:
	       dom = ''
	       
	  try:
	       trassa = grab.doc.select(u'//strong[contains(text(),"Производитель")]/following::span[1]').text()
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//div[@class="product-popup__description"]').text()
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//strong[contains(text(),"Условия хранения")]/following::div[1]').text()
	  except IndexError:
	       price = ''
	  try:
	       plosh = grab.doc.select(u'//div[contains(text(),"Состав")]/following-sibling::div').text()
	  except IndexError:
	       plosh = ''

	  try:
	       vid = grab.doc.select(u'//strong[contains(text(),"Бренд")]/following::span[1]').text()
	  except IndexError:
	       vid = '' 
	       
	  try:
	       ohrana = grab.doc.select(u'//strong[contains(text(),"Страна")]/following::span[1]').text()
	  except IndexError:
	       ohrana =''

	  
	  try:
	       elek = grab.doc.select(u'//div[@class="product-popup__breadcrumbs"]/span[3]/a/span').text()
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
	       comp3 = grab.doc.select(u'//strong[contains(text(),"Белки")]/following::div[1]').text()
	  except IndexError:
	       comp3 = '' 
	  try:
	       comp4 = grab.doc.select(u'//strong[contains(text(),"Жиры")]/following::div[1]').text()
	  except IndexError:
	       comp4 = ''        
          try:
	       comp5 = grab.doc.select(u'//strong[contains(text(),"Углеводы")]/following::div[1]').text()
          except IndexError:
	       comp5 = ''        
	  try:
	       comp6 = grab.doc.select(u'//strong[contains(text(),"Калорийность")]/following::div[1]').text()
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
                      'ulica': uliza,
                      'dom': dom+u' р.',
                      'trassa': trassa,
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
	 
	  
	  
	  self.ws.write(self.result, 0, 'Metro')
	  self.ws.write(self.result, 1, 'Москва')
	  self.ws.write(self.result, 2, 'Метро,Проспект Мира')
	  self.ws.write(self.result, 3, task.project['rayon'])
	  self.ws.write(self.result, 4, task.project['punkt'])
	  self.ws.write(self.result, 5, task.project['electr'])
	  self.ws.write(self.result, 6, task.project['teritor'])
	  self.ws.write(self.result, 7, task.project['ulica'])
	  self.ws.write(self.result, 8, task.project['dom'])
	  self.ws.write(self.result, 17, task.project['cena'])
	  self.ws.write(self.result, 15, task.project['vid'])
	  self.ws.write(self.result, 16, task.project['ohrana'])
	  self.ws.write(self.result, 12, task.project['trassa'])
	  self.ws.write(self.result, 13, task.project['udal'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  self.ws.write(self.result, 18, task.project['company'])
	  self.ws.write(self.result, 19, task.project['company1'])
	  self.ws.write(self.result, 20, task.project['company2'])
	  self.ws.write(self.result, 21, task.project['company3'])
	  self.ws.write(self.result, 22, task.project['company4'])
	  self.ws.write(self.result, 23, task.project['company5'])
	  self.ws.write(self.result, 24, task.project['company6'])
	  self.ws.write_string(self.result, 25, task.project['url'])

	  print('*'*50)
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*50) 
	  self.result+= 1
	       

	  #if int(self.result) >= int(self.num)-3:
	       #self.stop()		    

     
bot = Gdedom_Zem(thread_number=5,network_try_limit=2000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')  
#command = 'mount -a'
#os.system('echo %s|sudo -S %s' % ('1122', command))
#time.sleep(2)
bot.workbook.close()
print('Done')
    





