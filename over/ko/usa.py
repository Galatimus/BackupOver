#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Yelp_Car_Dealers.xlsx') 

	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  #self.ws.write(0, 0, u"ШТАТ")
	  #self.ws.write(0, 1, u"ГОРОД")
	  #self.ws.write(0, 2, u"НАЗВАНИЕ_КОМПАНИИ")
	  #self.ws.write(0, 3, u"АДРЕС")
	  self.ws.write(0, 0, u"ВЕБСАЙТ")
	  #self.ws.write(0, 5, u"ТЕЛЕФОН")
	  #self.ws.write(0, 6, u"УСЛУГИ")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
          yield Task ('post',url='https://www.yelp.com/city',refresh_cache=True,network_try_count=100)

	       
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[contains(@href,"city")]'):
	       self.cit = elem.text()  
	       #print cit
	       yield Task('next', url='https://www.yelp.com/search?find_desc=Car Dealers&find_loc='+self.cit,refresh_cache=True,network_try_count=100)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=1000)
	    
        
     def task_next(self,grab,task):
	  for elem in grab.doc.select(u'//h3/a[contains(@href,"Dealers")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur        
	       yield Task("item", url=ur,refresh_cache=True,network_try_count=100)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100) 
	  
	  
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//span[contains(text(),"Next")]/ancestor::a')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('next',url= u,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       print('*'*100)
	       print '!!!','NO PAGE NEXT','!!!'
	       print('*'*100)     
     
     def task_item(self, grab, task):
	  
	  #try:
	       #try:
                    #ray = grab.doc.select(u'//span[@itemprop="addressLocality"]').text()
	       #except IndexError:
		    #ray = grab.doc.select(u'//strong[@class="street-address"]').text().replace(u'Serving ','').replace(u' Area','')
          #except IndexError:
               #ray =''
	  
	  #try:
	       #uliza = grab.doc.select(u'//h1').text()
	  #except IndexError:
	       #uliza =''
	       
	  #try:
               #dom = grab.doc.select(u'//div[@class="lightbox-map hidden"]').attr('data-business-address')
	  #except IndexError:
	       #dom = ''
		
	    
	  #try:
               #tip = grab.doc.select(u'//span[@class="biz-phone"]').text()
          #except IndexError:
	       #tip = ''
	      
	  try:
	       novo = grab.doc.select(u'//span[contains(@class,"website")]/a').text()
	  except IndexError:
	       novo = ''
          #try:
               #kol_komnat = grab.doc.select(u'//span[@itemprop="addressRegion"]').text()
          #except IndexError:
               #kol_komnat = ''
	       
	  #try:
	       #ln = []
	       #for m in grab.doc.select('//div[@class="ywidget service-internal-links"]/ul/li/a/span'):
	            #mes = m.text() 
	            #ln.append(mes)
	       #plosh = ', '.join(ln)
          #except IndexError:
	       #plosh =''

          #try:
               #price = grab.doc.select(u'//div[@class="object_descr_price"]').text().split(u'.')[0]
          #except IndexError:
               #price = ''
          #try:
               #opis = grab.doc.select(u'//div[@class="object_descr_text"]/text()').text() 
          #except DataNotFound:
               #opis = ''
	       
	  #try:
	       #m2 = grab.doc.select(u'//div[@id="price_rur"]/following-sibling::div').text()#.split(u'включая')[0]
          #except IndexError:
               #m2 =''	       
	      
	       
	  projects = {'novo': novo}
	              #'ulica': uliza,
	              #'dom': dom,
	              #'url': task.url,
	              #'tip': tip,
	              #'novo': novo,
	              #'plosh': plosh,
	              #'cena': price,
	              #'opis': opis,
	              #'metr': m2,
	              #'col_komnat': kol_komnat}
	
	
	
	  yield Task('write',project=projects,grab=grab)
	
	
	
	
	
	
     def task_write(self,grab,task):
	  
	  print('*'*50)	       
	  #print  task.project['col_komnat']
	  #print  task.project['rayon']
	  #print  task.project['ulica']
	  #print  task.project['dom']
	  #print  task.project['tip']
	  print  task.project['novo']
	  #print  task.project['plosh']

	  
    
	  #self.ws.write(self.result, 1,task.project['rayon'])
	  #self.ws.write(self.result, 2,task.project['ulica'])
	  #self.ws.write(self.result, 3,task.project['dom'])
	  #self.ws.write(self.result, 5,task.project['tip'])
	  self.ws.write_string(self.result, 0,task.project['novo'])
	  #self.ws.write(self.result, 0,task.project['col_komnat'])
	  #self.ws.write(self.result, 6,task.project['plosh'])

	  
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  
	  
	  #if self.result > 20:
	       #self.stop()

     
bot = Cian_Kv(thread_number=10,network_try_limit=2000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
workbook.close()
print('Done!')

     
     