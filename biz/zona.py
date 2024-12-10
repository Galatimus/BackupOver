#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab import Grab
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import math
import os
import re
from datetime import datetime,timedelta
import xlsxwriter

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)







i = 0
l= open('Links/zona.txt').read().splitlines()
dc = len(l)
page = l[i]  
oper = u'Продажа'
     


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     

     class Zona_Biz(Spider):
	  
	  
	  
          def prepare(self):
	      
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
			 time.sleep(1)
			 g = Grab(timeout=20, connect_timeout=20)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
			 g.go(self.f)
			 #global sub
			 self.sub = g.doc.select(u'//h3[@class="main-header"]').text().split(' "')[1].replace('"','')
			 self.num = re.sub('[^\d]','',g.doc.select(u'//*[contains(text(),"Всего предложений:")]').text().split(' |')[0])
			 self.pag = int(math.ceil(float(int(self.num))/float(5)))
			 print self.sub,self.num
			 print self.pag
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 del g
			 continue	  	       
	       self.workbook = xlsxwriter.Workbook(u'zona/Bizzona_%s' % bot.sub + u'_Готовый_бизнес_'+oper+'.xlsx')
               self.ws = self.workbook.add_worksheet(u'bizzona')
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
	       self.ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 30, u"ДАТА ПАРСИНГА")
	       self.ws.write(0, 31, u"МЕСТОПОЛОЖЕНИЕ")	       
	       self.ws.write(0, 32, u"КРАТКОЕ_ОПИСАНИЕ_БИЗНЕСА")
	       self.ws.write(0, 33, u"ДЕТАЛЬНОЕ_ОПИСАНИЕ_БИЗНЕСА")
	       self.ws.write(0, 34, u"ПЕРЕЧЕНЬ_ИСПОЛЬЗУЕМЫХ_ОБЪЕКТОВ_НЕДВИЖИМОСТИ")
	       self.ws.write(0, 35, u"ЗАГОЛОВОК")
	       
	       self.result= 1
            
            
            
              
    
	  def task_generator(self): 
	       for x in range(self.pag+1):
	            yield Task ('post',url=self.f+'?offset='+str(x*5),refresh_cache=True,network_try_count=100)
	       
	       
	  def task_post(self,grab,task):
	       for elem in grab.doc.select(u'//a[contains(@title,"Подробнее")]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,post = task.url,network_try_count=100)
	       #yield Task("page", grab=grab,refresh_cache=True,network_try_count=100,use_proxylist=False)
        
            
	  def task_page(self,grab,task):
	      
	       try:
		    pg = grab.doc.select(u'//li[@class="active"]/following-sibling::li[1]/a')
		    u = grab.make_url_absolute(pg.attr('href'))
		    yield Task ('post',url= u,network_try_count=100,refresh_cache=True)
	       except DataNotFound:
		    print('*'*100)
		    print '!!!!','NO PAGE NEXT','!!!!'
		    print('*'*100)
		    logger.debug('%s taskq size' % self.task_queue.size())
        
	  def task_item(self, grab, task):
	       #pass
	     
	       try:
	            ry = grab.doc.select(u'//div[contains(text(),"Расположения:")]/following-sibling::div').text()
		    ray = re.findall(u', (.*?) район',ry)[0]
	       except IndexError:
	            ray = '' 
	       try:
		    punkt = grab.doc.select(u'//p[contains(text(),"Тел. код города")]').text().split(u'Тел. код города ')[1].split(': ')[0]
               except IndexError:
		    punkt = ''
	       try:
		    tr2 = grab.doc.select(u'//div[contains(text(),"Расположения:")]/following-sibling::div').text()
                    uliza = re.findall(u'ул. (.*?),',tr2)[0]
	       except IndexError:
		    uliza = ''
               try:
                    dm = grab.doc.select(u'//div[contains(text(),"Расположения:")]/following-sibling::div').text()
                    dom = re.split('\W+', dm,1)[1]
               except IndexError:
                    dom = ''
		    
               try:
                    metro = grab.doc.select(u'//div[contains(text(),"Расположения:")]/following-sibling::div').text().split(u'м. ')[1]
	       except IndexError:
		    metro = ''
	       try:
		    oborot = grab.doc.select(u'//div[contains(text(),"Обороты/мес:")]/following-sibling::div').text()
	       except IndexError:
		    oborot = ''
	       try:
	            pribil = grab.doc.select(u'//div[contains(text(),"Прибыль/мес:")]/following-sibling::div').text()
	       except IndexError:
	            pribil = ''
	       try:
		    #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	            price = grab.doc.select(u'//div[@class="btn-price-bisnes on-offer-page form-group"]').text()
                    #else:
                         #price =''
               except IndexError:
	            price = ''
               try:
                    sfera = grab.doc.select(u'//a[@class="name_biz"]').text().split(u' "')[1].replace('"','')
               except IndexError:
                    sfera = ''
		    
               try:
                    dolya = grab.doc.select(u'//div[contains(text(),"Доля бизнеса:")]/following-sibling::div').text()
               except IndexError:
                    dolya = ''
		    
               try:
                    sotrud = grab.doc.select(u'//div[contains(text(),"Общее количество персонала:")]/following-sibling::div').number()
               except IndexError:
                    sotrud = ''
               try:
                    dolgi = grab.doc.select(u'//a[@class="category-link"]').text()
               except IndexError:
                    dolgi = ''
		    
	       try:
	            zag = grab.doc.select(u'//a[@class="name_biz"]').text()
	       except IndexError:
	            zag = ''		    
              
		    
               try:
                    srok = grab.doc.select(u'//h4[contains(text(),"Материальное имущество:")]/following-sibling::div').text()
               except IndexError:
                    srok = ''
		    
	       try:
	            srokok = grab.doc.select(u'//div[contains(text(),"Срок окупаемости:")]/following-sibling::div').text()
	       except IndexError:
	            srokok = ''		    
               try:
                    srok_sush = grab.doc.select(u'//div[contains(text(),"Cрок существования бизнеса:")]/following-sibling::div').text()
               except IndexError:
	            srok_sush = ''
               try:
                    prich = grab.doc.select(u'//div[contains(text(),"Причина продажи бизнеса:")]/following-sibling::div').text()
               except IndexError:
	            prich = ''		    
            
               try:
	            opis = grab.doc.select(u'//h4[contains(text(),"Детальное описание бизнеса:")]/following-sibling::div').text() 
	       except IndexError:
	            opis = ''
               try:
                    phone = re.sub('[^\d\+]', u'',grab.doc.select(u'//div[contains(text(),"Номер телефона:")]/following-sibling::div').text())
               except IndexError:
                    phone = ''
	    
               
	       try:
		    conv = [(u'Сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		            (u'Вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		            (u' August ',u'.08.'), (u' July ',u'.07.'),
			    (u' May ',u'.05.'),(u' June ',u'.06.'),
			    (u' March ',u'.03.'),(u' April ',u'.04.'),
			    (u' January ',u'.01.'),(u' December ',u'.12.'),
			    (u' September ',u'.09.'),(u' November ',u'.11.'),
			    (u' February ',u'.02.'),(u' October ',u'.10.')]
	            d = grab.doc.select(u'//div[contains(text(),"Дата публикации:")]/span').text()
		    data = reduce(lambda d, r: d.replace(r[0], r[1]), conv, d)
	       except IndexError:
	            data = ''
	    
	       try:
	            mesto = grab.doc.select(u'//div[contains(text(),"Расположения:")]/following-sibling::div').text()
	       except IndexError:
	            mesto =''
		    
	       try:
		    opis1 = grab.doc.select(u'//h4[contains(text(),"Краткое описание бизнеса:")]/following-sibling::div').text() 
	       except IndexError:
	            opis1 = ''
		    
	       try:
	            opis2 = grab.doc.select(u'//h4[contains(text(),"Перечень используемых объектов недвижимости:")]/following-sibling::div').text() 
	       except IndexError:
	            opis2 = ''		    
	
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt,
		           'ulica': uliza,
	                   'dom': re.sub('[^\d]', u'',dom)[:2],
	                   'oborot': oborot,
	                   'metro': metro,
	                   'price': price,
	                   'pribil': pribil,
	                   'sfera': sfera,
	                   'dolya': dolya,
	                   'sotrud': sotrud,
	                   'dolg': dolgi,
	                   'srok': srok,
	                   'srok_ok': srokok,
	                   'srok1': srok_sush,
	                   'prichina': prich,
	                   'opis': opis,
	                   'opis1': opis1,
	                   'opis2': opis2,
	                   'zag': zag,
	                   'phone': phone,
	                   'mesto': mesto,
	                   'dataraz': data}
	
	
	
	       yield Task('write',project=projects,grab=grab)
	

	
	
	
	
	  def task_write(self,grab,task):
	     
	       print('*'*100)
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['metro']
	       print  task.project['oborot']
	       print  task.project['price']
	       print  task.project['pribil']
	       print  task.project['sfera']
	       print  task.project['srok_ok']
	       print  task.project['dolya']
	       print  task.project['sotrud']
	       print  task.project['dolg']
               print  task.project['srok']
	       print  task.project['srok1']
	       print  task.project['prichina']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['dataraz']
	       print  task.project['mesto']
	       
	       
               self.ws.write(self.result,0, task.project['sub'])
	       self.ws.write(self.result,1, task.project['rayon'])
	       self.ws.write(self.result,3, task.project['punkt'])
	       self.ws.write(self.result,5, task.project['ulica'])
	       self.ws.write(self.result,6, task.project['dom'])
	       self.ws.write(self.result,7, task.project['metro'])
	       self.ws.write(self.result,17, task.project['oborot'])
	       self.ws.write(self.result,11, oper)
	       self.ws.write(self.result,18, task.project['pribil'])
	       self.ws.write(self.result,10, task.project['sfera'])
	       self.ws.write(self.result,19, task.project['sotrud'])
	       self.ws.write(self.result,13, task.project['price'])
	       self.ws.write(self.result,16, task.project['dolya'])
	       self.ws.write(self.result,23, task.project['srok'])
	       self.ws.write(self.result,12, task.project['dolg'])
	       self.ws.write(self.result,22, task.project['srok1'])
	       self.ws.write(self.result,24, task.project['prichina'])
	       self.ws.write(self.result,21, task.project['srok_ok'])
	       #self.ws.write(self.result,21, task.project['voda'])
	       #self.ws.write(self.result,22, task.project['kanal'])
	       #self.ws.write(self.result,23, task.project['elekt'])
	       #self.ws.write(self.result,24, task.project['teplo'])
	       #self.ws.write(self.result,19, task.project['ohrana'])
	       self.ws.write(self.result,25, task.project['opis1']+','+task.project['opis'])
	       self.ws.write(self.result,26, u'BIZZONA.RU')
	       self.ws.write_string(self.result,27, task.project['url'])
	       self.ws.write(self.result,28, task.project['phone'])
	       self.ws.write(self.result,33, task.project['opis'])
	       self.ws.write(self.result,35, task.project['zag'])
	       self.ws.write(self.result,32, task.project['opis1'])
	       self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result,29, task.project['dataraz'])
	       self.ws.write(self.result,31, task.project['mesto'])
	       self.ws.write(self.result,34, task.project['opis2'])
	      
	      
	       
	
	       print('*'*100)
	       print self.sub
	       print 'Ready - '+str(self.result)+'/'+str(self.num)
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print '***',i+1,'/',dc,'***'
	       print oper
	       print('*'*100)
	       self.result+= 1
	       
	       #if self.result > 100:
                    #self.stop()	       
	

     bot = Zona_Biz(thread_number=5, network_try_limit=1000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=5, connect_timeout=5)
     bot.run()
     print bot.sub
     print('Wait 2 sec...')
     time.sleep(1)
     print('Save it...')    
     command = 'mount -a'# cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
     #command = 'apt autoremove'
     p = os.system('echo %s|sudo -S %s' % ('1122', command))
     print p
     time.sleep(2)
     bot.workbook.close()
     #workbook.close()
     print('Done!')
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  break
	  
time.sleep(5)
#os.system("/home/oleg/pars/biz/bizfs.py")  
 