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

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


#g = Grab()
#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http') 

class biztorg(Spider):
     
     
     
     def prepare(self):
	  
	  self.workbook = xlsxwriter.Workbook(u'0001-0013_00_Б_001-0093_BIZTOR.xlsx')
	  self.ws = self.workbook.add_worksheet(u'biztorg')
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
	  self.ws.write(0, 31, u"МЕСТОПОЛОЖЕНИЕ")
	  self.ws.write(0, 32, u"ДОПОЛНИТЕЛЬНАЯ_ИНФОРМАЦИЯ")
	  self.ws.write(0, 33, u"НЕДВИЖИМОСТЬ(В_СОБСТВЕННОСТИ)")
	  self.ws.write(0, 34, u"НЕДВИЖИМОСТЬ(В_АРЕНДЕ)")
	  self.ws.write(0, 35, u"СЕРТИФИКАТЫ,ЛИЦЕНЗИИ")
	  self.ws.write(0, 36, u"НЕДВИЖИМОСТЬ")
	  self.ws.write(0, 37, u"ЗАГОЛОВОК")
	  
	  self.result= 1
	 
     def task_generator(self):
	  for x in range(1,147):#897
	       yield Task ('post',url='http://biztorg.ru/offers/page/%d'% x,refresh_cache=True,network_try_count=100)
		
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//h4/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,network_try_count=100)
	  
   
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h1/following-sibling::text()').text().split(u', ')[1]
	  except IndexError:
	       sub = ''
	
	  try:
	       if u'Москва' in sub:
		    ter = grab.doc.select(u'//div[@class="property-detail-subtitle full"]/div').text().split(u', ')[1]
	       else:
		    ter = grab.doc.select(u'//div[@class="property-detail-subtitle full"]/div').text().split(u', ')[2]
	  except IndexError:
	       ter = ''
	  try:
	       punkt= grab.doc.select(u'//h1/following-sibling::text()').text().split(u', ')[2]
	  except IndexError:
	       punkt = ''
	  uliza = ''
	  try:
	       ray = grab.doc.select(u'//div[@class="property-detail-subtitle full"]/div').text()
	       
	  except IndexError:
	       ray = ''
	       
	  dom=''     
	  try:
	       if u'Москва'in sub:
		    metro = grab.doc.select(u'//div[@class="property-detail-subtitle full"]/div').text().split(u', ')[2]
	       else:
		    metro = ''
	  except IndexError:
	       metro = ''
	  try:
	       oborot = grab.doc.select(u'//li[contains(text(),"Выручка")]').text().replace(u'aВыручка',u'руб.')
	  except IndexError:
	       oborot = ''
	  try:
	       pribil = grab.doc.select(u'//li[contains(text(),"Прибыль")]').text().replace(u'aПрибыль',u'руб.')
	  except IndexError:
	       pribil = ''
	  try:
	       #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	       price = grab.doc.select(u'//div[contains(text(),"Стоимость")]').text().replace(u'a Стоимость',u'руб.')
	       #else:
		    #price =''
	  except IndexError:
	       price = ''
	  try:
	       sfera = grab.doc.select(u'//h1').text()
	  except IndexError:
	       sfera = ''
	       
	  try:
	       dolya = grab.doc.select(u'//li[contains(text(),"Доля")]').text().replace(u'Доля','')
	  except IndexError:
	       dolya = ''
	       
	  try:
               sotrud = grab.doc.select(u'//li[contains(text(),"Персонал")]').text().replace(u'Персонал','')
	  except IndexError:
	       sotrud = ''
	  try:
	       dolgi = grab.doc.select(u'//td[@class="td1"][contains(text(),"Балансовая стоимость основных средств:")]/following-sibling::td').text()
	  except IndexError:
	       dolgi = ''
	 
	       
	  try:
	       srok = grab.doc.select(u'//li[contains(text(),"Заемные средства")]/following::li[2]').text().replace(u' Окупаемость','')
	  except IndexError:
	       srok = ''
	  try:
	       srok_sush = grab.doc.select(u'//li[contains(text(),"Доля")]/following-sibling::li[1]').text().replace(u' Возраст','')
	  except IndexError:
	       srok_sush = ''
	  try:
	       prich = grab.doc.select(u'//h4[contains(text(),"Средства производства")]/following-sibling::p[1]').text()
	  except IndexError:
	       prich = ''		    
       
	  try:
	       opis = grab.doc.select(u'//h4[contains(text(),"Дополнительная информация")]/following-sibling::p[1]').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       sob = grab.doc.select(u'//h4[contains(text(),"Недвижимость (в собственности)")]/following-sibling::p[1]').text() 
	  except IndexError:
	       sob = ''
	       
	  try:
	       are = grab.doc.select(u'//h4[contains(text(),"Недвижимость (в аренде)")]/following-sibling::p[1]').text() 
          except IndexError:
	       are = ''
	       
	  try:
	       sert = grab.doc.select(u'//h4[contains(text(),"Сертификаты, лицензии")]/following-sibling::p[1]').text() 
	  except IndexError:
	       sert = ''
	       
	  try:
	       nedv = grab.doc.select(u'//h4[contains(text(),"Недвижимость")]/following-sibling::p[1]').text() 
	  except IndexError:
	       nedv = ''	       
	   
	  
	  try:
	       data = grab.doc.select(u'//h1/following-sibling::text()').text()
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
	              'sob': sob,
	              'arend': are,
	              'sertif': sert,
	              'nedv': nedv,
                      'srok': srok,
                      'srok1': srok_sush,
                      'prichina': prich,
                      'opis': opis,
                      'dataraz': data}
   
	  try:
	       link = 'http://biztorg.ru/getphone/'+ re.sub(u'[^\d]','',task.url)
	       headers ={'Accept': '*/*',
			 'Accept-Encoding': 'gzip,deflate',
			 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			 'Cookie': 'PHPSESSID = habatu57k9ieruonfflmv5jq94',
			 'Host': 'biztorg.ru',
			 'Referer': task.url,
			 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			 'X-Requested-With' : 'XMLHttpRequest'}
	       #print link
	       gr = Grab()
	       gr.setup(url=link,headers=headers)
	       yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       yield Task('phone',grab=grab,project=projects)
	       
	       
     def task_phone(self, grab, task):
          
          try:
               phone = grab.doc.json['data']
          except IndexError:
               phone=''	            
	                  
   
	  yield Task('write',project=task.project,phone=phone,grab=grab)
   

   
   
   
   
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
	  print  task.phone
	  print  task.project['dataraz']
	  
	  
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,32, task.project['rayon'])
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
	  self.ws.write(self.result,23, task.project['prichina'])
	  self.ws.write(self.result,25, task.project['opis'])
	  self.ws.write(self.result,32, task.project['opis'])
	  self.ws.write(self.result,26, u'РБК_БИЗТОРГ')
	  self.ws.write_string(self.result,27, task.project['url'])
	  self.ws.write(self.result,28, task.phone)
	  self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result,31, task.project['dataraz'])
	  self.ws.write(self.result,33, task.project['sob'])
	  self.ws.write(self.result,34, task.project['arend'])
	  self.ws.write(self.result,35, task.project['sertif'])
	  self.ws.write(self.result,36, task.project['nedv'])
	  self.ws.write(self.result,37, task.project['sfera'])
	   
   
	  print('*'*100)
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  #if self.result > 20:
	       #self.stop()
	  
	  
   

bot = biztorg(thread_number=5, network_try_limit=1000)
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
