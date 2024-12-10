#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
import re
import urllib
import time
import random
import os
import xlsxwriter
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



workbook = xlsxwriter.Workbook(u'HH_7_Requests.xlsx')




class Brsn_Com(Spider):
    
    
    
    def prepare(self):
	 
	
	self.ws = workbook.add_worksheet(u'HH')
	self.ws.write(0, 0, u"ПОЧТА")
	self.ws.write(0, 1, u"ТЕЛЕФОН")
	self.ws.write(0, 2, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	self.ws.write(0, 3, u"ЗАПРОС")
	#self.ws.write(0, 4, u"УЛИЦА")
	#self.ws.write(0, 5, u"ДОМ")
	#self.ws.write(0, 6, u"ОРИЕНТИР")
	#self.ws.write(0, 7, u"СЕГМЕНТ")
	#self.ws.write(0, 8, u"ТИП_ПОСТРОЙКИ")
	#self.ws.write(0, 9, u"НАЗНАЧЕНИЕ_ОБЪЕКТА")
	#self.ws.write(0, 10, u"ПОТРЕБИТЕЛЬСКИЙ_КЛАСС")
	#self.ws.write(0, 11, u"СТОИМОСТЬ")
	#self.ws.write(0, 12, u"ИЗМЕНЕНИЕ_СТОИМОСТИ")
	#self.ws.write(0, 13, u"ДОПОЛНИТЕЛЬНЫЕ_КОММЕРЧЕСКИЕ_УСЛОВИЯ")
	#self.ws.write(0, 14, u"ПЛОЩАДЬ")
	#self.ws.write(0, 15, u"ЭТАЖ")
	#self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	#self.ws.write(0, 17, u"ГОД_ПОСТРОЙКИ")
	#self.ws.write(0, 18, u"ОПИСАНИЕ")
	#self.ws.write(0, 19, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	#self.ws.write(0, 20, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	#self.ws.write(0, 21, u"ТЕЛЕФОН")
	#self.ws.write(0, 22, u"КОНТАКТНОЕ_ЛИЦО")
	#self.ws.write(0, 23, u"КОМПАНИЯ")
	#self.ws.write(0, 24, u"МЕСТОПОЛОЖЕНИЕ")
	#self.ws.write(0, 25, u"МЕСТОРАСПОЛОЖЕНИЕ")
	#self.ws.write(0, 26, u"БЛИЖАЙШАЯ_СТАНЦИЯ_МЕТРО")
	#self.ws.write(0, 27, u"РАССТОЯНИЕ_ДО_БЛИЖАЙШЕЙ_СТАНЦИИ_МЕТРО")
	#self.ws.write(0, 28, u"ОПЕРАЦИЯ")
	#self.ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
	#self.ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ")
	#self.ws.write(0, 31, u"ДАТА_ПАРСИНГА")
	#self.ws.write(0, 32, u"КАДАСТРОВЫЙ_НОМЕР")
	#self.ws.write(0, 33, u"ЗАГОЛОВОК")
	#self.ws.write(0, 34, u"ШИРОТА_ИСХ")
	#self.ws.write(0, 35, u"ДОЛГОТА_ИСХ")
	self.result= 1
	
            
            
            
              
    
    def task_generator(self):
        yield Task ('post',url='https://hh.ru/search/vacancy?text=Event',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Ивент',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Кейтеринг',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Декоратор',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Креатор',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Организатор',network_try_count=100,refresh_cache=True)
	yield Task ('post',url='https://hh.ru/search/vacancy?text=Мероприятие',network_try_count=100,refresh_cache=True)

	
	
	
  
        
    def task_post(self,grab,task):
        
	for elem in grab.doc.select(u'//div[@class="vacancy-serp-item__title"]/a'):
	    ur = grab.make_url_absolute(elem.attr('href'))  
	    #print ur
	    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	    
    def task_page(self,grab,task):
	try:
	    pg = grab.doc.select(u'//a[@data-qa="pager-next"]')
	    u = grab.make_url_absolute(pg.attr('href'))
	    yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	except IndexError:
	    print('*'*100)
	    print '!!!','NO PAGE NEXT','!!!'
	    print('*'*100)	
  
	
        
        
        
    def task_item(self, grab, task):
	
        try:
            sub = grab.doc.select(u'//div[@class="vacancy-contacts__body"]/a[contains(@href,"mailto")]').text()
        except IndexError:
            sub = ''
	try:
            ray = grab.doc.select(u'//p[@data-qa="vacancy-contacts__phone"]').text().split(', ')[0]
        except IndexError:
            ray = random.choice(list(open('../../phone.txt').read().splitlines()))
        #try:
            #if sub == u"Москва":
                #punkt= u"Москва"
            #else:
		#if grab.doc.select(u'//div[@class="breadcrumbs"]/a[4]').text().find(u'метро')>=0:
                    #punkt = grab.doc.select(u'//dt[contains(text(),"Адрес:")]/following-sibling::dd[1]').text().split(', ')[1]
		#else:
		    #punkt = grab.doc.select(u'//div[@class="breadcrumbs"]/a[4]').text()
        #except IndexError:
            #punkt = ''
        #try:
            #ter= grab.doc.select(u'//dt[contains(text(),"Округ:")]/following-sibling::dd[1]').text()
        #except IndexError:
            #ter =''	    
	#try:
            #uliza = grab.doc.select(u'//dt[contains(text(),"Комиссия/Тип договора:")]/following-sibling::dd[1]/span').text()
        #except IndexError:
	    #uliza = '' 
	#try:
            #dom = grab.doc.select(u'//dt[contains(text(),"Тип строения:")]/following-sibling::dd[1]').text()
        #except IndexError:
	    #dom = ''
	    
	#try:
            #seg = grab.doc.select(u'//a[@class="active_tabs"][contains(@name,"karta")]').text().split(' - ')[0]
        #except IndexError:
            #seg = '' 
	    
	#try:
            #naz = grab.doc.select(u'//h3[contains(text(),"Назначение помещения:")]/following-sibling::p').text()
          ##print naz
        #except IndexError:
	    #naz = '' 
	    
        #try:
            #klass = grab.doc.select(u'//dt[contains(text(),"Класс строения:")]/following-sibling::dd[1]').text()
        #except IndexError:
            #klass = ''
	    
	#try:
	    ##try:
	    #price = grab.doc.select(u'//span[@class="price_row"]').text()#.split(': ')[1]
	    ##except IndexError:
		##price = grab.doc.select(u'//span[@class="price_row"]').text()#.split(': ')[1]+u' / за м2'
	#except IndexError:
	    #price = ''
	    
	#try:
            #plosh = grab.doc.select(u'//dt[contains(text(),"Общая площадь:")]/following-sibling::dd[1]').text()
          ##print plosh
        #except IndexError:
            #plosh = '' 
	    
        #try:
            #et = grab.doc.select(u'//dt[contains(text(),"Ближайшие станции метро:")]/following-sibling::dd[1]').text()
        #except IndexError:
            #et = ''
	    
        #try:
            #mat = grab.doc.select(u'//h1/span').text()
        #except IndexError:
            #mat = ''
	    
	#try:
            #opis = grab.doc.select(u'//div[@class="item_description"]').text()
        #except IndexError:
            #opis = ''
	    
        #try:
            #phone = re.sub('[^\d\+]','',grab.doc.select(u'//dt[contains(text(),"Телефон владельца:")]/following-sibling::dd[1]/span[@id="owner-phone"]').text())[:12]
          ##print phone
        #except IndexError:
            #phone = '' 
	    
        #try:
            #lico = grab.doc.select(u'//span[@class="user-name"]').text()
        #except IndexError:
            #lico = ''
	    
	#try:
            #comp = grab.doc.select(u'//div[@class="name_block_item"]/span[contains(text(),"(агент)")]').text()
        #except IndexError:
            #comp = '' 
	#try:
	    #ohrana = grab.doc.select(u'//dt[contains(text(),"Адрес:")]/following-sibling::dd[1]').text()
	#except IndexError:
	    #ohrana =''
	#try:
	    #gaz = grab.doc.rex_text(u'google.maps.LatLng(.*?);').split(', ')[0].replace('(','')
	#except IndexError:
	    #gaz =''
	#try:
	    #voda = grab.doc.rex_text(u'google.maps.LatLng(.*?);').split(', ')[1].replace(')','')
	#except IndexError:
	    #voda =''
	#try:
	    #kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	#except IndexError:
	    #kanal =''
	#try:
	    #elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	#except IndexError:
	    #elek =''
	#try:
	    #teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	#except IndexError:
	    #teplo =''
	    
	#try:
            #data= grab.doc.rex_text(u'Дата обновления: <nobr>(.*?)</nobr>').split(' ')[0]
        #except IndexError:
            #data = ''
	    
        try:
            oper = urllib.unquote(task.url).decode('utf8').split('query=')[1]
        except IndexError:
            oper = ''
	    
	
	    
	
	projects = {'url': urllib.unquote(task.url).decode('utf8') ,
	            'sub': sub,
	            'oper':oper,
	            'ray': re.sub('[^\d\+]','',ray)
	            #'punkt':  re.sub('[\d]','',punkt).replace(u'Объявление',''),
	            #'teritor': ter,
	            #'uliza': uliza,
	            #'dom': dom,
	            #'seg': seg,
	            #'naznachenie': naz,
	            #'klass': klass,
	            #'cena': price,
	            #'ploshad': plosh,
	            #'et': et,
	            #'mat': mat,
	            #'opisanie': opis,
	            #'phone':phone,
	            #'company':comp,
	            #'lico':lico,
	            #'ohrana':ohrana,
                    #'gaz': gaz,
                    #'voda': voda,
                    #'kanaliz': kanal,
                    #'electr': elek,
                    #'teplo': teplo,
	            #'data':data,
	            #'oper':oper
	            
	            }
	yield Task('write',project=projects,grab=grab)
	
    def task_write(self,grab,task):
	
	print('*'*50)
	print  task.project['sub']
	print  task.project['ray']
	#print  task.project['punkt']
	#print  task.project['teritor']
	#print  task.project['uliza']
	#print  task.project['dom']
	#print  task.project['seg']
	#print  task.project['naznachenie']
	#print  task.project['klass']
	#print  task.project['cena']
	#print  task.project['ploshad']
	#print  task.project['et']
	#print  task.project['mat']
	#print  task.project['opisanie']
	print  task.project['url']
	#print  task.project['phone']
	#print  task.project['lico']
	#print  task.project['company']
	#print  task.project['ohrana']
	#print  task.project['gaz']
	#print  task.project['voda']
	#print  task.project['kanaliz']
	#print  task.project['electr']
	#print  task.project['teplo']
	#print  task.project['data']
	print  task.project['oper']
	
	
	
	self.ws.write_string(self.result, 0, task.project['sub'])
	self.ws.write_string(self.result, 1, task.project['ray'])
	self.ws.write_string(self.result, 2, task.project['url'])
	self.ws.write_string(self.result, 3, task.project['oper'])
	#self.ws.write(self.result, 13, task.project['uliza'])
	#self.ws.write(self.result, 8, task.project['dom'])
	##self.ws.write(self.result, 6, task.project['orentir'])
	#self.ws.write(self.result, 7, task.project['seg'])
	##self.ws.write(self.result, 8, task.project['tip'])
	#self.ws.write(self.result, 9, task.project['naznachenie'])
	#self.ws.write(self.result, 10, task.project['klass'])
	#self.ws.write(self.result, 11, task.project['cena'])
	#self.ws.write(self.result, 14, task.project['ploshad'])	
	#self.ws.write(self.result, 26, task.project['et'])
	##self.ws.write(self.result, 14, task.project['ets'])
	##self.ws.write(self.result, 15, task.project['god'])
	#self.ws.write(self.result, 33, task.project['mat'])
	##self.ws.write(self.result, 17, task.project['potolok'])
	##self.ws.write(self.result, 18, task.project['sost'])
	#self.ws.write(self.result, 24, task.project['ohrana'])
	#self.ws.write(self.result, 34, task.project['gaz'])
	#self.ws.write(self.result, 35, task.project['voda'])
	##self.ws.write(self.result, 22, task.project['kanaliz'])
	##self.ws.write(self.result, 23, task.project['electr'])
	##self.ws.write(self.result, 24, task.project['teplo'])
	#self.ws.write_string(self.result, 20, task.project['url'])
	#self.ws.write(self.result, 21, task.project['phone'])
	#self.ws.write(self.result, 22, task.project['lico'])
	#self.ws.write(self.result, 23, task.project['company'])
	#self.ws.write(self.result, 30, task.project['data'])
	#self.ws.write(self.result, 18, task.project['opisanie'])
	#self.ws.write(self.result, 19, u'Базаметров.ру')
	#self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	#self.ws.write(self.result, 28, task.project['oper'])
	
	print('*'*50)
	print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	logger.debug('Tasks - %s' % self.task_queue.size()) 
	print('*'*50)
	
	self.result+= 1
	
        #if self.result > 200:
	    #self.stop()	
	

 
       
bot = Brsn_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
try:
    bot.run()
except KeyboardInterrupt:
    pass
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
workbook.close()
print('Done')

