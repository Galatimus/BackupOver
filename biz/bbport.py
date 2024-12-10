#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import re
#import requests
from grab import Grab
from datetime import datetime,timedelta
import xlsxwriter
from sub import conv
import random
import os

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)





     

class Bae(Spider):
     
     
     
     def prepare(self):
	  
	  for p in range(1,5):
	       try:
		    #time.sleep(1)
		    g = Grab()
		    g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
		    g.go('https://bbport.ru/business/?vt=1&region=1&city=-1&sp=1')
		    print g.doc.code
		    if g.doc.code ==200:
			 self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="pagination__btn"]/following::li[1]/a').text())
			 print 'OK'
			 print self.num
			 del g
			 break
	       except(GrabTimeoutError,GrabNetworkError,IndexError,KeyError,AttributeError,GrabConnectionError):
		    print g.config['proxy'],'Change proxy'
		    g.change_proxy()
		    del g
		    continue	  
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0013_00_Б_001-0057_BBPORT.xlsx')
	  self.ws = self.workbook.add_worksheet(u'Bbport')
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
	  self.ws.write(0, 32, u"ДОПОЛНИТЕЛЬНАЯ_ИНФОРМАЦИЯ")
	  self.ws.write(0, 33, u"МАТЕРИАЛЬНЫЕ_АКТИВЫ")
	  self.ws.write(0, 34, u"НЕМАТЕРИАЛЬНЫЕ_АКТИВЫ")
	  self.ws.write(0, 35, u"ЗАГОЛОВОК")
	  
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  for x in range(1,int(self.num)+1):
	       yield Task ('post',url='https://bbport.ru/business/?vt=1&region=1&city=-1&sp=1&page=%d'% x,refresh_cache=True,network_try_count=100)
		
     def task_post(self,grab,task):
	  #for d in grab.doc.select(u'//div[@class="object__line"]/div[@class="id"]/following-sibling::div'):
	       #dat = d.text()
	       #print dat
	    
	  
	  for elem in grab.doc.select(u'//a[@class="object__title wa pr_15"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,network_try_count=100)
	  
	  
	    
    
   
   
   
     def task_item(self, grab, task):
	  try:
	       dt = grab.doc.select(u'//div[@class="locBox"]/div').text()#.split(u' г. ')[1]
	       sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(u'крайский','')
	  except IndexError:
	       sub = u'Москва'
	
	  try:
	       ray = re.sub('[0-9\()]','',grab.doc.select(u'//ul[@class="compressLongGeoOrCat"][1]/li/a[contains(text(),"район")]').text())
	  except IndexError:
	       ray = ''
	  try:
	       punkt = grab.doc.select(u'//div[@class="locBox"]/div').text()
	  except IndexError:
	       punkt = u'Москва'
	  try:
	       uliza = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Район")]/following::div[1]').text()
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//ul[@class="categories__list"]').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro = grab.doc.select(u'//span[@class="metro__text"]').text()
	  except IndexError:
	       metro = ''
	       
	  try:
	       try:
	            mesto = grab.doc.select(u'//div[@class="map mb_45"]/text()').text().replace('-','')
	       except IndexError:    
		    mesto = grab.doc.select(u'//div[@class="locBox"]').text()#.replace('-','')
          except IndexError:
	       mesto = ''	       
	  try:
	       oborot = grab.doc.select(u'//div[contains(text(),"Выручка:")]/following::div[1]').text()#.replace(u' 7',u' руб.')
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//div[contains(text(),"Прибыль:")]/following::div[@class="countBox"][1]').text()#.replace(u' 7',u' руб.')
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//div[contains(text(),"Стоимость:")]/following::div[@class="countBox"][1]').text()#.replace(u' 7',u' руб.')
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//h1').text().split(u' г. ')[0]
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//div[contains(text(),"Доля в бизнесе:")]/following-sibling::div').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       sotrud = grab.doc.select(u'//h2[contains(text(),"Сотрудники")]/following::div[contains(text(),"Количество")]/following-sibling::div').text()
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Активность")]/following::div[1]').text()
	  except IndexError:
	       dolgi = ''
	 
	       
	  try:
	       srok = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Окупаемость")]/following::div[1]').text()
	  except IndexError:
	       srok = ''
	  try:
	       srok_sush = grab.doc.select(u'//div[contains(text(),"Возраст:")]/following::div[@class="countBox"][1]').text()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//div[contains(text(),"Причина продажи")]/following-sibling::div').text()
	  except IndexError:
	       prich = '' 
       
	  try:
	       opis = grab.doc.select(u'//h2[contains(text(),"Дополнительная информация")]/following-sibling::div/div').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       akt = grab.doc.select(u'//h2[contains(text(),"Информация об активах бизнеса")]/following::div[1]').text().split(u'Материальные активы')[1].split(u'Нематериальные активы')[0] 
          except IndexError:
               akt = ''	
	       
	  try:
	       nakt = grab.doc.select(u'//h2[contains(text(),"Информация об активах бизнеса")]/following::div[1]').text().split(u'Нематериальные активы')[1] 
          except IndexError:
	       nakt = ''	       
	  #try:
	       #ph= grab.doc.select(u'//div[@class="phone togglePhone"]').attr('data-id')
	       #url_ph = 'https://spb.bbport.ru/clients/getphone/?JsHttpRequest='+ph+'-xml&id='+ph
	       #r= requests.post(url_ph,verify=True,allow_redirects=False,timeout=15000)
	       #phone = re.sub('[^\d\+]','',r.content.split('phone')[1])
	  #except IndexError:
	       #phone = ''
       
	  
	  try:
	       con = [(u' августа',u'.08.'), (u' июля',u'.07.'),
		    (u' мая',u'.05.'),(u' июня',u'.06.'),
		    (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
		    (u' января ',u'.01.'),(u' декабря ',u'.12.'),
		    (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
		    (u' февраля ',u'.02.'),(u' октября ',u'.10.'),
		    (u'Сегодня',datetime.today().strftime('%d.%m.%Y')),
	            (u'Вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1)))]
	       dt1 = grab.doc.select(u'//div[@class="time"]').text()
	       data =  reduce(lambda dt1, r: dt1.replace(r[0], r[1]), con, dt1).replace('-','.')
	  except IndexError:
	       data = ''
       
	  
   
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'ulica': uliza,
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
	              'akt': akt,
	              'akt2': nakt,
                      'srok1': srok_sush,
                      'prichina': prich,
                      'opis': opis,
                      'phone': random.choice(list(open('../phone.txt'))),
	              'mesto': mesto,
                      'dataraz': data}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['ulica']
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
	  print  task.project['dom']
          print  task.project['mesto']  
	  
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,4, task.project['ulica'])
	  self.ws.write(self.result,12, task.project['dom'])
	  self.ws.write(self.result,7, task.project['metro'])
	  self.ws.write(self.result,17, task.project['oborot'])
	  self.ws.write(self.result,11, u'Продажа')
	  self.ws.write(self.result,18, task.project['pribil'])
	  self.ws.write(self.result,10, task.project['sfera'])
	  self.ws.write(self.result,19, task.project['sotrud'])
	  self.ws.write(self.result,13, task.project['price'])
	  self.ws.write(self.result,16, task.project['dolya'])
	  self.ws.write(self.result,21, task.project['srok'])
	  self.ws.write(self.result,15, task.project['dolg'])
	  self.ws.write(self.result,22, task.project['srok1'])
	  self.ws.write(self.result,24, task.project['prichina'])
	  self.ws.write(self.result,31, task.project['mesto'])
	  #self.ws.write(self.result,21, task.project['voda'])
	  #self.ws.write(self.result,22, task.project['kanal'])
	  #self.ws.write(self.result,23, task.project['elekt'])
	  #self.ws.write(self.result,24, task.project['teplo'])
	  #self.ws.write(self.result,19, task.project['ohrana'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'Buy business portal')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,32, task.project['opis'])
	  self.ws.write(self.result,33, task.project['akt'])
	  self.ws.write(self.result,34, task.project['akt2'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,29, task.project['dataraz'])
	  self.ws.write(self.result,35, task.project['sfera'])
	  #self.ws.write(self.result,36, task.project['parkovka'])
	 
	 
	  
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print '***',i+1,'/',dc,'***'
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  #if self.result > 100:
	       #self.stop()
   

bot = Bae(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')    
#command = 'mount -a'# cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
##command = 'apt autoremove'
#p = os.system('echo %s|sudo -S %s' % ('1122', command))
#print p
#time.sleep(2)
bot.workbook.close()
#workbook.close()
print('Done!')
time.sleep(5)
os.system("/home/oleg/pars/biz/altera.py")

    
	  
	  
	  