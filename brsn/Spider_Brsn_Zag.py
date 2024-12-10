#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
#from grab import Grab
import re
#import xlwt
import time
import xlsxwriter
from datetime import datetime,timedelta

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#i = 0
#l= open('/home/oleg/CIAN/Links/Zem_Prod.txt').read().splitlines()
#dc = len(l)
#page = l[i] 
#oper = u'Продажа'
     
#g = Grab(timeout=100, connect_timeout=100)

workbook = xlsxwriter.Workbook(u'Brsn_Загород.xlsx')

#result = 1
#print r

#while True:
     #print '********************************************',i+1,'/',dc,'*******************************************'
     #wb = xlwt.Workbook(encoding=('utf -8')) 
    

class Cian_Zag(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"ТРАССА")
	  self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	  self.ws.write(0, 9, u"КАДАСТРОВЫЙ_НОМЕР_ЗЕМЕЛЬНОГО_УЧАСТКА")
	  self.ws.write(0, 10, u"ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 12, u"СТОИМОСТЬ")
	  self.ws.write(0, 13, u"ЦЕНА_М2")
	  self.ws.write(0, 14, u"ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 15, u"КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 17, u"МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 18, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 19, u"ПЛОЩАДЬ_УЧАСТКА")
	  self.ws.write(0, 20, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  self.ws.write(0, 21, u"ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 22, u"ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 23, u"КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 24, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 25, u"ТЕПЛОСНАБЖЕНИЕ")
	  self.ws.write(0, 26, u"ЛЕС")
	  self.ws.write(0, 27, u"ВОДОЕМ")
	  self.ws.write(0, 28, u"БЕЗОПАСНОСТЬ")
	  self.ws.write(0, 29, u"ОПИСАНИЕ")
	  self.ws.write(0, 30, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 31, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 32, u"ТЕЛЕФОН")
	  self.ws.write(0, 33, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 34, u"КОМПАНИЯ")
	  self.ws.write(0, 35, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 36, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 37, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(0,14):
	       yield Task ('post',url='http://www.brsn.ru/doma-i-dachi/doma.html?start='+str(x*20),network_try_count=100)
            
            
     def task_page(self,grab,task):
	  try:         
	       pg = grab.doc.select(u'//li[@class="pagination-next"]/a')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*50)
	       print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!','NO PAGE NEXT','!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	       print('*'*50)
	       logger.debug('%s taskq size' % self.task_queue.size())             
        
        
            
            
     def task_post(self,grab,task):
	          
	  for elem in grab.doc.select(u'//div[@class="photo-container"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
        
        
     def task_item(self, grab, task):
	  try:
	       sub = u'Брянская область'#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[0]
	  except DataNotFound:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"raion")]').text().replace(u'р-н ','')
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').exists()==True:
		    #punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	       #else:
	       punkt= grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"city")]').text()
		    
		    
	       #if self.sub == u'Москва':
			 #punkt = u'Москва'
	       #if self.sub == u'Санкт-Петербург':
			 #punkt = u'Санкт-Петербург'
	  except IndexError:
	       punkt = ''
	       
	  try:
	       if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').exists()==True:
		    ter= grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[3].replace(u'улица','')
	       else:
		    ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"street")]').text()
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//h1[@class="offer-title"]').number()
		      #if re.sub(u'[^\d]','',d).isdigit()==True:
			  #dom = d.split(', ')[0]
		      #else:
			  #dom = ''
          except DataNotFound:
	       dom = ''	       
	       
	  try:
	       trassa = grab.doc.select(u'//div[@class="object_descr_metro"]/a[contains(text(),"шоссе")]').text()
		#print rayon
	  except DataNotFound:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//span[@class="objects_item_metro_comment"]/span[contains(text(),"км.")]').text()
	  except DataNotFound:
	       udal = ''
          try:
	       #if grab.doc.select(u'//div[@class="object_descr_title"]').text().find(u'дом') <> -1:
                    #tip_ob = u'Дом'
               #else:
		    #tip_ob = u'Таунхаус '
	       tip_ob = grab.doc.select(u'//h1').text().split(' ')[1].replace(',','').replace(u'Часть',u'Часть дома')
          except IndexError:
               tip_ob = ''	       
	       
	  try:
	       price = grab.doc.select(u'//div[@class="pricecard"]').text().replace(' ','').replace(u'a',u' р.')
	  except DataNotFound:
	       price = ''
	       
	  
	       
	  try:
	       plosh = grab.doc.select(u'//p[@class="text-justify"][contains(text(),"площадь:")]/b[1]').text()+u' м2'
	  except IndexError:
	       plosh = ''
	       
          try:
               etash = grab.doc.rex_text(u', <b>(.*?)</b> этаж')
          except IndexError:
               etash = ''
	       
          try:
               plosh_uch =  grab.doc.rex_text(u'<b>Участок:</b> (.*?)<br />')
          except DataNotFound:
               plosh_uch = ''
	  
	  try:
               mat = grab.doc.rex_text(u', (.*?), площадь:')
          except DataNotFound:
               mat = ''	  
	       
	  try:
	       vid = grab.doc.select(u'//th[contains(text(),"Тип земли:")]/following-sibling::td').text()
	  except DataNotFound:
	       vid = '' 
	       
	       
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
	       teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	  except DataNotFound:
	       teplo =''
	  try:
	       les = re.sub(u'^.*(?=лес)','', grab.doc.select(u'//*[contains(text(), "лес")]').text())[:3].replace(u'лес',u'есть')
	  #gazz = gaz.replace('True',u'есть')
	  except DataNotFound:
	       les =''
	    
	  try:
	       vodoem = re.sub(u'^.*(?=озер)','', grab.doc.select(u'//*[contains(text(), "озер")]').text())[:4].replace(u'озер',u'есть')
	  #gazz = gaz.replace('True',u'есть')
	  except DataNotFound:
	       vodoem =''	  
	       
	  try:
	       oper = u'Продажа'#grab.doc.select(u'//li[@class="c-header__menu__item  c-header__menu__item_active"]').text() 
	  except DataNotFound:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[@id="dopinfo"]/p').text() 
	  except DataNotFound:
	       opis = ''
	       
	  try:
	       phone = grab.doc.rex_text(u'href="tel:(.*?)">') 
	  except DataNotFound:
	       phone = ''
	       
	  try:
	       lico = grab.doc.select(u'//img[@class="thumbnail"][contains(@src,"components")]/following::b[1]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//img[@class="thumbnail"][contains(@src,"agency")]/following::b[1]').text()
	  except DataNotFound:
	       comp = ''
	       
	  try:
               conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
	            (u' мая ',u'.05.'),(u' июня ',u'.06.'),
	            (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
	            (u' января ',u'.01.'),(u' декабря ',u'.12.'),
	            (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
	            (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
	       dt= grab.doc.select(u'//b[contains(text(),"Обновлено:")]/following-sibling::span').text()#.split(', ')[0]
	       data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
		   #print data
          except DataNotFound:
               data = ''
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	               'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
	              'object': tip_ob,
                      'cena': price,
                      'plosh':plosh,
	              'etach': etash,
	              'plouh': plosh_uch,
	              'mat': mat,
                      'vid': vid,
                      'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal,
                      'electr': elek,
                      'teplo': teplo,
	              'les': les,
                      'vodoem':vodoem,	              
                      'opis':opis,
                      'phone':phone,
                      'lico':lico,
                      'company':comp,
                      'data':data,
                      'oper':oper
                      }
          
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['object']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['etach']
	  print  task.project['plouh']
	  print  task.project['mat']
	  print  task.project['vid']
	  print  task.project['ohrana']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['les']
	  print  task.project['vodoem']	  
	  print  task.project['opis']
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['data']
	  print  task.project['oper']
	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 7, task.project['trassa'])
	  self.ws.write(self.result, 8, task.project['udal'])
	  self.ws.write(self.result, 11, task.project['oper'])
	  self.ws.write(self.result, 10, task.project['object'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  self.ws.write(self.result, 21, task.project['gaz'])
	  self.ws.write(self.result, 16, task.project['etach'])
	  self.ws.write(self.result, 17, task.project['mat'])
	  self.ws.write(self.result, 23, task.project['kanaliz'])
	  self.ws.write(self.result, 24, task.project['electr'])
	  self.ws.write(self.result, 19, task.project['plouh'])
	  self.ws.write(self.result, 28, task.project['ohrana'])
	  self.ws.write(self.result, 22, task.project['voda'])	  
	  self.ws.write(self.result, 25, task.project['teplo'])
          self.ws.write(self.result, 26, task.project['les'])
          self.ws.write(self.result, 27, task.project['vodoem'])
	  self.ws.write(self.result, 29, task.project['opis'])
          self.ws.write(self.result, 37, task.project['vid'])
	  self.ws.write(self.result, 30, u'Брянский сервер недвижимости')
	  self.ws.write_string(self.result, 31, task.project['url'])
	  self.ws.write(self.result, 32, task.project['phone'])
	  self.ws.write(self.result, 33, task.project['lico'])
	  self.ws.write(self.result, 34, task.project['company'])
	  self.ws.write(self.result, 35, task.project['data'])
	  self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	       
	       
	  #if self.result > 50:
	       #self.stop()

     
bot = Cian_Zag(thread_number=5,network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.run()
workbook.close()
print('Done!') 







