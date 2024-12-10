#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
from PIL import Image
from cStringIO import StringIO
import pytesseract
import re
import math
from grab import Grab
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

g = Grab(timeout=10, connect_timeout=10)

g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')

i = 37
l= open('links/Kv_Arenda.txt').read().splitlines()
dc = len(l)
page = l[i]
oper = u'Аренда'

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class Region_Kv(Spider):
          def prepare(self):
	       self.f = page
               while True:
		    try:
			 time.sleep(1)
			 g.go(page)
			 conv = [(u'Архангельск',u'Архангельская область'),(u'Волгоград',u'Волгоградская область'),
			         (u'Вологда',u'Вологодская область'),(u'Воронеж',u'Воронежская область'),
			         (u'Чита',u'Забайкальский край'),(u'Иркутск',u'Иркутская область'),
			         (u'Кемерово',u'Кемеровская область'),(u'Киров',u'Кировская область'),
			         (u'Красноярск',u'Красноярский край'),(u'Курган',u'Курганская область'),
			         (u'Липецк',u'Липецкая область'),(u'Мурманск',u'Мурманская область'),
			         (u'Великий Новгород',u'Новгородская область'),(u'Омск',u'Омская область'),
			         (u'Оренбург',u'Оренбургская область'),(u'Пермь',u'Пермский край'),
			         (u'Псков',u'Псковская область'),(u'Уфа',u'Республика Башкортастан'),
			         (u'Якутск',u'Республика Саха (Якутия)'),(u'Казань',u'Республика Татарстан'),
			         (u'Ростов',u'Ростовская область'),(u'Рязань',u'Рязанская область'),
			         (u'Самара',u'Самарская область'),(u'Санкт-Петербург',u'Санкт-Петербург'),
			         (u'Саратов',u'Саратовская область'),(u'Екатеринбург',u'Свердловская область'),
			         (u'Ставрополь',u'Ставропольский край'),(u'Тамбов',u'Тамбовская область'),(u'Новосибирск',u'Новосибирская область'),
			         (u'Томск',u'Томская область'),(u'Тула',u'Тульская область'),(u'Краснодар',u'Краснодарский край'),
			         (u'Ижевск',u'Удмуртская республика'),(u'Сургут и ХМАО',u'Хантыманскийский автономный округ - Югра'),
			         (u'Челябинск',u'Челябинская область'),(u'Салехард',u'Ямало-Ненецкий автономный округ'),
			         (u'Ярославль',u'Ярославская область'),(u'Тюмень',u'Тюменская область')]
			 
			 if g.doc.select(u'//span[@id="AdvCount"]').exists()==True:
			      dt= g.doc.select(u'//li[contains(text(),"Ваш город:")]/a').text()
			      self.sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
			      self.num = re.sub('[^\d]','',g.doc.select(u'//span[@id="AdvCount"]').text())
			      self.pag = int(math.ceil(float(int(self.num))/float(50)))
			      print self.sub,self.num,self.pag
			      break
			 else:
			      self.sub=''
			      self.pag=1
			      self.num=1
			      break
		    except(GrabTimeoutError,GrabNetworkError,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 continue
	       self.workbook = xlsxwriter.Workbook('Kv/Rugion_%s' % bot.sub + u'_Жилье_'+oper+str(i+1)+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Rugion_Жилье')
	       self.ws.write(0, 0, "СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, "МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, "НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, "ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 4, "УЛИЦА")
	       self.ws.write(0, 5, "ДОМ")
	       self.ws.write(0, 6, "ОРИЕНТИР")
	       self.ws.write(0, 7, "СТАНЦИЯ_МЕТРО")
	       self.ws.write(0, 8, "ДО_МЕТРО_МИНУТ")
	       self.ws.write(0, 9, "ПЕШКОМ_ТРАНСПОРТОМ")
	       self.ws.write(0, 10, "ТИП_ОБЪЕКТА")
	       self.ws.write(0, 11, "ОПЕРАЦИЯ")
	       self.ws.write(0, 12, "СТОИМОСТЬ")
	       self.ws.write(0, 13, "ЦЕНА_М2")
	       self.ws.write(0, 14, "КОЛИЧЕСТВО_КОМНАТ")
	       self.ws.write(0, 15, "ПЛОЩАДЬ_ОБЩАЯ")
	       self.ws.write(0, 16, "ПЛОЩАДЬ_ЖИЛАЯ")
	       self.ws.write(0, 17, "ПЛОЩАДЬ_КУХНИ")
	       self.ws.write(0, 18, "ПЛОЩАДЬ_КОМНАТ")
	       self.ws.write(0, 19, "ЭТАЖ")
	       self.ws.write(0, 20, "ЭТАЖНОСТЬ")
	       self.ws.write(0, 21, "МАТЕРИАЛ_СТЕН")
	       self.ws.write(0, 22, "ГОД_ПОСТРОЙКИ")
	       self.ws.write(0, 23, "РАСПОЛОЖЕНИЕ_КОМНАТ")
	       self.ws.write(0, 24, "БАЛКОН")
	       self.ws.write(0, 25, "ЛОДЖИЯ")
	       self.ws.write(0, 26, "САНУЗЕЛ")
	       self.ws.write(0, 27, "ОКНА")
	       self.ws.write(0, 28, "СОСТОЯНИЕ")
	       self.ws.write(0, 29, "ВЫСОТА_ПОТОЛКОВ")
	       self.ws.write(0, 30, "ЛИФТ")
	       self.ws.write(0, 31, "РЫНОК")
	       self.ws.write(0, 32, "КОНСЬЕРЖ")
	       self.ws.write(0, 33, "ОПИСАНИЕ")
	       self.ws.write(0, 34, "ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 35, "ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 36, "ТЕЛЕФОН")
	       self.ws.write(0, 37, "КОНТАКТНОЕ_ЛИЦО")
	       self.ws.write(0, 38, "КОМПАНИЯ")
	       self.ws.write(0, 39, "ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 40, "ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 41, "ДАТА_ПАРСИНГА")
	       self.ws.write(0, 42, "МЕСТОПОЛОЖЕНИЕ")
	       self.result= 1
	       
          def task_generator(self):
               for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'%d'%x+'.php',network_try_count=100)
            
          
            
	  def task_post(self,grab,task):
	       
               for elem in grab.doc.select('//div[@class="rl_note"]/preceding-sibling::a'):
	            ur = grab.make_url_absolute(elem.attr('href'))  
	            #print ur	      
	            yield Task('item', url=ur,network_try_count=100)
               #yield Task("page", grab=grab,refresh_cache=True,network_try_count=700)
        
        
	  def task_item(self, grab, task):
	       try:
                    punkt = grab.doc.select(u'//li[contains(text(),"Ваш город:")]/a').text()
               except DataNotFound:
	            punkt = ''
		    
               try:
                    ter =  grab.doc.select(u'//span[contains(text(),"Район города:")]/following-sibling::text()').text()
		  #print ter
               except DataNotFound:
                    ter =''
		    
	       try:
	            #if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
                         #uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
                    #else:    
                    uliza = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(',')[0]
               except IndexError:
                    uliza = ''
		    
               try:
                    dom =  grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').number()
               except IndexError:
                    dom = ''
		    
               try:
		    if grab.doc.select(u'//div[@class="title"]').text().find(u'квартир') > 0:
			 tip_ob = u'Квартира'
                    else:
                         tip_ob = u'Комната' 
               except DataNotFound:
                    tip_ob = ''
		  
	       try:
	            orentir = grab.doc.select(u'//span[contains(text(),"Ориентир:")]/following-sibling::text()').text()
		    #print rayon
	       except DataNotFound:
		    orentir = ''

	       try:
		    price = grab.doc.select(u'//span[contains(text(),"Цена общая:")]/following-sibling::text()').text()
		#print price + u' руб'	    
	       except DataNotFound:
		    price = ''
		    
               try:
                    price_kv = grab.doc.select(u'//span[contains(text(),"Цена за")]/following-sibling::text()').text()
               except DataNotFound:
                    price_kv = ''
		    
               try:
                    komnat = grab.doc.select(u'//span[contains(text(),"Комнаты:")]/following-sibling::text()').number()
               except DataNotFound:
                    komnat = ''

	       try:
		    plosh = grab.doc.select(u'//span[contains(text(),"Площадь")]/following-sibling::text()').text()
		 #print rayon
	       except DataNotFound:
		    plosh = ''
		    
               try:
                    et = grab.doc.select(u'//span[contains(text(),"Этаж")]/following-sibling::text()').text().split(u' ')[0]
		    etas = re.sub('[^\d]', '',et)
               except IndexError:
                    etas = '' 
		    
               try:
                    ets = grab.doc.select(u'//span[contains(text(),"Этаж")]/following-sibling::text()').text().split(u' ')[2]
		    etass = re.sub('[^\d]', '',ets)
               except IndexError:
                    etass = ''
		    
               try:
                    mat = grab.doc.select(u'//span[contains(text(),"Тип дома")]/following-sibling::text()').text()
               except DataNotFound:
                    mat = ''

	       try:
	            kanal = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text()
	       except DataNotFound:
	            kanal =''

	       try:
                    rinok = grab.doc.select(u'//span[contains(text(),"Тип:")]/following-sibling::text()').text()
               except DataNotFound:
		    rinok =''
		  
	       try:
		    opis = grab.doc.select(u'//span[contains(text(),"Дополнительная информация:")]/following-sibling::text()').text() 
	       except DataNotFound:
		    opis = ''
		  
	       try:
		    #if  re.sub(u'[^\d]','',grab.doc.select(u'//div[@style="clear: both; margin-bottom: 15px"]/following-sibling::br//following-sibling::text()').text()).isdigit()==False:
		    lico = grab.doc.select(u'//div[@class="field_info"][contains(text(),"Телефон:")]/following-sibling::div[1]').text()
		   
		#print rayon
	       except DataNotFound:
		    lico = ''
		  
	       try:
		    com = grab.doc.select(u'//div[@class="field_info"][contains(text(),"Агентство")]/a').text()
		#print rayon
	       except DataNotFound:
		    com = ''
		  
		  
	       try:
		    conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
		            (u' мая ',u'.05.'),(u' июня ',u'.06.'),
		            (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
		            (u' января ',u'.01.'),(u' декабря ',u'.12.'),
		            (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
		            (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
		    #d = grab.doc.select(u'//div[@class="createDate"]/text()').text()
		    d = grab.doc.rex_text(u'<br>Обновлено (.*?)&nbsp;&nbsp;')
		    data = reduce(lambda d, r: d.replace(r[0], r[1]), conv, d)[:10]
		#print rayon
	       except DataNotFound:
		    data = ''
	       try:
	            conv1 = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
		              (u' мая ',u'.05.'),(u' июня ',u'.06.'),
		              (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
		              (u' января ',u'.01.'),(u' декабря ',u'.12.'),
		              (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
		              (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
		    d1 = grab.doc.rex_text(u'Опубликовано (.*?)&nbsp;&nbsp;')
		    data1 = reduce(lambda d1, r: d1.replace(r[0], r[1]), conv1, d1)[:10]
               except DataNotFound:
		    data1 = ''		    
		  
	      
		  
		  
	       try:
		
		    phone_url = task.url.replace('detail','phone')
	            g2 = grab.clone(timeout=20, connect_timeout=20)
	            g2.go(phone_url)
                    im = Image.open(StringIO(g2.response.body))
	            x,y = im.size
	            phone = pytesseract.image_to_string(im.convert("RGB").resize((int(x*10), int(y*10)),Image.BICUBIC))
	       except (AttributeError,DataNotFound,IOError):
		    phone = ''  

	      
	       projects = {'sub': self.sub,
		            'uliza': uliza,
	                    'dom': dom,
		            'punkt': punkt,
	                    'terit':ter,  
		            'phone': phone,
		            'price': price,
	                    'price_kv': price_kv,
	                    'komnati': komnat,
	                    'rinok': rinok,
		            'opis': opis,
	                    'url': task.url,
		            'orentir': orentir,
		            'ploshad': plosh,
	                    'etach': etas,
	                    'etachs': etass,
	                    'mat_st': mat,
		            'tip': tip_ob,
		            'kanal': kanal,
		            'lico':lico,
		            'com':com,
		            'dataraz': data,
	                    'dataraz1': data1}
	
	
	
	       yield Task('write',project=projects,grab=grab,refresh_cache=True)

	
	  def task_write(self,grab,task):
	      
	       print('*'*100)
	       print  task.project['sub']
	       print  task.project['uliza']
	       print  task.project['dom']
	       print  task.project['punkt']
	       print  task.project['terit']	      
	       print task.project['url']
	       print  task.project['phone']
	       print  task.project['opis']
	       print  task.project['price']
	       print  task.project['price_kv']
	       print  task.project['komnati']
	       print  task.project['rinok']
	       print  task.project['orentir']	      
	       print  task.project['ploshad']
	       print  task.project['etach']
	       print  task.project['etachs']
	       print  task.project['mat_st']
	       print  task.project['tip']
	       print  task.project['kanal']
	       print  task.project['lico']
	       print  task.project['com']
	       print  task.project['dataraz']
	       print  task.project['dataraz1']

	
	       self.ws.write(self.result,0, task.project['sub'])
	       self.ws.write(self.result,4, task.project['uliza'])
	       self.ws.write(self.result,3, task.project['terit'])
	       self.ws.write(self.result,2, task.project['punkt'])
	       self.ws.write(self.result,5, task.project['dom']) 
	       self.ws.write(self.result,6, task.project['orentir'])
	       self.ws.write(self.result,10, task.project['tip'])
	       self.ws.write(self.result,11, oper)
	       self.ws.write(self.result,12, task.project['price'])
	       self.ws.write(self.result,13, task.project['price_kv'])
	       self.ws.write(self.result,14, task.project['komnati'])
	       self.ws.write(self.result,15, task.project['ploshad'])
	       self.ws.write(self.result,19, task.project['etach'])
	       self.ws.write(self.result,20, task.project['etachs'])
	       self.ws.write(self.result,21, task.project['mat_st'])
	       self.ws.write(self.result,42, task.project['kanal'])
	       self.ws.write(self.result,31, task.project['rinok'])
	       self.ws.write(self.result,33, task.project['opis'])
	       self.ws.write_string(self.result,35, task.project['url'])
	       self.ws.write(self.result,36, task.project['phone'])
	       self.ws.write(self.result,37, task.project['lico'])
	       self.ws.write(self.result,38, task.project['com'])
	       self.ws.write(self.result,39, task.project['dataraz1'])
	       self.ws.write(self.result,40, task.project['dataraz'])
	       self.ws.write(self.result,34, re.findall('http://dom.(.*?)/',task.url)[0])
	       self.ws.write(self.result,41, datetime.today().strftime('%d.%m.%Y'))
	       
	       print('*'*100)	
	       print self.sub
	       print 'Ready - '+str(self.result)+'/'+str(self.num)
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print oper
               print('*'*100)
	       self.result+= 1
	       
	       
	       #if self.result > 10:
	            #self.stop()	       

     
     bot = Region_Kv(thread_number=10,network_try_limit=1000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=50, connect_timeout=500)
     bot.run()
     print bot.sub
     print(u'Спим 2 сек...')
     time.sleep(2)
     print(u'Сохранение...')
     bot.workbook.close()
     print(u'Done!')
     time.sleep(1)
     i=i+1
     try:
          page = l[i]
     except IndexError:
	  if oper == u'Продажа':
	       i = 0
               l= open('links/Kv_Arenda.txt').read().splitlines()
               dc = len(l)
               page = l[i]
	       oper = u'Аренда'
	  else:
	       break
