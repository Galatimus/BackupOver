#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import requests
from requests.exceptions import ConnectionError
import re
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Wiki-Prom_Заводы.xlsx')

    

class Wiki(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet('wiki-prom')
	  self.ws.write(0, 0, u"Название организации")
	  self.ws.write(0, 1, u"Отрасль")
	  self.ws.write(0, 2, u"Адрес")
	  self.ws.write(0, 3, u"Сайт")
	  self.ws.write(0, 4, u"Email")
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  yield Task ('post',url='http://www.wiki-prom.ru/navigator.html',refresh_cache=True,network_try_count=100)

            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//li[@class="name"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('next', url=ur,refresh_cache=True,network_try_count=100)
	 
     def task_next(self, grab, task): 
	  for el in grab.doc.select(u'//h4/a'):
	       ur1 = grab.make_url_absolute(el.attr('href'))  
	       #print ur1
	       yield Task('item', url=ur1,refresh_cache=True,network_try_count=100)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	  
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//ul[@class="pagination clearfix"]/li/a[contains(text(),"Следующая")]')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('next',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*100)
	       print '!!','NO PAGE NEXT','!!'
	       print('*'*100)
	       logger.debug('%s taskq size' % self.task_queue.size()) 
        
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h1').text()
	  except IndexError:
	       sub = ''
	  try:
	       ray =grab.doc.select(u'//div[@class="meta"]/a[2]').text()
	  except IndexError:
	       ray = ''          
	  try:
	       punkt = grab.doc.select(u'//span[contains(text(),"Адрес:")]/following-sibling::text()').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//div[@class="meta"]/a[4]').text()
	      
	  except IndexError:
	       ter =''
	       
	  try:
	       ulm = grab.make_url_absolute(grab.doc.select(u'//div[@class="meta"]/a[contains(@target,"blank")]').attr('href'))
	       r= requests.get(ulm,verify=True,allow_redirects=True,timeout=100)
	       m = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9]+)',r.content)
	       g2 = grab.clone(timeout=50, connect_timeout=50,proxy_auto_change=True)
	       g2.go(ulm)
	       contact_url = g2.doc.select('//a[contains(@href, "contact")]/@href').text()
	       g2.go(contact_url)
	       m1 = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9]+)',g2.response.body)	       
	       uliza=','.join(list(set(m+m1)))
	  except (ConnectionError,IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError):
	       uliza = ''
	       
	  uliza1 = ''
	  
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza}
          
	  #try:
	       #yield Task('write',project=projects,url=uliza,refresh_cache=True,network_try_count=100)
	  #except Exception:
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     def task_write(self,grab,task):
	  
	  
	  
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['url']
	
	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write_string(self.result, 3, task.project['teritor'])
	  self.ws.write_string(self.result, 4, task.project['ulica'])
	
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	  
	  
	  if self.result > 100:
	       self.stop()	  
	       
	 

     
bot = Wiki(thread_number=2,network_try_limit=2000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







