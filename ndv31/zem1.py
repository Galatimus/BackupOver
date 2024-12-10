#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import MySQLdb
import re
#import xlwt
import time
#import xlsxwriter
from datetime import datetime,timedelta

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Brsn_Zem(Spider):
     def prepare(self):
	  self.db = MySQLdb.connect(host='192.168.1.22', user='oleg', passwd='1122', db='Rway',use_unicode=True,charset='utf8')
	  self.cursor = self.db.cursor()
	  #self.cursor.execute('SET NAMES `utf8`')
	  
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(5):
               yield Task ('post',url='http://belgorod.ndv31.ru/sale_earth?s_earth_from=&s_earth_to=&price_from=&price_to=&address=All&page=%d'%x,network_try_count=100)
	  for x1 in range(5):
	       yield Task ('post',url='http://oskol.ndv31.ru/sale_earth?s_earth_from=&s_earth_to=&price_from=&price_to=&address=All&page=%d'%x1,network_try_count=100)	       
                 
     def task_post(self,grab,task):
    
	  for elem in grab.doc.select(u'//h3[@class="field-content"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	  
        
        
     def task_item(self, grab, task):
	  try:
	       sub = u'Белгородская область'#grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p').text().split(', ')[0]
	  except IndexError:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//label[contains(text(),"Район:")]/following-sibling::span').text()
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//h1').text().split('. ')[1].split(', ')[0]
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text().split(', ')[0]
	  except IndexError:
	       ter =''
	       
	  try:
	       
	       uliza = grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text().split(', ')[1]
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	       
          try:
               dom = grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::div').text()
          except DataNotFound:
               dom = ''
	       
	  try:
	       trassa = grab.doc.select(u'//label[contains(text(),"Шоссе:")]/following-sibling::p').text().split(', ')[0]
		#print rayon
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//label[contains(text(),"Растояние до города:")]/following-sibling::span').text()
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//div[@class="object-info--price"]').text()
	  except IndexError:
	       price = ''
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Площадь земли:")]/following-sibling::div').text()
	  except IndexError:
	       plosh = ''
	  try:
	       vid = u'ИЖС'#grab.doc.select(u'//h3').text().split(u', ')[1]
	  except DataNotFound:
	       vid = '' 
	       
	       
	  ohrana =''
	  try:
	       gaz = grab.doc.select(u'//label[contains(text(),"Газ:")]/following-sibling::span').text()
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//label[contains(text(),"Вода:")]/following-sibling::span').text()
	  except DataNotFound:
	       voda =''
	  try:
	       kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	  except DataNotFound:
	       kanal =''
	  try:
	       elek = grab.doc.select(u'//label[contains(text(),"Свет:")]/following-sibling::span').text()
	  except DataNotFound:
	       elek =''
	  try:
	       con = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
	            (u' мая ',u'.05.'),(u' июня ',u'.06.'),
	            (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
	            (u' января ',u'.01.'),(u' декабря ',u'.12.'),
	            (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
	            (u' февраля ',u'.02.'),(u' октября ',u'.10.')]
	       dt1= grab.doc.select(u'//div[@class="advdesc"]').text().split(u' Обновлено: ')[1]
	       teplo = reduce(lambda dt1, r: dt1.replace(r[0], r[1]), con, dt1)[:10]
	  except DataNotFound:
	       teplo =''
	       
	  try:
	       oper = u'Продажа'  
	  except DataNotFound:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="object-info--description"]').text() 
	  except DataNotFound:
	       opis = ''
	       
	  try:
	       #try:
	            #phone = grab.doc.select(u'//b[contains(text(),"Контакт:")]/following-sibling::text()[2]').text().replace(' ','')
	       #except DataNotFound:
	       phone = re.sub('[^\d\+]', u'',grab.doc.select(u'//div[@class="manger-info--phone"]').text())
	       
	  except IndexError:
	       phone = ''
	       
	  try:
	       lico = grab.doc.select(u'//div[@class="manager-info--name"]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = u'ООО Золотая Середина'#grab.doc.select(u'//div[@class="avtor"]/a[contains(@href, "firma")]/h4').text()
	  except IndexError:
	       comp = ''
	       
	  try:
	       data = grab.doc.select(u'//span[contains(text(),"Дата публикации:")]/following-sibling::div').text().replace('-','.')
	  except IndexError:
	       data = ''
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter.replace(uliza,''),
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
                      'vid': vid,
                      'ohrana':sub+', '+ohrana,
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

	  yield Task('write',project=projects,grab=grab)
            
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
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['vid']
	  #print  task.project['ohrana']
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
	  
	  
	  self.cursor.execute("INSERT INTO `Rway`.`Земля` "
	                      "(`СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ`,"
	                      "`МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_РАЙОН`,"
		              "`НАСЕЛЕННЫЙ_ПУНКТ`,"
	                      "`ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ`,"
	                      "`УЛИЦА`,"
	                      "`ДОМ`,"
	                      "`ОРИЕНТИР`,"
	                      "`ТРАССА`,"
	                      "`УДАЛЕННОСТЬ`,"
	                      "`СТОИМОСТЬ`,"
	                      "`ЦЕНА_ЗА_СОТКУ`,"
	                      "`ПЛОЩАДЬ`,"
	                      "`КАТЕГОРИЯ_ЗЕМЛИ`,"
	                      "`ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ`,"
	                      "`ГАЗОСНАБЖЕНИЕ`,"
	                      "`ВОДОСНАБЖЕНИЕ`,"
	                      "`КАНАЛИЗАЦИЯ`,"
	                      "`ЭЛЕКТРОСНАБЖЕНИЕ`,"
	                      "`ТЕПЛОСНАБЖЕНИЕ`,"
	                      "`ОХРАНА`,"
	                      "`ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ`,"
	                      "`ОПИСАНИЕ`,"
	                      "`ИСТОЧНИК_ИНФОРМАЦИИ`,"
	                      "`ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ`,"
	                      "`ТЕЛЕФОН`,"
	                      "`КОНТАКТНОЕ_ЛИЦО`,"
	                      "`КОМПАНИЯ`,"
	                      "`ДАТА_РАЗМЕЩЕНИЯ`,"
	                      "`ДАТА_ОБНОВЛЕНИЯ`,"
	                      "`ДАТА_ПАРСИНГА`,"
	                      "`ОПЕРАЦИЯ`,"
	                      "`МЕСТОПОЛОЖЕНИЕ`)"
	                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
	                      (task.project['sub'],
	                      task.project['rayon'],
	                      task.project['punkt'],
	                      task.project['teritor'],
	                      task.project['ulica'],
	                      '',
	                      '',
	                      '',
	                      '',
	                      task.project['cena'],
	                      '',
	                      task.project['plosh'],
	                      '',
	                      task.project['vid'],
	                      '',
	                      '',
	                      '',
	                      '',
	                      '',
	                      '',
	                      '',
	                      task.project['opis'],
	                      'АН "Золотая Середина"',
	                      task.project['url'],
	                      task.project['phone'],
	                      task.project['lico'],
	                      task.project['company'],
	                      task.project['data'],
	                      '',
	                      datetime.today().strftime('%d.%m.%Y'),
	                      task.project['oper'],
	                      task.project['dom']))
	  
	  
	  self.db.commit()
	
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	       
	       
	  #if self.result > 20:
	       #self.stop()

     
bot = Brsn_Zem(thread_number=2,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
bot.db.close()
print('Done!') 







