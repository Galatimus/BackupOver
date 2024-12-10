#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import random
import re
from datetime import datetime
import xlsxwriter
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Bae(Spider):
     
     
     
     def prepare(self):
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0013_00_Б_001-0067_BASSET.xlsx')
	  self.ws = self.workbook.add_worksheet(u'BAE')
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
	  self.ws.write(0, 12, u"СЕГМЕНТ_ГОТОВОГО_БИЗНЕСА")
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
	  self.ws.write(0, 31, u"ЗАГОЛОВОК")
	  self.ws.write(0, 32, u"ДАТА ПРОВЕРКИ АКТУАЛЬНОСТИ")
	  
	  self.result= 1
	 
       
       
       
	 

     def task_generator(self):
	  for x in range(1,532):#497
	       yield Task ('post',url='http://business-asset.ru/index.php?page=basebiz&country=172&paginationPage=%d'% x,refresh_cache=True,network_try_count=100)
		
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//h2/a[contains(@target,"blank")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,post = task.url,network_try_count=100)
	  
	  
	    
    
   
   
   
     def task_item(self, grab, task):
	  try:
	       sub = re.sub('[0-9\()]','',grab.doc.select(u'//ul[@class="compressLongGeoOrCat"][1]/li[2]').text())
	  except IndexError:
	       sub = ''
	
	  try:
	       ray = re.sub('[0-9\()]','',grab.doc.select(u'//ul[@class="compressLongGeoOrCat"][1]/li/a[contains(text(),"район")]').text())
	  except IndexError:
	       ray = ''
	  try:
	       punkt = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Город")]/following::div[1]').text()
	  except IndexError:
	       punkt = ''
	  try:
	       uliza = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Район")]/following::div[1]').text()
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"До метро")]/following::div[1]').number()
	  except IndexError:
	       dom = ''
	       
	  try:
	       metro = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Район/метро")]/following::div[1]').text()
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Выручка")]/following::div[@class="val"][1]').text()
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Кассовая прибыль")]/following::div[1]').text()
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//div[@class="val"]/div[@class="price"]').text().replace(u' Совместная инвестиция','')
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//h1/span[@itemprop="name"]').text()
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Продаваемая доля")]/following::div[1]').text()
	  except IndexError:
	       dolya = ''
	       
	  try:
	       sotrud = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Численность персонала")]/following::div[1]').text()
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
	       srok_sush = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Возраст")]/following::div[1]').text()
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//div[@class="label"]/span[contains(text(),"Причина продажи")]/following::div[1]').text()
	  except IndexError:
	       prich = ''		    
       
	  try:
	       opis = grab.doc.select(u'//p[@itemprop="description"]').text() 
	  except IndexError:
	       opis = ''
	  #try:
	       #lin = []
               #for em in grab.doc.select(u'//ul[@class="compressLongGeoOrCat"][2]/li/a/span'):
                    #urr = em.text()
                    #lin.append(urr)
	       #phone = ",".join(lin)
	  #except IndexError:
	       #phone = ''
       
	  
	  try:
	       data = grab.doc.select(u'//div[@class="date"]').text().split(u' в ')[0]
	  except IndexError:
	       data = ''
	       
	  try:
	       data1 = grab.doc.select(u'//div[@class="date"]').text().split(u'Проверка актуальности:')[1]
	  except IndexError:
	       data1 = ''	       
       
	  
   
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
                      'srok1': srok_sush,
                      'prichina': prich,
                      'opis': opis,
                      'phone': random.choice(list(open('../phone.txt'))),
	              'aktual': data1,
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
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['dataraz']
	  print  task.project['aktual']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,1, task.project['rayon'])
	  self.ws.write(self.result,3, task.project['punkt'])
	  self.ws.write(self.result,4, task.project['ulica'])
	  self.ws.write(self.result,8, task.project['dom'])
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
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,26, u'Business_Asset_Exchange')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.project['phone'])
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,29, task.project['dataraz'])
	  self.ws.write(self.result,31, task.project['sfera'])
	  self.ws.write(self.result,32, task.project['aktual'])
	 
	 
	 
	  
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print '***',i+1,'/',dc,'***'
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  #if self.result > 50:
	       #self.stop()
   

bot = Bae(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
command = 'mount -a'# cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
#command = 'apt autoremove'
p = os.system('echo %s|sudo -S %s' % ('1122', command))
print p
time.sleep(5)
bot.workbook.close()
#workbook.close()
print('Done!')
time.sleep(5)
os.system("/home/oleg/pars/biz/bizmast.py")


    
	  
	  
	  