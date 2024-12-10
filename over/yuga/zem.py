#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
import os
import time
import json
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



i = 0
l= open('zem.txt').read().splitlines()

page = l[i] 






while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'
     class Nedvizhka_Zem(Spider):
	  def prepare(self):
	       self.f = page
	       #self.link =l[i]
	       while True:
		    try:
                         time.sleep(2)
			 g = Grab(timeout=5, connect_timeout=5)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')			 
                         g.go(self.f)
			 self.sub =  g.doc.select(u'//h1/following-sibling::h3').text()
			 try:
			      try:
				   self.pag = re.sub('[^\d]','',g.doc.select(u'//div[@class="pagination"]/span[@class="grey"]/following-sibling::a').text())
			      except IndexError:
				   self.pag = re.sub('[^\d]','',g.doc.select(u'//div[@class="pagination"]/a[2]').text())
			 except IndexError:
			      self.pag = 1
			 print self.sub,self.pag
			 del g
			 break 
		    except(GrabTimeoutError,GrabNetworkError,IndexError,GrabConnectionError):
		         print g.config['proxy'],'Change proxy'
		         g.change_proxy()
			 del g
		         continue
                    
		    
	       
	       self.workbook = xlsxwriter.Workbook(u'zem/Dom-Yuga_%s' % bot.sub + u'_Земля_'+str(i+1)+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Земля')
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
	       self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 30, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 31, u"МЕСТОПОЛОЖЕНИЕ")
	       
	       self.result= 1
            
            
            
              
    
	  def task_generator(self):
	       if self.pag == 1:
                    yield Task ('post',url=self.f+'/',refresh_cache=True,network_try_count=100)
               else:
	            for x in range(1,int(self.pag)+1):
	                 yield Task ('post',url=self.f+'/?page=%d'%x,refresh_cache=True,network_try_count=100)
	          
	       
            
	  def task_post(self,grab,task):
	       links = grab.doc.select(u'//td[@class="relative"]/a[1]')
	       for elem in links:
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
     
	  def task_item(self, grab, task):
	       try:
		    ray = grab.doc.select(u'//div[@class="clr"]/h3').text()
	       except IndexError:
		    ray = ''          
	       try:
                    punkt = grab.doc.select(u'//div[@class="clr"]/h3').text().split(', ')[1]
	       except IndexError:
		    punkt = ''
	       try:
		    ter= grab.doc.select(u'//div[@class="clr"]/h3').text().split(', ')[2]
	       except IndexError:
		    ter =''
	       try:
		    uliza= grab.doc.select(u'//div[@class="clr"]/h3').text().split(', ')[3]
	       except (IndexError,UnboundLocalError):
		    uliza = ''
	       try:
		    dom = re.compile(r'[0-9]+$',re.S).search(ray).group(0)
	       except (IndexError,AttributeError):
		    dom = ''
		     
	      
		 
	       try:
		    metro = grab.doc.select(u'//div[@class="dbl_nav"]/a[2]').text()
		 #print rayon
	       except IndexError:
		    metro = ''
		   
	       try:
		    metro_min = grab.doc.select(u'//span[contains(text(),"Объект")]/following-sibling::p').text()
		 #print rayon
	       except IndexError:
		    metro_min = ''
		   
	       try:
		    metro_tr = grab.doc.select(u'//span[@class="object_item_metro_comment"]').text().split(u'мин. ')[1]
	       except IndexError:
		    metro_tr = ''
	       try:
		    price = grab.doc.select(u'//h2[@class="red"]').text()
		 #print price + u' руб'	    
	       except IndexError:
		    price = ''
    
	       try:
		    plosh_ob = grab.doc.select(u'//h2[contains(text(),"Площадь")]/following-sibling::div').text().replace(u'Площадь участка: ','')
	       except IndexError:
		    plosh_ob = ''
     
	       
		    
	       try:
		    et = grab.doc.select(u'//th[contains(text(),"Газоснабжение")]/following-sibling::td').text()
		 #print price + u' руб'	    
	       except IndexError:
		    et = '' 
		   
	       try:
		    etagn = grab.doc.select(u'//span[contains(text(),"Дата последнего изменения:")]').text().split(', ')[1]
               except IndexError:
		    etagn = ''
		     
	       
		
		     
	       try:
		    opis = grab.doc.select(u'//div[@itemprop="description"]').text() 
	       except IndexError:
		    opis = ''
		
	       try:
		    phone = re.sub('[^\d]','',grab.doc.select(u'//a[@class="show-phone"]').attr('data-phone'))
	       except IndexError:
		    phone = ''
		   
	       try:
		    lico = grab.doc.select(u'//span[contains(text(),"Добавил(а)")]/following-sibling::p').text()
	       except IndexError:
		    lico = ''
		    
	       try:
		    comp = grab.doc.select(u'//td[contains(text(),"Агентство:")]/following-sibling::td').text()
		 #print rayon
	       except IndexError:
		    comp = ''
		    
	       try:
		    data = grab.doc.select(u'//span[contains(text(),"Дата публикации:")]').text().split(', ')[1]
	       except IndexError:
		    data = ''
		    
	       
		    
	       
		   
		   
	       
		   
	      
	   
	       projects = {'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt,
		           'teritor': ter,
		            'ulica':uliza.replace(dom,''),
		           'dom': dom,
		           'metro': metro,
	                   'naz': metro_min,		           
		           'tran': metro_tr,
		           'cena': price,		           
		           'plosh_ob':plosh_ob,		           
		           'etach': et,
		           'etashost': etagn,      
		           'opis':opis,
		           'url':task.url,
		           'phone':phone,
		           'lico':lico,
		           'company':comp,
		           'data':data}
	     
	     
	     
	       try:
		    ad_id= grab.doc.select(u'//h2[contains(text(),"Контакты")]/following-sibling::div').attr('data-antispam-contacts-token')
		    link = 'https://dom.yuga.ru/cgi-bin/kernel.cgi?module=antispam&act=show_details&token='+ad_id
		    headers ={'Accept': 'application/json, text/javascript, */*; q=0.01',
			      'Accept-Encoding': 'gzip,deflate',
			      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			      'Cookie': '__cfduid='+ad_id+'.',
			      'Host': 'dom.yuga.ru',
			      'Referer': task.url,
			      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			      'X-Requested-With' : 'XMLHttpRequest'} 
		    gr = Grab()
		    gr.setup(url=link,headers=headers)		    
		    yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
               except IndexError:
	            yield Task('phone',grab=gr,project=projects)	     
	     
	     
	       
	     
	  def task_phone(self, grab, task):
	       json_data = json.loads(grab.response.body)
	       try:
		    licco = json_data['owner_fio'].split(', ')[0]
	       except IndexError:
		    licco =''
	       try:
		    compan = json_data['owner_fio'].split(', ')[1]
	       except IndexError:
		    compan=''
	       try:
		    phone = re.sub('[^\d\+]','',json_data['owner_phone'])
	       except IndexError:
		    phone=''	  
	     
	       yield Task('write',project=task.project,licco=licco,compan=compan,phone=phone,grab=grab)
	     
	     
	  def task_write(self,grab,task):
	       
	       print('*'*50)	       
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['teritor']
	       print  task.project['ulica']
	       print  task.project['dom']
	      
	       print  task.project['naz']	      
	       print  task.project['tran']
	       print  task.project['cena']	       
	       print  task.project['plosh_ob']	       
	       print  task.project['etach']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.licco
	       print  task.compan
	       print  task.phone	       
	       print  task.project['data']
	       print  task.project['etashost']
	       
	 
	       self.ws.write(self.result, 0,task.project['sub'])
	       self.ws.write(self.result, 31,task.project['rayon'])
	       self.ws.write(self.result, 2,task.project['punkt'])
	       self.ws.write(self.result, 3,task.project['teritor'])
	       self.ws.write(self.result, 4,task.project['ulica'])
	       self.ws.write(self.result, 5,task.project['dom'])
	       self.ws.write(self.result, 9,task.project['metro'])
	       self.ws.write(self.result, 14,task.project['naz'])
	       #self.ws.write(self.result, 10,task.project['object'])
	       #self.ws.write(self.result, 9,oper)
	       self.ws.write(self.result, 10, task.project['cena'])
	       #self.ws.write(self.result, 13, task.project['cena_m'])
	       #self.ws.write(self.result, 14, task.project['col_komnat'])
	       self.ws.write(self.result, 12, task.project['plosh_ob'])
	       #self.ws.write(self.result, 16, task.project['plosh_gil'])
	       #self.ws.write(self.result, 17, task.project['plosh_kuh'])
	       #self.ws.write(self.result, 18, task.project['plosh_com'])
	       self.ws.write(self.result, 15, task.project['etach'])
	       self.ws.write(self.result, 29, task.project['etashost'])
	       self.ws.write(self.result, 22, task.project['opis'])
	       self.ws.write(self.result, 23, u'ЮГА.РУ')
	       self.ws.write_string(self.result, 24, task.project['url'])
	       self.ws.write(self.result, 25, task.phone)
	       self.ws.write_string(self.result, 26, task.licco)
	       self.ws.write_string(self.result, 27, task.compan)
	       self.ws.write(self.result, 28, task.project['data'])
	       self.ws.write(self.result, 30, datetime.today().strftime('%d.%m.%Y'))
	      
	       
	       print('*'*50)
	       print self.sub
	      
	       print 'Ready - '+str(self.result)
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print '***',i+1,'/',len(l),'***'
	       print  task.project['metro']
	       print('*'*50)
	       self.result+= 1
	       
	       
	       
	       
	       #if self.result > 5:
		    #self.stop()

     bot = Nedvizhka_Zem(thread_number=5,network_try_limit=2000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     bot.run()
     #print bot.sub,bot.end
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
	  break          

     
     
