#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import os
import math
import time
import re
from datetime import datetime
import xlsxwriter

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



 



i = 0
l= open('Links/Dmir_Prod.txt').read().splitlines()
dc = len(l)
page = l[i]  
oper = u'Продажа'
     


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     

     class Dmir_Biz(Spider):
	  
	  
	  
          def prepare(self):
	       #self.count = 1 
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
			 time.sleep(5)
			 g = Grab(timeout=20, connect_timeout=20)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
			 g.go(self.f)
			 #global sub
			 self.sub = g.doc.select('//a[@class="menu-first-child"]').text()
			 self.num = re.sub('[^\d]','',g.doc.select(u'//title').text().split(' - ')[0])
                         self.pag = int(math.ceil(float(int(self.num))/float(120)))
                         print self.sub,self.num,self.pag
			 del g 
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 del g
			 continue	  	       
	       self.workbook = xlsxwriter.Workbook(u'dmir/Dmir_%s' % bot.sub + u'_Готовый_бизнес_'+oper+'.xlsx')
               self.ws = self.workbook.add_worksheet(u'Dmir_Готовый_бизнес')
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
	       for x in range(1,self.pag+1):
                    link = self.f+'&page='+str(x)
                    yield Task ('post',url=link.replace(u'&page=1',''),refresh_cache=True,network_try_count=1000)
        
	  def task_post(self,grab,task):
	       
	       for elem in grab.doc.select(u'//input[@name="rlt_cnt"]/following-sibling::a'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
	            #print ur
		    yield Task('item',url=ur,refresh_cache=True,network_try_count=1000)
		        
        
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
		    #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	            price = grab.doc.select('//span[@id="price_offer"]').text()
                    #else:
                         #price =''
               except IndexError:
	            price = ''
               try:
                    sfera = grab.doc.select(u'//h1[@class="displayinline pr10"]').text().split(', ')[0].replace(u'Продаю ','').replace(u'Сдаю ','')
               except IndexError:
                    sfera = ''
		    
               try:
                    et2 = grab.doc.select(u'//li[contains(text(),"этажность")]').number()
               except IndexError:
                    et2 = ''
		    
               try:
                    sposob = grab.doc.select(u'//div[@class="fwnorm"]').text()
               except IndexError:
                    sposob = ''
		    
	       try:
	            zag = grab.doc.select(u'//h1').text()
	       except IndexError:
	            zag = ''              
		    
               try:
                    sos = grab.doc.select(u'//li[contains(text(),"состояние")]/b').text()
               except DataNotFound:
                    sos = ''
            
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
	            data = grab.doc.select(u'//dt[contains(text(),"Размещено")]/following::span[1]').text()
	       except IndexError:
	            data = ''
		    
               try:
	            mesto = grab.doc.select(u'//h2[@class="subtitle"]/small').text()
	       except IndexError:
	            mesto = ''		    
	    
	       
	
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt[1:],
		           'ulica': uliza[1:].replace(u'м.',u'улица'),
	                   'dom': dom[1:],
	                   'metro_min': metro_min,
	                   'metro': metro,
	                   'price': price,
	                   'metro_kak': metro_kak,
	                   'sfera': sfera,
	                   'ets': et2,
	                   'sposob': sposob,
	                   'zag': zag,
	                   'sost': sos,
	                   'opis': opis,
	                   'phone': phone,
	                   'koll':mesto,
	                   'dataraz': data}
	
	
	
	       yield Task('write',project=projects,grab=grab)
	

	
	
	
	
	  def task_write(self,grab,task):
	       if task.project['opis'] <> '':
		    print('*'*100)
		    print  task.project['sub']
		    print  task.project['rayon']
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
		    print  task.project['sost']
		    print  task.project['opis']
		    print  task.project['url']
		    print  task.project['phone']
		    print  task.project['dataraz']
		    print  task.project['koll']
		    
		    
		    self.ws.write(self.result,0, task.project['sub'])
		    self.ws.write(self.result,1, task.project['rayon'])
		    self.ws.write(self.result,3, task.project['punkt'])
		    self.ws.write(self.result,5, task.project['ulica'])
		    self.ws.write(self.result,6, task.project['dom'])
		    self.ws.write(self.result,7, task.project['metro'])
		    self.ws.write(self.result,8, task.project['metro_min'])
		    self.ws.write(self.result,11, oper)
		    self.ws.write(self.result,9, task.project['metro_kak'])
		    self.ws.write(self.result,10, task.project['sfera'])
		    self.ws.write(self.result,12, task.project['sposob'])
		    self.ws.write(self.result,13, task.project['price'])
		    self.ws.write(self.result,14, task.project['ets'])
		    self.ws.write(self.result,15, task.project['sost'])
		    self.ws.write(self.result,25, task.project['opis'])
		    self.ws.write(self.result,26, u'Недвижимость и цены')
		    self.ws.write_string(self.result,27, task.project['url'])
		    self.ws.write(self.result,28, task.project['phone'])
		    self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result,29, task.project['dataraz'])
		    self.ws.write(self.result,31, task.project['koll'])
		    self.ws.write(self.result,32, task.project['zag'])
		   
		   
		    
	     
		    print('*'*100)
		    print self.sub
		    print 'Ready - '+str(self.result)+'/'+str(self.num)
		    logger.debug('Tasks - %s' % self.task_queue.size()) 
		    print '***',i+1,'/',dc,'***'
		    print oper
		    print('*'*100)
		    self.result+= 1
		    
		    #if self.result > 10:
			 #self.stop()	       
	

     bot = Dmir_Biz(thread_number=1, network_try_limit=10000)
     bot.load_proxylist('../tipa.txt','text_file')
     #bot.create_grab_instance(timeout=5, connect_timeout=10)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(2)
     print('Save it...')
     try:
	  command = 'mount -a'
	  os.system('echo %s|sudo -S %s' % ('1122', command))
	  time.sleep(3)
	  bot.workbook.close()
	  print('Done')
     except IOError:
	  time.sleep(30)
	  os.system('echo %s|sudo -S %s' % ('1122', 'mount -a'))
	  time.sleep(10)
	  bot.workbook.close()
	  print('Done!')
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  if oper == u'Продажа':
	       i = 0
	       l= open('Links/Dmir_Arenda.txt').read().splitlines()
	       dc = len(l)
	       page = l[i]  
	       oper = u'Аренда'
	  else:
	       break
	  
	  
	  