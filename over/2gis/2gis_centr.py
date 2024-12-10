#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,GrabConnectionError 
import re
from grab import Grab
import logging
from sub import conv
import time
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

g = Grab(timeout=20, connect_timeout=20)

#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')

i = 0
l= open('new1.txt').read().splitlines()
dc = len(l)
page = l[i]

#b = 1
#z = ['торговые центры','бизнес-центры','торгово-развлекательные центры','торгово-офисный центр']
#for line in z:
     #print b,'-',line
     #b += 1
#t=int(input('Выберите тип построки (введите число) и нажмите Enter :'))
#zap = z[t-1]
zap = 'Агентства недвижимости'
print 'Запрос - '+zap

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'	 
     class gis(Spider): 
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
			 g.go(page)
			 self.gor = g.doc.select(u'//div[@class="tools__group"]/div[@class="tools__btn tools__city"]').text()
			 dt = self.gor
			 self.sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
			 print self.gor
			 print self.sub
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
	       self.workbook = xlsxwriter.Workbook(u'Total/2Gis_%s' % bot.gor +'_'+ zap+ u'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'2Gis'+'_'+bot.gor)
	       self.ws.write(0, 0,u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 2, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 3, u"АДРЕС")
	       self.ws.write(0, 4, u"СЕГМЕНТ")
	       self.ws.write(0, 5, u"ТИП_ОБЪЕКТА")
	       self.ws.write(0, 6, u"ТИП_ЗДАНИЯ")
	       self.ws.write(0, 7, u"КОЛЛИЧЕСТВО_ЭТАЖЕЙ")
	       self.ws.write(0, 8, u"НАИМЕНОВАНИЕ_ОБЪЕКТА")
	       self.ws.write(0, 9, u"ТЕЛЕФОН")
	       self.ws.write(0, 10, u"САЙТ_ОБЪЕКТА")
	       self.ws.write(0, 11, u"ОПИСАНИЕ")
	       self.ws.write(0, 12, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 13, u"ССЫЛКА_НА_ОБЪЕКТ")
	       self.ws.write(0, 14, u"ДАТА_СБОРА_ИНФОРМАЦИИ")
	       self.ws.write(0, 15, u"НАИМЕНОВАНИЕ_ПРОДАВЦА")
	       
	       
	       self.result= 1
	      
          def task_generator(self):
	       yield Task ('post',url = page+zap,refresh_cache=True,network_try_count=100)
		    
	  def task_post(self,grab,task):
	       for elem in grab.doc.select(u'//h3[@class="miniCard__headerTitle"]/a'):
	            #ur1 = re.sub('queryState.*$','',grab.make_url_absolute(elem.attr('href'))).replace('?','')
		    ur1 = grab.make_url_absolute(elem.attr('href'))
		    if ur1.find(u'stop')<0:
			 ur=ur1
	                 #print ur
	                 yield Task('item', url=ur,refresh_cache=True)
	       yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
		    
	  def task_page(self,grab,task):
	       try:
		    pg = grab.doc.select(u'//span[@class="pagination__page _current"]/following-sibling::a[1]')
		    u = grab.make_url_absolute(pg.attr('href'))
		    yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	       except IndexError:
		    print('*'*50)
		    print '!!!','NO PAGE NEXT','!!!'
		    print('*'*50)
		    logger.debug('%s taskq size' % self.task_queue.size())	
	       
	       
          
		    
          def task_item(self, grab, task):
	       
	             
               try:
                    phone =  re.sub(u'[^\d\+]','',grab.doc.select(u'//a[@class="contact__phonesItemLink"]').text())
		    
               except IndexError:
                    phone = ''
               try:
                    ter = grab.doc.select(u'//div[contains(text(),"район")]').text().split(u' район')[0]
               except IndexError:
                    ter = ''
               try:
                    try:
                         try:
                              adr = grab.doc.select(u'//address[@class="card__address"]').text().replace(', ',',')
                         except IndexError:
                              adr = grab.doc.select(u'//div[@class="firmCard__address"]').text().replace(', ',',')
                    except IndexError:
                         adr = grab.doc.select(u'//address[@class="geoCard2__address"]').text().replace(', ',',')
               except IndexError:
                    adr =''
               try:
                    tip_ob = grab.doc.select(u'//h1[@class="cardHeader__headerNameText"]').text().split(u', ')[1]
               except IndexError:
                    tip_ob = ''
		    
               try:
		    g2 = grab.clone(proxy_auto_change=True)
		    g2.go(page+adr)
		    #lin = []
		    #for s in g2.doc.select(u'//div[@class="miniCard__additional"]'):#.text()#.split(', ')[0]
			 #lin.append(s.text())
		    #result=[v for i,v in enumerate(lin) if v not in lin[:i]] 
		    #tip_zd = ','.join(result) 
		    tip_zd = g2.doc.select(u'//div[@class="miniCard__additional"]').text().replace(u'МагазинПодкачка колесТуалет',u'Административное здание')
                    url_zd = g2.make_url_absolute(g2.doc.select('//a[@class="miniCard__headerTitleLink"]').attr('href'))
		    #g2.go(url_zd)
		    #et = g.doc.select(u'//div[@class="cardFeatures__item"]/div[contains(text(),"этаж")]').text().split(', ')[1]
               except (GrabTimeoutError,GrabNetworkError,GrabConnectionError,IndexError):
                    tip_zd = ''
		    url_zd =''
		    #et =''
               try:
		    try:
                         et = grab.doc.select(u'//div[@class="card__shortBuildingInfo"]').text()
		    except IndexError:
                         et = grab.doc.select(u'//div[@class="cardFeatures__item"]/div[contains(text(),"этаж")]').text().split(', ')[1]
               except IndexError:
                    et = ''
		    
               try:
		    try:
                         name = grab.doc.select(u'//h1[@class="cardHeader__headerNameText"]').text()
	            except IndexError:
		         name = grab.doc.select(u'//h1[@class="geoCard2__name"]').text()
               except IndexError:
                    name = ''
		    
               try:
                    web = grab.doc.select(u'//div[@class="contact__link _type_website"]/a').text()
               except IndexError:
                    web = ''
		    
               try:
		    url_opis = grab.doc.select(u'//div[@class="card__adsIn"]/a').attr('href')
		    g2 = grab.clone(proxy_auto_change=True)
		    g2.go(url_opis)
		    opis = g2.doc.select(u'//div[@class="articleCard__content"]').text()
               except (GrabTimeoutError,GrabNetworkError,GrabConnectionError,IndexError):
                    opis = ''
		    
	       try:
	            prod = grab.doc.select(u'//div[@class="firmCard__legal"]').text()
               except IndexError:
	            prod = ''               
		    
		    
               projects = {'sub': self.sub,
	                   'obrazovanie':self.gor,
	                   'teritory':ter,
	                   'phone': phone,
	                   'segment': zap,
	                   'adress':adr,
	                   'tip_ob':tip_ob,
	                   'name':name,
	                   'zdanie':tip_zd,
	                   'etash':et,
	                   'web_url':web,
	                   'opisanie':opis,
	                   'prodavech':prod,
	                   'url_is':url_zd,
	                   'url': task.url
	                   }
	       yield Task('write',project=projects,grab=grab)
	       
	  def task_write(self,grab,task):
	       print('*'*50)
	       print  task.project['sub']
	       print  task.project['obrazovanie']
	       print  task.project['teritory']
	       print  task.project['segment']
	       print  task.project['adress']
	       print  task.project['tip_ob']
	       print  task.project['zdanie']
	       print  task.project['etash']
	       print  task.project['name']
	       print  task.project['phone']
	       print  task.project['web_url']
	       print  task.project['opisanie']
	       print  task.project['url']
	       print  task.project['url_is']
	       print  task.project['prodavech']
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['obrazovanie'])
	       self.ws.write(self.result, 2, task.project['teritory'])
	       self.ws.write(self.result, 3, task.project['adress'])
	       self.ws.write(self.result, 4, task.project['segment'])
               self.ws.write(self.result, 9, task.project['phone'])
               self.ws.write_string(self.result, 12, task.project['url'])
	       self.ws.write_string(self.result, 13, task.project['url_is'])
	       self.ws.write(self.result, 11, task.project['opisanie'])
	       self.ws.write(self.result, 5, task.project['tip_ob'])
	       self.ws.write(self.result, 6, task.project['zdanie'])
	       self.ws.write(self.result, 7, task.project['etash'])
	       self.ws.write_string(self.result, 10, task.project['web_url'])
	       self.ws.write(self.result, 8, task.project['name'])
	       self.ws.write(self.result,14, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result, 15, task.project['prodavech'])
	       print('*'*50)
	       print self.gor
	       print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print '***',i+1,'/',dc,'***'
	     
               print('*'*50)
               self.result+= 1
	       
	       #if self.result > 20:
                    #self.stop()
	

     bot = gis(thread_number=5,network_try_limit=1000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=50, connect_timeout=50)
     bot.run()     
     print(u'Сохранение...')
     print(u'Спим 2 сек...')
     time.sleep(2) 
     bot.workbook.close()
     print('Done!')     
     
     i=i+1
     try:
          page = l[i]
     except IndexError:
	  print('Ready_done!')
	  break
     