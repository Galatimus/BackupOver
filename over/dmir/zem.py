#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import os
import re
import math
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


  



i = 0
l= open('Links/Zem_Prod.txt').read().splitlines()
dc = len(l)
page = l[i]  
oper = u'Продажа'
     


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     

     class Dmir_Zem(Spider):
	  
	  
	  
          def prepare(self):
	       #self.count = 1 
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
		         time.sleep(5)
			 g = Grab(timeout=20, connect_timeout=100)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')			 
			 g.go(self.f)
			 #conv = [ (u'кой',u'кая'),(u'области',u'область'),(u'ком',u'кий'),
				  #(u'Москве',u'Москва'),(u'Петербурге',u'Петербург'),
				  #(u'крае',u'край'),(u'республике ','')]
			 #dt= g.doc.rex_text(u'участков (.*?)</h1>').replace(u'кой',u'кая').replace(u'области',u'область') 
			 #self.sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
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
	       self.workbook = xlsxwriter.Workbook(u'Zem/Dmir_%s' % bot.sub + u'_Земля_'+oper+'.xlsx')
               self.ws = self.workbook.add_worksheet(u'DMIR_ЗЕМЛЯ')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 4, u"УЛИЦА")
	       self.ws.write(0, 5, u"ДОМ")
	       self.ws.write(0, 6, u"ОРИЕНТИР")
	       self.ws.write(0, 7, u"ТРАССА")
	       self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	       self.ws.write(0, 9, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 10, u"СТОИМОСТЬ")
	       self.ws.write(0, 11, u"ЦЕНА_ЗА_СОТКУ")
	       self.ws.write(0, 12, u"ПЛОЩАДЬ")
	       self.ws.write(0, 13, u"КАТЕГОРИЯ_ЗЕМЛИ")
	       self.ws.write(0, 14, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	       self.ws.write(0, 15, u"ГАЗОСНАБЖЕНИЕ")
	       self.ws.write(0, 16, u"ВОДОСНАБЖЕНИЕ")
	       self.ws.write(0, 17, u"КАНАЛИЗАЦИЯ")
	       self.ws.write(0, 18, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	       self.ws.write(0, 19, u"ТЕПЛОСНАБЖЕНИЕ")
	       self.ws.write(0, 20, u"ОХРАНА")
	       self.ws.write(0, 21, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	       self.ws.write(0, 22, u"ОПИСАНИЕ")
	       self.ws.write(0, 23, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 24, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 25, u"ТЕЛЕФОН")
	       self.ws.write(0, 26, u"КОНТАКТНОЕ_ЛИЦО")
	       self.ws.write(0, 27, u"КОМПАНИЯ")
	       self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 29, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ_ЦЕНЫ")
	       self.ws.write(0, 31, u"ДАТА_ИЗМЕНЕНИЯ_ЦЕНЫ")
	       self.ws.write(0, 32, u"МЕСТОПОЛОЖЕНИЕ")
	       self.result= 1
	        
            
            
            
              
    
	  def task_generator(self):
	       for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'&page=%d'%x,refresh_cache=True,network_try_count=50)
      
            
	  def task_post(self,grab,task):
     
	       
	       for elem in grab.doc.select('//td/input[@type="hidden"]/following-sibling::a'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=50)
	       
	
        
	  def task_item(self, grab, task):
	       try:
		    mesto =  grab.doc.select(u'//h2[@class="subtitle"]/small').text() 
	       except DataNotFound:
	            mesto = ''
	     
	       try:
		    ray =  grab.doc.rex_text(u'в (.*?)районе</a></li></ul>').replace(u'ком',u'кий') 
		  
	       except DataNotFound:
		    ray = ''
	       try:
		    if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'ш. ') > 0:
                         punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
                    else:    
                         punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[1]
	       except IndexError:
		    punkt = ''
	       try:
		    if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'ш. ') > 0:
                         uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[4]
                    else:    
                         uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[2]
	       except IndexError:
		    uliza = ''
               try:
                    if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'ш. ') > 0:
                         dom = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[5]
                    else:    
                         dom = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
               except IndexError:
                    dom = ''
	       try:
	            if grab.doc.select(u'//li[@class="metro"]').text().find(u'ш. ') > 0:
                         trassa = grab.doc.select(u'//li[@class="metro"]').text().split(',')[0]
                    else:
                         trassa = ''
               except IndexError:
	            trassa = ''
	       try:
	            if grab.doc.select(u'//li[@class="metro"]').text().find(u'км.') > 0:
                         udal = grab.doc.select(u'//li[@class="metro"]').text().split(',')[1]
                    else:
                         udal = ''
               except IndexError:
	            udal = ''
	       try:
		    if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	                 price = grab.doc.select('//span[@id="price_offer"]').text()
                    else:
                         price =''
               except IndexError:
	            price = ''
               try:
                    if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') > 0:
                         price_sot = grab.doc.select('//span[@id="price_offer"]').text()
                    else:
                         price_sot =''
               except IndexError:
                    price_sot = ''
               try:
                    plosh = grab.doc.select(u'//ul[@id="land_data"]/li[contains(text(),"площадь")]').text().replace(u' площадь','')
               except IndexError:
                    plosh = ''
               try:
                    vid = grab.doc.select(u'//ul[@id="land_data"]/li[contains(text(),"назначение")]').text().replace(u' назначение','')
               except IndexError:
                    vid = ''
               try:
                    gaz = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"газ")]').text().replace(u'есть газ',u'есть').replace(u'нет газа','')
               except IndexError:
                    gaz =''
               try:
                    voda = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"водоснабжение")]').text().replace(u'есть водоснабжение',u'есть').replace(u'нет водоснабжения','')
               except IndexError:
                    voda =''
               try:
                    kanal = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"канализация")]').text().replace(u'есть канализация',u'есть').replace(u'нет канализации','')
               except IndexError:
                    kanal =''
               try:
                    elekt = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"электричество")]').text().replace(u'есть электричество',u'есть').replace(u'нет электричества','')
               except IndexError:
                    elekt =''
	       try:
	            teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
               except IndexError:
	            teplo =''
	       try:
                    ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
               except IndexError:
                    ohrana =''
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
	                   'trassa': trassa,
	                   'udal': udal[1:],
	                   'price': price,
	                   'price_sot': price_sot,
	                   'ploshad': plosh,
	                   'vid': vid,
	                   'gaz': gaz,
	                   'voda':voda,
	                   'kanal': kanal,
	                   'elekt': elekt,
	                   'teplo': teplo,
	                   'ohrana': ohrana,
	                   'opis': opis,
	                   'phone': phone,
	                   'lico':lico,
	                   'mesto':mesto,
	                   'company':com,
	                   'dataraz': data,
	                   'data1': data1,
	                   'data2': data2
	                      }
	
	
	
	       yield Task('write',project=projects,grab=grab)
	

	
	
	
	
	  def task_write(self,grab,task):
	       if task.project['opis'] <> '':
		    print('*'*100)
		    print  task.project['sub']
		    print  task.project['rayon']
		    print  task.project['punkt']
		    print  task.project['ulica']
		    print  task.project['dom']
		    print  task.project['trassa']
		    print  task.project['udal']
		    print  task.project['price']
		    print  task.project['price_sot']
		    print  task.project['ploshad']
		    print  task.project['vid']
		    print  task.project['gaz']
		    print  task.project['voda']
		    print  task.project['kanal']
		    print  task.project['elekt']
		    print  task.project['teplo']
		    print  task.project['ohrana']
		    print  task.project['opis']
		    print task.project['url']
		    print  task.project['phone']
		    print  task.project['lico']
		    print  task.project['company']
		    print  task.project['dataraz']
		    print  task.project['mesto']
		    print  task.project['data1']
		    print  task.project['data2']
		    
		    self.ws.write(self.result, 0, task.project['sub'])
		    self.ws.write(self.result, 1, task.project['rayon'])
		    self.ws.write(self.result, 2, task.project['punkt'])
		    self.ws.write(self.result, 4, task.project['ulica'])
		    self.ws.write(self.result, 7, task.project['trassa'])
		    self.ws.write(self.result, 8, task.project['udal'])
		    self.ws.write(self.result, 9, oper)
		    self.ws.write(self.result, 10, task.project['price'])
		    self.ws.write(self.result, 11, task.project['price_sot'])
		    self.ws.write(self.result, 12, task.project['ploshad'])
		    self.ws.write(self.result, 14, task.project['vid'])
		    self.ws.write(self.result, 15, task.project['gaz'])
		    self.ws.write(self.result, 16, task.project['voda'])
		    self.ws.write(self.result, 17, task.project['kanal'])
		    self.ws.write(self.result, 18, task.project['elekt'])
		    self.ws.write(self.result, 19, task.project['teplo'])
		    self.ws.write(self.result, 20, task.project['ohrana'])
		    self.ws.write(self.result, 22, task.project['opis'])
		    self.ws.write(self.result, 23, u'Недвижимость и цены')
		    self.ws.write_string(self.result, 24, task.project['url'])
		    self.ws.write(self.result, 25, task.project['phone'])
		    self.ws.write(self.result, 26, task.project['lico'])
		    self.ws.write(self.result, 27, task.project['company'])
		    self.ws.write(self.result, 28, task.project['dataraz'])
		    self.ws.write(self.result, 29, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result, 30, task.project['data1'])
		    self.ws.write(self.result, 31, task.project['data2'])
		    self.ws.write(self.result, 32, task.project['mesto'])
		   
		   
		    
	     
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
		    if str(self.result) == str(self.num):
			 self.stop()	       

     bot = Dmir_Zem(thread_number=2, network_try_limit=500)
     bot.load_proxylist('../tipa.txt','text_file')
     #bot.create_grab_instance(timeout=5, connect_timeout=10)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(2)
     print('Save it...')
     try:
	  command = 'mount -a'
	  os.system('echo %s|sudo -S %s' % ('1122', command))
	  time.sleep(5)
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
	       l= open('Links/Zem_Arenda.txt').read().splitlines()
	       dc = len(l)
	       page = l[i]  
	       oper = u'Аренда'
	  else:
	       break
	  
	  
	  