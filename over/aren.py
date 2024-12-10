#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import os
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






   
     
class move_Com(Spider):
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'Ocenschiki.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"Фио Эксперта")
	  self.ws.write(0, 1, u"Вкратце о себе")
	  self.ws.write(0, 2, u"Статус специалиста")
	  self.ws.write(0, 3, u"Дополнительная информация о специалисте")
	  self.ws.write(0, 4, u"Место нахождения")
	  self.ws.write(0, 5, u"Контактная информация")
	  self.ws.write(0, 6, u"Членство в СРОО")
	  self.ws.write(0, 7, u"Статус эксперта СРОО")
	  self.ws.write(0, 8, u"Сертификация")
	  self.ws.write(0, 9, u"Основная сфера деятельности")
	  self.ws.write(0, 10, u"О специализации подробней")
	  self.ws.write(0, 11, u"Опыт работы в оценке или экспертизе")
	  self.ws.write(0, 12, u"Дата начала работы")
	  self.ws.write(0, 13, u"Опыт проведения экспертного обследования")
	  self.ws.write(0, 14, u"Ученая степень")
	  self.ws.write(0, 15, u"В поисках постоянной работы")
	  self.ws.write(0, 16, u"Возможность выполнения работ по оценке")
	  self.ws.write(0, 17, u"Выполняю работы по оценке")
	  self.ws.write(0, 18, u"Возможность выполнения работ по судебной экспертизе")
	  self.ws.write(0, 19, u"Возможность удаленной работы")
	  self.ws.write(0, 20, u"Интересующие темы")
	  self.ws.write(0, 21, u"Специализация")
	  self.ws.write(0, 22, u"О специализации подробней")
	  self.ws.write(0, 23, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 24, u"ДАТА_ПАРСИНГА")

	  self.result= 1
	  
	   
	   
	   
	   
     def task_generator(self):
	  for x in range(1,372):#78
               yield Task ('post',url='https://ocenschiki-i-eksperty.ru/knowledge-base/list/profiles/%d'%x,refresh_cache=True,network_try_count=100)
     
   
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//div[@class="info"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)

	       
     def task_item(self, grab, task):
	  try:
	       subb = grab.doc.select(u'//h1').text()
	  except IndexError:
	       subb =''	  
	  try:
	       sub = grab.doc.select(u'//div[contains(@title,"Вкратце о себе")]/following-sibling::div[1]').text()
	  except IndexError:
	       sub =''	  
	  try:
	       mesto = grab.doc.select(u'//div[contains(@title,"Статус специалиста")]/following-sibling::div[1]').text()
	  except IndexError:
	       mesto =''
	       
	  try:
	       punkt = grab.doc.select(u'//div[contains(@title,"Дополнительная информация о специалисте")]/following-sibling::div[1]').text()
	  except IndexError:
	       punkt = ''	       
	   
	  try:
	       ter= grab.doc.select(u'//div[contains(@title,"Место нахождения")]/following-sibling::div[1]').text()
	  except IndexError:
	       ter =''
	  try:
	       uliza= grab.doc.select(u'//div[contains(@title,"Контактная информация")]/following-sibling::div[1]').text() 
	  except IndexError:
	       uliza =''
	  try:
	       dom = grab.doc.select(u'//div[contains(@title,"Членство в СРОО")]/following-sibling::div[1]').text()
	  except IndexError:
	       dom = ''
	    
	  try:
	       tip = grab.doc.select(u'//div[contains(@title,"Статус эксперта СРОО")]/following-sibling::div[1]').text()
	  except IndexError:
	       tip = ''
	  try:
	       naz = grab.doc.select(u'//div[contains(@title,"Сертификация")]/following-sibling::div[1]').text()
	  except IndexError:
	       naz =''
	  try:
	       klass =  grab.doc.select(u'//div[contains(@title,"Основная сфера деятельности")]/following-sibling::div[1]').text()
	  except IndexError:
	       klass = ''
	  try:
	       
	       price = grab.doc.select(u'//div[contains(text(),"О специализации подробней")]/following-sibling::div').text()
	  except IndexError:
	       price =''
	  try: 
	       plosh = grab.doc.select(u'//div[contains(text(),"Опыт работы в оценке или экспертизе")]/following-sibling::div[1]').text()
	  except IndexError:
	       plosh=''
	  try:
	       ohrana = grab.doc.select(u'//div[contains(text(),"Дата начала работы")]/following-sibling::div[1]').text()
	  except IndexError:
	       ohrana =''
	  try:
	       gaz =  grab.doc.select(u'//div[contains(text(),"Опыт проведения экспертного обследования")]/following-sibling::div[1]').text()
	  except IndexError:
	       gaz =''
	  try:
	       voda =  grab.doc.select(u'//div[contains(text(),"Ученая степень")]/following-sibling::div[1]').text().split(' - ')[1]
	  except IndexError:
	       voda =''
	  try:
	       kanal =  grab.doc.select(u'//div[contains(text(),"В поисках постоянной работы")]/following-sibling::div[1]').text()
	  except IndexError:
	       kanal =''
	  try:
	       elek =  grab.doc.select(u'//div[contains(text(),"Возможность выполнения работ по оценке")]/following-sibling::div[1]').text()
	  except IndexError:
	       elek =''
	  try:
	       teplo =  grab.doc.select(u'//div[contains(text(),"Выполняю работы по оценке")]/following-sibling::div[1]/ul').text()
	  except IndexError:
	       teplo =''

	  try:
	       opis = grab.doc.select(u'//div[contains(text(),"Возможность выполнения работ по судебной экспертизе")]/following-sibling::div[1]').text() 
	  except IndexError:
	       opis = ''
	  try:
	       lico =  grab.doc.select(u'//div[contains(text(),"Возможность удаленной работы")]/following-sibling::div[1]').text()
	  except IndexError:
	       lico = ''
	  try:
	       comp = grab.doc.select(u'//div[contains(text(),"Интересующие темы")]/following-sibling::div[1]').text()
	  except IndexError:
	       comp = ''
	  
	  try: 
	       data =  grab.doc.select(u'//div[contains(text(),"Специализация")]/following-sibling::div[1]/ul').text()
	  except IndexError:
	       data=''
	       
	  
	  try:
	       phone =  grab.doc.select(u'//div[contains(text(),"О специализации подробней")]/following-sibling::div[1]').text()
	  except IndexError:
	       phone = ''
	       

	  
	  

   
	  projects = {'sub': sub,
                     'adress': mesto,
	             'fio': subb,
                      'terit':ter, 
                      'punkt':punkt, 
                      'ulica':uliza,
                      'dom':dom,
                      'tip':tip,
                      'naz':naz,
                      'klass': klass,
                      'cena': price,
                      'plosh': plosh,
	              'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal,
                      'electr': elek,
                      'teplo': teplo,
                      'opis': opis,
                      'url': task.url,
                      'phone': phone,
                      'lico':lico,
                      'company': comp,
                      'data':data}
		      
     
     
	  yield Task('write',project=projects,grab=grab)
     
     
     
     def task_write(self,grab,task):
	  #time.sleep(1)
	  print('*'*100)
	  print  task.project['fio']
	  print  task.project['sub']
	  print  task.project['punkt']
	  print  task.project['terit']
	  print  task.project['ulica']
	  print task.project['dom']
	  print  task.project['tip']
	  print  task.project['naz']
	  print  task.project['klass']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['ohrana']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['adress']
	  print  task.project['data']
	 
	 
     
	  
	  
          self.ws.write(self.result, 0, task.project['fio'])
	  self.ws.write(self.result, 1, task.project['sub'])
	  self.ws.write(self.result, 2, task.project['adress'])
	  self.ws.write(self.result, 3, task.project['terit'])
	  self.ws.write(self.result, 4, task.project['punkt'])
	  self.ws.write(self.result, 5, task.project['ulica'])
	  self.ws.write(self.result, 6, task.project['dom'])
	  self.ws.write(self.result, 7, task.project['tip'])
	  self.ws.write(self.result, 8, task.project['naz'])
	  self.ws.write(self.result, 9, task.project['klass'])
	  self.ws.write(self.result, 10, task.project['cena'])
	  self.ws.write(self.result, 11, task.project['plosh'])
	  self.ws.write(self.result, 12, task.project['ohrana'])
	  self.ws.write(self.result, 13, task.project['gaz'])
	  self.ws.write(self.result, 14, task.project['voda'])
	  self.ws.write(self.result, 15, task.project['kanaliz'])
	  self.ws.write(self.result, 16, task.project['electr'])
	  self.ws.write(self.result, 17, task.project['teplo'])
	  self.ws.write(self.result, 18, task.project['opis'])
	  self.ws.write_string(self.result, 23, task.project['url'])
	  self.ws.write(self.result, 19, task.project['lico'])
	  self.ws.write(self.result, 20, task.project['company'])
	  self.ws.write(self.result, 21, task.project['data'])
	  self.ws.write(self.result, 22, task.project['phone'])
	  self.ws.write(self.result, 24, datetime.today().strftime('%d.%m.%Y'))

	  print('*'*10)
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*10)
	  self.result+= 1

bot = move_Com(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
bot.workbook.close()
print('Done...')
    
       
     
     
     