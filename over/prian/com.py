#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
import logging
from datetime import datetime,timedelta
from grab.error import DataNotFound 
import time
import re
import xlsxwriter

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Prian_Коммерческая.xlsx')


     

class Rosreal_Com(Spider):
     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СТРАНА")
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
	  self.ws.write(0, 31, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 32, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 33, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 34, u"ЦЕНА_ЗА_М2")
	  self.ws.write(0, 35, u"МЕСТОПОЛОЖЕНИЕ")
	  self.result= 1

     def task_generator(self):
          for x in range(239):#1463
	       yield Task ('post',url= 'https://prian.ru/commercial_property/?next='+str(x*18),network_try_count=100)


     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//dl/dt/a[@class="cat_detail_item "]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
   
   
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//td[contains(text(),"Адрес")]/following-sibling::td').text().split(', ')[0]
	  except IndexError:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//td[contains(text(),"Расположение")]/following-sibling::td').text()
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//td[contains(text(),"Адрес")]/following-sibling::td').text().split(', ')[1]
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter = grab.doc.select(u'//td[contains(text(),"Адрес")]/following-sibling::td').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       if grab.doc.select(u'//p[@class="pbig"]/a[contains(@title,"Недвижимость в")][contains(text(),"район")]').exists()==False:
		    uliza = grab.doc.select(u'//p[@class="pbig"]').text().split(', ')[2]
	       else:
		    uliza = ''
	  except IndexError:
	       uliza = ''

	  try:
	       naz = grab.doc.select(u'//meta[@name="description"]').attr('content').split(u' в ')[0][:26]
	  except IndexError:
	       naz = ''
	       
	  try:
	       price = grab.doc.select(u'//meta[@name="description"]').attr('content').split(u' за ')[1].split(' (')[0]
	  except IndexError:
	       price = ''

	  try:
	       plosh = grab.doc.select(u'//td[contains(text(),"Площадь")]/following-sibling::td/b').text()
	  except DataNotFound:
	       plosh = ''
	       
	  
	  try: 
	       klass = grab.doc.select(u'//td[contains(text(),"Этаж")]/following-sibling::td/b').text()
	  except DataNotFound:
	       klass =''

	  try:
	       ohrana = grab.doc.select(u'//td[contains(text(),"Этажность")]/following-sibling::td/b').text()
	  except DataNotFound:
	       ohrana =''
	  try:
	       gaz = re.sub(u'[^\d]','', grab.doc.select(u'//i[contains(text(),"Год постройки:")]').text())
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//td[contains(text(),"Цена за кв.м.")]/following-sibling::td/b').text()
	  except DataNotFound:
	       voda =''
	  try:
	       kanal = grab.doc.select(u'//td[contains(text(),"Адрес")]/following-sibling::td').text()
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
	       opis = grab.doc.select(u'//div[@class="pr-b-object-description pr-b-object-description_three"]').text()  
	  except DataNotFound:
	       opis = ''
	       
	  try:
	       try:
	            phone = re.sub('[^\d\+\,]', u'',grab.doc.select(u'//a[@class="phone"]').text())
	       except IndexError:
		    phone = re.sub('[^\d]\+\,', u'',grab.doc.select(u'//div[contains(text(),"Телефон компании:")]/following-sibling::p/a').text())
	  except IndexError:
	       phone = ''
	       
	  try:
	       lico = grab.doc.select(u'//span[@class="name"]').text()#.split(', ')[1]
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//a[@class="companyinfo"]').text()
	  except IndexError:
	       comp = ''
	       
	  try:
	       data = grab.doc.rex_text(u'обновления: (.*?)<br>')
	  except IndexError:
	       data = '' 
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
                      'naz': naz,
                      'cena': price,
                      'plosh':plosh,
                      'klass': klass.replace(ohrana,''),
                      'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal+' '+ray,
                      'electr': elek,
                      'teplo': teplo,
                      'opis':opis,
                      'phone':phone,
                      'lico':lico,
                      'company':comp,
                      'data':data
                      }
     
	  yield Task('write',project=projects,grab=grab)
       
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['naz']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['klass']
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
	  
	  
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 6, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 9, task.project['naz'])
	  self.ws.write(self.result, 33, u'Продажа')
	  self.ws.write(self.result, 11, task.project['cena'])
	  self.ws.write(self.result, 12, task.project['plosh'])
	  self.ws.write(self.result, 13, task.project['klass'])
	  self.ws.write(self.result, 15, task.project['gaz'])
	  self.ws.write(self.result, 34, task.project['voda'])
	  self.ws.write(self.result, 35, task.project['kanaliz'])
	  self.ws.write(self.result, 23, task.project['electr'])
	  self.ws.write(self.result, 24, task.project['teplo'])
	  self.ws.write(self.result, 14, task.project['ohrana'])	       
	  self.ws.write(self.result, 25, task.project['opis'])
	  self.ws.write(self.result, 26, u'prian.ru')
	  self.ws.write_string(self.result, 27, task.project['url'])
	  self.ws.write(self.result, 28, task.project['phone'])
	  self.ws.write(self.result, 29, task.project['lico'])
	  self.ws.write(self.result, 30, task.project['company'])
	  self.ws.write(self.result, 31, task.project['data'])
	  self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	  
	  #if self.result > 20:
	       #self.stop()	 	  
	  
	     


bot = Rosreal_Com(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')







