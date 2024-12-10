#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from sub import conv
import re
#import xlwt
import time
import xlsxwriter
from datetime import datetime,timedelta

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'0001-0016_00_C_001-0018_ALIANT.xlsx')

    

class Cian_Zem(Spider):
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
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for line in open('aliant.txt').read().splitlines():
               yield Task ('item',url=line.strip(),refresh_cache=True,network_try_count=100)
                
     def task_item(self, grab, task):
	  try:
	       dt = grab.doc.select(u'//div[contains(text(),"Город:")]/span').text()
	       sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	  except DataNotFound:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//em/a[contains(text(),"р-н")]').text()
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       #if  grab.doc.select(u'//em/a[2][contains(text(),"р-н")]').exists()==True:
	       punkt= grab.doc.select(u'//div[contains(text(),"Город:")]/span').text()#.split(', ')[2]
	       
		    
		    
	       #if self.sub == u'Москва':
			 #punkt = u'Москва'
	       #if self.sub == u'Санкт-Петербург':
			 #punkt = u'Санкт-Петербург'
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').exists()==True:
	       ter= grab.doc.select(u'//div[contains(text(),"Район:")]/span').text()#.split(', ')[3].replace(u'улица','')
	       #else:
		    #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//div[contains(text(),"Улица:")]/span').text().split(', ')[0]
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//div[contains(text(),"Номер дома:")]/span').number()
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//td[contains(text(),"Объект:")]/following-sibling::td').text()
		#print rayon
	  except DataNotFound:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//td[contains(text(),"Класс:")]/following-sibling::td').text()
	  except DataNotFound:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//div[contains(text(),"Цена:")]/span').text()
	  except DataNotFound:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//div[contains(text(),"Общая площадь:")]/span').text()
	  except DataNotFound:
	       plosh = ''
	  try:
	       vid = grab.doc.select(u'//td[contains(text(),"Тип:")]/following-sibling::td').text()
	  except DataNotFound:
	       vid = '' 
	  try:
	       et = grab.doc.select(u'//div[contains(text(),"Этаж:")]/span').text()#.split('/')[0]
	  except IndexError:
	       et = ''
	  try:
	       et2 = grab.doc.select(u'//td[contains(text(),"Этаж/этажей:")]/following-sibling::td').text().split('/')[1]
	  except IndexError:
	       et2 = ''
	  
	  try:
	       mat = grab.doc.select(u'//div[contains(text(),"Высота потолков")]/span').text()
	  except IndexError:
	       mat = ''
          try:
               godp = grab.doc.select(u'//div[contains(text(),"Состояние ремонта")]/span').text()
          except IndexError:
               godp = ''	       
	       
	       
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
	  except IndexError:
	       teplo =''
	       
	  try:
	       oper = grab.doc.select(u'//div[contains(text(),"Тип сделки:")]/span').text().replace(u'Сдам',u'Аренда').replace(u'Спрос',u'Аренда').replace(u'Продам',u'Продажа')  
	  except IndexError:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[contains(text(),"Параметры")]/ancestor::div[1]').text().replace(u'Описание','')  
	  except IndexError:
	       opis = ''
	       
	  try:
	       try: 
	            phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//a[@class="desk"]/@href').text())
	       except IndexError:
		    phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//a[@class="mobile"]/@href').text())
	  except IndexError:
	       phone = ''
	       
	  try:
	       try: 
	            lico = grab.doc.select(u'//td[contains(text(),"Продавец:")]/following-sibling::td').text()
	       except IndexError:
		    lico = grab.doc.select(u'//td[contains(text(),"Агент:")]/following-sibling::td').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = u'Элиант недвижимость'#grab.doc.select(u'//td[contains(text(),"Фирма продавец:")]/following-sibling::td').text().split(' :: ')[0]
	  except IndexError:
	       comp = ''
	       
	  try:
	       data= grab.doc.select(u'//td[contains(text(),"Изменено:")]/following-sibling::td').text().split(' ')[0]
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
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
	              'et': et,
	              'ets': et2,
	              'mat': mat,
	              'god':godp,
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
                      'data':data,
                      'oper':oper
                      }
          
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     def task_write(self,grab,task):
	  if task.project['sub']<>'':	       
	       print('*'*50)
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['teritor']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['trassa']
	       print  task.project['udal']
	       print  task.project['cena']
	       print  task.project['plosh']
	       print  task.project['et']
	       print  task.project['ets']
	       print  task.project['mat']
	       print  task.project['god']
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
	       print  task.project['oper']
	       
	       #global result
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 3, task.project['teritor'])
	       self.ws.write(self.result, 4, task.project['ulica'])
	       self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 9, task.project['trassa'])
	       self.ws.write(self.result, 10, task.project['udal'])
	       self.ws.write(self.result, 33, task.project['oper'])
	       self.ws.write(self.result, 11, task.project['cena'])
	       self.ws.write(self.result, 12, task.project['plosh'])
	       self.ws.write(self.result, 13, task.project['et'])
	       self.ws.write(self.result, 14, task.project['ets'])
	       self.ws.write(self.result, 18, task.project['god'])
	       self.ws.write(self.result, 17, task.project['mat'])	  
	       #self.ws.write(self.result, 18, task.project['vid'])
	       self.ws.write(self.result, 20, task.project['gaz'])
	       self.ws.write(self.result, 21, task.project['voda'])
	       self.ws.write(self.result, 22, task.project['kanaliz'])
	       self.ws.write(self.result, 23, task.project['electr'])
	       self.ws.write(self.result, 24, task.project['teplo'])
	       self.ws.write(self.result, 19, task.project['ohrana'])	       
	       self.ws.write(self.result, 25, task.project['opis'])
	       self.ws.write(self.result, 26, u'АН "Элиант Недвижимость"')
	       self.ws.write_string(self.result, 27, task.project['url'])
	       self.ws.write(self.result, 28, task.project['phone'])
	       self.ws.write(self.result, 29, task.project['lico'])
	       self.ws.write(self.result, 30, task.project['company'])
	       self.ws.write(self.result, 31, task.project['data'])
	       self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
	       print('*'*50)
	       #print task.sub
	       
	       print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       #print '*',i+1,'/',dc,'*'
	       #print oper
	       print('*'*50)	       
	       self.result+= 1
		    
	       #if self.result >= 30:
		    #self.stop()	       	       
	 

     
bot = Cian_Zem(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
workbook.close()
print('Done!') 






