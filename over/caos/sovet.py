#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
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


workbook = xlsxwriter.Workbook(u'Srosovet.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"ФИО")
	  self.ws.write(0, 1, u"Должность")
	  self.ws.write(0, 2, u"Место работы")
	  self.ws.write(0, 3, u"Направление")
	  self.ws.write(0, 4, u"Сайт компании")
	  self.ws.write(0, 5, u"Номер телефона")
	  self.ws.write(0, 6, u"E-mail")
	  self.ws.write(0, 7, u"E-mail (личный)")
	  self.ws.write(0, 8, u"Субъект РФ")
	  self.ws.write(0, 9, u"Название СРО")
	  self.ws.write(0, 10, u"Статус членства")
	  self.ws.write(0, 11, u"Источник")
	  self.ws.write(0, 12, u"Дата сбора информации")
	  self.ws.write(0, 13, u"Дата обновления")
	  self.ws.write(0, 14, u"Гиперссылка")
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(1,28):
               yield Task ('post',url='https://srosovet.ru/partnership/members-list/?page=%d'%x,network_try_count=100)
	       
	       
	       
	       
	       
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//a[contains(@href,"person")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)	       
                
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h2').text()
	  except IndexError:
	       sub = ''
	  try:
	       ray =  ''#grab.doc.select(u'//td[contains(text(),"Организация (место работы)")]/following-sibling::td').text().split('Должность: ')[1].split(' Подробнее')[0]
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//a[contains(@onclick,"pnlCv")]').text()#.split('Должность: ')[1].split(' Подробнее')[0]
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #ln = []
	       #for m in grab.doc.select(u'//td[contains(text(),"Квалификационный аттестат")]/following-sibling::td/b[contains(text(),"Направление:")]/following-sibling::text()[1]'):
		    #mes = m.text() 
		    #ln.append(mes)
	       #ter = ', '.join(ln)
	       ter= grab.doc.select(u'//td[contains(text(),"Переподготовка")]/following-sibling::td[1]').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       uliza = grab.doc.select(u'//div[contains(text(),"Данные обновлены")]').text().split(' в ')[1]
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//h5[@id="srchMarkContact"]/following-sibling::table[1]/tbody/tr/td[2]').text()#.split(', ')[0]
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//h5[@id="srchMarkContact"]/following-sibling::table[1]/tbody/tr/td[3]').text()#.split(', ')[1]
	  except IndexError:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//td[contains(text(),"Регионы деятельности")]/following-sibling::td').text()#.split(', ')[1].replace(u'г.','')
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//span[@class="reestr-info__status"]').text().split(': ')[1]
	  except IndexError:
	       price = ''   
	
          #udal = reduce(lambda udal, r: udal.replace(r[0], r[1]), conv, udal).replace(u' областьская ',' ') 
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal.replace(u' крайский ',' '),
                      'cena': price }
          
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
	  print  task.project['cena']

	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write_string(self.result, 14, task.project['url'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write_string(self.result, 6, task.project['trassa'])
	  self.ws.write(self.result, 8, task.project['udal'])
	  self.ws.write(self.result, 10, task.project['cena'])
	  self.ws.write(self.result, 11, u'Ассоциация «СРОО «ЭС»')
	  self.ws.write(self.result, 12, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	  #if self.result >= 10:
	       #self.stop()	       	       
	 

     
bot = Cian_Zem(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
try:
     bot.run()
except KeyboardInterrupt:
     pass
workbook.close()
print('Done!') 







