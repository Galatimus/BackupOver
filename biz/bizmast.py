#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
from datetime import datetime
import xlsxwriter
import os
from sub import conv
from mesto import ul
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#lin = open('Altera.txt').read().splitlines()


class alterainvest(Spider):
     
     
     
     def prepare(self):
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0100_00_Б_001-0221_BIZMAS.xlsx')
	  self.ws = self.workbook.add_worksheet(u'bizmast')
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
	  self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 30, u"ДАТА ПАРСИНГА")
	  self.ws.write(0, 31, u"МЕСТОПОЛОЖЕНИЕ")
	  self.ws.write(0, 32, u"ЗАГОЛОВОК")
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  for x in range(1,372):#131
               yield Task ('post',url='http://www.bizmast.ru/catalog/?PAGEN_1=%d'%x,refresh_cache=True,network_try_count=100)	  
	


     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="item"]/div[2]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       if 'prodannye-obekty' not in ur:
	            yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
   
     def task_item(self, grab, task):
	  try:
	       dt = grab.doc.select(u'//th[contains(text(),"Город")]/following-sibling::td').text()
               sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	  except IndexError:
	       sub = ''
	
	  try:
	       ray = grab.doc.select(u'//th[contains(text(),"Административный округ")]/following-sibling::td/a').text()
	  except IndexError:
	       ray = ''
	  try:
	       punkt = grab.doc.select(u'//th[contains(text(),"Город")]/following-sibling::td').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//th[contains(text(),"Ориентировочное месторасположение")]/following-sibling::td').text()
	  except IndexError:
	       ter =''	       
	  try:
	       uliza= grab.doc.select(u'//th[contains(text(),"Средства производства")]/following-sibling::td').text()
	  except (IndexError,UnboundLocalError):
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//th[contains(text(),"Причина продажи бизнеса")]/following-sibling::td').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro = grab.doc.select(u'//th[contains(text(),"Станция метро")]/following-sibling::td/a').text()
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.select(u'//th[contains(text(),"Среднемесячные обороты")]/following-sibling::td').text()
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//th[contains(text(),"Ежемесячная прибыль")]/following-sibling::td').text()
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//th[contains(text(),"Фиксированная стоимость бизнеса")]/following-sibling::td').text()
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//th[contains(text(),"Отрасль")]/following-sibling::td/a').text()
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//div[contains(text(),"Доля:")]/following-sibling::div').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       sotrud = grab.doc.select(u'//th[contains(text(),"Количество сотрудников")]/following-sibling::td').number()
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//div[contains(text(),"Раздел:")]/following-sibling::div').text()
	  except IndexError:
	       dolgi = ''
	 
	       
	  try:
	       srok = grab.doc.select(u'//p[contains(text(),"Окупаемость")]/span').text()
	  except IndexError:
	       srok = ''
	  try:
	       srok_sush = grab.doc.select(u'//th[contains(text(),"Срок существования бизнеса")]/following-sibling::td').number()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//th[contains(text(),"Недвижимость")]/following-sibling::td').text()
	  except IndexError:
	       prich = ''		    
       
	  try:
	       opis = grab.doc.select(u'//td[@itemprop="description"]').text() 
	  except IndexError:
	       opis = ''
	  try:
	       phone = re.sub('[^\d\+]', u'',grab.doc.select(u'//th[contains(text(),"Телефон консультанта")]/following-sibling::td').text())
	  except IndexError:
	       phone = ''
       
	  
	  try:
	       data = grab.doc.select(u'//title').text()
	  except IndexError:
	       data = ''
       
	  
   
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'ulica': uliza,
	              'terit':ter, 
                      'dom': dom,
                      'oborot': oborot,
                      'metro': metro,
                      'price': price,
                      'pribil': pribil,
                      'sfera': sfera,
                      'dolya': dolya,
                      'sotrud': sotrud,
                      'dolg': dolgi,
                      'srok': srok,
                      'srok1': srok_sush,
                      'prichina': prich,
                      'opis': opis,
                      'phone': phone,
                      'dataraz': data}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['terit']
	  print  task.project['ulica']
	  print  task.project['dom']
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
	  print  task.project['prichina']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,2, task.project['terit'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,23, task.project['ulica'])
	  self.ws.write(self.result,24, task.project['dom'])
	  self.ws.write(self.result,7, task.project['metro'])
	  self.ws.write(self.result,17, task.project['oborot'])
	  self.ws.write(self.result,11, u'Продажа')
	  self.ws.write(self.result,18, task.project['pribil'])
	  self.ws.write(self.result,10, task.project['sfera'])
	  self.ws.write(self.result,19, task.project['sotrud'])
	  self.ws.write(self.result,13, task.project['price'])
	  self.ws.write(self.result,16, task.project['dolya'])
	  self.ws.write(self.result,21, task.project['srok'])
	  self.ws.write(self.result,12, task.project['dolg'])
	  self.ws.write(self.result,22, task.project['srok1'])
	  self.ws.write(self.result,15, task.project['prichina'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'Первый Брокер')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,32, task.project['dataraz'])
	 
	 
	 
	  
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print '***',i+1,'/',dc,'***'
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  #if self.result > 500:
	       #self.stop()
   

bot = alterainvest(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
bot.workbook.close()
print('Done')
time.sleep(5)
os.system("/home/oleg/pars/biz/delomart.py")
 