#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task,SpiderError
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Emails.xlsx')

kd = open('mail.txt').read().splitlines()

class Ya39_Com(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet('Emails')
	  self.ws.write(0, 0, u"Домен")
	  self.ws.write(0, 1, u"Emails")
	  #self.ws.write(0, 2, u"URL")
	 
	       
	  self.result= 1
	  
	  self.em =[]
	  self.ems=[]
	  self.vse=[]
	
	       
    
     def task_generator(self):
	  for line in kd:
               yield Task ('item',url='http://'+line.strip(),refresh_cache=True,network_try_count=10)
               yield Task ('item2',url='http://'+line.strip(),refresh_cache=True,network_try_count=10)
   	 
     def task_item2(self, grab, task):
	  try: 
	       contact_url = grab.make_url_absolute(grab.doc.select(u'//a[contains(@href, "contact")]').attr('href'))
	       yield Task('item3', url=contact_url,refresh_cache=True,network_try_count=10)
	  except (IndexError,TypeError): 
	       yield Task('item3',grab=grab ,refresh_cache=True,network_try_count=10)
	       
	       
     def task_item3(self, grab, task):
	  try:
	       self.em = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9]+)',grab.response.body)
	       #emls=','.join(em).replace(u'--Rating@Mail.ru','').replace(u'Rating@Mail.ru','')
	       #print emls
	  except (IndexError,TypeError):
	       self.em =''
	  #yield Task('write',self.em=em,grab=grab)
	  
	  #self.ws.write_string(self.result, 0, emls)
	  #self.result+= 1
     def task_item(self, grab, task):
	  try:
	       self.ems = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9]+)',grab.response.body)
	       #sub=','.join(s).replace(u'--Rating@Mail.ru','').replace(u'Rating@Mail.ru','')
	       #print sub
	  except (IndexError,TypeError):
	       self.ems = ''
	  #yield Task('write',ems=ems,grab=grab)
	  #print self.em
	  #print self.ems
	  self.vse=self.em+self.ems
	  #print self.vse
	  sub=','.join([elem for idx, elem in enumerate(self.vse) if elem not in self.vse[:idx]])
	  print sub
	  
     #def task_write(self,grab,task):
	  #print self.em
	  #print task.ems
	       
	  self.ws.write_string(self.result, 1, sub)
	  self.ws.write_string(self.result, 0, task.url.replace('http://',''))
	  self.result+= 1
    
	
	  print('*'*50)
          print 'Ready - '+str(self.result)+'/'+str(len(kd))
	  print 'Task - '+str(self.task_queue.size())
	  print('*'*50)
	  
          #if self.result > 100:
               #self.stop()	  
	       
	 

     
bot = Ya39_Com(thread_number=1,network_try_limit=100)
#bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







