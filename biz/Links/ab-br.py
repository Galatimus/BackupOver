#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
from datetime import datetime
import xlsxwriter

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab()
#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http') 



     



     

class Abbr(Spider):
     
     
     
     def prepare(self):
	  
	  self.workbook = xlsxwriter.Workbook(u'/home/oleg/Biz/Ready/Abbr_Готовый_бизнес.xlsx')
	  self.ws = self.workbook.add_worksheet(u'Abbr')
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
	  self.ws.write(0, 29, u"ДАТА_ДЕЙСТВИЯ_ПРЕДЛОЖЕНИЯ")
	  self.ws.write(0, 30, u"ДАТА ПАРСИНГА")
	  
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  for x in range(1,10):#897
	       yield Task ('post',url='http://www.ab-br.ru/buyer/index.php?page=%d'% x+'&sch_order=date&sch_sort_type=desc&sch_keywords=&sch_id=&sch_price_ot=&sch_price_ot_cur=&sch_price_do=&sch_price_do_cur=&sch_okup_ot=&sch_okup_do=&sch_region_str=&sch_activity_str=&view_type=&sch_store_time=&sch_valuta=rub&sch_sell=&sch_asc_rec=&sch_broker=',refresh_cache=True,network_try_count=100)
		
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@align="right"]/a[@title="подробнее"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,post = task.url,network_try_count=100)
	  
	  
	    
    
   
   
   
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//td[@class="td1"][contains(text(),"Место нахождения:")]/following-sibling::td').text().split(u'» ')[1]
	  except IndexError:
	       sub = ''
	
	  try:
	       tr = grab.doc.select(u'//td[@class="td1"][contains(text(),"Место нахождения:")]/following-sibling::td').text()
	       t1=0
	       for w1 in tr.split(u'» '):
		    t1+=1
		    if w1.find(u'р-н')>=0:
			 ter = tr.split(u'» ')[t1-1]
			 break
	       if w1.find(u'р-н')<0:
		    ter =''
	  except IndexError:
	       ter = ''
	  try:
	       if sub.find(u'Петербург')>=0:
		    punkt = sub
               elif sub.find(u'Москва')>=0:
                    punkt = sub
               else:
		    text= grab.doc.select(u'//td[@class="td1"][contains(text(),"Иная существенная информация о продаваемом бизнесе:")]/following-sibling::td').text().split(u'Продажа готового бизнеса: ')[1]
                    a = text.split('\n')
                    for x in range(0, len(a)):
                         p=(a[x].split(u' и ')[-2])
			 punkt= re.findall('\s(\S+)(?:\n|\Z)', p)[0].replace(u'окон','')
	  except IndexError:
	       punkt = ''
	  try:
	       tr2 = grab.doc.select(u'//span[@class="desc_f"][contains(text(),"Расположение")]/following::span[1]').text()
	       t3=0
	       for w3 in tr2.split(','):
		    t3+=1
		    if w3.find(u'ул.')>=0:
			 uliza = tr2.split(', ')[t3-1]
			 break
	       if w3.find(u'ул.')<0:
		    uliza =''
	  except IndexError:
	       uliza = ''
	  try:
	       ray = grab.doc.select(u'//td[@class="td1"][contains(text(),"Место нахождения:")]/following-sibling::td[contains(text(),"округ")]').text().split(u'» ')[0]
	       
	  except IndexError:
	       ray = ''
	       
	  dom=''     
	  try:
	       tr = grab.doc.select(u'//span[@class="desc_f"][contains(text(),"Расположение")]/following::span[1]').text()
	       t=0
	       for w in tr.split(','):
		    t+=1
		    if w.find(u'м.')>=0:
			 metro = tr.split(', ')[t-1]
			 break
	       if w.find(u'м.')<0:
		    metro =''
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.select(u'//td[@class="td1"][contains(text(),"Ежемесячная выручка от реализации - в среднем за год:")]/following-sibling::td').text()
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//td[@class="td1"][contains(text(),"Ежемесячная чистая прибыль:")]/following-sibling::td').text()
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//td[@class="td1"][contains(text(),"Цена:")]/following-sibling::td').text()
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//td[@class="td1"][contains(text(),"Сфера деятельности:")]/following-sibling::td').text()
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//td[@class="td1"][contains(text(),"Продается:")]/following-sibling::td').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       sotrud = grab.doc.select(u'//td[@class="td1"][contains(text(),"Количество работников:")]/following-sibling::td').number()
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//td[@class="td1"][contains(text(),"Балансовая стоимость основных средств:")]/following-sibling::td').text()
	  except IndexError:
	       dolgi = ''
	 
	       
	  try:
	       srok = grab.doc.select(u'//td[@class="td1"][contains(text(),"Cрок окупаемости бизнеса:")]/following-sibling::td').text()
	  except IndexError:
	       srok = ''
	  try:
	       srok_sush = grab.doc.select(u'//td[@class="td1"][contains(text(),"Срок существования бизнеса:")]/following-sibling::td').text()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//td[@class="td1"][contains(text(),"Причина продажи бизнеса:")]/following-sibling::td').text()
	  except IndexError:
	       prich = ''		    
       
	  try:
	       opis = grab.doc.select(u'//td[@class="td1"][contains(text(),"Иная существенная информация о продаваемом бизнесе:")]/following-sibling::td').text() 
	  except IndexError:
	       opis = ''
	  try:
	       phone = re.sub('[^\d\+]', u'',grab.doc.select(u'//span[@class="desc_f"][contains(text(),"Номер телефона")]/following::span[1]').text())
	  except IndexError:
	       phone = ''
       
	  
	  try:
	       data = grab.doc.select(u'//td[@class="td2"][contains(text(),"Предложение действует:")]').text().split(' - ')[1]
	  except IndexError:
	       data = ''
       
	  
   
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
	              'teritory': ter,
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
	  print  task.project['teritory']
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
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,4, task.project['teritory'])
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
	  self.ws.write(self.result,23, task.project['dolg'])
	  self.ws.write(self.result,22, task.project['srok1'])
	  self.ws.write(self.result,24, task.project['prichina'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'Ассоциация бизнес-брокеров России')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,29, task.project['dataraz'])
	   
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  #if self.result > 200:
	       #self.stop()
	  
	  
   

bot = Abbr(thread_number=3, network_try_limit=100000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print('Спим 1 сек...')
time.sleep(1)
print('Сохранение...')
bot.workbook.close()
print('Done!')
time.sleep(1)


    
	  
	  
	  