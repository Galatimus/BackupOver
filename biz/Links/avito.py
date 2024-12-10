#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import requests
import xlsxwriter
import re
import time
from datetime import datetime,timedelta


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab(timeout=20, connect_timeout=20)

g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')


i = 0
l= open('Links/Avito.txt').read().splitlines()
dc = len(l)
page = l[i]

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'	       
     class Avito_Biz(Spider):
	  def prepare(self):
	       self.pg = 1
	       self.f = page
	       self.link =l[i]
	       
	       self.agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
	                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
	                      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
	                      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
	                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0',
	                      'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
	                      'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
	                      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
	                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
	                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	                      'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
	                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
	                      'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
	                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
	                      'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
	                      'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
	                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
	                      'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
	                      'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
	                      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
	                      'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
	                      'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
	                      'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
	                      'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
	                      'Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0',
	                      'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
	                      'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0',
	                      'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
	                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	                      'Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62',
	                      'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62',
	                      'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
	                      'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1',
	                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0)  Gecko/20100101 Firefox/18.0',
	                      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
	                      'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
	                      'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51',
	                      'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0',
	                      'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
	                      'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
	                      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
	                      'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)',
	                      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
	                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)',
	                      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	                      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
	                      'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2',
	                      'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
	                      'Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50',
	                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
	                      'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
	                      'Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11',
	                      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/537.11',
	                      'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11',
	                      'Mozilla/5.0 (Windows NT 6.0) yi; AppleWebKit/345667.12221 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/453667.1221',
	                      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
	                      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
	                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
	                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1',
	                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
	                      'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
	                      'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
	                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:14.0) Gecko/20120405 Firefox/14.0a1',
			      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
			      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
	                      ]
	       self.g = 0
	       
               while True:
                    try:
                         g.go(self.f)
                         self.sub = g.doc.select(u'//i[@class="avico avico-geo-blue"]/following::text()').text()
                         print self.sub
                         break
                    except(GrabTimeoutError,GrabNetworkError, GrabConnectionError):
                         print g.config['proxy'],'Change proxy'
                         g.change_proxy()
                         continue
                    except DataNotFound:
                         time.sleep(5)
                         print g.config['proxy'],'Change > proxy'
                         g.change_proxy()
                         continue
	       
	       
	       self.workbook = xlsxwriter.Workbook(u'avito/Avito_%s' % bot.sub + u'_Готовый_бизнес.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Авито')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, u"УЛИЦА")
	       self.ws.write(0, 4, u"ДОМ")
	       self.ws.write(0, 5, u"МЕТРО")
	       self.ws.write(0, 6, u"ДО_МЕТРО")
	       self.ws.write(0, 7, u"СЕГМЕНТ_ГОТОВОГО_БИЗНЕСА")
	       self.ws.write(0, 8, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 9, u"ЦЕНА_ПРОДАЖИ")
	       self.ws.write(0, 10, u"ОПИСАНИЕ")
	       self.ws.write(0, 11, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 12, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 13, u"КОНТАКТЫ")
	       self.ws.write(0, 14, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 15, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 16, u"ДАТА_СБОРА")
	      
	       self.result= 1
              
    
	  def task_generator(self):
	       
	       yield Task ('post',url=self.f,refresh_cache=True,network_try_count=100)
          
        
	  def task_post(self,grab,task):
	       
	       try:
		    num = re.sub("[^0-9]", "",grab.doc.select('//div[@class="nav-helper-content nav-helper-text"]').text())
		 #pag = str(float(math.ceil(float(int(num))/float(20)))).replace('.0','')
	       except DataNotFound:
		    #pag = ''
		    num = ''
	       for elem in grab.doc.select('//form[@class][@data-favorite="false"]/following-sibling::a[@class="item-link"]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur	      
		    yield Task('item', url=ur,num=num,refresh_cache=True,network_try_count=100)
	       
	       yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	  
        
        
        
            
	  def task_page(self,grab,task):
	       try:
		    pg = grab.doc.select(u'//li[@class="page page-next"]/a')
		    u = grab.make_url_absolute(pg.attr('href'))
		    yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	       except DataNotFound:
		    print('*'*100)
		    print '!!!','NO PAGE NEXT','!!!'
		    print('*'*100)
		    logger.debug('%s taskq size' % self.task_queue.size())
	  
     
	  
        
	  def task_item(self, grab, task):
	       try:
		    subect = grab.doc.rex_text(u'купить в (.*?) на Avito')
               except DataNotFound:
		    subect =''
	       
	       try:
		    d = grab.doc.select('//span[@class="avito-address-text"]').text()
		    if d.find(u'р-н') > 0:
		         ray = re.sub('^.*,', '', d)[5:]
		    else:
		         ray = ''
		 #print ray 
	       except DataNotFound:
		    ray = '' 
	       try:
		    punkt = self.sub#re.sub(',.*$', '', grab.doc.select('//span[@class="avito-address-text"]').text().replace(self.sub +', ',''))
		 #print punkt
	       except DataNotFound:
		    punkt = ''
	       try:
		    metro = grab.doc.select(u'//span[@class="avito-address-text"][contains(text(),"м.")]').text().split(', ')[1]
	       except IndexError:
		    metro = ''
		    
               try:
                    seg = grab.doc.select(u'//header[@class="single-item-header b-with-padding"]').text()
               except DataNotFound:
                    seg =''
	       
	       try:
		    price = grab.doc.select('//div[@class="info-price"]/span[@class="price-value"]').text()
		 #print price
	       except DataNotFound:
		    price =''
		
	       try:
		    opis = grab.doc.select('//div[@class="description-preview-wrapper"]/p').text() 
		 #print opis
	       except DataNotFound:
		    opis = ''
	       
	       try:
                    
		    conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		             (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		             (u'июня', '.06.2016'),(u'июля', '.07.2016'),(u'августа', '.08.2016'),
		             (u'ноября', '.11.2015'),(u'сентября', '.09.2016')]
		    dt= grab.doc.rex_text(u'Размещено(.*?)<')
		    data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')[0:10].replace(u'в','')
		 #print data
	       except DataNotFound:
		    data = ''
               time.sleep(7)
	       try:
		    ph = grab.doc.select('//div[@class="clearfix"]/a[@rel="nofollow"]')
		    url_phone = grab.make_url_absolute(ph.attr('href'))+'?async'
		    pkey = grab.doc.rex_text(u'Объявление №(.*?)<')
		    key = grab.doc.rex_text(u'/phone/(.*?)"')
		  
		    headers ={'Accept': 'application/json, text/javascript, */*; q=0.01',
		                 'Accept-Encoding': 'gzip,deflate',
		                 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		                 'Cookie': 'sessid='+key+'.'+pkey, 
		                 'Host': 'm.avito.ru',
		                 'Referer': task.url,
		                 'User-Agent': self.agent[self.g], 
		                 'X-Requested-With' : 'XMLHttpRequest'
		              } 
		    r= requests.get(url_phone,headers=headers,verify=True,allow_redirects=False,timeout=10000)
		    phone = re.sub('[^\d]', u'',r.content)[:11]
		 
	       except DataNotFound:
		    phone = ''
	       
	       if self.g == 76:
		    self.g = 0
		    #yield Task ('proxy',grab=grab,use_proxylist=False)
	       else:
		    self.g+= 1
	     
          
               	     
	  
	       projects = {'sub': self.sub,
	                   'subeck':subect,
		           'rayon': ray,
		           'punkt': punkt,
		           'metro': metro,
		           'cena': price,
		           'seg': seg,
	                   'opis': opis,
		           'url': task.url,
		           'phone': phone,
		           'koll':task.num,
		           'data':data
		           }
          
	  
	       yield Task('write',project=projects,grab=grab)
	
     
	
	  def task_write(self,grab,task):
	       #time.sleep(1)
	       print('*'*100)	
	       print  task.project['subeck']
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['metro']
	       print  task.project['seg']
	       print  task.project['cena']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['data']
	       
	  
	       
	       
     
	       self.ws.write(self.result, 0, task.project['subeck'])
	       self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 5, task.project['metro'])
	       self.ws.write(self.result, 7, task.project['seg'])
	       self.ws.write(self.result, 8, u'Продажа')
	       self.ws.write(self.result, 9, task.project['cena'])
	       self.ws.write(self.result, 10, task.project['opis'])
	       self.ws.write(self.result, 11, u'AVITO.RU')
	       self.ws.write_string(self.result, 12, task.project['url'])
	       self.ws.write(self.result, 13, task.project['phone'])
	       self.ws.write(self.result, 14, task.project['data'])	       
	       self.ws.write(self.result, 15, task.project['data'])
	       self.ws.write(self.result, 16, datetime.today().strftime('%d.%m.%Y'))
	      
	       
	       
	       print('*'*100)
	       print self.sub
	       print 'Ready - '+str(self.result)+'/'+task.project['koll']
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print '***',i+1,'/',dc,'***'
	       print('*'*100)
	       self.result+= 1
	       
	       
	       
	       if self.result > 2000:
	            self.stop()	       
	

     bot = Avito_Biz(thread_number=1, network_try_limit=2000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     bot.run()
     print bot.sub
     print(u'Спим 3 сек...')
     time.sleep(3)
     print(u'Сохранение...')
     bot.workbook.close()
     print('Done!')
     time.sleep(1)
     i=i+1
     try:
          page = l[i]
     except IndexError:
	  break
	 
       
     
     
     