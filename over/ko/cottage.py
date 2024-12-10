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

logging.basicConfig(level=logging.DEBUG)









class Gdedom_Zem(Spider):
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'Cottage_ru_Поселки.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"НАИМЕНОВАНИЕ_ПОСЕЛКА")
	  self.ws.write(0, 2, u"ПРОДАВЕЦ")
	  self.ws.write(0, 3, u"СТОИМОСТЬ")
	  self.ws.write(0, 4, u"ОПИСАНИЕ")
	  self.ws.write(0, 5, u"ПЛОЩАДЬ_УЧАСТКА")
	  self.ws.write(0, 6, u"ПЛОЩАДЬ_ДОМА")
	  self.ws.write(0, 7, u"ШОССЕ")
	  self.ws.write(0, 8, u"УДАЛЕННОСТЬ_РЯДОМ")
	  self.ws.write(0, 9, u"УДАЛЕННОСТЬ_ОТ_МКАД")
	  self.ws.write(0, 10, u"ВОДОЕМ")
	  self.ws.write(0, 11, u"ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 12, u"ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 13, u"КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 14, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 15, u"ИНФРАСТРУКТУРА")
	  self.ws.write(0, 16, u"ШИРОТА_ИСХ")
	  self.ws.write(0, 17, u"ДОЛГОТА_ИСХ")
	  self.ws.write(0, 18, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 19, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 20, u"ДАТА_ПАРСИНГА")
	  self.result= 1


     def task_generator(self):
	  yield Task ('next',url='https://www.cottage.ru/maps_new/',refresh_cache=True,network_try_count=100)
	     
   
   
   
     def task_next(self,grab,task):
	  for el in grab.doc.select(u'//ul[@class="list-unstyled"]/li/a'):
	       urr = grab.make_url_absolute(el.attr('href'))  
	       #print urr
	       yield Task('goto', url=urr+'objects/village/',refresh_cache=True,network_try_count=100)
	       yield Task('goto', url=urr+'objects/village/poselki-tounhausov/',refresh_cache=True,network_try_count=100)
	       yield Task('goto', url=urr+'objects/village/bez-podryada/',refresh_cache=True,network_try_count=100)
	       yield Task('goto', url=urr+'objects/complex/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://www.cottage.ru/objects/village/poselki-tounhausov/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://www.cottage.ru/objects/village/bez-podryada/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://www.cottage.ru/objects/village/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://www.cottage.ru/objects/complex/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://spb.cottage.ru/objects/village/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://spb.cottage.ru/objects/village/poselki-tounhausov/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://spb.cottage.ru/objects/village/bez-podryada/',refresh_cache=True,network_try_count=100)
	  yield Task('goto', url='https://spb.cottage.ru/objects/complex/',refresh_cache=True,network_try_count=100)
	  
   
     def task_goto(self,grab,task):
	  for li in grab.doc.select(u'//a[@itemprop="name url"]'):
	       urlgo = grab.make_url_absolute(li.attr('href'))
	       #print urlgo
	       yield Task('item', url=urlgo,refresh_cache=True,network_try_count=100)
	  yield Task('page', grab=grab,refresh_cache=True,network_try_count=100)

	
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//li[@class="current active"]/following-sibling::li[1]/a')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('goto',url= u,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       print 'no_page'

	
     def task_item(self, grab, task):
	  
	  try:
	       ray = grab.doc.select(u'//i[@class="fa fa-map-marker"]/following-sibling::text()').text()
	  except IndexError:
	       ray = '' 
	  try:
	       punkt = grab.doc.select(u'//h1').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//*[contains(text(),"Продавец")]').text().replace(u'Продавец: ','')
	  except IndexError:
	       ter =''
	       
	  try:
	       uliza = grab.doc.select(u'//div[@class="grid-box-object-info__box"][1]').text()
	  except IndexError:
	       uliza = ''
	       
	  try:
	       cena = grab.doc.select(u'//div[@class="grid-box-object-gallery-top-leftpanel__price"]').text()
          except IndexError:
	       cena = ''	  
	       
	  try:
	       dom = grab.doc.select(u'//div[contains(text(),"Участ")]/following::div[1]/div').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       try:
	            trassa = grab.doc.select(u'//div[contains(text(),"Площадь дома")]/following::div[1]/div').text()
	       except IndexError:
		    trassa = grab.doc.select(u'//div[contains(text(),"Дома")]/following::div[1]/div').text()
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//div[contains(text(),"Шоссе")]/following::div[1]/div').text()
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//div[contains(text(),"Рядом")]/following::div[1]/div').text()
	  except IndexError:
	       price = ''
	  try:
	       plosh = grab.doc.select(u'//div[contains(text(),"от МКАД")]/following::div[1]/div').text()
	  except IndexError:
	       plosh = ''

	  try:
	       vid = grab.doc.select(u'//div[contains(text(),"Ближайший водоём")]/following::div[1]/div').text()
	  except IndexError:
	       vid = '' 
	       
	  try:
	       oper = grab.doc.select(u'//div[contains(text(),"Газ")]/following::div[1]/div').text()
	  except IndexError:
	       oper = ''	       
	       
	  try:
	       ohrana = grab.doc.select(u'//div[contains(text(),"Водоснабжение")]/following::div[1]/div').text()
	  except IndexError:
	       ohrana =''
	  try:
	       elek = grab.doc.select(u'//div[contains(text(),"Канализация")]/following::div[1]/div').text()
	  except IndexError:
	       elek =''
	       
	  try:
	       lng = grab.doc.select(u'//div[contains(text(),"Электричество")]/following::div[1]/div').text()
	  except IndexError:
	       lng =''		    
	  try:
	       teplo = grab.doc.select(u'//div[@class="grid-box-object-info-params__name w-100"]/div').text()
	  except IndexError:
	       teplo =''
	       
	 
	  try:
	       opis = grab.doc.select(u'//div[@id="contact-map"]').attr('data-lat')
	  except IndexError:
	       opis = ''
	       
	  try:
	       park = grab.doc.select(u'//div[@id="contact-map"]').attr('data-lon') 
	  except IndexError:
	       park = ''    
	       
	  
	  
	       
	 
		    
	  
	  clearText = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", uliza)
	  clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText)

	       
	  projects = {'url': task.url,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': clearText.replace(u'читать далее',''),
                      'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
                      'vid': vid,
	              'shir': opis,
                      'ohrana':ohrana,
                      'electr': elek,
                      'teplo': teplo,
                      'dol': lng,
	              'cena1': cena,
                      'opera': oper,
                      'parkov':park}
	  
	  yield Task('write',project=projects,grab=grab)
	    
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  #print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['ohrana']
	  print  task.project['electr']
	  print  task.project['dol']
	  print  task.project['teplo']
	  print  task.project['cena1']
	  print task.project['url']
	  print  task.project['vid']
	  print task.project['opera']
	  print  task.project['parkov']
	  print  task.project['shir']
	  
	  
	  #self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 0, task.project['rayon'])
	  self.ws.write(self.result, 1, task.project['punkt'])
	  self.ws.write(self.result, 2, task.project['teritor'])
	  self.ws.write(self.result, 3, task.project['cena1'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 6, task.project['trassa'])
	  self.ws.write(self.result, 7, task.project['udal'])
	  self.ws.write(self.result, 8, task.project['cena'])
	  self.ws.write(self.result, 9, task.project['plosh'])
	  self.ws.write(self.result, 10, task.project['vid'])
	  self.ws.write(self.result, 11, task.project['opera'])
	  self.ws.write(self.result, 12, task.project['ohrana'])
	  self.ws.write(self.result, 13, task.project['electr'])
	  self.ws.write(self.result, 14, task.project['dol'])
	  self.ws.write(self.result, 15, task.project['teplo'])
	  self.ws.write(self.result, 16, task.project['shir'])
	  self.ws.write(self.result, 17, task.project['parkov'])
	  self.ws.write(self.result, 18, u'Cottage.ru')
	  self.ws.write_string(self.result, 19, task.project['url'])
	  self.ws.write(self.result, 20, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)	  
	  print 'Ready - '+str(self.result)	  
	  print('*'*50) 
	  self.result+= 1
	       

	  #if int(self.result) >= int(self.num)-3:
	       #self.stop()		    

     
bot = Gdedom_Zem(thread_number=7,network_try_limit=20000)
bot.load_proxylist('../../tipa.txt','text_file')
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






