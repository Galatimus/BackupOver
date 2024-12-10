#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import base64
import json
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


 
oper = u'Продажа'
     


#while True:
     #print '********************************************',i+1,'/',dc,'*******************************************'
     

class Irr_Biz(Spider):
     
     
     
     def prepare(self):
	  for p in range(1,20):
	       try:
		    time.sleep(1)
		    g = Grab()
		    g.proxylist.load_file(path='../ivan.txt',proxy_type='http')
		    g.go('https://russia.irr.ru/business/business/')
		    print g.doc.code
		    if g.doc.code ==200:
			 self.num = re.sub('[^\d]', '',g.doc.select(u'//div[@class="listingStats"]').text().split('из ')[1])
			 self.pag = int(math.ceil(float(int(self.num))/float(30)))
			 print 'OK'
			 del g
			 break
	       except(GrabTimeoutError,GrabNetworkError,IndexError,KeyError,AttributeError,GrabConnectionError):
		    print g.config['proxy'],'Change proxy'
		    g.change_proxy()
		    del g
		    continue     
	  
	  print self.num,self.pag
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0008_00_Б_001-0024_IRR.xlsx')
	  self.ws = self.workbook.add_worksheet(u'Irr_Готовый_бизнес')
	  self.ws.write(0, 0,u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"ОРИЕНТИР")
	  self.ws.write(0, 3, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 4, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 5, u"УЛИЦА")
	  self.ws.write(0, 6, u"ДОМ")
	  self.ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
	  self.ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
	  self.ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
	  self.ws.write(0, 10, u"СФЕРА БИЗНЕСА")
	  self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 12, u"СПОСОБ РЕАЛИЗАЦИИ")
	  self.ws.write(0, 13, u"ЦЕНА ПРОДАЖИ")
	  self.ws.write(0, 14, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 15, u"СОСТОЯНИЕ")
	  self.ws.write(0, 16, u"ПРОДАВАЕМАЯ ДОЛЯ В БИЗНЕСЕ")
	  self.ws.write(0, 17, u"СРЕДНЕМЕСЯЧНЫЙ ОБОРОТ")
	  self.ws.write(0, 18, u"ЕЖЕМЕСЯЧНАЯ ЧИСТАЯ ПРИБЫЛЬ")
	  self.ws.write(0, 19, u"ЧИСЛО СОТРУДНИКОВ")
	  self.ws.write(0, 20, u"НАЛИЧИЕ ДОЛГОВЫХ ОБЯЗАТЕЛЬСТВ")
	  self.ws.write(0, 21, u"СРОК ОКУПАЕМОСТИ")
	  self.ws.write(0, 22, u"СРОК СУЩЕСТВОВАНИЯ БИЗНЕСА")
	  self.ws.write(0, 23, u"ОСНОВНЫЕ СРЕДСТВА")
	  self.ws.write(0, 24, u"ПРИЧИНА ПРОДАЖИ")
	  self.ws.write(0, 25, u"ОПИСАНИЕ")
	  self.ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 28, u"ТЕЛЕФОН ПРОДАВЦА")
	  self.ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 30, u"ДАТА ПАРСИНГА")
	  self.ws.write(0, 31, u"ССЫЛКА_НА_САЙТ")
	  self.ws.write(0, 32, u"ЗАГОЛОВОК")
	  self.ws.write(0, 33, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.conv = [(u' августа',u'.08.2018'), (u' июля',u'.07.2019'),
	       (u' мая',u'.05.2019'),(u' июня',u'.06.2019'),
	       (u' марта',u'.03.2019'),(u' апреля',u'.04.2019'),
	       (u' января',u'.01.2019'),(u' декабря',u'.12.2017'),
	       (u' сентября',u'.09.2017'),(u' ноября',u'.11.2018'),
	       (u' февраля',u'.02.2018'),(u' октября',u'.10.2018'), 
	       (u'сегодня,',datetime.today().strftime('%d.%m.%Y'))]	  
	  
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  #for x in range(1,self.pag+1):
	       #link = 'http://russia.irr.ru/business/business/page'+str(x)+'/'
	       #yield Task ('post',url=link.replace(u'page1/',''),refresh_cache=True,network_try_count=100)
          yield Task ('post',url='https://russia.irr.ru/business/business/',refresh_cache=True,network_try_count=100)
	  
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="listing__itemTitle"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	    
     def task_page(self,grab,task):
          try:
               pg = grab.doc.select(u'//li[contains(@class,"active")]/following-sibling::li[1]/a')
               u = grab.make_url_absolute(pg.attr('href'))
               yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
          except IndexError:
               print 'no_page'    
   
   
   
     def task_item(self, grab, task):
	  #pass tatarstan-resp
	
	  try:
	       sub =  grab.doc.rex_text('"address_region":"(.*?)"').decode("unicode_escape").replace(u'russia\/moskva-region\/',u'Москва').replace(u'russia\/tatarstan-resp\/',u'Татарстан')	     
	  except (IndexError,TypeError,ValueError):
	       sub = ''
	  except KeyError:
	       sub = u'Санкт-Петербург'
	  try:
	       punkt = grab.doc.rex_text('"address_city":"(.*?)"').decode("unicode_escape")
	  except (IndexError,TypeError,ValueError,KeyError):
	       punkt = ''
	  try:
	       uliza = grab.doc.select(u'//li[contains(text(),"АО:")]').text().split(': ')[1]
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//li[contains(text(),"Район города:")]').text().split(': ')[1]
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro = grab.doc.rex_text('"metro":"(.*?)"').decode("unicode_escape")
	  except (IndexError,TypeError,ValueError,KeyError):
	       metro = ''
	  try:
	       metro_min = grab.doc.select(u'//li[contains(text(),"Срок существования бизнеса, лет:")]').text().split(': ')[1]
	  except IndexError:
	       metro_min = ''
	  try:
	       metro_kak = grab.doc.select(u'//li[contains(text(),"Доля в бизнесе, %:")]').text().split(': ')[1]
	  except IndexError:
	       metro_kak = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select('//div[@class="productPage__price js-contentPrice"]').text()
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//h1[@class="productPage__title js-productPageTitle"]').text().replace(u'Продаю ','').replace(u'Сдаю ','')
	  except IndexError:
	       sfera = ''
	       
	  try:
	       et2 = grab.doc.select(u'//li[contains(text(),"этажность")]').number()
	  except IndexError:
	       et2 = ''
	       
	  try:
	       sposob = grab.doc.select(u'//li[contains(text(),"Тип бизнеса:")]').text().split(': ')[1]
	  except IndexError:
	       sposob = ''
	       
	  try:
	       zag = grab.doc.select(u'//h1').text() 
	  except IndexError:
	       zag = ''	 
	       
	  #try:
	       
	       
	       #url_ph = grab.doc.select(u'//a[@class="js-sellerSiteLink"]').attr('href')
	       #g2 = grab.clone(timeout=2000, connect_timeout=2000)
	       #g2.go(url_ph)
	       #sos = g2.doc.select(u'//i[@class="icon icon_globeEmpty proAccountHead__icon"]/following-sibling::text()').text()
	  #except IndexError:
	  sos = ''
       
	  try:
	       opis = grab.doc.select(u'//h4[contains(text(),"Описание")]/following-sibling::p').text() 
	  except IndexError:
	       opis = ''
	  try:
	       phone = re.sub('[^\d]', '',base64.b64decode(grab.doc.select('//input[@name="phoneBase64"]').attr('value')))
	  except IndexError:
	       phone = ''
       
	  
	  try:
	       data = grab.doc.rex_text(u'date_create":"(.*?)"}').split(' ')[0].replace('-','.')
	  except IndexError:
	       data = ''
	       
	  try:
	       d1 = grab.doc.select(u'//div[@class="productPage__createDate"]').text()
               data1 = reduce(lambda d1, r: d1.replace(r[0], r[1]), self.conv, d1).replace(u'Размещено ','')
          except IndexError:
	       data1 = '' 	       
       
	  
   
	  projects = {'url': sos,
                      'url1':task.url,
                      'sub': sub,
                      #'rayon': ray,
                      'punkt': punkt,
                      'ulica': uliza,
                      'dom': dom,
                      'metro_min': metro_min,
                      'metro': metro,
                      'price': price,
                      'metro_kak': metro_kak,
                      'sfera': sfera,
                      'ets': et2,
	              'zag': zag,
                      'sposob': sposob,
                      'opis': opis,
                      'phone': phone,
	              'dataraz1': data1[:10],
                      'dataraz': data}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	
	  print('*'*100)
	  print  task.project['sub']
	  #print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['metro']
	  print  task.project['metro_min']
	  print  task.project['price']
	  print  task.project['metro_kak']
	  print  task.project['sfera']
	  print  task.project['ets']
	  print  task.project['sposob']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['url1']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,32, task.project['zag'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,1, task.project['ulica'])
	  self.ws.write(self.result,4, task.project['dom'])
	  self.ws.write(self.result,7, task.project['metro'])
	  self.ws.write(self.result,22, task.project['metro_min'])
	  self.ws.write(self.result,11, oper)
	  self.ws.write(self.result,16, task.project['metro_kak'])
	  self.ws.write(self.result,10, task.project['sfera'])
	  self.ws.write(self.result,12, task.project['sposob'])
	  self.ws.write(self.result,13, task.project['price'])
	  self.ws.write(self.result,14, task.project['ets'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'Из рук в руки')
	  self.ws.write_string(self.result,27, task.project['url1'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,29, task.project['dataraz'])
	  self.ws.write_string(self.result,31, task.project['url'])
	  self.ws.write(self.result, 33, task.project['dataraz1'])
	  
	 
	 
	  
   
	  print('*'*100)
	  print 'Ready - '+str(self.result)+'/'+str(self.num)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print '***',i+1,'/',dc,'***'
	  print oper
	  print('*'*100)
	  self.result+= 1
	  
	  #if self.result > 30:
	       #self.stop()	       
   

bot = Irr_Biz(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../ivan.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(3)
bot.workbook.close()
print('Done')
time.sleep(5)
os.system("/home/oleg/pars/biz/ba.py")
