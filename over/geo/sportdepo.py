#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
import xlsxwriter





logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)




#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')




class fason(Spider):
     def prepare(self):
	  
	  self.workbook = xlsxwriter.Workbook(u'Sportdepo.xlsx')
	  self.ws = self.workbook.add_worksheet()
	  self.ws.write(0, 0, u"Команда1")
	  self.ws.write(0, 1, u"1>2")
	  self.ws.write(0, 2, u"1=2")
	  self.ws.write(0, 3, u"1<2")
	  self.ws.write(0, 4, u"Команда2")
	  self.ws.write(0, 5, u"1>2")
	  self.ws.write(0, 6, u"1=2")
	  self.ws.write(0, 7, u"1<2")
	  self.ws.write(0, 8, u"Сумма:1>2")
	  self.ws.write(0, 9, u"Сумма:1=2")
	  self.ws.write(0, 10, u"Сумма:1<2")
	  
    
	  self.result= 1
	 
	  
     
     
     def task_generator(self):
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/9662/',refresh_cache=True,network_try_count=100) 
          yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/3982/',refresh_cache=True,network_try_count=100) 
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/34999/',refresh_cache=True,network_try_count=100) 
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/664/',refresh_cache=True,network_try_count=100) 
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/3662/',refresh_cache=True,network_try_count=100) 
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/131/',refresh_cache=True,network_try_count=100) 
	  yield Task ('post',url='https://www.sportdepo.ru/catalog/name/Price/id/51425/',refresh_cache=True,network_try_count=100) 
	  
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="cat"]/h2/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur	      
	       yield Task('next',url=ur+'?page=all',refresh_cache=True,network_try_count=100)
	  for el in grab.doc.select(u'//div[@class="catalog"]/div/a/following-sibling::div/h3/a'):
	       urr = grab.make_url_absolute(el.attr('href'))  
	       #print urr	 
               yield Task('next',url=urr+'?page=all',refresh_cache=True,network_try_count=100)
     
     def task_next(self,grab,task):
	  for ele in grab.doc.select(u'//a[@class="img_price"]'):
	       urs = grab.make_url_absolute(ele.attr('href'))  
	       #print urs
	       yield Task('item',url=urs,refresh_cache=True,network_try_count=100)

     def task_item(self, grab, task):
	  
	  try:
	       pli = grab.doc.select(u'//h1').text()
	  except IndexError:
	       pli = ''
	  try:
	       kol = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[2]/td[4]').text()
	  except IndexError:
	       kol = ''
	  try:
	       ves = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[2]/td[6]').text()
	  except IndexError:
	       ves = ''		       
	       
	  try:
	       ar = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[2]/td[8]').text()
          except IndexError:
	       ar = ''
	  try:
	       koll = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[4]/td[1]').text()
	  except IndexError:
	       koll = ''
	  try:
	       cvet = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[6]/td[4]').text()
	  except IndexError:
	       cvet = ''
	  try:
	       raz = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[6]/td[6]').text()
	  except IndexError:
	       raz = ''	       
          try:
	       pic = grab.doc.select(u'//td[contains(text(),"сравнение тоталов таймов")]/following::tbody[@class="f11"][1]/tr[6]/td[8]').text()
	  except IndexError:
	       pic = ''
	 
	       
	       
	  projects = {'sub':pli,
                      'adress': kol,
                      'terit':ves, 
                      'punkt':ar, 
                      'ulica':koll,
                      'dom':cvet,
                      'tip':raz,
	              'naz':pic}
	       
	  yield Task('write',project=projects,grab=grab)
	       
	       
     def task_write(self,grab,task):
	  #time.sleep(1)
	  print('*'*50)	       
	  print  task.project['sub']
	  print  task.project['adress']
	  print  task.project['terit']
	  print  task.project['punkt']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['tip']
	  print  task.project['naz']
	 
	 
	       
	       
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['adress'])
	  self.ws.write(self.result, 2, task.project['terit'])
	  self.ws.write(self.result, 3, task.project['punkt'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 6, task.project['tip'])
	  self.ws.write(self.result, 7, task.project['naz'])
	  #self.ws.write(self.result, 8, task.project['itog1'])
	  #self.ws.write(self.result, 9, task.project['itog2'])
	  #self.ws.write(self.result, 10, task.project['itog3'])
	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)
	  print 'Tasks - %s' % self.task_queue.size() 
	  print('*'*50)
	  
	 
	  
	  
	  self.result+= 1
	  
	  
	  #if self.result > 30:
	       #self.stop() 

bot = fason(thread_number=5, network_try_limit=2000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print('Сохранение...')
bot.workbook.close()
print('Done!')
     
