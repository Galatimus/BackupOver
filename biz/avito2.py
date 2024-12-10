#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
from cStringIO import StringIO
import pytesseract
from PIL import Image 
import base64
import xlsxwriter
import os
import random
import json
import math
import re
import time
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logging.basicConfig(level=logging.DEBUG)





i = 0
l= open('Links/Avito2.txt').read().splitlines()
dc = len(l)
page = l[i]

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'	       
     class Avito_Biz(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	       while True:
                    try:
			 time.sleep(1)
			 g = Grab(timeout=5, connect_timeout=10)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')			 
                         g.go(self.f)
                         self.sub = g.doc.rex_text(u'selected >(.*?)</option>')
                         self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="breadcrumbs-link-count js-breadcrumbs-link-count"]').text())
                         self.pag = int(math.ceil(float(int(self.num))/float(50)))
                         print self.pag,self.num
                         print self.sub
			 del g
                         break
                    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
                         print g.config['proxy'],'Change proxy'
                         g.change_proxy()
			 del g
                         continue
                    	       
	       self.workbook = xlsxwriter.Workbook(u'avito/Avito_%s' % bot.sub + u'_Готовый_бизнес'+str(i)+'.xlsx')
	       self.ws = self.workbook.add_worksheet()
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, u"УЛИЦА")
	       self.ws.write(0, 4, u"ДОМ")
	       self.ws.write(0, 5, u"МЕТРО")
	       self.ws.write(0, 6, u"СФЕРА БИЗНЕСА")
	       self.ws.write(0, 7, u"СЕГМЕНТ_ГОТОВОГО_БИЗНЕСА")
	       self.ws.write(0, 8, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 9, u"ЦЕНА_ПРОДАЖИ")
	       self.ws.write(0, 10, u"ОПИСАНИЕ")
	       self.ws.write(0, 11, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 12, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 13, u"КОНТАКТЫ")
	       self.ws.write(0, 14, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 15, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 16, u"АДРЕС")
	       self.ws.write(0, 17, u"ЗАГОЛОВОК")
	      
	       self.result= 1
              
    
	  def task_generator(self):
	       for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'?p=%d'%x,refresh_cache=True,network_try_count=100)
          
        
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//a[@class="item-description-title-link"]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur	      
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)

	  def task_item(self, grab, task):
	             
	       try:
		    ray = grab.doc.select(u'//span[contains(text(),"Адрес")]/following-sibling::span').text().split(u'р-н ')[1]
	       except IndexError:
		    ray = '' 
	       try:
		    if self.sub == u'Москва':
			 punkt= u'Москва'
		    elif self.sub == u'Санкт-Петербург':
		         punkt= u'Санкт-Петербург'
		    elif self.sub == u'Севастополь':
		         punkt= u'Севастополь'
		    else:
			 punkt =  grab.doc.rex_text(u'selected >(.*?)</option>')
		 #print punkt
	       except IndexError:
		    punkt = ''
	       try:
		    metro = grab.doc.select(u'//span[contains(text(),"Адрес")]/following-sibling::span').text().split('м. ')[1]
	       except IndexError:
		    metro = ''
		    
               try:
                    seg = grab.doc.select(u'//h1').text()
               except IndexError:
                    seg =''
		    
	       try:
	            sfera = grab.doc.select(u'//div[@class="b-catalog-breadcrumbs"]/a[4]').text()
	       except IndexError:
	            sfera =''		    
	       
	       try:
		    price = grab.doc.select('//span[@class="price-value-string js-price-value-string"]').text()
		 #print price
	       except IndexError:
		    price =''
		
	       try:
		    opis = grab.doc.select('//div[@class="item-description"]/div').text() 
		 #print opis
	       except IndexError:
		    opis = ''
	       try:
	            rphone = re.sub('[^\d]','',grab.doc.select(u'//span[@class="item-phone-button-sub-text"]').text()+str(random.randint(1000000,9999999)))
	       except IndexError:
	            rphone = ''		    
	       
	       try:
                    
		    conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		             (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		             (u'июня', '.06.2019'),(u'июля', '.07.2019'),(u'августа', '.08.2018'),(u'мая', '.05.2019'),
		             (u'января', '.01.2019'),(u'февраля', '.02.2019'),(u'марта', '.03.2019'),(u'апреля', '.04.2019'),
		             (u'ноября', '.11.2018'),(u'сентября', '.09.2018'),(u'октября', '.10.2018'),(u'декабря', '.12.2018')]
		    dt= grab.doc.select(u'//div[@class="title-info-metadata-item-redesign"]').text().split(u'размещено ')[1]
		    data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','').split(u'в')[0]
		 #print data
	       except IndexError:
		    data = ''
	       try:
	            mesto = grab.doc.select(u'//span[contains(text(),"Адрес")]/following-sibling::span').text()
	       except IndexError:
	            mesto =''
		    
	       clearText = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", opis)
	       clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText)
	       
	       
	       projects = {'sub': self.sub,
	                   'rayon': ray,
		           'punkt': punkt,
		           'metro': metro,
		           'cena': price,
		           'seg': seg,
	                   'sfera': sfera,
	                   'opis': clearText,
	                   'mesto': mesto,
	                   'phone2':rphone,
		           'url': task.url,
		            'data':data.replace('20182018','2018')
		           }
	       try:
		    #ad_id= re.sub(u'[^\d]','',task.url[-9:])
		    ad_id = re.sub(u'[^\d]','',grab.doc.rex_text(u'prodid(.*?)price'))
		    ad_phone = re.sub(u'[^0-9a-z]','',grab.doc.rex_text(u'avito.item.phone(.*?);'))
		    ad_subhash = re.findall(r'[0-9a-f]+', ad_phone)
		    if int(ad_id) % 2 == 0:
			 ad_subhash.reverse()
		    ad_subhash = ''.join(ad_subhash)[::3]
		    link = 'https://www.avito.ru/items/phone/'+ad_id+'?pkey='+ad_subhash
		    headers ={'Accept': 'application/json, text/javascript, */*; q=0.01',
			      'Accept-Encoding': 'gzip,deflate',
			      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			      'Cookie': 'sessid='+ad_id+'.'+ad_subhash,
			      'Host': 'www.avito.ru',
			      'Referer': task.url,
			      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			      'X-Requested-With' : 'XMLHttpRequest'}
		    gr = Grab()
		    gr.setup(url=link,headers=headers)
                    yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=10)
               except IndexError:
                    yield Task('phone',grab=grab,project=projects)
		    
		    
		    
	  def task_phone(self, grab, task):
	       	       
	       try:
		    #json_data = json.loads(grab.response.body)
		    data_image64 = grab.doc.json['image64'].replace('data:image/png;base64,','') 
		    imgdata = base64.b64decode(data_image64)
		    im = Image.open(StringIO(imgdata))
		    x,y = im.size
		    phon = pytesseract.image_to_string(im.convert("RGB").resize((int(x*2), int(y*3)),Image.BICUBIC))
		    del im
	       except (IndexError,ValueError,IOError):
		    phon = ''
		    
	       phone=re.sub(u'[^\d]','',phon)
	       if phone == '05':
	            phone = task.project['phone2']		    
	  
	       yield Task('write',project=task.project,phone=phone,grab=grab)
	
     
	
	  def task_write(self,grab,task):
	       
	       if task.phone <> '':
		    
		    print('*'*100)	
		    print  task.project['sub']
		    print  task.project['rayon']
		    print  task.project['punkt']
		    print  task.project['metro']
		    print  task.project['seg']
		    print  task.project['cena']
		    print  task.project['opis']
		    print  task.project['url']
		    print  task.phone
		    print  task.project['data']
		    print  task.project['mesto']
		    print  task.project['sfera']
		    
	       
		    
		    
	  
		    self.ws.write(self.result, 0, task.project['sub'])
		    self.ws.write(self.result, 1, task.project['rayon'])
		    self.ws.write(self.result, 2, task.project['punkt'])
		    self.ws.write(self.result, 5, task.project['metro'])
		    self.ws.write(self.result, 6, task.project['sfera'])
		    self.ws.write(self.result, 7, task.project['seg'])
		    self.ws.write(self.result, 17, task.project['seg'])
		    self.ws.write(self.result, 8, u'Продажа')
		    self.ws.write(self.result, 9, task.project['cena'])
		    self.ws.write(self.result, 10, task.project['opis'])
		    self.ws.write(self.result, 11, u'AVITO.RU')
		    self.ws.write_string(self.result, 12, task.project['url'])
		    self.ws.write(self.result, 13, task.phone)
		    self.ws.write(self.result, 14, task.project['data'])	       
		    self.ws.write(self.result, 15, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result, 16, task.project['mesto'])	      
		   
		    
		    
		    print('*'*100)
		    print self.sub
		    print 'Ready - '+str(self.result)+'/'+str(self.num)
		    print 'Tasks - %s' % self.task_queue.size() 
		    print '***',i+1,'/',dc,'***'
		    print('*'*100)
		    self.result+= 1
	       
		    #if self.result >= 50:
			 #self.stop()
			 
	       
	            if str(self.result) == str(self.num):
		         self.stop() 
	

     bot = Avito_Biz(thread_number=5, network_try_limit=1000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=5, connect_timeout=5)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(1)
     print('Save it...')
     command = 'mount -a'
     os.system('echo %s|sudo -S %s' % ('1122', command))
     time.sleep(2)
     bot.workbook.close()
     print('Done')
  
     time.sleep(1)
     i=i+1
     try:
          page = l[i]
     except IndexError:
	  break
	 
       
     
     
     