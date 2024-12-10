#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
#import requests
import re
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab(timeout=2, connect_timeout=2)
g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')



i = 0
l= open('Links/1.txt').read().splitlines()
page = l[i]
oper = u'Продажа'




while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'	       
     class Domofond_Com(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	      
               while True:
                    try:
                         time.sleep(2)
                         g.go(self.f)
                         for elem in g.doc.select(u'//ul[@class="pagination"]/li/a'):
                              self.last = elem.number()
                         self.sub = g.doc.rex_text(u'class="active">(.*?)</span>')
                         print self.sub,self.last
                         break
                    except(GrabTimeoutError,GrabNetworkError, GrabConnectionError):
                         print g.config['proxy'],'Change proxy'
                         g.change_proxy()
                         continue
                    except DataNotFound:
                         time.sleep(1)
                         print g.config['proxy'],'Change > proxy'
                         g.change_proxy()
                         continue
                    except AttributeError:
		         self.last = 1
               self.workbook = xlsxwriter.Workbook(u'com/Domofond_%s' % bot.sub + u'_Коммерческая_'+oper+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Domofond_Коммерческая')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МЕСТОРАСПОЛОЖЕНИЕ")
	       self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 4, u"УЛИЦА")
	       self.ws.write(0, 5, u"ДОМ")
	       self.ws.write(0, 6, u"ОРИЕНТИР")
	       self.ws.write(0, 7, u"СЕГМЕНТ")
	       self.ws.write(0, 8, u"ТИП_ПОСТРОЙКИ")
	       self.ws.write(0, 9, u"НАЗНАЧЕНИЕ_ОБЪЕКТА")
	       self.ws.write(0, 10, u"ПОТРЕБИТЕЛЬСКИЙ_КЛАСС")
	       self.ws.write(0, 11, u"СТОИМОСТЬ")
	       self.ws.write(0, 12, u"ПЛОЩАДЬ")
	       self.ws.write(0, 13, u"ЭТАЖ")
	       self.ws.write(0, 14, u"ЭТАЖНОСТЬ")
	       self.ws.write(0, 15, u"ГОД_ПОСТРОЙКИ")
	       self.ws.write(0, 16, u"МАТЕРИАЛ_СТЕН")
	       self.ws.write(0, 17, u"ВЫСОТА_ПОТОЛКА")
	       self.ws.write(0, 18, u"СОСТОЯНИЕ")
	       self.ws.write(0, 19, u"БЕЗОПАСНОСТЬ")
	       self.ws.write(0, 20, u"ГАЗОСНАБЖЕНИЕ")
	       self.ws.write(0, 21, u"ВОДОСНАБЖЕНИЕ")
	       self.ws.write(0, 22, u"КАНАЛИЗАЦИЯ")
	       self.ws.write(0, 23, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	       self.ws.write(0, 24, u"ТЕПЛОСНАБЖЕНИЕ")
	       self.ws.write(0, 25, u"ОПИСАНИЕ")
	       self.ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 28, u"ТЕЛЕФОН")
	       self.ws.write(0, 29, u"КОНТАКТНОЕ_ЛИЦО")
	       self.ws.write(0, 30, u"КОМПАНИЯ")
	       self.ws.write(0, 31, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 32, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 33, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 34, u"ЦЕНА_ЗА_М2")
	       self.result= 1
	       
                
                
                
                
	  def task_generator(self):
	       for x in range(1,self.last+1):
                    yield Task ('post',url=self.f+'?Page=%d'% x,refresh_cache=True,network_try_count=100)
          
        
	  def task_post(self,grab,task):
	       try:
	            num =  re.sub(u'^.*(?=из)', '', grab.doc.select('//p[@class="pull-left"]').text())
	       except DataNotFound:
		    num = ''
	       for elem in grab.doc.select('//a[@itemprop="sameAs"]'):
		    ur = 'http://m.domofond.ru/na-prodazhu/obyavleniye/'+re.sub('[^\d]','',grab.make_url_absolute(elem.attr('href')))   
		    #print ur
		    yield Task('item', url=ur,num=num,refresh_cache=True, network_try_count=100)
	      
            
	 
        
	  def task_item(self, grab, task):
	       try:
	            mesto = grab.doc.select(u'//span[@itemprop="address"]').text()#.replace(bot.sub,'')
	       except IndexError:
	            mesto =''
               try:
                    ter =  re.sub('[\d]', u'',grab.doc.select(u'//ol[@class="breadcrumb hidden-print"]/span[4]').text()).replace(u'Номер в каталоге:','')
               except DataNotFound:
                    ter =''
               #try:
                    #uliza = re.sub(u'[\d]','',grab.doc.select(u'//span[@itemprop="address"]').text().split(', ')[0])
               #except DataNotFound:
                    #uliza = ''
               #try:
                    #dom = re.sub(u'[^\d]','',grab.doc.select(u'//span[@itemprop="address"]').text().split(', ')[1])
               #except IndexError:
                    #dom = ''
		    
               try:
                    tip = grab.doc.select(u'//li[contains(text(),"Тип объекта:")]/following-sibling::li').text()
               except IndexError:
                    tip = ''
               try:
                    naz = grab.doc.select(u'//li[contains(text(),"Тип:")]/following-sibling::li').text()
               except IndexError:
                    naz =''
               try:
                    klass =  grab.doc.select(u'//li[contains(text(),"Цена за м²:")]/following-sibling::li').text()
               except IndexError:
                    klass = ''
               try:
                    price = grab.doc.select(u'//li[contains(text(),"Цена:")]/following-sibling::li').text()
               except IndexError:
                    price =''
               try: 
                    plosh = grab.doc.select(u'//li[contains(text(),"Площадь:")]/following-sibling::li').text()
               except IndexError:
                    plosh=''
               try:
                    ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
               except DataNotFound:
                    ohrana =''
               try:
                    gaz = re.sub(u'^.*(?=газ)','', grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
               except DataNotFound:
                    gaz =''
               try:
                    voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
               except DataNotFound:
                    voda =''
               try:
                    kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
               except DataNotFound:
                    kanal =''
               try:
                    elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
               except DataNotFound:
                    elek =''
               try:
                    teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
               except DataNotFound:
                    teplo =''
               time.sleep(1)
	       try:
		    url_op = task.url+'/FetchListingDescription'
		    g3 = grab.clone(timeout=20000, connect_timeout=20000)
		    g3.request(post='{"FetchListingDescription","Token","Timestamp","ContactId"}',url=url_op)
		    opis = g3.response.body
		    #r= requests.post(task.url+'/FetchListingDescription',verify=True,timeout=15000)
		    #opis = r.content 
	       except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
		    opis = ''
               try:
                    lico = grab.doc.select(u'//span[contains(text(),"Частное лицо:")]/following-sibling::span').text()
               except DataNotFound:
                    lico = ''
               try:
                    comp = grab.doc.select(u'//span[contains(text(),"Агентство:")]/following-sibling::span').text()
               except DataNotFound:
                    comp = ''
               try:
                    try: 
                         data = grab.doc.select(u'//li[contains(text(),"Дата обновления объявления:")]/following-sibling::li').text().replace('/','.')
                    except DataNotFound:
                         data = grab.doc.select(u'//li[contains(text(),"Дата публикации объявления:")]/following-sibling::li').text().replace('/','.')  
               except DataNotFound:   
                    data = ''
	       
	       time.sleep(1)
	       try:
     
		    url_ph = 'http://m.domofond.ru/Listing'+grab.doc.rex_text("Listing(.*?)'")
		    g2 = grab.clone(timeout=20000, connect_timeout=20000)
		    g2.request(post='{"ListingId","Token","Timestamp","ContactId"}',url=url_ph)
		    phone = re.sub('[^\d]','',g2.response.body)[:11]
	       except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
		    phone = ''
          
	       
		    
     
	
               projects = {'sub': self.sub,
	                  'adress': mesto,
	                   'terit':ter, 
	                   #'ulica':uliza, 
	                   #'dom':dom,
	                   'tip':tip,
	                   'naz':naz,
	                   'klass': klass,
	                   'cena': price,
	                   'plosh': plosh,
	                   'ohrana':ohrana,
	                   'gaz': gaz,
	                   'voda': voda,
	                   'kanaliz': kanal,
	                   'electr': elek,
	                   'teplo': teplo,
	                   'opis': opis,
	                   'url': task.url,
	                   'phone': phone,
	                   'lico':lico,
	                   'company': comp,
	                   'data':data,
	                   'koll':task.num}
	  
	  
	       yield Task('write',project=projects,grab=grab)
	  
	  
	  
	  def task_write(self,grab,task):
	       #time.sleep(1)
	       print('*'*100)	       
	       print  task.project['sub']
	       #print  task.project['rayon']
	       print  task.project['adress']
	       print  task.project['terit']
	       #print  task.project['ulica']
	       #print  task.project['dom']
	       print  task.project['tip']
	       print  task.project['naz']
	       print  task.project['klass']
	       print  task.project['cena']
	       print  task.project['plosh']
	       print  task.project['gaz']
	       print  task.project['voda']
	       print  task.project['kanaliz']
	       print  task.project['electr']
	       print  task.project['teplo']
	       print  task.project['ohrana']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.project['data']
	  
	       
	       
     
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['adress'])
	       self.ws.write(self.result, 3, task.project['terit'])
	       #self.ws.write(self.result, 4, task.project['ulica'])
	       #self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 8, task.project['tip'])
	       self.ws.write(self.result, 9, task.project['naz'])
	       self.ws.write(self.result, 34, task.project['klass'])
	       self.ws.write(self.result, 11, task.project['cena'])
	       self.ws.write(self.result, 12, task.project['plosh'])
	       self.ws.write(self.result, 19, task.project['ohrana'])
	       self.ws.write(self.result, 20, task.project['gaz'])
	       self.ws.write(self.result, 21, task.project['voda'])
	       self.ws.write(self.result, 22, task.project['kanaliz'])
	       self.ws.write(self.result, 23, task.project['electr'])
	       self.ws.write(self.result, 24, task.project['teplo'])
	       self.ws.write(self.result, 25, task.project['opis'])
	       self.ws.write(self.result, 26, u'DOMOFOND.RU')
	       self.ws.write_string(self.result, 27, task.project['url'])
	       self.ws.write(self.result, 28, task.project['phone'])
	       self.ws.write(self.result, 29, task.project['lico'])
	       self.ws.write(self.result, 30, task.project['company'])
	       self.ws.write(self.result, 31, task.project['data'])
	       self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result, 33, oper)
	       print('*'*100)
	       print self.sub
	       print 'Ready - '+str(self.result)+' '+task.project['koll']
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print '***',i+1,'/',len(l),'***'
	       print oper
	       print('*'*100)
	       self.result+= 1
	       
	      
	       
	       
	       
	       #if self.result > 10:
	            #self.stop()	       
	
	
	   
        
    
            
          
		    
     
    
		
	 

     bot = Domofond_Com(thread_number=1, network_try_limit=2000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     bot.run()
     print bot.sub
     print('Спим 2 сек...')
     time.sleep(2)
     print('Сохранение...')
     bot.workbook.close()
     print('Done!')
     time.sleep(1) 
     i=i+1
     try:
          page = l[i]
     except IndexError:
          if oper == u'Продажа':
               i = 0
               l= open('Links/2.txt').read().splitlines()
               dc = len(l)
               page = l[i]
               oper = u'Аренда'
          else:
               break
       
     
     
     