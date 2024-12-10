#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import time
from grab import Grab
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)




i = 0
l= open('links/Com_prod.txt').read().splitlines()
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
                    time.sleep(1)
		    g = Grab(timeout=20, connect_timeout=20)
		    g.proxylist.load_file(path='../tipa.txt',proxy_type='http') 
                    g.go(self.f)
                    self.sub = g.doc.select(u'//div[@class="adress adr"]').text().split(u', ')[0].replace(u' обл',u' область')
                    print self.sub
		    del g
                    break
                except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
                    print g.config['proxy'],'Change proxy'
                    g.change_proxy()
		    del g
                    continue
	     
	    self.workbook = xlsxwriter.Workbook(u'com/Ndv31_%s' % bot.sub + u'_Коммерческая_'+oper+str(i+1)+'.xlsx')
	    self.ws = self.workbook.add_worksheet(u'Ndv31_Коммерческая')
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
	    self.ws.write(0, 32, u"ДАТА_ПАРСИНГА")
	    self.ws.write(0, 33, u"ОПЕРАЦИЯ")
	    self.ws.write(0, 34, u"ЦЕНА_ЗА_М2")
	    self.ws.write(0, 35, u"МЕСТОПОЛОЖЕНИЕ")
	    self.result= 1
	    

	
	def task_generator(self):
	    yield Task ('post',url=page,refresh_cache=True,network_try_count=100)
	    
	    
	    
	def task_page(self,grab,task):
	    try:
		pg = grab.doc.select(u'//li[@class="pager-next"]/a')
		u = grab.make_url_absolute(pg.attr('href'))
		yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	    except DataNotFound:
		print('*'*100)
		print '!!!!!!!','NO PAGE NEXT','!!!'
		print('*'*100)
		logger.debug('%s taskq size' % self.task_queue.size())	
	    
	def task_post(self,grab,task):
	    links = grab.doc.select(u'//h3[@class="field-content"]/a')
		
	    for elem in links:
		ur = grab.make_url_absolute(elem.attr('href'))  
		#print ur
		yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	    yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
			
      
	    
	    
	    
	    
	def task_item(self, grab, task):
	    
	    
	    try:
		ray = grab.doc.select(u'//a[@class="js-popup-select popup-select Province-popup"]/following::span[1]').text()
	    except DataNotFound:
		ray =''
	    try:
		#if  grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(text(),"р-н")]').exists()==True:
		    #punkt= grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p').text().split(', ')[2]
		#else:
		punkt= grab.doc.select(u'//h1').text().split('. ')[1].split(', ')[0]
	    except IndexError:
		punkt = ''
	    try:
		#if  grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(text()," ул")]').exists()==False:
		ter= grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text().split(', ')[0]#.replace(u'ул.','')
		#else:
		    #ter= ''
	    except IndexError:
		ter =''    
	    try:
		#try:
		    #uliza = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(text()," ул")]').text()
		#except DataNotFound:
		uliza = grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text().split(', ')[1]
		#except DataNotFound:
		    #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"шоссе")]').text()
	    except IndexError:
		uliza = '' 
	    try:
		dom = grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text().split(', ')[2]
		
	    except IndexError:
		dom = ''
		
	    try:
		orentir = grab.doc.select(u'//label[contains(text(),"Жилой комплекс:")]/following-sibling::p').text()
	    except DataNotFound:
		orentir = ''
		
	    try:
	        seg = grab.doc.select(u'//div[@class="object-info--price-sq"]').text()
	      #print oren
	    except DataNotFound:
		seg = '' 
		
	    try:
	        naz = grab.doc.grab.doc.select(u'//h1').text().split('. ')[0].replace(u'Продам ','').replace(u'Сдам ','')
	      #print naz
	    except DataNotFound:
		naz = '' 
		
	    try:
		klass = grab.doc.rex_text(u'класса (.*?). ')[:1]
	    except DataNotFound:
		klass = ''
		
	    try:
	        price = grab.doc.select(u'//div[@class="object-info--price"]').text()
	      #print price
	    except DataNotFound:
		price = ''
		
	    try:
	        plosh = grab.doc.select(u'//div[@class="object-info--s"]').text()#.replace(u'м',u'м2')
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
	        opis = grab.doc.select(u'//div[@class="object-info--description"]').text()
	      #print opis
	    except DataNotFound:
		opis = ''
		
	    try:
		phone = re.sub('[^\d\+]','',grab.doc.select(u'//div[@class="manger-info--phone"]').text())
	      #print phone
	    except DataNotFound:
		phone = '' 
		
	    try:
		lico = grab.doc.select(u'//div[@class="manager-info--name"]').text()#.split(', ')[1]
	    except IndexError:
		lico = ''
		
	    try:
	        comp = grab.doc.select(u'//a[@rel="nofollow"]').text().replace(u'Показать телефон','')
	      #print comp
	      
	    except DataNotFound:
		comp = '' 
	    try:
		ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
	    except DataNotFound:
		ohrana =''
	    try:
		gaz = re.sub(u'^.*(?=газ)','', grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
	    except DataNotFound:
		gaz =''
	    try:
		voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
	    except DataNotFound:
		voda =''
	    try:
		kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	    except DataNotFound:
		kanal =''
	    try:
		elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	    except DataNotFound:
		elek =''
	    try:
		teplo =  grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text()
	    except DataNotFound:
		teplo =''
		
	    try:
		data= grab.doc.select(u'//span[contains(text(),"Дата публикации:")]/following-sibling::div').text().replace('-','.')
	    except IndexError:
		data = ''
		
	    
	    
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
		        'phone':phone,
		        'company':comp,
		        'lico':lico,
		        'ohrana':ohrana,
		        'gaz': gaz,
		        'voda': voda,
		        'kanaliz': kanal,
		        'electr': elek,
		        'teplo': teplo,
		        'data':data}
	    
	    yield Task('write',project=projects,grab=grab)
	    
	def task_write(self,grab,task):
	    
	    print('*'*50)
	    print  task.project['sub']
	    print  task.project['ray']
	    print  task.project['punkt']
	    print  task.project['teritor']
	    print  task.project['uliza']
	    print  task.project['dom']
	    print  task.project['orentir']
	    print  task.project['seg']
	    print  task.project['naznachenie']
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
	    self.ws.write(self.result, 6, task.project['orentir'])
	    self.ws.write(self.result, 34, task.project['seg'])
	    #self.ws.write(self.result, 8, task.project['tip'])
	    self.ws.write(self.result, 9, task.project['naznachenie'])
	    self.ws.write(self.result, 10, task.project['klass'])
	    self.ws.write(self.result, 11, task.project['cena'])
	    self.ws.write(self.result, 12, task.project['ploshad'])	
	    self.ws.write(self.result, 13, task.project['et'])
	    self.ws.write(self.result, 14, task.project['ets'])
	    #self.ws.write(self.result, 15, task.project['god'])
	    #self.ws.write(self.result, 16, task.project['mat'])
	    #self.ws.write(self.result, 17, task.project['potolok'])
	    #self.ws.write(self.result, 18, task.project['sost'])
	    self.ws.write(self.result, 19, task.project['ohrana'])
	    self.ws.write(self.result, 20, task.project['gaz'])
	    self.ws.write(self.result, 21, task.project['voda'])
	    self.ws.write(self.result, 22, task.project['kanaliz'])
	    self.ws.write(self.result, 23, task.project['electr'])
	    self.ws.write(self.result, 35, task.project['teplo'])
	    self.ws.write_string(self.result, 27, task.project['url'])
	    self.ws.write(self.result, 28, task.project['phone'])
	    self.ws.write(self.result, 29, task.project['lico'])
	    self.ws.write(self.result, 30, u'ООО Золотая Середина')
	    self.ws.write(self.result, 31, task.project['data'])
	    self.ws.write(self.result, 25, task.project['opisanie'])
	    self.ws.write(self.result, 26, u'АН "Золотая Середина"')
	    self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
	    self.ws.write(self.result, 33, oper)
	    
	    
	    print('*'*50)
            print self.sub
            print 'Ready - '+str(self.result)
            logger.debug('Tasks - %s' % self.task_queue.size()) 
            print '***',i+1,'/',dc,'***'
            print oper
            print('*'*50)
	    
	    self.result+= 1
	    
	    #if self.result > 50:
		#self.stop()	

    bot = MK_Com(thread_number=5,network_try_limit=1000)
    bot.load_proxylist('../tipa.txt','text_file')
    bot.create_grab_instance(timeout=500, connect_timeout=5000)
    bot.run()
    print('Wait 2 sec...')
    time.sleep(2)
    print('Save it...')
    try:
	command = 'mount -a'
	os.system('echo %s|sudo -S %s' % ('1122', command))
	time.sleep(2)
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
            l= open('links/Com_arenda.txt').read().splitlines()
            dc = len(l)
            page = l[i]
            oper = u'Аренда'
        else:
            break    