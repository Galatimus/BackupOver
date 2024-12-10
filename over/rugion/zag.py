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
from grab import Grab
from datetime import datetime
import math
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

g = Grab(timeout=20, connect_timeout=20)

i = 1
l= open('links/Zag_Prod.txt').read().splitlines()
page = l[i]
oper = u'Продажа'

while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'
     class Region_Zag(Spider):
          def prepare(self):
	       self.f = page
	       self.link =l[i]
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
	       self.workbook = xlsxwriter.Workbook('zag/Rugion_%s' % bot.sub + u'_Загород_'+oper+str(i+1)+'.xlsx')
               self.ws = self.workbook.add_worksheet(u'Rugion_Загород')
	       self.ws.write(0, 0, "СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, "МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, "НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, "ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 4, "УЛИЦА")
	       self.ws.write(0, 5, "ДОМ")
	       self.ws.write(0, 6, "ОРИЕНТИР")
	       self.ws.write(0, 7, "ТРАССА")
	       self.ws.write(0, 8, "УДАЛЕННОСТЬ")
	       self.ws.write(0, 9, "КАДАСТРОВЫЙ_НОМЕР_ЗЕМЕЛЬНОГО_УЧАСТКА")
	       self.ws.write(0, 10, "ТИП_ОБЪЕКТА")
	       self.ws.write(0, 11, "ОПЕРАЦИЯ")
	       self.ws.write(0, 12, "СТОИМОСТЬ")
	       self.ws.write(0, 13, "ЦЕНА_М2")
	       self.ws.write(0, 14, "ПЛОЩАДЬ_ОБЩАЯ")
	       self.ws.write(0, 15, "КОЛИЧЕСТВО_КОМНАТ")
	       self.ws.write(0, 16, "ЭТАЖНОСТЬ")
	       self.ws.write(0, 17, "МАТЕРИАЛ_СТЕН")
	       self.ws.write(0, 18, "ГОД_ПОСТРОЙКИ")
	       self.ws.write(0, 19, "ПЛОЩАДЬ_УЧАСТКА")
	       self.ws.write(0, 20, "ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	       self.ws.write(0, 21, "ГАЗОСНАБЖЕНИЕ")
	       self.ws.write(0, 22, "ВОДОСНАБЖЕНИЕ")
	       self.ws.write(0, 23, "КАНАЛИЗАЦИЯ")
	       self.ws.write(0, 24, "ЭЛЕКТРОСНАБЖЕНИЕ")
	       self.ws.write(0, 25, "ТЕПЛОСНАБЖЕНИЕ")
	       self.ws.write(0, 26, "ЛЕС")
	       self.ws.write(0, 27, "ВОДОЕМ")
	       self.ws.write(0, 28, "БЕЗОПАСНОСТЬ")
	       self.ws.write(0, 29, "ОПИСАНИЕ")
	       self.ws.write(0, 30, "ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 31, "ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 32, "ТЕЛЕФОН")
	       self.ws.write(0, 33, "КОНТАКТНОЕ_ЛИЦО")
	       self.ws.write(0, 34, "КОМПАНИЯ")
	       self.ws.write(0, 35, "ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 36, "ДАТА_ОБНОВЛЕНИЯ")
               self.ws.write(0, 37, "ДАТА_ПАРСИНГА")
               self.ws.write(0, 38, "МЕСТОПОЛОЖЕНИЕ")
	       self.result= 1
    
          def task_generator(self):
               for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'%d'%x+'.php',network_try_count=100)
        
            
          def task_page(self,grab,task):
	       try:
		    pg = grab.doc.select(u'//span[@class="pageslink_active"]/following::a[1]')
		    u = grab.make_url_absolute(pg.attr('href'))
		    yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	       except DataNotFound:
		    print('*'*100)
	            print '!!!!','NO PAGE NEXT','!!!!'
	            print('*'*100)
	            logger.debug('%s taskq size' % self.task_queue.size())
        
            
	  def task_post(self,grab,task):
	       
	   
               for elem in grab.doc.select('//div[@class="rl_note"]/preceding-sibling::a'):
                    ur = grab.make_url_absolute(elem.attr('href'))  
                    #print ur	      
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
               #yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
                
	 
        
        
        
	  def task_item(self, grab, task):
	       try:
                    if grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().find(u'р-н') > 0:
			 ray = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(', ')[0]
		    else:
		         ray =''
		  #print ray
	       except DataNotFound:
		    ray =''
		  
		  
	      
	       try:
		    if grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().find(u' г') > 0:
		         punkt = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(', ')[0]
		    
		    elif grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().find(u'р-н') > 0:
		         punkt = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(', ')[1]
		    else:
			 punkt = ''
	       except (DataNotFound,IndexError):
		    punkt = ''
		    
               try:
                    ter =  grab.doc.select(u'//span[contains(text(),"Район города:")]/following-sibling::text()').text()
		  #print ter
               except DataNotFound:
                    ter =''
		    
	       try:
		    if grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().find(u' ул') > 0:
			 uliza = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(', ')[0]
		    else:
			 uliza =''

	       except DataNotFound:
		    uliza =''
		    
               try:
                    dom = re.sub(u'[^\d]','',grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text())
               except DataNotFound:
                    dom = ''
		  
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
                    price_sot = grab.doc.select(u'//span[contains(text(),"Цена за")]/following-sibling::text()').text()
               except DataNotFound:
	            price_sot = ''		    
		  
		  
	       try:
		    plosh = grab.doc.select(u'//span[contains(text(),"Площадь	дома")]/following-sibling::text()').text()
		 #print rayon
	       except DataNotFound:
		    plosh = ''
		  
               try:
                    plosh1 = grab.doc.select(u'//span[contains(text(),"Площадь участка")]/following-sibling::text()').text()
               except DataNotFound:
                    plosh1 = ''		  
	       
		  
	       try:
		    vid = grab.doc.select(u'//span[contains(text(),"Тип")]/following-sibling::text()').text()
		#print rayon
	       except DataNotFound:
		    vid = ''
		  
	       try:
		    ohrana =re.sub(u'^.*(?=храна)','',grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
	       except DataNotFound:
		    ohrana =''
		    
		    
	       try:
		    gaz = re.sub(u'^.*(?=газ)','',grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
	       except DataNotFound:
		    gaz =''
	       try:
		    voda = re.sub(u'^.*(?=вод)','',grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
               except DataNotFound:
		    voda =''
		    
	       try:
	            kanal = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text()
	       except DataNotFound:
	            kanal =''
		    
	       try:
	            elek = re.sub(u'^.*(?=лектричество)','',grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	       except DataNotFound:
		    elek =''
		    
	       try:
		    teplo = re.sub(u'^.*(?=топление)','',grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	       except DataNotFound:
	            teplo =''
		    
	       try:
                    les = re.sub(u'^.*(?=лес)','', grab.doc.select(u'//*[contains(text(), "лес")]').text())[:3].replace(u'лес',u'есть')
               except DataNotFound:
                    les =''
		      
               try:
                    vodoem = re.sub(u'^.*(?=озер)','', grab.doc.select(u'//*[contains(text(), "озер")]').text())[:4].replace(u'озер',u'есть')
               except DataNotFound:
                    vodoem =''
	       
		  
	       try:
		    opis = grab.doc.select(u'//span[contains(text(),"Дополнительная информация:")]/following-sibling::text()').text() 
	       except DataNotFound:
		    opis = ''
		  
	       try:
		    #if  re.sub(u'[^\d]','',grab.doc.select(u'//div[@style="clear: both; margin-bottom: 15px"]/following-sibling::br//following-sibling::text()').text()).isdigit()==False:
			 #lico = grab.doc.select(u'//div[@style="clear: both; margin-bottom: 15px"]/following-sibling::br//following-sibling::text()').text()
		    #else:
		    lico=grab.doc.select(u'//div[@class="field_info"][contains(text(),"Телефон:")]/following-sibling::div[1]').text()
		#print rayon
	       except DataNotFound:
		    lico = ''
		  
	       try:
		    com = grab.doc.select(u'//a[@class="all_ads_user_link"]').text()
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
	            g2 = grab.clone(timeout=200, connect_timeout=200)
	            g2.go(phone_url)
                    im = Image.open(StringIO(g2.response.body))
	            x,y = im.size
	            phone = pytesseract.image_to_string(im.convert("RGB").resize((int(x*10), int(y*10)),Image.BICUBIC))
	            #phone = re.sub('[\s]', u'',pho)
	       except (AttributeError,DataNotFound,IOError):
		    phone = ''  
		  
	       
		  
	      
	      
	      
	      
	      
	       projects = {'sub': self.sub,
		            'rayon': ray,
		            'punkt': punkt,
	                    'terit':ter,  
	                    'ulica': uliza,
	                    'dom': dom,
		            'phone': phone,
		            'price': price,
		            'opis': opis,
	                    'price_sot': price_sot,
		            'url': task.url,
		            'orentir': orentir,
		            'ploshad': plosh,
	                    'ploshad_uch': plosh1,
		            'vid': vid,
		            'gaz': gaz,
		            'voda':voda,
		            'elekt': elek,
		            'ohrana': ohrana,
		            'teplo': teplo,
	                    'les': les,
                            'vodoem':vodoem,
		            'kanal': kanal,
		            'lico':lico,
		            'com':com,
		            'dataraz': data,
	                     'dataraz1': data1}
		            
		         
	
	
	
	       yield Task('write',project=projects,grab=grab)
	
  
	
	
	
	
	  def task_write(self,grab,task):
	      
	       print('*'*100)
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['terit']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print task.project['url']
	       print  task.project['phone']
	       print  task.project['opis']
	       print  task.project['price']
	       print  task.project['price_sot']
	       print  task.project['orentir']	      
	       print  task.project['ploshad']
	       print  task.project['ploshad_uch']
	       print  task.project['vid']
	       print  task.project['gaz']
	       print  task.project['voda']
	       print  task.project['kanal']
	       print  task.project['elekt']
	       print  task.project['teplo']
	       print  task.project['les']
	       print  task.project['vodoem']	       
	       print  task.project['ohrana']
	       print  task.project['lico']
	       print  task.project['com']
	       print  task.project['dataraz']
	       print  task.project['dataraz1']
	      
	       
	       
	
	
	
	
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 3, task.project['terit'])
	       self.ws.write(self.result, 4, task.project['ulica'])
	       self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 6, task.project['orentir'])
	       self.ws.write(self.result, 10, task.project['vid'])
	       self.ws.write(self.result, 12, task.project['price'])
	       self.ws.write(self.result,13, task.project['price_sot'])
	       self.ws.write(self.result, 14, task.project['ploshad'])
	       self.ws.write(self.result, 19, task.project['ploshad_uch'])
	       self.ws.write(self.result, 21, task.project['gaz'])
	       self.ws.write(self.result, 22, task.project['voda'])
	       self.ws.write(self.result, 38, task.project['kanal'])
	       self.ws.write(self.result, 24, task.project['elekt'])
	       self.ws.write(self.result, 25, task.project['teplo'])
	       self.ws.write(self.result, 26, task.project['les'])
	       self.ws.write(self.result, 27, task.project['vodoem'])
	       self.ws.write(self.result, 28, task.project['ohrana'])
	       self.ws.write(self.result, 29, task.project['opis'])
	       self.ws.write_string(self.result, 31, task.project['url'])
	       self.ws.write(self.result, 32, task.project['phone'])
	       self.ws.write(self.result, 33, task.project['lico'])
	       self.ws.write(self.result, 34, task.project['com'])
	       self.ws.write(self.result, 35, task.project['dataraz1'])
	       self.ws.write(self.result, 36, task.project['dataraz'])
	       self.ws.write(self.result, 30, re.findall('http://dom.(.*?)/',task.url)[0])
	       self.ws.write(self.result, 37, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result, 11, oper)
	       print('*'*100)	
	       print self.sub
	       print 'Ready - '+str(self.result)+'/'+str(self.num)
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print '***',i+1,'/',len(l),'***'
	       print oper
               print('*'*100)
	       self.result+= 1
	       
	       
	       
	       #if int(self.result) >= int(task.project['koll'])-1:
                    #self.stop()
	
	       #if self.result > 50:
	            #self.stop()
	

     bot = Region_Zag(thread_number=5,network_try_limit=2000)
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
	       l= open('links/Zag_Arenda.txt').read().splitlines()
	       page = l[i]
	       oper = u'Аренда'
	  else:
	       break
