#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
from grab import Grab
import logging
import time
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)




class gis(Spider): 
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'Total/2Gis_Москва.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"НАЗВАНИЕ_ОРГАНИЗАЦИИ")
	  self.ws.write(0, 1, u"МЕСТОПОЛОЖЕНИЕ")
	  self.ws.write(0, 2, u"ТЕЛЕФОН")
	  self.ws.write(0, 3, u"ВЕБ_САЙТ_ОРГАНИЗАЦИИ")
	  self.ws.write(0, 4, u"ВИДЫ_УСЛУГ")
	  #self.ws.write(0, 3, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 4, u"ОРИЕНТИР")
	  #self.ws.write(0, 5, u"УДАЛЕННОСТЬ")
	  #self.ws.write(0, 6, u"РАСПОЛОЖЕНИЕ")
	  
	  #self.ws.write(0, 9, u"ОПЕРАЦИЯ")
	  #self.ws.write(0, 10, u"СТОИМОСТЬ")
	  #self.ws.write(0, 11, u"ЦЕНА_ЗА_СОТКУ")
	  #self.ws.write(0, 12, u"ПЛОЩАДЬ")
	  #self.ws.write(0, 13, u"КАТЕГОРИЯ_ЗЕМЛИ")
	  #self.ws.write(0, 14, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	  #self.ws.write(0, 15, u"ГАЗОСНАБЖЕНИЕ")
	  #self.ws.write(0, 16, u"ВОДОСНАБЖЕНИЕ")
	  #self.ws.write(0, 17, u"КАНАЛИЗАЦИЯ")
	  #self.ws.write(0, 18, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  #self.ws.write(0, 19, u"ТЕПЛОСНАБЖЕНИЕ")
	  #self.ws.write(0, 20, u"ОХРАНА")
	  #self.ws.write(0, 21, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  #self.ws.write(0, 22, u"ОПИСАНИЕ")
	  #self.ws.write(0, 23, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 24, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 25, u"ТЕЛЕФОН")
	  #self.ws.write(0, 26, u"КОНТАКТНОЕ_ЛИЦО")
	  #self.ws.write(0, 27, u"КОМПАНИЯ")
	  #self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
	  #self.ws.write(0, 29, u"ДАТА_ПАРСИНГА")
	  
	  self.result= 1
	 
     def task_generator(self):
	  yield Task ('post',url = 'http://2gis.ru/moscow/rubrics/',network_try_count=100)
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//a[@class="link _scheme_none rubricsList__listItemLinkTitle"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('page',url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	       
     def task_page(self, grab, task):
	  for elem1 in grab.doc.select('//a[@class="link _scheme_none rubricsList__listItemLinkTitle"]'):
	       ur1 = grab.make_url_absolute(elem1.attr('href'))
	       #print ur1 
	       yield Task('Org',url=ur1,refresh_cache=True,network_try_count=100)
	  yield Task("pagin", grab=grab,refresh_cache=True,network_try_count=100)
	  
	  
     def task_pagin(self,grab,task):
			
	  try:
	       pg = grab.doc.select(u'//span[@class="pagination__page _current"]/following-sibling::a[1]')
	       u = grab.make_url_absolute(pg.attr('href'))	    
	       yield Task ('page',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*100)
	       print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!','NO PAGE NEXT','!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	       print('*'*100)
	       logger.debug('%s taskq size' % self.task_queue.size())	       
	       
	       
     def task_Org(self, grab, task):
	  for elem2 in grab.doc.select('//a[@class="miniCard__headerTitleLink"]'):
	       ur2 = grab.make_url_absolute(elem2.attr('href'))
	       #print ur2 
	       yield Task('item',url=ur2,refresh_cache=True,network_try_count=100)
	       
     def task_item(self, grab, task):
	  try:
	       lin = []
               for elem in grab.doc.select(u'//a[@class="contact__phonesItemLink"]'):
                    ur = re.sub(u'[^\d\+]','',elem.text())
                    lin.append(ur)
               phone = ', '.join(lin)
	  except DataNotFound:
	       phone = ''
	 
	  try:
	       firm = grab.doc.select(u'//h1').text()
	       
	  except DataNotFound:
	       firm = ''
	       
	  try:
	       adr = grab.doc.select(u'//span[@class="card__addressPart"]/a').text()
	  except DataNotFound:
	       adr = ''
	       
	  #try:
	       #oren = grab.doc.select(u'//span[@class="firmCard__nearStopName"]').text()
	  #except DataNotFound:
	       #oren = ''
	       
	  #try:
	       #udal = grab.doc.select(u'//span[@class="firmCard__nearStopComment"]').text().replace(u'— ','')
	  #except DataNotFound:
	       #udal = ''
	       
	  #try:
	       #mesto = grab.doc.select(u'//p[@class="firmCard__geoCommentItem"]').text()
	  #except DataNotFound:
	       #mesto = ''
	       
	  try:
	       web = grab.doc.select(u'//div[@class="contact__link _type_website"]/a').text()
	  except DataNotFound:
	       web = ''
	       
	  try:
	       opis = grab.doc.select(u'//h1/following-sibling::div').text()
	  except DataNotFound:
	       opis = ''		    
	       
	  
	       
	       
	  projects = {'org':firm,
                      'phone': phone,
                       'adress':adr,
                      'web_url':web,
                      'opisanie':opis
                       #'url': task.url
                      }
	  yield Task('write',project=projects,grab=grab)
	  
     def task_write(self,grab,task):
	  print('*'*50)
	  print  task.project['org']
	  print  task.project['phone']
	  print  task.project['adress']
	  print  task.project['web_url']
	  print  task.project['opisanie']
	  self.ws.write(self.result, 0, task.project['org'])
	  self.ws.write(self.result, 1, task.project['adress'])
	  self.ws.write(self.result, 2, task.project['phone'])
	  self.ws.write_string(self.result, 3, task.project['web_url'])
	  self.ws.write(self.result, 4, task.project['opisanie'])
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	 
	  print('*'*50)
	  self.result+= 1
	  
	  #if self.result > 20:
	       #self.stop()
   

bot = gis(thread_number=5,network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()     
bot.workbook.close()
time.sleep(2)     
print('Done!')