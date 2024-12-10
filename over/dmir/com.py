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
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http') 



i = 0
l= open('Links/Com_Prod.txt').read().splitlines()
dc = len(l)
page = l[i]  
oper = u'Продажа'
     


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     

     class Dmir_Com(Spider):
	  
	  
	  
          def prepare(self):
	       #self.count = 1 
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
			 time.sleep(5)
			 g = Grab(timeout=50, connect_timeout=100)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
			 g.go(self.f)
			 #conv = [ (u'кой',u'кая'),(u'области',u'область'),(u'ком',u'кий'),
				  #(u'Москве',u'Москва'),(u'Петербурге',u'Петербург'),
				  #(u'крае',u'край'),(u'республике','')]
			 #dt= g.doc.rex_text(u'недвижимости (.*?)</h1>').replace(u'кой',u'кая').replace(u'области',u'область') 
			 self.sub = g.doc.select(u'//a[@class="menu-first-child"]').text()#reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
			 self.num = re.sub('[^\d]','',g.doc.select(u'//title').text().split(' - ')[0])
                         self.pag = int(math.ceil(float(int(self.num))/float(120)))
                         print self.sub,self.num,self.pag
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 del g
			 continue	  	       
	       self.workbook = xlsxwriter.Workbook(u'com/Dmir_%s' % bot.sub + u'_Коммерческая_'+oper+'.xlsx')
               self.ws = self.workbook.add_worksheet(u'Dmir_Коммерческая')
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
	       self.result= 1
	      
            
            
            
              
    
	  def task_generator(self):
	       for x in range(1,self.pag+1):
	            yield Task ('post',url=self.f+'&page=%d'%x,refresh_cache=True,network_try_count=100)
             
	  def task_post(self,grab,task):
     
	       for elem in grab.doc.select(u'//td/input[@type="hidden"]/following-sibling::a'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)

	  def task_item(self, grab, task):
	       try:
		    mesto =  grab.doc.select(u'//h2[@class="subtitle"]/small').text() 
	       except IndexError:
	            mesto = ''
	     
	       try:
		    ray =  grab.doc.rex_text(u'в (.*?)районе</a></li></ul>').replace(u'ком',u'кий').split(' (')[0].replace(u'в ','') 
	       except IndexError:
		    ray = ''
	       try:
		    #if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
                         #punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
                    #else:    
                    punkt = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[1]
	       except IndexError:
		    punkt = ''
	       try:
		    try:
                         uliza = grab.doc.rex_text(u'Купить (.*?) в')
		    except IndexError:
			 uliza = grab.doc.rex_text(u'Купить (.*?) у')
	       except IndexError:
		    uliza = ''
               try:
                    dom = grab.doc.rex_text(u'в (.*?)районе</a></li></ul>').split(' (')[1].replace(u')','')
               except IndexError:
                    dom = ''
		    
               try:
                    tip = grab.doc.select(u'//ul[@id="house_data"]/li[contains(text(),"тип строения")]/b').text()#.split(' ')[0]
               except IndexError:
                    tip = ''
	       try:
                    naz = grab.doc.select(u'//h1').text()#.split(',')[0].replace(u'Сдаю ','').replace(u'Продаю ','')
               except IndexError:
                    naz = ''
	       try:
                    klass = grab.doc.select(u'//ul[@id="house_data"]/li[contains(text(),"класс")]').text().split(' ')[0]
               except IndexError:
                    klass = ''
	       try:
		    #if grab.doc.select(u'//span[@id="price_offer"]').text().find(u'сотку') < 0:
	            price = grab.doc.select('//span[@id="price_offer"]').text()
                    #else:
                         #price =''
               except IndexError:
	            price = ''
               try:
                    et = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"этаж")]').number()
               except IndexError:
                    et = ''
		    
               try:
                    et2 = grab.doc.select(u'//li[contains(text(),"этажность")]').number()
               except IndexError:
                    et2 = ''
		    
               try:
                    god = grab.doc.select(u'//li[contains(text(),"год постройки")]/b').number()
               except IndexError:
                    god = ''
		    
               try:
                    mat = grab.doc.select(u'//li[contains(text(),"дом")]/b').text()
               except IndexError:
                    mat = ''
		    
               try:
		    try:
                         pot = re.sub(u'[^0-9а-я .]','',grab.doc.rex_text(u'залог:(.*?)</td></tr>'))+' - залог'
		    except IndexError:
			 pot = re.sub(u'[^0-9а-я .]','',grab.doc.rex_text(u'предоплата:(.*?)</td></tr>'))+' - предоплата'
               except IndexError:
                    pot = ''
		    
               try:
                    sos = grab.doc.select(u'//li[contains(text(),"состояние")]/b').text()
               except DataNotFound:
                    sos = ''
               try:
                    plosh = grab.doc.select(u'//li[contains(text(),"общая площадь")]').text().replace(u' общая площадь','')
               except IndexError:
                    plosh = ''
               
               try:
                    gaz = re.sub('[^\d\.]','',grab.doc.rex_text(u'rLatLng(.*?);').split(', ')[0])
               except IndexError:
                    gaz =''
               try:
                    voda = re.sub('[^\d\.]','',grab.doc.rex_text(u'rLatLng(.*?);').split(', ')[1])
               except IndexError:
                    voda =''
               try:
                    kanal = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"канализация")]').text().replace(u'есть канализация',u'есть').replace(u'нет канализации','')
               except IndexError:
                    kanal =''
               try:
                    elekt = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"электричество")]').text().replace(u'есть электричество',u'есть').replace(u'нет электричества','')
               except IndexError:
                    elekt =''
	       try:
	            teplo = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"отопление")]').text().replace(u'есть отопление',u'есть').replace(u'нет отопления','')
               except IndexError:
	            teplo =''
	       try:
                    ohrana = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"охрана")]').text().replace(u'есть охрана',u'есть').replace(u'нет охраны','')
               except IndexError:
                    ohrana =''
               try:
                    park = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"парковка")]').text().replace(u'есть парковка',u'есть').replace(u'нет парковки','')
               except IndexError:
                    park =''
               try:
	            opis = grab.doc.select(u'//div[@class="mb20 objectDesc"]').text() 
	       except IndexError:
	            opis = ''
               try:
                    ph = grab.doc.rex_text('<div class="phone">(.*?)</div>').replace('<br>',',')
                    phone = re.sub('[^\d\,]', u'',ph)
               except IndexError:
                    phone = ''
	    
               try:
                    lico = grab.doc.select(u'//dt[contains(text(),"Разместил")]/following-sibling::dd/span').text()
               except IndexError:
	            lico = ''
	    
	       try:
	            com = grab.doc.select(u'//dt[contains(text(),"Компания")]/following-sibling::dd/span').text()
               except IndexError:
	            com = ''
	       try:
	            data = grab.doc.select(u'//dt[contains(text(),"Размещено")]/following::span[1]').text()
	       except IndexError:
	            data = ''
	    
	       try:
		    try:
	                 data1 =  grab.doc.select(u'//li[@class="metro"]/b[contains(text(),"м.")]').text()#.split(', ')[1]
		    except IndexError:
			 data1 =  grab.doc.select(u'//th[contains(text(),"метро:")]/following-sibling::td').text().split(', ')[0]
	       except IndexError:
	            data1 = ''
   
               try:
                    try:
                         data2 =  grab.doc.select(u'//li[@class="metro"][contains(text(),"ш.")]/text()[1]').text()#.split(', ')[1]
                    except IndexError:
	                 data2 =  grab.doc.select(u'//th[contains(text(),"шоссе:")]/following-sibling::td').text().split(', ')[0]
               except IndexError:
                    data2 = ''
	
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt[1:],
		           'ulica': uliza,
	                   'dom': dom,
	                   'naz': naz,
	                   'tip': tip,
	                   'price': price,
	                   'klass': klass,
	                   'ploshad': plosh,
	                   'et': et,
	                   'ets': et2,
	                   'god': god,
	                   'mat': mat,
	                   'potolok': pot,
	                   'sost': sos,
	                   'gaz': gaz,
	                   'voda':voda,
	                   'kanal': kanal,
	                   'elekt': elekt,
	                   'teplo': teplo,
	                   'ohrana': ohrana,
	                   'parkovka': park,
	                   'opis': opis,
	                   'phone': phone,
	                   'mesto':mesto,
	                   'lico':lico,
	                   'company':com,
	                   'dataraz': data,
	                   'data1': data1,
	                   'data2': data2
	                      }
	
	
	
	       yield Task('write',project=projects,grab=grab)
	

	
	
	
	
	  def task_write(self,grab,task):
	       if task.project['opis'] <> '':
		    print('*'*100)
		    print  task.project['sub']
		    print  task.project['rayon']
		    print  task.project['punkt']
		    print  task.project['ulica']
		    print  task.project['dom']
		    print  task.project['naz']
		    print  task.project['tip']
		    print  task.project['price']
		    print  task.project['klass']
		    print  task.project['ploshad']
		    print  task.project['et']
		    print  task.project['ets']
		    print  task.project['god']
		    print  task.project['mat']
		    print  task.project['potolok']
		    print  task.project['sost']
		    print  task.project['gaz']
		    print  task.project['voda']
		    print  task.project['kanal']
		    print  task.project['elekt']
		    print  task.project['teplo']
		    print  task.project['ohrana']
		    print  task.project['parkovka']
		    print  task.project['opis']
		    print  task.project['url']
		    print  task.project['phone']
		    print  task.project['lico']
		    print  task.project['company']
		    print  task.project['dataraz']
		    print  task.project['mesto']
		    print  task.project['data1']
		    print  task.project['data2']
		    
		    self.ws.write(self.result,0, task.project['sub'])
		    self.ws.write(self.result,1, task.project['rayon'])
		    self.ws.write(self.result,2, task.project['punkt'])
		    self.ws.write(self.result,7, task.project['ulica'])
		    self.ws.write(self.result,3, task.project['dom'])
		    self.ws.write(self.result,33, task.project['naz'])
		    self.ws.write(self.result,8, task.project['tip'])
		    self.ws.write(self.result,28, oper)
		    self.ws.write(self.result,11, task.project['price'])
		    self.ws.write(self.result,10, task.project['klass'])
		    self.ws.write(self.result,14, task.project['ploshad'])
		    self.ws.write(self.result,15, task.project['et'])
		    self.ws.write(self.result,16, task.project['ets'])
		    self.ws.write(self.result,17, task.project['god'])
		    self.ws.write(self.result,16, task.project['mat'])
		    self.ws.write(self.result,13, task.project['potolok'])
		    #self.ws.write(self.result,18, task.project['sost'])
		    self.ws.write(self.result,34, task.project['gaz'])
		    self.ws.write(self.result,35, task.project['voda'])
		    #self.ws.write(self.result,22, task.project['kanal'])
		    #self.ws.write(self.result,23, task.project['elekt'])
		    #self.ws.write(self.result,24, task.project['teplo'])
		    #self.ws.write(self.result,19, task.project['ohrana'])
		    self.ws.write(self.result,18, task.project['opis'])
		    self.ws.write(self.result,19, u'Недвижимость и цены')
		    self.ws.write_string(self.result,20, task.project['url'])
		    self.ws.write(self.result,21, task.project['phone'])
		    self.ws.write(self.result,22, task.project['lico'])
		    self.ws.write(self.result,23, task.project['company'])
		    self.ws.write(self.result,29, task.project['dataraz'])
		    self.ws.write(self.result,31, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result,26, task.project['data1'])
		    self.ws.write(self.result,36, task.project['data2'])
		    self.ws.write(self.result,37, task.project['parkovka'])
		    self.ws.write(self.result, 24, task.project['mesto'])
		   
		   
		    
	     
		    print('*'*100)
		    print self.sub
		    print 'Ready - '+str(self.result)+'/'+str(self.num)
		    logger.debug('Tasks - %s' % self.task_queue.size()) 
		    print '***',i+1,'/',dc,'***'
		    print oper
		    print('*'*100)
		    self.result+= 1
		    
		    #if self.result > 10:
			 #self.stop()
		    if str(self.result) == str(self.num):
			 self.stop()		    
	     

     bot = Dmir_Com(thread_number=2, network_try_limit=1000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=50, connect_timeout=100)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(2)
     print('Save it...')    
     command = 'mount -a'
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
	  if oper == u'Продажа':
               i = 0
               l= open('Links/Com_Arenda.txt').read().splitlines()
               dc = len(l)
               page = l[i]
               oper = u'Аренда'
          else:
	       break
	  
	  
	  