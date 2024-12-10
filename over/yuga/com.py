#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging


#from PIL import Image
import os
import json
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






i = 0
l= open('com.txt').read().splitlines()
page = l[i]





while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'	       
     class move_Com(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	      
               while True:
                    try:
                         time.sleep(2)
			 g = Grab(timeout=10, connect_timeout=20)
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
		    
	       self.workbook = xlsxwriter.Workbook(u'com/Dom-Yuga_%s' % bot.sub + u'_Коммерческая_'+str(i+1)+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Коммерческая')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
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
	       self.ws.write(0, 32, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 33, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 34, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 35, u"МЕСТОПОЛОЖЕНИЕ")
	      
	       self.result= 1
	       
                
                
                
                
	  def task_generator(self):
	       if self.pag == 1:
		    yield Task ('post',url=self.f+'/',refresh_cache=True,network_try_count=100)
	       else:
		    for x in range(1,int(self.pag)+1):
                         yield Task ('post',url=self.f+'/?page=%d'%x,refresh_cache=True,network_try_count=100)
          
        
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//td[@class="relative"]/a[1]'):
		    ur = grab.make_url_absolute(elem.attr('href'))
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True, network_try_count=100)
	      
            
	 
        
	  def task_item(self, grab, task):
	       try:
	            mesto = grab.doc.select(u'//div[@class="clr"]/h3').text()
	       except IndexError:
	            mesto =''
		    
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
		    uliza =''
               try:
                    dom = re.compile(r'[0-9]+$',re.S).search(mesto).group(0)
		  
               except (IndexError,AttributeError):
                    dom = ''
	         
               try:
                    tip = grab.doc.select(u'//td[contains(text(),"Планировка")]/following-sibling::td').text()
               except IndexError:
                    tip = ''
               try:
                    naz = grab.doc.select(u'//span[contains(text(),"Назначение")]/following::div[2]').text()
               except IndexError:
                    naz =''
               try:
                    klass =  grab.doc.select(u'//div[@class="dbl_nav"]/a[2]').text()
               except IndexError:
                    klass = ''
               try:
                    price = grab.doc.select(u'//h2[@class="red"]').text()
               except IndexError:
                    price =''
               try: 
                    plosh = grab.doc.select(u'//h2[contains(text(),"Площадь")]/following-sibling::div').text()
               except IndexError:
                    plosh=''
               try:
                    ohrana = grab.doc.select(u'//span[contains(text(),"Этажность")]/following::div[2]').text()
               except IndexError:
                    ohrana =''
               try:
                    gaz =  grab.doc.select(u'//dt[@itemprop="name"][contains(text(),"Материал стен")]/following-sibling::dd').text()
               except IndexError:
                    gaz =''
               try:
                    voda =  grab.doc.select(u'//h4').text().split('/')[1]
               except IndexError:
                    voda =''
               try:
                    kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
               except IndexError:
                    kanal =''
               try:
                    elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
               except DataNotFound:
                    elek =''
               try:
                    teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
               except DataNotFound:
                    teplo =''
               #time.sleep(1)
	       try:
		    opis = grab.doc.select(u'//div[@itemprop="description"]').text() 
	       except IndexError:
	            opis = ''
               try:
		    lico = grab.doc.select(u'//div[@class="phone"]/preceding-sibling::div[@class="name"]').text()
	       except IndexError:
                    lico = ''
               try:
                    comp = grab.doc.select(u'//span[contains(text(),"Дата последнего изменения:")]').text().split(', ')[1]
               except IndexError:
                    comp = ''
               
	       try: 
		    data = grab.doc.select(u'//span[contains(text(),"Дата публикации:")]').text().split(', ')[1]
	       except IndexError:
		    data=''
		    
	      
          
	       
		    
     
	
               projects = {'sub': self.sub,
	                  'adress': mesto,
	                   'terit':ter, 
	                   'punkt':punkt, 
	                   'ulica':uliza.replace(dom,''),
	                   'dom':dom,
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
	                   'lico':lico,
	                   'company': comp,
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
	       #time.sleep(1)
	       print('*'*100)	       
	       print  task.project['sub']
	       print  task.project['punkt']
	       print  task.project['terit']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['tip']
	       print  task.project['naz']
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
	       print  task.licco
	       print  task.compan
	       print  task.phone
	       print  task.project['company']
	       print  task.project['data']
	       print  task.project['adress']
	       
	      
	      
	  
	       
	       
     
	       self.ws.write(self.result, 0, task.project['sub'])
	       #self.ws.write(self.result, 1, task.project['adress'])
	       self.ws.write(self.result, 3, task.project['terit'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 4, task.project['ulica'])
	       self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 8, task.project['tip'])
	       self.ws.write(self.result, 9, task.project['naz'])
	       self.ws.write(self.result, 34, task.project['klass'])
	       self.ws.write(self.result, 11, task.project['cena'])
	       self.ws.write(self.result, 12, task.project['plosh'])
	       self.ws.write(self.result, 14, task.project['ohrana'])
	       self.ws.write(self.result, 16, task.project['gaz'])
	       self.ws.write(self.result, 35, task.project['voda'])
	       self.ws.write(self.result, 22, task.project['kanaliz'])
	       self.ws.write(self.result, 23, task.project['electr'])
	       #self.ws.write(self.result, 24, task.project['teplo'])
	       self.ws.write(self.result, 25, task.project['opis'])
	       self.ws.write(self.result, 26, u'ЮГА.РУ')
	       self.ws.write_string(self.result, 27, task.project['url'])
	       self.ws.write(self.result, 28, task.phone)
	       self.ws.write_string(self.result, 29, task.licco)
	       self.ws.write_string(self.result, 30, task.compan)
	       self.ws.write(self.result, 31, task.project['data'])
	       self.ws.write(self.result, 32, task.project['company'])
	       self.ws.write(self.result, 33, datetime.today().strftime('%d.%m.%Y'))
	       #self.ws.write(self.result, 33, oper)
	       self.ws.write(self.result, 35, task.project['adress'])
			     
	       print('*'*100)
	       #print self.sub
	       print 'Ready - '+str(self.result)
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print '***',i+1,'/',len(l),'***'
	       print  task.project['klass']
	       print('*'*100)
	       self.result+= 1
	       
	      
	       
	       
	       
	       #if self.result >= 10:
	            #self.stop()	       

     bot = move_Com(thread_number=5, network_try_limit=2000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(2)
     print('Save it...')    
     command = 'mount -a'#'mount -t cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
     p = os.system('echo %s|sudo -S %s' % ('1122', command))
     print p
     time.sleep(10)
     bot.workbook.close()
     #workbook.close()
     print('Done!')
     i=i+1
     try:
          page = l[i]
     except IndexError:
          break
       
     
     
     