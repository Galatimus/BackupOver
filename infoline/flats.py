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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Infoline_Жилье.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, "СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, "МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, "НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, "ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, "УЛИЦА")
	  self.ws.write(0, 5, "ДОМ")
	  self.ws.write(0, 6, "ОРИЕНТИР")
	  self.ws.write(0, 7, "СТАНЦИЯ_МЕТРО")
	  self.ws.write(0, 8, "ДО_МЕТРО_МИНУТ")
	  self.ws.write(0, 9, "ПЕШКОМ_ТРАНСПОРТОМ")
	  self.ws.write(0, 10, "ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, "ОПЕРАЦИЯ")
	  self.ws.write(0, 12, "СТОИМОСТЬ")
	  self.ws.write(0, 13, "ЦЕНА_М2")
	  self.ws.write(0, 14, "КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 15, "ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 16, "ПЛОЩАДЬ_ЖИЛАЯ")
	  self.ws.write(0, 17, "ПЛОЩАДЬ_КУХНИ")
	  self.ws.write(0, 18, "ПЛОЩАДЬ_КОМНАТ")
	  self.ws.write(0, 19, "ЭТАЖ")
	  self.ws.write(0, 20, "ЭТАЖНОСТЬ")
	  self.ws.write(0, 21, "МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 22, "ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 23, "РАСПОЛОЖЕНИЕ_КОМНАТ")
	  self.ws.write(0, 24, "БАЛКОН")
	  self.ws.write(0, 25, "ЛОДЖИЯ")
	  self.ws.write(0, 26, "САНУЗЕЛ")
	  self.ws.write(0, 27, "ОКНА")
	  self.ws.write(0, 28, "СОСТОЯНИЕ")
	  self.ws.write(0, 29, "ВЫСОТА_ПОТОЛКОВ")
	  self.ws.write(0, 30, "ЛИФТ")
	  self.ws.write(0, 31, "РЫНОК")
	  self.ws.write(0, 32, "КОНСЬЕРЖ")
	  self.ws.write(0, 33, "ОПИСАНИЕ")
	  self.ws.write(0, 34, "ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 35, "ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 36, "ТЕЛЕФОН")
	  self.ws.write(0, 37, "КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 38, "КОМПАНИЯ")
	  self.ws.write(0, 39, "ДАТА_РАЗМЕЩЕНИЯ_ОБЪЯВЛЕНИЯ")
	  self.ws.write(0, 40, "ДАТА_ПАРСИНГА")
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(1,265):#270
               yield Task ('post',url='http://www.vrx.ru/data/prodazha/kvartiry.html?page=%d'%x,network_try_count=100)
	  for x in range(1,150):#182
               yield Task ('post',url='http://www.vrx.ru/data/prodazha/novostroyki.html?page=%d'%x,network_try_count=100)
	  for x in range(1,34):#43
	       yield Task ('post',url='http://www.vrx.ru/data/arenda/kvartiry.html?page=%d'%x,network_try_count=100)
          for x in range(1,8):#8
               yield Task ('post',url='http://www.vrx.ru/data/arenda/novye_kvartiry.html?page=%d'%x,network_try_count=100)
	  for x in range(1,21):#21
	       yield Task ('post',url='http://www.vrx.ru/data/prodazha/komnaty.html?page=%d'%x,network_try_count=100)
	  #for x in range(1,5):#5
	  yield Task ('post',url='http://www.vrx.ru/data/base.php?apptype=1&city=48&folds=1&page=1',network_try_count=100)
          #yield Task ('post',url='http://www.vrx.ru/data/base.php?apptype=1&city=48&folds=3',network_try_count=500)
	  #yield Task ('post',url='http://www.vrx.ru/data/base.php?apptype=3&city=48&folds=3',network_try_count=500)
                 
        
        
            
            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//img[@title="Подробнее"]/ancestor::a'):
	       ur = grab.make_url_absolute(elem.attr('href')).replace(u'prodazha/','').replace(u'arenda/','')  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	 
        
        
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//em/a[1]').text()
	  except DataNotFound:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//em/a[contains(text(),"р-н")]').text()
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       if  grab.doc.select(u'//em/a[2][contains(text(),"р-н")]').exists()==True:
		    punkt= grab.doc.select(u'//em/a[3]').text()#.split(', ')[2]
	       else:
		    punkt= grab.doc.select(u'//em/a[2]').text()#.split(', ')[1]
		    
		    
	       #if self.sub == u'Москва':
			 #punkt = u'Москва'
	       #if self.sub == u'Санкт-Петербург':
			 #punkt = u'Санкт-Петербург'
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').exists()==True:
	       ter= grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район ")]').text()#.split(', ')[3].replace(u'улица','')
	       #else:
		    #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//td[contains(text(),"Адрес:")]/following-sibling::td').text().split(', ')[0]
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//td[contains(text(),"Адрес:")]/following-sibling::td').number()
	  except IndexError:
	       dom = ''       
	  try:
               if grab.doc.select(u'//td[contains(text(),"Объект:")]/following-sibling::td').text().find(u'квартира') > 0:
	            tip_ob = u'Квартира'
               else:
	            tip_ob = u'Комната' 
          except IndexError:
	       tip_ob = ''       
	  try:
	       udal = grab.doc.select(u'//td[contains(text(),"Комнат:")]/following-sibling::td').number()
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//td[contains(text(),"Стоимость:")]/following-sibling::td').text()
	  except IndexError:
	       price = ''   
	  try:
	       plosh_ob = grab.doc.select(u'//td[contains(text(),"Площадь:")]/following-sibling::td').text().split(u'/')[0]+u' кв.м'
	  except IndexError:
	       plosh_ob = ''
	  try:
	       plosh_gil = grab.doc.select(u'//td[contains(text(),"Площадь:")]/following-sibling::td').text().split(u'/')[1]+u' кв.м'
	  except IndexError:
	       plosh_gil = ''
	  try:
	       plosh_kuh = grab.doc.select(u'//td[contains(text(),"Площадь:")]/following-sibling::td').text().split(u'/')[2]
	  except IndexError:
	       plosh_kuh = ''
	  try:
	       vid = grab.doc.select(u'//td[contains(text(),"Тип:")]/following-sibling::td').text()
	  except IndexError:
	       vid = '' 
	  try:
	       et = grab.doc.select(u'//td[contains(text(),"Этаж/этажей:")]/following-sibling::td').text().split('/')[0]
	  except IndexError:
	       et = ''
	  try:
	       et2 = grab.doc.select(u'//td[contains(text(),"Этаж/этажей:")]/following-sibling::td').text().split('/')[1]
	  except IndexError:
	       et2 = ''
	  
	  try:
	       mat = grab.doc.select(u'//td[contains(text(),"Материал:")]/following-sibling::td').text()
	  except IndexError:
	       mat = ''
          try:
               godp = grab.doc.select(u'//td[contains(text(),"Год постр./сдача:")]/following-sibling::td').text()
          except IndexError:
               godp = ''	       
	       
	       
	  try:
	       bal = grab.doc.select(u'//td[contains(text(),"Балкон:")]/following-sibling::td').text()
	  except IndexError:
	       bal =''
	  try:
	       sanuz = grab.doc.select(u'//td[contains(text(),"Санузел:")]/following-sibling::td').text()
	  except IndexError:
	       sanuz =''
	  try:
	       rinok = grab.doc.select(u'//td[contains(text(),"Раздел:")]/following-sibling::td').text().split(u' :: ')[0]
	  except IndexError:
	       rinok =''
	  
	       
	  try:
	       oper = grab.doc.select(u'//td[contains(text(),"Операция:")]/following-sibling::td').text() 
	  except IndexError:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//td[contains(text(),"Комментарий к заявке:")]/following::tr[1]').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       try: 
	            phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//td[contains(text(),"Телефон агента:")]/following-sibling::td').text())
	       except IndexError:
		    phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//td[contains(text(),"Конт. тел.:")]/following-sibling::td').text())
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
	       comp = grab.doc.select(u'//td[contains(text(),"Фирма продавец:")]/following-sibling::td').text().split(' :: ')[0]
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
                      'tip_ob': tip_ob,
                      'udal': udal,
                      'cena': price,
                      'plosh_ob':plosh_ob,
	              'plosh_gil':plosh_gil,
	              'plosh_kuh':plosh_kuh,
	              'et': et,
	              'ets': et2,
	              'mat': mat,
	              'god':godp,
                      'vid': vid,
                      'balkon':bal,
                      'sanuz': sanuz,
                      'rinok': rinok,
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
	  print  task.project['tip_ob']
	  print  task.project['udal']
	  print  task.project['cena']
	  print  task.project['plosh_ob']
	  print  task.project['plosh_gil']
	  print  task.project['plosh_kuh']
	  print  task.project['et']
	  print  task.project['ets']
	  print  task.project['mat']
	  print  task.project['god']
	  print  task.project['vid']
	  print  task.project['balkon']
	  print  task.project['sanuz']
	  print  task.project['rinok']
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
	  self.ws.write(self.result, 10, task.project['tip_ob'])
	  self.ws.write(self.result, 11, task.project['oper'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['udal'])
	  self.ws.write(self.result, 15, task.project['plosh_ob'])
	  self.ws.write(self.result, 16, task.project['plosh_gil'])
	  self.ws.write(self.result, 17, task.project['plosh_kuh'])
	  self.ws.write(self.result, 19, task.project['et'])
	  self.ws.write(self.result, 20, task.project['ets'])	  
	  self.ws.write(self.result, 21, task.project['mat'])
	  self.ws.write(self.result, 22, task.project['god'])
	  self.ws.write(self.result, 24, task.project['balkon'])
	  self.ws.write(self.result, 26, task.project['sanuz'])
	  self.ws.write(self.result, 28, task.project['vid'])
	  self.ws.write(self.result, 31, task.project['rinok'])
	  self.ws.write(self.result, 33, task.project['opis'])	       
	  self.ws.write(self.result, 34, u'INFOLINE')
	  self.ws.write_string(self.result, 35, task.project['url'])
	  self.ws.write(self.result, 36, task.project['phone'])
	  self.ws.write(self.result, 37, task.project['lico'])
	  self.ws.write(self.result, 38, task.project['company'])
	  self.ws.write(self.result, 39, task.project['data'])
	  self.ws.write(self.result, 40, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)	       
	  self.result+= 1
	  
	  #if self.result > 50:
	       #self.stop()
	       
	 

     
bot = Cian_Zem(thread_number=5,network_try_limit=2000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







