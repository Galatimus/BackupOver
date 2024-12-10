#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
import time
import os
import math
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logging.basicConfig(level=logging.DEBUG)



i = 0
l= open('Links/Zem.txt').read().splitlines()

page = l[i] 
oper = u'Продажа'





while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'
     class Nedvizhka_Zem(Spider):
	  def prepare(self):
	       self.f = page
	       #self.link =l[i]
	       for p in range(1,51):
		    try:
                         time.sleep(2)
			 g = Grab(timeout=20, connect_timeout=50)
			 g.proxylist.load_file(path='../ivan.txt',proxy_type='http')			 
                         g.go(self.f)
			 if g.doc.select(u'//div[@class="navigation"]').exists()==True:
			      print g.doc.code
                              self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="search-count"]').text())
			      self.pag = str(float(math.ceil(float(int(self.num))/float(20)))).replace('.0','')
			      self.sub = g.doc.select(u'//li[@class="has-child"]/a').text()
			      print self.sub,self.pag,self.num
			      del g
			      break
			 else:
                              print 'Ждемс...'
                              time.sleep(60)
                              del g
                              continue
		    except(GrabTimeoutError,GrabNetworkError,IndexError,GrabConnectionError):
		         print g.config['proxy'],'Change proxy'
		         g.change_proxy()
			 del g
		         continue
                    
	       else:
	            self.sub = ''
	            self.pag = 0
	            self.num=1	       
	       
	       self.workbook = xlsxwriter.Workbook(u'zem/Nedvizhka_%s' % self.sub + u'_Земля_'+str(i+1)+ '.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Nedvizhka_Земля')
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
	       self.ws.write(0, 31, u"ШИРОТА_ИСХ")
	       self.ws.write(0, 32, u"ДОЛГОТА_ИСХ")	       
	       
	       self.result= 1
            
            
            
              
    
	  def task_generator(self):
	       for x in range(1,int(self.pag)+1):
                    yield Task ('post',url=self.f+'?page=%d'%x+'&grid_type=table',refresh_cache=True,network_try_count=50)
	          
	       
            
	  def task_post(self,grab,task):
	       links = grab.doc.select(u'//tr[@class="property"]/td[3]/a')
	       for elem in links:
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=50)
     
	  def task_item(self, grab, task):
	       try:
		    ray = grab.doc.select(u'//header[@class="property-title"]/figure/a[2]').text()
	       except IndexError:
		    ray = ''          
	       try:
		    punkt= grab.doc.select(u'//header[@class="property-title"]/figure/a[1]').text().replace(self.sub,'')
	       except IndexError:
		    punkt = ''
	       try:
		    ter= grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Микрорайон")]/following-sibling::dd').text()
	       except IndexError:
		    ter =''
	       try:
		    uliza = grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Улица")]/following-sibling::dd').text()
	       except IndexError:
		    uliza = ''
	       try:
		    dom = grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Номер дома")]/following-sibling::dd').number()
	       except IndexError:
		    dom = ''
		     
	       try:
		    orentir = grab.doc.select(u'//label[contains(text(),"Жилой комплекс:")]/following-sibling::p').text()
	       except IndexError:
		    orentir = ''              
		 
	       try:
		    metro = grab.doc.select(u'//h4').text().split('/')[1]
		 #print rayon
	       except IndexError:
		    metro = ''
		   
	       try:
		    metro_min = grab.doc.select(u'//dt[contains(text(),"Тип участка")]/following-sibling::dd[1]').text()
		 #print rayon
	       except IndexError:
		    metro_min = ''
		   
	       try:
		    metro_tr = grab.doc.select(u'//span[@class="object_item_metro_comment"]').text().split(u'мин. ')[1]
	       except IndexError:
		    metro_tr = ''

	       try:
		    price = grab.doc.select(u'//dt[contains(text(),"Цена")]/following-sibling::dd[1]').text()
		 #print price + u' руб'	    
	       except IndexError:
		    price = ''

     
	       try:
		    try:
		         plosh_ob = grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Площадь общая")]/following-sibling::dd[1]').text()
		    except IndexError:
			 plosh_ob = grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Площадь земли")]/following-sibling::dd[1]').text()
	       except IndexError:
		    plosh_ob = ''
     
	       
		    
	       try:
		    et = grab.doc.select(u'//th[contains(text(),"Газоснабжение")]/following-sibling::td').text()
		 #print price + u' руб'	    
	       except IndexError:
		    et = '' 
		   
	       try:
		    etagn = grab.doc.select(u'//dt[contains(text(),"Обновленно")]/following-sibling::dd[1]').text()
		 #print price + u' руб'	    
	       except IndexError:
		    etagn = ''

		     
	       try:
		    opis = grab.doc.select(u'//p[@itemprop="description"]').text() 
	       except IndexError:
		    opis = ''
		
	       try:
		    phone = grab.doc.select(u'//dt[contains(text(),"Телефон")]/following-sibling::dd').text()
	       except IndexError:
		    phone = ''
		   
	       try:
		    try:
	                 lico = grab.doc.select(u'//div[@class="agent-contact-info"]/div/h3').text()
		    except IndexError: 
	                 lico = grab.doc.select(u'//dt[contains(text(),"Агент")]/following-sibling::dd[1]').text()
	       except IndexError:
		    lico = ''
		    
	       try:
		    comp = grab.doc.select(u'//dd[contains(text(),"Организация")]/following-sibling::dt[1]').text()
		 #print rayon
	       except IndexError:
		    comp = ''
		    
	       try:
		    data = grab.doc.select(u'//dt[contains(text(),"Дата подачи")]/following-sibling::dd[1]').text()
	       except IndexError:
		    data = ''
		    
		    
	       try:
		    lat = grab.doc.rex_text(u'data-geo="(.*?)"').split(';')[0]
	       except IndexError:
		    lat =''
		    
	       try:
		    lng = grab.doc.rex_text(u'data-geo="(.*?)"').split(';')[1]
	       except IndexError:
	            lng =''		    
		    
	       
		    
	       
		   
		   
	       
		   
	      
	   
	       projects = {'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt,
		           'teritor': ter,
		           'ulica': uliza,
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
	                   'dol': lat,
	                   'shir': lng,	                   
		           'lico':lico,
		           'company':comp,
		           'data':data}
	     
	     
	     
	       yield Task('write',project=projects,grab=grab)
	     
	     
	     
	     
	     
	     
	  def task_write(self,grab,task):
	       
	       print('*'*50)	       
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['teritor']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['metro']
	       print  task.project['naz']	      
	       print  task.project['tran']
	       print  task.project['cena']	       
	       print  task.project['plosh_ob']	       
	       print  task.project['etach']
	       print  task.project['etashost']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.project['data']
	       
	 
	       self.ws.write(self.result, 0,task.project['sub'])
	       self.ws.write(self.result, 1,task.project['rayon'])
	       self.ws.write(self.result, 2,task.project['punkt'])
	       self.ws.write(self.result, 3,task.project['teritor'])
	       self.ws.write(self.result, 4,task.project['ulica'])
	       self.ws.write(self.result, 5,task.project['dom'])
	       self.ws.write(self.result, 11,task.project['metro'])
	       self.ws.write(self.result, 14,task.project['naz'])
	       #self.ws.write(self.result, 10,task.project['object'])
	       self.ws.write(self.result, 9,oper)
	       self.ws.write(self.result, 10, task.project['cena'])
	       #self.ws.write(self.result, 13, task.project['cena_m'])
	       #self.ws.write(self.result, 14, task.project['col_komnat'])
	       self.ws.write(self.result, 12, task.project['plosh_ob'])
	       #self.ws.write(self.result, 16, task.project['plosh_gil'])
	       self.ws.write(self.result, 31, task.project['dol'])
	       self.ws.write(self.result, 32, task.project['shir'])
	       self.ws.write(self.result, 15, task.project['etach'])
	       self.ws.write(self.result, 29, task.project['etashost'])
	       self.ws.write(self.result, 22, task.project['opis'])
	       self.ws.write(self.result, 23, u'Nedvizhka.RU')
	       self.ws.write_string(self.result, 24, task.project['url'])
	       self.ws.write(self.result, 25, task.project['phone'])
	       self.ws.write(self.result, 26, task.project['lico'])
	       self.ws.write(self.result, 27, task.project['company'])
	       self.ws.write(self.result, 28, task.project['data'])
	       self.ws.write(self.result, 30, datetime.today().strftime('%d.%m.%Y'))
	      
	       
	       print('*'*50)
	       print self.sub
	      
	       print 'Ready - '+str(self.result)+'/'+self.num
	       print 'Tasks - %s' % self.task_queue.size()
	       print '***',i+1,'/',len(l),'***'
	       print oper
	       print('*'*50)
	       self.result+= 1
	       
	       
	       
	       
	       #if self.result > 10:
		    #self.stop()
		    
		    
		    
               if int(self.result) >= int(self.num)-1:
                    self.stop()
		    
		    
		    
     
     bot = Nedvizhka_Zem(thread_number=5,network_try_limit=500)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=500, connect_timeout=500)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(1)
     print('Save it...') 
     command = 'mount -a'
     os.system('echo %s|sudo -S %s' % ('1122', command))
     time.sleep(2)
     bot.workbook.close()
     print('Done')
     
     i=i+1
     try:
          page = l[i]
     except IndexError:
          break

time.sleep(5)
os.system("/home/oleg/pars/nedv/comm.py")
