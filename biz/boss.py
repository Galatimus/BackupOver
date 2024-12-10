#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
from datetime import datetime
import xlsxwriter
import math
import os
import random
from grab import Grab
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



class alterainvest(Spider):
     
     
     
     def prepare(self):
	  for p in range(1,50):
	       try:
		    #time.sleep(1)
		    g = Grab()
		    g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
		    g.go('https://www.beboss.ru/business/search/cntry-ru')
		    print g.doc.code    
		    self.num = re.sub('[^\d]', '',g.doc.select(u'//p[@class="rb-filter-result__htext"]').text())
		    self.pag = int(math.ceil(float(int(self.num))/float(10)))
		    print 'OK'
		    del g
		    break
	       except(GrabTimeoutError,GrabNetworkError,IndexError,KeyError,AttributeError,GrabConnectionError):
		    print g.config['proxy'],'Change proxy'
		    g.change_proxy()
		    del g
		    continue     
	  else:
	       self.pag = 1
	  print self.num,self.pag  
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0100_00_Б_001-0206_BEBOSS.xlsx')
	  self.ws = self.workbook.add_worksheet()
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
	  self.ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 31, u"ДАТА ПАРСИНГА")
	  self.ws.write(0, 32, u"МЕСТОПОЛОЖЕНИЕ")
	  self.ws.write(0, 33, u"ЗАГОЛОВОК")
	  self.ws.write(0, 34, u"КОНТАКТНОЕ_ЛИЦО")
	  self.conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
		    (u' мая ',u'.05.'),(u' июня ',u'.06.'),
		    (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
		    (u' января ',u'.01.'),(u' декабря ',u'.12.'),
		    (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
		    (u' февраля ',u'.02.'),(u' октября ',u'.10.')]
		        
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  for x in range(1,self.pag+1):
	       yield Task ('post',url='https://www.beboss.ru/business/search/cntry-ru?page=%d'%x,refresh_cache=True,network_try_count=100)	  

     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="obj__right"]/a[contains(text(),"Подробнее")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
   
     def task_item(self, grab, task):
	  try:
	       orent = grab.doc.select(u'//div[@class="publ-address"]/p').text()
	  except IndexError:
	       orent = ''
	  try:
	       metro = grab.doc.select(u'//title').text().split(' | ')[1]
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.select(u'//title').text().split(' | ')[0]
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//div[contains(text(),"Доля к продаже")]/following-sibling::div').text()
	  except IndexError:
	       pribil = ''
	  try:
	       price = grab.doc.select(u'//h2[@class="publ-price__num"]').text()[:-1]+'р.'
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//div[contains(text(),"Среднемесячная выручка")]/following-sibling::div').text()[:-1]+'р.'
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//div[contains(text(),"Возраст бизнеса")]/following-sibling::div').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       sotrud = grab.doc.select(u'//div[contains(text(),"Количество сотрудников")]/following-sibling::div').number()
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//h2[contains(text(),"Основные виды продукции, услуг")]/following-sibling::p').text()
	  except IndexError:
	       dolgi = ''
	  try:
	       srok = grab.doc.select(u'//span[contains(text(),"Размещено")]/following-sibling::span').text()
	  except IndexError:
	       srok = ''
	  try:
	       srok_sush = grab.doc.select(u'//span[contains(text(),"Обновлено")]/following-sibling::span').text()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//th[contains(text(),"Недвижимость")]/following-sibling::td').text()
	  except IndexError:
	       prich = ''    
	  try:
	       opis = grab.doc.select(u'//p[@itemprop="description"]').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       mat = grab.doc.select(u'//span[@class="bk-agent__name"]').text()
	  except IndexError:
	       mat = ''	       
  
	  try:
	       data = grab.doc.select(u'//h1').text()
	  except IndexError:
	       data = ''
       
	  srok_sush = reduce(lambda srok_sush, r: srok_sush.replace(r[0], r[1]), self.conv, srok_sush)
	  srok = reduce(lambda srok, r: srok.replace(r[0], r[1]), self.conv, srok)
	  
	  clearText = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", mat)
	  clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText)	  
   
	  projects = {'url': task.url,
                      'orentir': orent,                      
                     'oborot': oborot,
                      'metro': metro,
                      'price': price,
                      'pribil': pribil,
                      'sfera': sfera,
                      'dolya': dolya,
                      'sotrud': sotrud,
	              'mat': clearText,
                      'dolg': dolgi,
                      'srok': srok,
                      'srok1': srok_sush,
                      'prichina': prich,
                      'opis': opis,
                      'phone': random.choice(list(open('../phone.txt').read().splitlines())),
                      'dataraz': data}
	  try:
	       link = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode='+orent
	       yield Task('adres',url=link,project=projects,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       yield Task('adres',grab=grab,project=projects)
	       
	       
     def task_adres(self, grab, task):
     
	  try:   
	       sub= grab.doc.rex_text(u'AdministrativeAreaName":"(.*?)"')
	  except IndexError:
	       sub = 'Москва'
	       
	  try:
	       ray = grab.doc.rex_text(u'SubAdministrativeAreaName":"(.*?)"')
	  except IndexError:
	       ray = ''	       
	  try:   
	       punkt= grab.doc.rex_text(u'LocalityName":"(.*?)"')
	  except IndexError:
	       punkt = ''
	  try:
	       ter=  grab.doc.rex_text(u'DependentLocalityName":"(.*?)"')
	  except IndexError:
	       ter =''
	  try:
	       uliza=grab.doc.rex_text(u'ThoroughfareName":"(.*?)"')
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.rex_text(u'PremiseNumber":"(.*?)"')
	  except IndexError:
	       dom = ''
     
	  project2 ={'punkt':punkt,
	             'sub': sub,
	             'rayon': ray,
	             'teritor': ter,
	             'ulica':uliza,
	             'dom':dom}   
   
	  yield Task('write',project=task.project,proj=project2,grab=grab)
   
     def task_write(self,grab,task):
	
	  print('*'*100)
	  print  task.proj['sub']
	  print  task.proj['rayon']
	  print  task.proj['punkt']
	  print  task.proj['teritor']
	  print  task.proj['ulica']
	  print  task.proj['dom']
	  print  task.project['metro']
	  print  task.project['oborot']
	  print  task.project['price']
	  print  task.project['pribil']
	  print  task.project['sfera']
	  print  task.project['dolya']
	  print  task.project['sotrud']
	  print  task.project['dolg']
	  print  task.project['srok']
	  print  task.project['srok1']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  print  task.project['orentir']
	  print  task.project['mat']
	  
	  
	  self.ws.write(self.result,0, task.proj['sub'])
	  self.ws.write(self.result,4, task.proj['teritor'])
	  self.ws.write(self.result,1, task.proj['rayon'])
	  self.ws.write(self.result,3, task.proj['punkt'])
	  self.ws.write(self.result,5, task.proj['ulica'])
	  self.ws.write(self.result,6, task.proj['dom'])
	  self.ws.write(self.result,10, task.project['metro'])
	  self.ws.write(self.result,12, task.project['oborot'])
	  self.ws.write(self.result,11, u'Продажа')
	  self.ws.write(self.result,16, task.project['pribil'])
	  self.ws.write(self.result,17, task.project['sfera'])
	  self.ws.write(self.result,19, task.project['sotrud'])
	  self.ws.write(self.result,13, task.project['price'])
	  self.ws.write(self.result,22, task.project['dolya'])
	  self.ws.write(self.result,29, task.project['srok'])
	  self.ws.write(self.result,23, task.project['dolg'])
	  self.ws.write(self.result,30, task.project['srok1'])
	  self.ws.write(self.result,33, task.project['dataraz'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'БИБОСС')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,31, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,32, task.project['orentir'])
	  self.ws.write_string(self.result, 34, task.project['mat'])
	 
	 
	 
	  
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)+'/'+self.num
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*100)
	  self.result+= 1
	  
	  #if self.result > 500:
	       #self.stop()
   

bot = alterainvest(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
time.sleep(2)
bot.workbook.close()
print('Done')
time.sleep(5)
os.system("/home/oleg/pars/biz/zona.py")

 