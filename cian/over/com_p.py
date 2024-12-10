#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import math
import re
import os
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)



i = 0
l= open('Links/com_p1.txt').read().splitlines()
page = l[i]
oper = u'Продажа'



while True:
    print '********************************************',i+1,'/',len(l),'*******************************************'	  
    class Cian_Com(Spider):
	def prepare(self):
	    self.f = page
	    self.link =l[i]	    
	    for p in range(1,21):
		try:
		    time.sleep(5)
		    g = Grab(timeout=20, connect_timeout=50)
		    g.proxylist.load_file(path='../tipa.txt',proxy_type='http') 		    
		     
		    g.go(self.f)
		    print g.response.code
		    self.sub = g.doc.rex_text(u'data-mark="location">(.*?)</button>')
                        #self.sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace('\u002D',' ').replace(u'в ',' ')
		    print self.sub
		    del g
		    break
		except(GrabTimeoutError,GrabNetworkError,IndexError,DataNotFound,GrabConnectionError):
		    print g.config['proxy'],'Change proxy'
		    g.change_proxy()
		    del g
		    continue	    
	    else:
		self.sub =''
		    
		    
		    
	    self.workbook = xlsxwriter.Workbook(u'com/Cian_'+oper+str(i+1)+'.xlsx')
	    self.ws = self.workbook.add_worksheet(u'Cian_Коммерческая')
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
	    self.ws.write(0, 36, u"ТРАССА")
	    self.ws.write(0, 37, u"ПАРКОВКА")
	    self.ws.write(0, 38, u"ОХРАНА")
	    self.ws.write(0, 39, u"КОНДИЦИОНИРОВАНИЕ")
	    self.ws.write(0, 40, u"ИНТЕРНЕТ")
	    self.ws.write(0, 41, u"ТЕЛЕФОН (КОЛИЧЕСТВО ЛИНИЙ)")
	    self.ws.write(0, 42, u"УСЛУГИ")
	    self.ws.write(0, 43, u"СИСТЕМА ВЕНТИЛЯЦИИ")    
	    self.result= 1
	    #self.count = 2
	    
		
		
		
		  
	
	def task_generator(self):
	    yield Task ('post',url=self.f.strip(),refresh_cache=True,network_try_count=100)
	    
	#def task_next(self,grab,task):
	    #for em in grab.doc.select(u'//a[@class="c-com-promo-block-links-item___Nimbl"][contains(@href, "kupit")]'):
		#urr = grab.make_url_absolute(em.attr('href'))
		#print urr	    
	        #yield Task('post', url=urr,refresh_cache=True,network_try_count=100)
	    
	def task_post(self,grab,task):	
	    time.sleep(2)
	    for elem in grab.doc.select(u'//h3/a'):
		ur = elem.attr('href')  
		#print ur
		#time.sleep(2)
		yield Task('item', url=ur,refresh_cache=True, network_try_count=100)
	    yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)	
	    
	def task_page(self,grab,task):
	    time.sleep(1)
	    try:
		pg = grab.doc.select(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a')
		u = pg.attr('href')
		yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
		#self.count +=1
	    except DataNotFound:
		print('*'*100)
		print '!!!','NO PAGE NEXT','!!!'
		print('*'*100)
		print 'Tasks - %s' % self.task_queue.size() 	
	    
	
			
      
	    
	    
	    
	    
	def task_item(self, grab, task):
	    #time.sleep(1)
	    try:
		usl = grab.doc.select(u'//div[@class="cf-object-descr-add"]/span[contains(text(),"включая:")]').text().split(': ')[1]
	    except IndexError:
		usl = ''	
	    try:
		ray = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').text()
	    except DataNotFound:
		ray =''
	    try:
		if self.sub == u'Москва':
		    punkt= u'Москва'
		elif self.sub == u'Санкт-Петербург':
		    punkt= u'Санкт-Петербург'
		elif self.sub == u'Севастополь':
		    punkt= u'Севастополь'
		else:
		    if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2][contains(text(),"район")]').exists()==True:
			punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]/a[3]').text()
		    elif grab.doc.select(u'//h1[@class="object_descr_addr"]/a[3][contains(text(),"район")]').exists()==True:
			punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2]').text()
		    else:
			punkt=grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2]').text()
	    except IndexError:
		punkt = ''
	    try:
		ter=  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район ")]').text()
	    except IndexError:
		ter =''
	    try:
		try:
		    try:
			try:
			    try:
				try:
				    try:
					try:
					    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ул.")]').text()
					except IndexError:
					    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пер.")]').text()
				    except IndexError:
					uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"просп.")]').text()
				except IndexError:
				    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ш.")]').text()
			    except IndexError:
				uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"бул.")]').text()
			except IndexError:
			    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"проезд")]').text()
		    except IndexError:
			uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"наб.")]').text()
		except IndexError:
		    uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пл.")]').text()
	    except IndexError:
		uliza =''
	    
	    try:
		if uliza == '':
		    dom =''
		else:
		    dom = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(@href,"house")]').text()
	    except IndexError:
		dom = ''
		
	    try:
		seg = grab.doc.select(u'//dt[contains(text(),"Тип здания:")]/following-sibling::dd[1]').text()
	      #print oren
	    except DataNotFound:
		seg = '' 
		
	    try:
		naz = grab.doc.select(u'//div[@class="object_descr_title"]').text()
	      #print naz
	    except IndexError:
		naz = '' 
		
	    try:
		klass = grab.doc.select(u'//dt[contains(text(),"Класс:")]/following-sibling::dd[1]').text()
	    except IndexError:
		klass = ''
		
	    try:
		price = grab.doc.select(u'//div[@class="object_descr_price"]').text()
	      #print price
	    except IndexError:
		price = ''
		
	    try:
		plosh = grab.doc.select(u'//dt[contains(text(),"Площадь:")]/following-sibling::dd[1]').text()#.replace(u'м',u'м2')
	      #print plosh
	    except IndexError:
		plosh = '' 
		
	    try:
		et = grab.doc.select(u'//dt[contains(text(),"Этаж:")]/following-sibling::dd[1]').text().split(u' из ')[0]
	    except IndexError:
		et = ''
		
	    try:
		et2 = grab.doc.select(u'//dt[contains(text(),"Этаж:")]/following-sibling::dd[1]').text().split(u' из ')[1]
	    except IndexError:
		et2 = ''
		
	    try:
		ln = []
		for m in grab.doc.select(u'//div[@class="object_descr_text"]/text()'):
		    urr = m.text()
		    #print urr
		    ln.append(urr)		
		opis = "".join(ln)
	      #print opis
	    except IndexError:
		opis = ''
		
	    try:
		    try:
		        phone = re.sub(u'[^\d\+]','',grab.doc.select(u'//div[@class="cf_offer_show_phone-number"]/a').text())
                    except IndexError:
			phone = re.sub(u'[^\d\+]','',grab.doc.rex_text(u'offerPhone(.*?),'))
	    except IndexError:
		phone = '' 
		
	    try:
		try:
		    lico = grab.doc.select(u'//h3[@class="realtor-card__title"][contains(text(),"Представитель: ")]').text().replace(u'Представитель: ','')
		except IndexError:
		    lico = grab.doc.select(u'//h3[@class="realtor-card__title"]/a[contains(@href,"agents")]').text() 
	    except IndexError:
		lico = ''
		
	    try:
		try:
		    comp = grab.doc.select(u'//h3[@class="realtor-card__title"]/a[contains(@href,"company")]').text()
		except IndexError:
		    comp = grab.doc.select(u'//h4[@class="realtor-card__subtitle"]').text()
	    except IndexError:
		comp = '' 
	    try:
		ohrana = grab.doc.select(u'//dt[contains(text(),"Год постройки:")]/following-sibling::dd[1]').text()
	    except IndexError:
		ohrana =''
	    try:
		gaz = grab.doc.select(u'//h1').text()
	    except IndexError:
		gaz =''
	    try:
		voda =  grab.doc.select(u'//p[@class="objects_item_metro_prg"]/a').text()
	    except IndexError:
		voda =''
	    try:
		kanal = grab.doc.select(u'//p[@class="objects_item_metro_prg"]/span[2]').text()#.split(u'включая')[0]
	    except IndexError:
		kanal =''
	    try:
		elek = grab.doc.select(u'//title').text()
	    except IndexError:
		elek =''
	    try:
		teplo = grab.doc.select(u'//dt[contains(text(),"Парковка:")]/following-sibling::dd[1]').text()
	    except IndexError:
		teplo =''
		
	    try:
		conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		        (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		        (u'Окт', '.10.2017'),(u'окт', '.10.2017'),
		        (u'Сен', '.09.2017'),(u'сен', '.09.2017'),
		        (u'Авг', '.08.2017'),(u'авг', '.08.2017'),
		        (u'Июл', '.07.2017'),(u'июл', '.07.2017'),
		        (u'Июн', '.06.2017'),(u'июн', '.06.2017'),
		        (u'Фев', '.02.2017'),(u'фев', '.02.2017'),
		        (u'Мар', '.03.2017'),(u'мар', '.03.2017'),
		        (u'Апр', '.04.2017'),(u'апр', '.04.2017'), 
		        (u'Янв', '.01.2017'),(u'янв', '.01.2017'),
		        (u'Ноя', '.11.2017'),(u'ноя', '.11.2017'),
		        (u'Дек', '.12.2016'),(u'дек', '.12.2016'),
		        (u'Май', '.05.2017'),(u'май', '.05.2017')]
		dt= grab.doc.select(u'//ul[@class="offerStatuses"]/following-sibling::span[@class="object_descr_dt_added"]').text().split(', ')[0]
		data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
		       #print data
	    except IndexError:
		data = ''
		
		
	    try:
		lat = grab.doc.rex_text(u'center: (.*?)],').split(',')[0].replace('[','')
	    except IndexError:
		lat =''
	
	    try:
		lng = grab.doc.rex_text(u'center: (.*?)],').split(',')[1]
	    except IndexError:
		lng =''
		
	    try:
                cond = grab.doc.select(u'//dt[contains(text(),"Кондиционирование:")]/following-sibling::dd[1]').text()
            except IndexError:
	        cond =''
		
	    try:
	        vent = grab.doc.select(u'//dt[contains(text(),"Вентиляция:")]/following-sibling::dd[1]').text()
	    except IndexError:
	        vent =''		
		
	    try:
		li = []
		for e in grab.doc.select(u'//ul[@class="cf-comm-offer-detail__infrastructure"]/li'):
		    ur = e.text()
		    #print ur
		    li.append(ur)		
		uslu = ",".join(li)
	    except IndexError:
	        uslu = ''		
	    
	    projects = {'url': task.url,
		        'sub': self.sub,
		        'ray': ray,
		        'punkt': punkt.replace(u' городской округ',''),
		        'teritor': ter,
		        'uliza': uliza,
		        'dom': dom,
		        'seg': seg,
		        'naznachenie': naz,
		        'klass': klass,
	                'uslovi': usl,
	                'uslugi':uslu,
		        'cena': price,
		        'ploshad': plosh,
		        'et': et,
		        'ets': et2,
		        'opisanie': opis,
		        'phone':phone.replace(u'79311111111',''),
		        'company':comp,
		        'lico':lico,
		        'ohrana':ohrana,
		        'gaz': gaz,
		        'voda': voda,
		        'kanaliz': kanal,
		        'electr': elek,
		        'teplo': teplo,
	                'condi':cond,
	                'internet':vent,
	                'dol': lat,
	                'shir': lng,	                
		        'data':data,
		        'oper':oper
		        
		        }
	    yield Task('write',project=projects,grab=grab)
	    
	def task_write(self,grab,task):
	    
	    print('*'*50)
	    print  task.project['sub']
	    print  task.project['ray']
	    print  task.project['punkt']
	    print  task.project['teritor']
	    print  task.project['uliza']
	    print  task.project['dom']
	    print  task.project['seg']
	    print  task.project['naznachenie']
	    print  task.project['uslovi'] 
	    print  task.project['klass']
	    print  task.project['cena']
	    print  task.project['ploshad']
	    print  task.project['et']
	    print  task.project['ets']
	    print  task.project['opisanie']
	    print  task.project['url']
	    print  task.project['phone']
	    print  task.project['lico']
	    print  task.project['company']
	    print  task.project['ohrana']
	    print  task.project['gaz']
	    print  task.project['voda']
	    print  task.project['kanaliz']
	    print  task.project['electr']
	    print  task.project['teplo']
	    print  task.project['data']
	    
	    
	    
	    
	    self.ws.write(self.result, 0, task.project['sub'])
	    self.ws.write(self.result, 1, task.project['ray'])
	    self.ws.write(self.result, 2, task.project['punkt'])
	    self.ws.write(self.result, 3, task.project['teritor'])
	    self.ws.write(self.result, 4, task.project['uliza'])
	    self.ws.write(self.result, 5, task.project['dom'])
	    self.ws.write(self.result, 43, task.project['internet'])
	    self.ws.write(self.result, 8, task.project['seg'])
	    self.ws.write(self.result, 42, task.project['uslugi'])
	    self.ws.write(self.result, 9, task.project['naznachenie'])
	    self.ws.write(self.result, 10, task.project['klass'])
	    self.ws.write(self.result, 11, task.project['cena'])
	    self.ws.write(self.result, 14, task.project['ploshad'])	
	    self.ws.write(self.result, 13, task.project['uslovi'])
	    self.ws.write(self.result, 15, task.project['et'])
	    self.ws.write(self.result, 16, task.project['ets'])
	    self.ws.write(self.result, 39, task.project['condi'])
	    self.ws.write(self.result, 34, task.project['shir'])
	    self.ws.write(self.result, 35, task.project['dol'])
	    self.ws.write(self.result, 17, task.project['ohrana'])
	    self.ws.write(self.result, 24, task.project['gaz'])
	    self.ws.write(self.result, 26, task.project['voda'])
	    self.ws.write(self.result, 27, task.project['kanaliz'])
	    self.ws.write(self.result, 33, task.project['electr'])
	    self.ws.write(self.result, 37, task.project['teplo'])
	    self.ws.write_string(self.result, 20, task.project['url'])
	    self.ws.write(self.result, 21, task.project['phone'])
	    self.ws.write(self.result, 22, task.project['lico'])
	    self.ws.write(self.result, 23, task.project['company'])
	    self.ws.write(self.result, 30, task.project['data'])
	    self.ws.write(self.result, 18, task.project['opisanie'])
	    self.ws.write(self.result, 19, u'ЦИАН')
	    self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	    self.ws.write(self.result, 28, task.project['oper'])
	    
	    
	    print('*'*50)
	    print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	    print 'Tasks - %s' % self.task_queue.size()
	    print '***',i+1,'/',len(l),'***'
	    print  task.project['oper']
	    print('*'*50)
	    
	    self.result+= 1
	    
	    
	    
	    #if self.result > 10:
		#self.stop()	
	    
	    
	   
    bot = Cian_Com(thread_number=1,network_try_limit=1000)
    bot.load_proxylist('../tipa.txt','text_file')
    bot.create_grab_instance(timeout=5, connect_timeout=10)
    bot.run()
    print('Wait 2 sec...')
    time.sleep(2)
    print('Save it...')
    try:
	command = 'mount -a'
	os.system('echo %s|sudo -S %s' % ('1122', command))
	time.sleep(3)
	bot.workbook.close()
	print('Done')
    except IOError:
	time.sleep(30)
	os.system('echo %s|sudo -S %s' % ('1122', 'mount -a'))
	time.sleep(10)
	bot.workbook.close()
	print('Done!')
    i=i+1
    try:
        page = l[i]
    except IndexError:
        if oper == u'Продажа':
	    i = 0
	    l= open('Links/com_a1.txt').read().splitlines()
	    dc = len(l)
	    page = l[i]
	    oper = u'Аренда'
        else:
	    break