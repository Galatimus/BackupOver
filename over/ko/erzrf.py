#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import math
import os
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)






     

class Dmir_Kv(Spider):
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'erzrf.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
	  self.ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
	  self.ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
	  self.ws.write(0, 10, u"ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 12, u"СТОИМОСТЬ")
	  self.ws.write(0, 13, u"ЦЕНА_М2")
	  self.ws.write(0, 14, u"КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 15, u"ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 16, u"ПЛОЩАДЬ_ЖИЛАЯ")
	  self.ws.write(0, 17, u"ПЛОЩАДЬ_КУХНИ")
	  self.ws.write(0, 18, u"ПЛОЩАДЬ_КОМНАТ")
	  self.ws.write(0, 19, u"ЭТАЖ")
	  self.ws.write(0, 20, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 21, u"МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 22, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 23, u"РАСПОЛОЖЕНИЕ_КОМНАТ")
	  self.ws.write(0, 24, u"БАЛКОН")
	  self.ws.write(0, 25, u"ЛОДЖИЯ")
	  self.ws.write(0, 26, u"САНУЗЕЛ")
	  self.ws.write(0, 27, u"ОКНА")
	  self.ws.write(0, 28, u"СОСТОЯНИЕ")
	  self.ws.write(0, 29, u"ВЫСОТА_ПОТОЛКОВ")
	  self.ws.write(0, 30, u"ЛИФТ")
	  self.ws.write(0, 31, u"РЫНОК")
	  self.ws.write(0, 32, u"КОНСЬЕРЖ")
	  self.ws.write(0, 33, u"ОПИСАНИЕ")
	  self.ws.write(0, 34, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 35, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 36, u"ТЕЛЕФОН")
	  self.ws.write(0, 37, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 38, u"КОМПАНИЯ")
	  self.ws.write(0, 39, u"ДАТА_РАЗМЕЩЕНИЯ_ОБЪЯВЛЕНИЯ")
	  self.ws.write(0, 40, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 41, u"ДАТА_ОБНОВЛЕНИЯ_ЦЕНЫ")
	  self.ws.write(0, 42, u"ДАТА_ИЗМЕНЕНИЯ_ЦЕНЫ")	       
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
          yield Task ('post',url='https://erzrf.ru/novostroyki?viewMode=list&scrollTo=viewMode&regionKey=143443001&region=moskva&costType=1&sortType=rating',refresh_cache=True,network_try_count=100)
   
   
       
     def task_post(self,grab,task):
	  
	  for elem in grab.doc.select('//h3/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       print ur
	       #yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)     
	    
    
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//li[@class="page-item ng-star-inserted active"]/following-sibling::li[1]/a')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('next',url= u,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       print('*'*100)
	       print '!!!','NO PAGE NEXT','!!!'
	       print('*'*100)   
   
   
     def task_item(self, grab, task):
	  #pass
	
	  try:
	       ray =  grab.doc.rex_text(u'в (.*?)районе</a></li></ul>').replace(u'ком',u'кий') 
	     
	  except DataNotFound:
	       ray = ''
	  try:
	       #if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
		    #punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
	       #else:    
	       punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[1]
	  except IndexError:
	       punkt = ''
	  try:
	       if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
		    uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
	       else:    
		    uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[2]
	  except IndexError:
	       uliza = ''
	  try:
	       if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
		    dom = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[4]
	       else:    
		    dom = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro = grab.doc.select(u'//li[@class="metro"]/b[1]').text()
	  except IndexError:
	       metro = ''
	  try:
	       metro_min = grab.doc.select(u'//li[@class="metro"]/b[2]').number()
	  except IndexError:
	       metro_min = ''
	  try:
	       metro_kak = grab.doc.select(u'//li[@class="metro"]/b[3]').text()
	  except IndexError:
	       metro_kak = ''
	  try:
	       tip_ob = grab.doc.select(u'//li[@id="flat_wrap"]/a').text().replace(u"Информация по комнате",u"Комната").replace(u"Информация по квартире",u"Квартира").replace(u"Информация по объекту",u"Доля в квартире")
	  except IndexError:
	       tip_ob = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select('//span[@id="price_offer"]').text()
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       price_m = grab.doc.select('//li[@class="meterprice"]/b[1]').text()
	  except IndexError:
	       price_m = ''
	  try:
	       kol_komnat = grab.doc.select(u'//ul[@id="flat_data"]/li[1][contains(text(),"комнат")]/b').number()
	  except IndexError:
	       kol_komnat = ''
	  try:
	       et = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"этаж")]').number()
	  except IndexError:
	       et = ''
	       
	  try:
	       et2 = grab.doc.select(u'//li[contains(text(),"этажность")]').number()
	  except IndexError:
	       et2 = ''
	       
	  try:
	       god = grab.doc.select(u'//li[contains(text(),"год постройки")]/b').number()
	  except IndexError:
	       god = ''
	       
	  try:
	       mat = grab.doc.select(u'//li[contains(text(),"дом")]/b').text()
	  except IndexError:
	       mat = ''
	       
	  try:
	       pot = grab.doc.select(u'//li[contains(text(),"потолки")]/b').text()
	  except IndexError:
	       pot = ''
	       
	  try:
	       sos = grab.doc.select(u'//li[contains(text(),"состояние")]/b').text()
	  except IndexError:
	       sos = ''
	  try:
	       bal = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(), "балкон")]/b').number()
	  except IndexError:
	       bal = ''
	  try:
	       logy = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(), "лоджия")]/b').number()
	  except IndexError:
	       logy = ''
	  try:
	       plosh_ob = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"общая площадь")]/b').text()
	  except IndexError:
	       plosh_ob = ''
	  try:
	       plosh_g = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"жилая площадь")]/b').text()
	  except IndexError:
	       plosh_g = ''
	  try:
	       plosh_k = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"площадь кухни")]/b').text()
	  except IndexError:
	       plosh_k = ''
	  try:
	       plosh_kom = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"площадь комнат")]/b').text()
	  except IndexError:
	       plosh_kom = ''               
	  try:
	       san_u = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(), "санузл")]/b').number()
	  except IndexError:
	       san_u =''
	  try:
	       okna = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(), "окна")]/b').text()
	  except IndexError:
	       okna =''
	  try:
	       lift = grab.doc.select(u'//li[contains(text(),"лифт")]').number()
	  except IndexError:
	       lift =''
	  try:
	       kons = re.sub(u'^.*(?=консьерж)','', grab.doc.select(u'//*[contains(text(), "консьерж")]').text())[:8].replace(u'консьерж',u'есть')
	  except IndexError:
	       kons = ''
	  try:
	       opis = grab.doc.select(u'//div[@class="mb20 objectDesc"]').text() 
	  except IndexError:
	       opis = ''
	  try:
	       ph = grab.doc.rex_text('<div class="phone">(.*?)</div>').replace('<br>',',')
	       phone = re.sub('[^\d\,]', u'',ph)
	  except IndexError:
	       phone = ''
       
	  try:
	       lico = grab.doc.select(u'//dt[contains(text(),"Разместил")]/following-sibling::dd/span').text()
	  except IndexError:
	       lico = ''
       
	  try:
	       com = grab.doc.select(u'//dt[contains(text(),"Компания")]/following-sibling::dd/span').text()
	  except IndexError:
	       com = ''
	  try:
	       data = grab.doc.select(u'//dt[contains(text(),"Размещено")]/following::span[1]').text()
	  except IndexError:
	       data = ''
       
	  try:
	       data1 =  grab.doc.select(u'//span[@class="fz_small"]').text().split(', ')[1]
	  except IndexError:
	       data1 = ''

	  try:
	       data2 =  grab.doc.select(u'//li[@id="history_wrap"]/table').text()
	  except IndexError:
	       data2 = ''
   
	  projects = {'url': task.url,
                      'sub': self.sub,
                      'rayon': ray,
                      'punkt': punkt[1:],
                      'ulica': uliza[1:].replace(u'м.',u'улица'),
                      'dom': dom[1:],
                      'metro_min': metro_min,
                      'metro': metro,
                      'price': price,
                      'price_m': price_m,
                      'comnat': kol_komnat,
                      'metro_kak': metro_kak,
                      'object':tip_ob,
                      'ploshad1': plosh_ob,
                      'ploshad2': plosh_g,
                      'ploshad3': plosh_k,
                      'ploshad4': plosh_kom,
                      'et': et,
                      'ets': et2,
                      'god': god,
                      'balkon':bal,
                      'logia':logy,
                      'mat': mat,
                      'potolok': pot,
                      'sost': sos,
                      'usel': san_u,
                      'okna':okna,
                      'lift': lift,
                      'kons': kons,
                      'opis': opis,
                      'phone': phone,
                      'lico':lico,
                      'company':com,
                      'dataraz': data,
                      'data1': data1,
                      'data2': data2
                         }
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['metro_min']
	  print  task.project['metro']
	  print  task.project['object']
	  print  task.project['price']
	  print  task.project['price_m']
	  print  task.project['comnat']
	  print  task.project['metro_kak']
	  print  task.project['ploshad1']
	  print  task.project['ploshad2']
	  print  task.project['ploshad3']
	  print  task.project['ploshad4']
	  print  task.project['et']
	  print  task.project['ets']
	  print  task.project['god']
	  print  task.project['balkon']
	  print  task.project['logia']
	  print  task.project['mat']
	  print  task.project['potolok']
	  print  task.project['sost']
	  print  task.project['usel']
	  print  task.project['okna']
	  print  task.project['lift']
	  print  task.project['kons']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['dataraz']
	  print  task.project['data1']
	  print  task.project['data2']
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,2, task.project['punkt'])
	  self.ws.write(self.result,4, task.project['ulica'])
	  self.ws.write(self.result,5, task.project['dom'])
	  self.ws.write(self.result,8, task.project['metro_min'])
	  self.ws.write(self.result,7, task.project['metro'])
	  self.ws.write(self.result,11, oper)
	  self.ws.write(self.result,12, task.project['price'])
	  self.ws.write(self.result,9, task.project['metro_kak'])
	  self.ws.write(self.result,10, task.project['object'])
	  #self.ws.write(self.result,12, task.project['ploshad1'])
	  self.ws.write(self.result,13, task.project['price_m'])
	  self.ws.write(self.result,14, task.project['comnat'])
	  self.ws.write(self.result,15, task.project['ploshad1'])
	  self.ws.write(self.result,16, task.project['ploshad2'])
	  self.ws.write(self.result,17, task.project['ploshad3'])
	  self.ws.write(self.result,18, task.project['ploshad4'])
	  self.ws.write(self.result,19, task.project['et'])
	  self.ws.write(self.result,20, task.project['ets'])
	  self.ws.write(self.result,21, task.project['mat'])
	  self.ws.write(self.result,22, task.project['god'])
	  self.ws.write(self.result,24, task.project['balkon'])
	  self.ws.write(self.result,25, task.project['logia'])
	  self.ws.write(self.result,26, task.project['usel'])
	  self.ws.write(self.result,27, task.project['okna'])
	  self.ws.write(self.result,28, task.project['sost'])
	  self.ws.write(self.result,29, task.project['potolok'])
	  self.ws.write(self.result,30, task.project['lift'])
	  self.ws.write(self.result,32, task.project['kons'])
	  self.ws.write(self.result,33, task.project['opis'])
	  self.ws.write(self.result,34, u'Недвижимость и цены')
	  self.ws.write_string(self.result,35, task.project['url'])
	  self.ws.write(self.result,36, task.project['phone'])
	  self.ws.write(self.result,37, task.project['lico'])
	  self.ws.write(self.result,38, task.project['company'])
	  self.ws.write(self.result,39, task.project['dataraz'])
	  self.ws.write(self.result,40, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,41, task.project['data1'])
	  self.ws.write(self.result,42, task.project['data2'])
	 
	 
	 
	  
   
	  print('*'*100)
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*100)
	  self.result+= 1
	       

   

bot = Dmir_Kv(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=100)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
time.sleep(1)
bot.workbook.close()
#workbook.close()
print('Done!')

	  
	  
	  