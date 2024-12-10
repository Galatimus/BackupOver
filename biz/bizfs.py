#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
import os
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



 



class BFS(Spider):
     
     
     
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'0001-0002_00_Б_001-0055_BFSALE.xlsx')
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
	  self.ws.write(0, 30, u"ДАТА ПАРСИНГА")
	  self.ws.write(0, 31, u"ССЫЛКА_НА_САЙТ")
	  self.ws.write(0, 32, u"ЗАГОЛОВОК")
	  
	  self.result= 1

       
       
	 

     def task_generator(self):
	  yield Task ('next',url='https://businessesforsale.ru/',refresh_cache=True,network_try_count=100)
	  
     def task_next(self,grab,task):
	  for el in grab.doc.select(u'//div[@class="popularBizStates"]/ul/li/a'):
	       urr = grab.make_url_absolute(el.attr('href')) +'kupit-biznes/'
	       #print urr
	       yield Task('post', url=urr,refresh_cache=True,network_try_count=100)
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//div[@id="resultRowContainer_beforeAd1"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)
	  yield Task('page', grab=grab,refresh_cache=True,network_try_count=100)
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//a[@class="bbsPager_next"]')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       print 'no_page'
   
   
     def task_item(self, grab, task):
	  #pass
	
	  try:
	       sub = grab.doc.select(u'//h2').text().split(', ')[1]
	  except IndexError:
	       sub = ''
	       
	  ray = ''
	  try:
	       if sub == u'Москва':
		    punkt = u'Москва'
	       elif sub == u'Санкт-Петербург':
		    punkt = u'Санкт-Петербург'
	       else:
		    punkt = grab.doc.select(u'//h2').text().split(', ')[2]
	  except IndexError:
	       punkt = ''
	  try:
	       uliza = grab.doc.select(u'//h2').text().split(', ')[3]
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//h2').text().split(', ')[4]
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro =''
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.rex_text(u'Среднемесячные обороты:(.*?).')
	  except IndexError:
	       oborot = ''
	  try:
	       try:
		    pribil = grab.doc.rex_text(u'Чистая прибыль(.*?)<')
	       except IndexError:
		    pribil = grab.doc.select(u'//th[contains(text(),"Прибыль")]/following::td[1]').text()
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//span[@class="title"][contains(text(),"Цена:")]/following-sibling::b').text()
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//h4/a[3]').text()
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//span[@class="desc_f"][contains(text(),"Доля бизнеса")]/following::span[1]').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       try:
		    sotrud = grab.doc.rex_text(u'Количество работников:(.*?)<')
	       except IndexError:
		    sotrud = grab.doc.select(u'//th[contains(text(),"Персонал")]/following::td[1]').text()
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//span[@class="desc_f"][contains(text(),"Суммы задолженностей")]/following::span[1]').text()
	  except IndexError:
	       dolgi = ''
	 
	       
	  try:
	       srok = grab.doc.rex_text(u'Окупаемость:(.*?)<')
	  except IndexError:
	       srok = ''
	  try:
	       try:
		    srok_sush = grab.doc.rex_text(u'Возраст бизнеса:(.*?)<')
	       except IndexError:
		    srok_sush = grab.doc.select(u'//th[contains(text(),"Возраст (годы)")]/following::td[1]').text()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//b[contains(text(),"Причины продажи:")]/following-sibling::text()').text()
	  except IndexError:
	       prich = ''
	  try:
	       sred = grab.doc.select(u'//b[contains(text(),"Активы:")]/following-sibling::text()').text()
	  except IndexError:
	       sred = ''    
       
	  try:
	       opis = grab.doc.select(u'//div[@id="apContainerLeft"]/p[4]').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       zag = grab.doc.select(u'//h1[@id="apAdTitle"]').text() 
	  except IndexError:
	       zag = ''		    
	  try:
	       web = grab.doc.select(u'//li[@class="website"]/a').attr('href') 
	  except IndexError:
	       web = ''   
	  try:
	       phone = re.sub('[^\d\+\,]', u'',grab.doc.select(u'//p[@class="ap_listedByName"]/following-sibling::text()').text())
	  except IndexError:
	       phone = ''
	       
	  data = ''

       
	  
   
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'ulica': uliza,
                      'dom': dom[1:],
                      'oborot': oborot,
                      'metro': metro,
                      'price': price,
                      'pribil': pribil,
                      'sfera': sfera,
                      'dolya': dolya,
                      'sotrud': sotrud,
                      'dolg': dolgi,
                      'srok': srok,
                      'zag': zag,
                      'srok1': srok_sush,
                      'prichina': prich,
                      'sredstva': sred,
                      'opis': opis,
                      'webs': web,
                      'phone': phone,
                      'dataraz': data}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
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
	  print  task.project['sredstva']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  print  task.project['webs']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,5, task.project['ulica'])
	  self.ws.write(self.result,6, task.project['dom'])
	  self.ws.write(self.result,7, task.project['metro'])
	  self.ws.write(self.result,17, task.project['oborot'])
	  self.ws.write(self.result,11, u'Продажа')
	  self.ws.write(self.result,18, task.project['pribil'])
	  self.ws.write(self.result,10, task.project['sfera'])
	  self.ws.write(self.result,19, task.project['sotrud'])
	  self.ws.write(self.result,13, task.project['price'])
	  self.ws.write(self.result,16, task.project['dolya'])
	  self.ws.write(self.result,21, task.project['srok'])
	  self.ws.write(self.result,20, task.project['dolg'])
	  self.ws.write(self.result,22, task.project['srok1'])
	  self.ws.write(self.result,23, task.project['sredstva'])
	  self.ws.write(self.result,24, task.project['prichina'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'BusinessesForSale.ru')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write_string(self.result,31, task.project['webs'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,29, task.project['dataraz'])
	  self.ws.write(self.result,32, task.project['zag'])
	 
	 
	 
	  
   
	  print('*'*50)
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*50)
	  self.result+= 1


bot = BFS(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=500)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')    
command = 'mount -a'    
p = os.system('echo %s|sudo -S %s' % ('1122', command))
print p
time.sleep(2)
bot.workbook.close()
print('Done!')

