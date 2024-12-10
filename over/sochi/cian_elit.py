#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Cian_Elit_Продажа_от_30млн.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet('Cian_Elit')
	  self.ws.write(0, 0, u"№")
	  self.ws.write(0, 1, u"Район")
	  self.ws.write(0, 2, u"Метро")
	  self.ws.write(0, 3, u"До метро")
	  self.ws.write(0, 4, u"Адрес")
	  self.ws.write(0, 5, u"Название_ЖК")
	  self.ws.write(0, 6, u"Тип дома / Здание")
	  self.ws.write(0, 7, u"Тип сделки")
	  self.ws.write(0, 8, u"Этаж/Этажность")
	  self.ws.write(0, 9, u"Фонд")
	  self.ws.write(0, 10, u"Кол-во комнат")
	  self.ws.write(0, 11, u"Площадь общая")
	  self.ws.write(0, 12, u"Площадь жилая")
	  self.ws.write(0, 13, u"Площадь комнат")
	  self.ws.write(0, 14, u"Площадь кухни")
	  self.ws.write(0, 15, u"Санузлов")
	  self.ws.write(0, 16, u"Санузлы")
	  self.ws.write(0, 17, u"Балкон")
	  self.ws.write(0, 18, u"Ремонт")
	  self.ws.write(0, 19, u"Вид из окон")
	  self.ws.write(0, 20, u"Цена")
	  self.ws.write(0, 21, u"Бюджет")
	  self.ws.write(0, 22, u"Арендная плата")
	  self.ws.write(0, 23, u"Описание")
	  self.ws.write(0, 24, u"Источник")
	  self.ws.write(0, 25, u"Ссылка")
	  self.ws.write(0, 26, u"Дата размещения")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  for x in range(1,60):#230
               yield Task ('post',url='http://spb.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=30000000&offer_type=flat&p=%d'%x+'&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4',refresh_cache=True,network_try_count=100)
          #for x1 in range(1,21):#92
               #yield Task ('post',url='http://spb.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&minprice=100000&offer_type=flat&p=%d'%x1+'&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4',refresh_cache=True,network_try_count=100)
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[contains(text(),"Подробнее")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	  
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               ray = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').text()
          except DataNotFound:
               ray =''
	  
	  try:
	       uliza = grab.doc.select(u'//a[@class="object_item_metro_name"]').text()
	      
	  except DataNotFound:
               uliza = ''
	       
	  try:
	       dom = grab.doc.select(u'//span[@class="object_item_metro_comment"]').text()
	   #print rayon
	  except DataNotFound:
	       dom = ''
	  try:
	       ard = grab.doc.select(u'//h1').text()
	  except DataNotFound:
	       ard = ''
	       
	  try:
	       tip_d = grab.doc.select(u'//th[contains(text(),"Тип дома:")]/following-sibling::td').text()
	  except DataNotFound:
	       tip_d = ''	       
		
	    
	  try:
               tip = grab.doc.select(u'//div[@class="object_descr_title"]/a[contains(text(),"ЖК ")]').text()
          except IndexError:
	       tip = ''
	      
	  try:
	       novo = grab.doc.select(u'//th[contains(text(),"Этаж:")]/following-sibling::td').text().replace(u'(Квартиры на других этажах)','')
	  except IndexError:
	       novo = ''
	  try:
	       f = grab.doc.select(u'//div[@class="object_descr_text"]/text()').text().split(', ')[0]
	       if f.find(u'фонд')>=0:
		    fond = f.split(u' фонд ')[0]
	       else:
		    fond =''
	  except IndexError:
	       fond = ''	       
          try:
               kol_komnat = grab.doc.select(u'//div[@class="object_descr_title"]/text()').number()
          except DataNotFound:
               kol_komnat = ''
          try:
               plosh = grab.doc.select(u'//th[contains(text(),"Общая площадь:")]/following-sibling::td').text().replace(u'–','')
          except DataNotFound:
	       plosh = ''
	  try:
	       oper = grab.doc.select(u'//th[contains(text(),"Жилая площадь:")]/following-sibling::td').text().replace(u'–','') 
	  except DataNotFound:
	       oper = ''	       
          try:
               price = grab.doc.select(u'//div[@class="object_descr_price"]').text()#.replace(u'Цена:','')
          except IndexError:
               price = ''
          try:
               opis = grab.doc.select(u'//div[@class="object_descr_text"]/text()').text() 
          except DataNotFound:
               opis = ''
	       
	  try:
	       remont = grab.doc.select(u'//th[contains(text(),"Площадь комнат:")]/following-sibling::td').text()#.replace(u'тип договора ','') 
	  except IndexError:
	       remont = ''
	  try:
	       sost = grab.doc.select(u'//th[contains(text(),"Площадь кухни:")]/following-sibling::td').text()#.replace(u'тип договора ','') 
	  except IndexError:
	       sost = ''  
	  try:
	       meb = grab.doc.select(u'//th[contains(text()," санузлов:")]/following-sibling::td').number()#.replace(u'тип договора ','') 
	  except IndexError:
	       meb = ''                     
	  try:
	       if 'Совмещенных санузлов:' in grab.doc.select(u'//th[contains(text()," санузлов:")]').text():
		    etag = 'Совмещенный'
	       elif 'Раздельных санузлов:' in grab.doc.select(u'//th[contains(text()," санузлов:")]').text():
		    etag = 'Раздельный' 
	       else:
		    etag =''
	       #etag = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"этаж")]').number()
	  except IndexError:
	       etag = ''
	  try:
	       etagn = grab.doc.select(u'//th[contains(text(),"Балкон:")]/following-sibling::td').text()
	  except IndexError:
	       etagn = ''                     
	  try:
	       opis1 = grab.doc.select(u'//th[contains(text(),"Ремонт:")]/following-sibling::td').text() 
	  except IndexError:
	       opis1 = ''
	  try:
	       vid = grab.doc.select(u'//th[contains(text(),"Вид из окна:")]/following-sibling::td').text()
	  except IndexError:
	       vid = ''
	       
	  try:
	       conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
	                (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
	                (u'Окт', '.10.2016'),(u'окт', '.10.2016'),
	                (u'Сен', '.09.2016'),(u'сен', '.09.2016'),
	                (u'Авг', '.08.2017'),(u'авг', '.08.2017'),
	                (u'Июл', '.07.2017'),(u'июл', '.07.2017'),
	                (u'Июн', '.06.2017'),(u'июн', '.06.2017'),
	                (u'Май', '.05.2017'),(u'май', '.05.2017'),
	                (u'Янв', '.05.2017'),(u'янв', '.05.2017'),
	                (u'Фев', '.05.2017'),(u'фев', '.05.2017'),
	                (u'Мар', '.05.2017'),(u'мар', '.05.2017'),
	                (u'Апр', '.04.2017'),(u'апр', '.04.2017'), 
	                (u'Апр', '.04.2017'),(u'апр', '.04.2017'),
	                (u'Май', '.05.2017'),(u'май', '.05.2017')]
	       dt= grab.doc.select(u'//ul[@class="offerStatuses"]/following-sibling::span[@class="object_descr_dt_added"]').text().split(', ')[0]
	       data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
		    #print data
	  except IndexError:
	       data = ''	       
	      
	       
	  projects = {'rayon': ray,
	              'ulica': uliza,
	              'dom': dom,
	              'adress': ard,
	              'tip': tip,
	              'tip2': tip_d,
	              'novo': novo,
	              'plosh': plosh,
	              'plosh1': remont,
	              'plosh2': sost,
	              'uzli': meb,
	              'uzli2': etag,
	              'oper':oper,
	              'cena': price,
	              'fond': fond,
	              'opis': opis,	              
	              'bal':etagn,
	              'rem': opis1,
	              'vidd': vid,
	              'data': data,	              
	              'col_komnat': kol_komnat}
	
	
	
	  yield Task('write',project=projects,grab=grab)
	
	
	
	
	
	
     def task_write(self,grab,task):
	  
	  print('*'*50)	       
	 
	  print  task.project['rayon']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['adress']
	  print  task.project['tip']
	  print  task.project['novo']
	  print  task.project['plosh']
	  print  task.project['fond']
	  print  task.project['cena']
	  print  task.project['opis']
	  print  task.project['col_komnat']
	  print  task.project['oper']
	  
    
	  self.ws.write(self.result, 1,task.project['rayon'])
	  self.ws.write(self.result, 2,task.project['ulica'])
	  self.ws.write(self.result, 3,task.project['dom'])
	  self.ws.write(self.result, 4,task.project['adress'])
	  self.ws.write(self.result, 5,task.project['tip'])
	  self.ws.write(self.result, 6,task.project['tip2'])
	  self.ws.write(self.result, 8,task.project['novo'])
	  self.ws.write(self.result, 7,u'Продажа')
	  self.ws.write(self.result, 11,task.project['plosh'])
	  self.ws.write(self.result, 20,task.project['cena'])
	  self.ws.write(self.result, 23,task.project['opis'])
	  self.ws.write(self.result, 24, u'CIAN.RU')
	  self.ws.write_string(self.result, 25,task.url)
	  self.ws.write(self.result, 0,self.result)
	  self.ws.write(self.result, 9,task.project['fond'])
	  self.ws.write(self.result, 10,task.project['col_komnat'])
	  self.ws.write(self.result, 12,task.project['oper'])
	  self.ws.write(self.result, 13,task.project['plosh1'])
	  self.ws.write(self.result, 14,task.project['plosh2'])
	  self.ws.write(self.result, 15,task.project['uzli'])
	  self.ws.write(self.result, 16,task.project['uzli2'])	  
	  self.ws.write(self.result, 17,task.project['bal'])
	  self.ws.write(self.result, 18,task.project['rem'])
	  self.ws.write(self.result, 19,task.project['vidd'])
	  self.ws.write(self.result, 26,task.project['data'])	  
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result >= 50:
	       #self.stop()

     
bot = Cian_Kv(thread_number=1,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!')

     
     