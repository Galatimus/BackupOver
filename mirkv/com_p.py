#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import math
import time
import os
from grab import Grab
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)




i = 1
l= open('links/Com_Prod.txt').read().decode('cp1251').splitlines()
dc = len(l)
page = l[i]
oper = u'Продажа'

while True:
    print '********************************************',i+1,'/',dc,'*******************************************'
    class MK_Com(Spider):
	
	
	
	def prepare(self):
	    self.f = page
	    self.link =l[i]
	    while True:
	        try:
                    time.sleep(3)
		    g = Grab(timeout=20, connect_timeout=20)
		    #g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
                    g.go(self.f)
                    self.sub = g.doc.select(u'//span[@class="current"]').text()
		    try:
                        self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="b-all-offers"]').text())
                        self.pag = int(math.ceil(float(int(self.num))/float(20)))
		    except IndexError:
			self.pag=0
			self.num=0
		    
                    print self.sub.encode('utf-8')
		    del g
                    break
                except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
                    print g.config['proxy'],'Change proxy'
                    #g.change_proxy()
		    del g
                    continue
	     
	    self.workbook = xlsxwriter.Workbook(u'com/Mirkvartir_%s' % bot.sub + u'_'+str(i)+'.xlsx')
	    self.ws = self.workbook.add_worksheet()
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
	    self.ws.write(0, 12, u"ИЗМЕНЕНИЕ_СТОИМОСТИ")
	    self.ws.write(0, 13, u"ДОПОЛНИТЕЛЬНЫЕ_КОММЕРЧЕСКИЕ_УСЛОВИЯ")
	    self.ws.write(0, 14, u"ПЛОЩАДЬ")
	    self.ws.write(0, 15, u"ЭТАЖ")
	    self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	    self.ws.write(0, 17, u"ГОД_ПОСТРОЙКИ")
	    self.ws.write(0, 18, u"ОПИСАНИЕ")
	    self.ws.write(0, 19, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	    self.ws.write(0, 20, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	    self.ws.write(0, 21, u"ТЕЛЕФОН")
	    self.ws.write(0, 22, u"КОНТАКТНОЕ_ЛИЦО")
	    self.ws.write(0, 23, u"КОМПАНИЯ")
	    self.ws.write(0, 24, u"МЕСТОПОЛОЖЕНИЕ")
	    self.ws.write(0, 25, u"МЕСТОРАСПОЛОЖЕНИЕ")
	    self.ws.write(0, 26, u"БЛИЖАЙШАЯ_СТАНЦИЯ_МЕТРО")
	    self.ws.write(0, 27, u"РАССТОЯНИЕ_ДО_БЛИЖАЙШЕЙ_СТАНЦИИ_МЕТРО")
	    self.ws.write(0, 28, u"ОПЕРАЦИЯ")
	    self.ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
	    self.ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ")
	    self.ws.write(0, 31, u"ДАТА_ПАРСИНГА")
	    self.ws.write(0, 32, u"КАДАСТРОВЫЙ_НОМЕР")
	    self.ws.write(0, 33, u"ЗАГОЛОВОК")
	    self.ws.write(0, 34, u"ШИРОТА_ИСХ")
	    self.ws.write(0, 35, u"ДОЛГОТА_ИСХ")
	    self.result= 1
	    
		
		
		
		  
	
	def task_generator(self):
	    for x in range(1,self.pag+1):
                yield Task ('post',url=self.f+'?p=%d'%x,refresh_cache=True,network_try_count=100)
	    
	
	    
	def task_post(self,grab,task):
	    if grab.doc.select(u'//h2[@class="nearby-header"]').exists()==True:
		links = grab.doc.select(u'//h2[@class="nearby-header"]/preceding::div[@class="item"]/a')
	    else:
		links = grab.doc.select(u'//div[@class="item"]/a')
		
	    for elem in links:
		ur = grab.make_url_absolute(elem.attr('href'))  
		#print ur
		yield Task('item', url=ur,refresh_cache=True,network_try_count=10)
	   
			
      
	    
	    
	    
	    
	def task_item(self, grab, task):
	    
	    
	    try:
		    try:
		        ray = grab.doc.select(u'//a[@class="js-popup-select popup-select Province-popup"]/following::span[@itemprop="name"][1]').text()
		    except IndexError:
			ray = grab.doc.select(u'//label[contains(text(),"Район:")]/following-sibling::p/a').text()
	    except IndexError:
		ray =''
	    try:
		#if  grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(text(),"р-н")]').exists()==True:
		    #punkt= grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p').text().split(', ')[2]
		#else:
		punkt= grab.doc.select(u'//a[@class="js-popup-select popup-select City-popup"]/following::span[@itemprop="name"][1]').text()#.split(', ')[1]
	    except IndexError:
		punkt = ''
	    try:
		    try:
		        ter= grab.doc.select(u'//a[@class="js-popup-select popup-select InhabitedPoint-popup"]/following::span[@itemprop="name"][1]').text()
		    except IndexError:
		        ter= grab.doc.select(u'//label[contains(text(),"Округ:")]/following-sibling::p/a').text()
	    except IndexError:
		ter =''
		
		
		
	    try:
		#try:
		    #uliza = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(text()," ул")]').text()
		#except DataNotFound:
		uliza = grab.doc.select(u'//a[@class="js-popup-select popup-select Street-popup"]/following::span[@itemprop="name"][1]').text()
		#except DataNotFound:
		    #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"шоссе")]').text()
	    except DataNotFound:
		uliza = '' 
	    try:
		dom = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(@href,"houseId")]').text().replace('/','-')
	    except DataNotFound:
		dom = ''
		
	    try:
		orentir = grab.doc.select(u'//label[contains(text(),"Жилой комплекс:")]/following-sibling::p').text()
	    except DataNotFound:
		orentir = ''
		
	    try:
	        seg = grab.doc.select(u'//h1[@class="offer-title"]/small').text().replace(u'Продажа ','').replace(u'Аренда ','').replace(',','')
	      #print oren
	    except DataNotFound:
		seg = '' 
		
	    try:
	        naz = grab.doc.select(u'//div[@id="EstateTypes"]/a').text()
	      #print naz
	    except DataNotFound:
		naz = '' 
		
	    try:
		klass = grab.doc.select(u'//label[contains(text(),"Здание:")]/following-sibling::p').text()
	    except DataNotFound:
		klass = ''
		
	    try:
	        price = grab.doc.select(u'//p[@class="price"]/strong').text()+u' р.'
	      #print price
	    except DataNotFound:
		price = ''
		
	    try:
	        plosh = grab.doc.select(u'//label[contains(text(),"Площадь:")]/following-sibling::p').text()#.replace(u'м',u'м2')
	      #print plosh
	    except DataNotFound:
		plosh = '' 
		
	    try:
		et = grab.doc.select(u'//label[contains(text(),"Этаж:")]/following-sibling::p').text().split(u'из ')[0]
	    except IndexError:
		et = ''
		
	    try:
		et2 = grab.doc.select(u'//label[contains(text(),"Этаж:")]/following-sibling::p').text().split(u'из ')[1]
	    except IndexError:
		et2 = ''
		
	    try:
	        opis = grab.doc.select(u'//div[@class="clear"]/following-sibling::p').text()
	      #print opis
	    except DataNotFound:
		opis = ''
		
	    		
	    try:
		lico = grab.doc.select(u'//h3[contains(text(),"Позвоните продавцу")]/following-sibling::p/text()').text()#.split(', ')[1]
	    except IndexError:
		lico = ''
		
	    try:
	        comp = grab.doc.select(u'//a[@rel="nofollow"]').text().replace(u'Показать телефон','')
	      #print comp
	      
	    except IndexError:
		comp = '' 
	    try:
		ohrana = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p').text()
	    except IndexError:
		ohrana =''
	    try:
		gaz = grab.doc.select(u'//div[@class="subway_list_long"]/p').text().split(', ')[0]
	    except IndexError:
		gaz =''
	    try:
		voda = grab.doc.select(u'//div[@class="subway_list_long"]/p').text().split(', ')[1]
	    except IndexError:
		voda =''
	    try:
		kanal = grab.doc.select(u'//title').text()
	    except IndexError:
		kanal =''
	    try:
		elek = grab.doc.select(u'//meta[@name="geo.position"]').attr('content').split(';')[0]
	    except IndexError:
		elek =''
	    try:
		teplo = grab.doc.select(u'//meta[@name="geo.position"]').attr('content').split(';')[1]
	    except IndexError:
		teplo =''
		
	    try:
		   
		conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		            (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		            (u'августа', '.08.2017'),(u'мая', '.05.2017'),(u'ноября', '.11.2017'),
		            (u'марта', '.03.2017'),(u'сентября', '.09.2017'),(u'октября', '.10.2017'),
		            (u'января', '.01.2017'),(u'февраля', '.02.2017'),(u'апреля', '.04.2017'),
		            (u'июля', '.07.2017'),(u'июня', '.06.2017'),(u'декабря', '.12.2017')]
		dt= grab.doc.rex_text(u'Опубликовано: (.*?)в ').replace(' (','')
		data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','').replace(u'более3-хмесяце','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=92)))
		#print data
	    except IndexError:
		data = ''
		
	    if punkt=='':
	        punkt=ter
		ter=''
	    else:
		punkt=punkt
		ter=ter
	    
	    projects = {'url': task.url,
		        'sub': self.sub,
		        'ray': ray,
		        'punkt': punkt,
		        'teritor': ter,
		        'uliza': uliza,
		        'dom': dom,
		        'orentir':orentir,
		        'seg': seg,
		        'naznachenie': naz,
		        'klass': klass,
		        'cena': price,
		        'ploshad': plosh,
		        'et': et,
		        'ets': et2,
		        'opisanie': opis,
		        'company':comp,
		        'lico':lico,
		        'ohrana':ohrana,
		        'gaz': gaz,
		        'voda': voda,
		        'kanaliz': kanal,
		        'electr': elek,
		        'teplo': teplo,
		        'data':data}
	    
	    try:
		#ad_id= re.sub(u'[^\d]','',task.url[-9:])
		ad_id= re.sub(u'[^\d]','',task.url)
		ad_phone = grab.doc.select(u'//span[@class="phone"]/a').attr('key')
		link = grab.make_url_absolute('/EstateOffers/AwesomeDecryptPhone/?offerId='+ad_id+'&encryptedPhone='+ad_phone)
		headers ={'Accept': '*/*',
			  'Accept-Encoding': 'gzip,deflate',
			  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			  'Cookie': 'sessid='+ad_id+'.'+ad_phone,
			  'Host': 'mirkvartir.ru',
			  'Referer': task.url,
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0', 
			  'X-Requested-With' : 'XMLHttpRequest'}
		gr = Grab()
		gr.setup(url=link)
	        yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
	    except IndexError:
	        yield Task('phone',grab=grab,project=projects)	    
	    
	def task_phone(self, grab, task):
	    try:
                    phone = grab.doc.rex_text(u'normalizedPhone":"(.*?)"')
	    except (IndexError,ValueError,GrabNetworkError,GrabTimeoutError,IOError):
	        phone = ''
		
	    yield Task('write',project=task.project,phone=phone,grab=grab)
	    
	def task_write(self,grab,task):
	    
	    print('*'*50)
	    print  task.project['sub'].encode('utf-8')
	    print  task.project['ray'].encode('utf-8')
	    print  task.project['punkt'].encode('utf-8')
	    print  task.project['teritor'].encode('utf-8')
	    print  task.project['uliza'].encode('utf-8')
	    print  task.project['dom'].encode('utf-8')
	    print  task.project['orentir'].encode('utf-8')
	    print  task.project['seg'].encode('utf-8')
	    print  task.project['naznachenie'].encode('utf-8')
	    print  task.project['klass'].encode('utf-8')
	    print  task.project['cena'].encode('utf-8')
	    print  task.project['ploshad'].encode('utf-8')
	    print  task.project['et'].encode('utf-8')
	    print  task.project['ets'].encode('utf-8')
	    print  task.project['opisanie'].encode('utf-8')
	    print  task.project['url'].encode('utf-8')
	    print  task.phone.encode('utf-8')
	    print  task.project['lico'].encode('utf-8')
	    print  task.project['company'].encode('utf-8')
	    print  task.project['ohrana'].encode('utf-8')
	    print  task.project['gaz'].encode('utf-8')
	    print  task.project['voda'].encode('utf-8')
	    print  task.project['kanaliz'].encode('utf-8')
	    print  task.project['electr'].encode('utf-8')
	    print  task.project['teplo'].encode('utf-8')
	    print  task.project['data'].encode('utf-8')
	   
	    
	    
	    
	    self.ws.write(self.result, 0, task.project['sub'])
	    self.ws.write(self.result, 1, task.project['ray'])
	    self.ws.write(self.result, 2, task.project['punkt'])
	    self.ws.write(self.result, 3, task.project['teritor'])
	    self.ws.write(self.result, 4, task.project['uliza'])
	    self.ws.write(self.result, 5, task.project['dom'])
	    self.ws.write(self.result, 6, task.project['orentir'])
	    self.ws.write(self.result, 7, task.project['seg'])
	    #self.ws.write(self.result, 8, task.project['tip'])
	    self.ws.write(self.result, 9, task.project['naznachenie'])
	    self.ws.write(self.result, 10, task.project['klass'])
	    self.ws.write(self.result, 11, task.project['cena'])
	    self.ws.write(self.result, 14, task.project['ploshad'])	
	    self.ws.write(self.result, 15, task.project['et'])
	    self.ws.write(self.result, 16, task.project['ets'])
	    #self.ws.write(self.result, 15, task.project['god'])
	    #self.ws.write(self.result, 16, task.project['mat'])
	    #self.ws.write(self.result, 17, task.project['potolok'])
	    #self.ws.write(self.result, 18, task.project['sost'])
	    self.ws.write(self.result, 24, task.project['ohrana'])
	    self.ws.write(self.result, 26, task.project['gaz'])
	    self.ws.write(self.result, 27, task.project['voda'])
	    self.ws.write(self.result, 33, task.project['kanaliz'])
	    self.ws.write(self.result, 34, task.project['electr'])
	    self.ws.write(self.result, 35, task.project['teplo'])
	    self.ws.write_string(self.result, 20, task.project['url'])
	    self.ws.write(self.result, 21, task.phone)
	    self.ws.write(self.result, 22, task.project['lico'])
	    self.ws.write(self.result, 23, task.project['company'])
	    self.ws.write(self.result, 29, task.project['data'])
	    self.ws.write(self.result, 18, task.project['opisanie'])
	    self.ws.write(self.result, 19, u'MIRKVARTIR.RU')
	    self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	    self.ws.write(self.result, 28, oper)
	    
	    
	    print('*'*50)
            print self.sub
            print 'Ready - '+str(self.result)+'/'+str(self.num)
            logger.debug('Tasks - %s' % self.task_queue.size()) 
            print '***',i+1,'/',dc,'***'
            print oper.encode('utf-8')
            print('*'*50)
	    
	    self.result+= 1
	    
	    #if self.result > 10:
		#self.stop()	

	   
    bot = MK_Com(thread_number=1,network_try_limit=1000)
    #bot.load_proxylist('../tipa.txt','text_file')
    bot.create_grab_instance(timeout=5, connect_timeout=10)
    bot.run()
    print('Wait 2 sec...')
    time.sleep(1)
    print('Save it...')
    command = 'mount -a'
    os.system('echo %s|sudo -S %s' % ('1122', command))
    time.sleep(2)
    bot.workbook.close()
    print('Done')
       