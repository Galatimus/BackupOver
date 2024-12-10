#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
#from grab import Grab
import re
from sub import conv
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



workbook = xlsxwriter.Workbook(u'zag/Farpost_Загород.xlsx')


class Farpost_Zag(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet(u'Farpost_Загород')
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
	  self.ws.write(0, 37, u"ВИД_ПРАВА")
	  #self.r = conv     
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  yield Task ('post1',url='http://www.farpost.ru/realty/sell_houses/',refresh_cache=True,network_try_count=100)
	  #yield Task ('post1',url='http://www.farpost.ru/realty/rent_business_realty/',refresh_cache=True,network_try_count=100)
	  #yield Task ('post1',url='http://www.farpost.ru/rest/hotels/',refresh_cache=True,network_try_count=100)
	  
	  for x in range(1,86):#78
	       yield Task ('post',url='http://www.farpost.ru/realty/sell_houses/?page=%d'%x,refresh_cache=True,network_try_count=100)
	  for x1 in range(1,8):#4
	       yield Task ('post',url='http://www.farpost.ru/realty/rent_houses/?page=%d'%x1,refresh_cache=True,network_try_count=100)
	  for x2 in range(1,22):#4
	       yield Task ('post',url='http://www.farpost.ru/realty/dacha/?page=%d'%x2,refresh_cache=True,network_try_count=100)	       
	       
     def task_post(self,grab,task):
    
	  for elem in grab.doc.select(u'//a[@class="bulletinLink"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  
	  
     def task_post1(self,grab,task):
	  for el in grab.doc.select(u'//div[@class="image"]/a[contains(@href,"html")]'):
	       ur1 = grab.make_url_absolute(el.attr('href'))  
	       print ur1
	       yield Task('item', url=ur1,refresh_cache=True,network_try_count=100)        
        
     def task_item(self, grab, task):
	  try:
	       dt = grab.doc.select(u'//td[@class="col_city"]/a').text()
	       if dt.find(u'район')<=0:
                    sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	       else:
		    sub ='Приморский край'
	  except IndexError:
	       sub = ''
	  try:
	       r = grab.doc.select(u'//td[@class="col_city"]/a').text()
	       if r.find(u'район')>=0:
		    ray = r
	       else:
		    ray=''
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       p= grab.doc.select(u'//td[@class="col_city"]/a').text()
	       if p.find(u'район')<=0:
		    punkt = p
	       else:
		    punkt=''
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"district-street")]').text()
	  except IndexError:
	       ter =''
	       
	  try:
               ul = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"street-district")]/text()').text()
               if re.sub('[^\d]','',ul.split(' ')[0]).isdigit()==True:
	            uliza = ul.split(' ')[0]+' '+ul.split(' ')[1]
               else:
	            uliza= ul.split(' ')[0]
          except IndexError:
	       uliza = ''
	       
          try:
	       d = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"street-district")]/text()').text()
	       if re.sub('[^\d]','',d.split(' ')[0]).isdigit()==True:
	            dom = re.sub('[^\d\/\а\б]','',d.split(' ')[2])#+' '+page.split(' ')[1]
	       else:
	            dom = re.sub('[^\d\/\а\б]','',d.split(' ')[1])
	  except IndexError:
	       dom = ''
	  try:
	       tip = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a').text().replace(u'Продажа ','').replace(u'Аренда ','').replace(u'домов и коттеджей',u'Дома и Коттеджи').replace(u'дач',u'Дача')#.split(', ')[0]
          except IndexError:
               tip = ''	       
	       
	  try:
	       trassa = grab.doc.select(u'//label[contains(text(),"Шоссе:")]/following-sibling::p').text().split(', ')[0]
		#print rayon
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//label[contains(text(),"Шоссе:")]/following-sibling::p').text().split(', ')[1]
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"price")]').text()#.replace(u'a',u'р.')
	  except IndexError:
	       price = ''
	       
	  try:
               try:
	            oper = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a[contains(@href,"houses")]').text().split(' ')[0]
               except IndexError:
	            oper = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a[contains(@href,"dacha")]').text().split(' ')[0]
          except IndexError:
	       oper = ''
	       
	  try:
	       plosh = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"areaTotal")]').text()
	  except IndexError:
	       plosh = ''
	       
	  
	  
	  
	       
	  try:
	       vid = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"areaLiving")]').text()
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
	       opis = grab.doc.select(u'//div[@class="bulletinText viewbull-field__container"]/p').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       ob = re.sub('[^\d]','',grab.doc.rex_text(u'>№(.+?)</b>'))
	       url_ph='http://www.farpost.ru/bulletin/'+ob+'/ajax_contacts?ajax=1'
	       g2 = grab.clone(timeout=500, connect_timeout=500,proxy_auto_change=True)
	       g2.go(url_ph)
	       phone =re.sub('[^\d]','',g2.doc.select(u'//span[@class="phone"]').text())
	       #phone = grab.doc.rex_text(u'href="tel:(.*?)">')
	  except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
	       phone = ''
	       
	  try:
	       lico = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"cadastreNumber")]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"realtyStatus")]').text()
	  except IndexError:
	       comp = ''
	       
	  try:
	       
	       con = [ ('сегодня', (datetime.today().strftime('%d.%m.%Y'))),
	            ('вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
	            (' июля', '.07.2016'),(' июня', '.06.2016'),(' августа', '.08.2016')] 
	       dt1= grab.doc.select(u'//div[@class="label"][contains(text(),"Актуально")]/following-sibling::div/div').text().split(u' ещё ')[0].split(', ')[1]
	       data = reduce(lambda dt1, r1: dt1.replace(r1[0], r1[1]), con, dt1)#.replace(' ','')#.replace(u'более3-хмесяце', u'07.2015')
	    #print data
	  except IndexError:
	       data = ''
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
	              'tip':tip,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
                      'vid': vid,
                      'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal,
                      'electr': elek,
                      'teplo': teplo,
                      'opis':opis,
                      'phone':phone,
                      'lico':lico,
                      'company':comp,
	              'operazia':oper,
                      'data':data }
          
	  yield Task('write',project=projects,grab=grab)
            
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['tip']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['vid']
	  print  task.project['ohrana']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['opis']
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['data']

	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 9, task.project['dom'])
	  self.ws.write(self.result, 7, task.project['trassa'])
	  self.ws.write(self.result, 8, task.project['udal'])
	  #self.ws.write(self.result, 9, task.project['oper'])
	  self.ws.write(self.result, 10, task.project['tip'])
	  self.ws.write(self.result, 11, task.project['operazia'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['vid'])
	  self.ws.write(self.result, 21, task.project['gaz'])
	  self.ws.write(self.result, 22, task.project['voda'])
	  self.ws.write(self.result, 23, task.project['kanaliz'])
	  self.ws.write(self.result, 24, task.project['electr'])
	  self.ws.write(self.result, 19, task.project['plosh'])
	  self.ws.write(self.result, 28, task.project['ohrana'])
	  self.ws.write(self.result, 29, task.project['opis'])
	  self.ws.write(self.result, 30, u'FARPOST.RU')
	  self.ws.write_string(self.result, 31, task.project['url'])
	  self.ws.write(self.result, 32, task.project['phone'])
	  self.ws.write(self.result, 9, task.project['lico'])
	  self.ws.write(self.result, 37, task.project['company'])
	  self.ws.write(self.result, 35, task.project['data'])
	  self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  print  task.project['operazia']
	  print('*'*50)	       
	  self.result+= 1
	       
	       
	       
	  #if self.result > 10:
	       #self.stop()

     
bot = Farpost_Zag(thread_number=5,network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







