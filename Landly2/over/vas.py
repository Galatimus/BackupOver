#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import pymongo
from pymongo import MongoClient
#from googletrans import Translator
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

urls = open('new.txt').read().splitlines()

for p in range(len(urls)):

     class Cian_Zem(Spider):
	  def prepare(self):
	       #self.trans= Translator(service_urls=['translate.google.com', 'translate.google.co.kr'], user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0', proxies=None, timeout=50)
	       self.client = MongoClient('mongodb://127.0.0.1:27017')
	       self.db = self.client['MyShop']
	       self.records = self.db['Chinavasion']
	       self.result= 1       
	 
	  def task_generator(self):
	       for x in range(1,int(urls[p].split(',')[1])):
	            yield Task ('post',url='https://www.chinavasion.com/china/wholesale/'+urls[p].split(',')[0]+'/?page=%d'%x,refresh_cache=True,network_try_count=100)     
		    
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//div[@class="product_tile short"]/a'):
		    ur = grab.make_url_absolute(elem.attr('href')) 
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True, network_try_count=100)	       
		     
	  def task_item(self, grab, task):
	       try:
		    sub = grab.doc.select(u'//div[@class="item vcard"]/h1').text()
	       except IndexError:
		    sub = ''
	       try:
		    ray = grab.doc.select(u'//div[@itemprop="description"]').text()
	       except IndexError:
		    ray = ''
	       try:
		    punkt= grab.doc.select(u'//meta[@itemprop="price"]/@content').text()
	       except IndexError:
		    punkt = ''
		    
	       try:
		    ter = []
		    for em in grab.doc.select(u'//div[@id="xys"]/img'):
			 urr = em.attr('src').replace('thumbnails/','').split('.thumb')[0]
			 ter.append('http:'+urr)
	       except IndexError:
		    ter =''
		    
	       try:
		    uliza = grab.doc.select(u'//span[@class="code"]').text()
	       except IndexError:
		    uliza = ''
	       try:
		    dom = []
		    for mm in grab.doc.select(u'//div[@id="specs"]/p'):
			 dom.append(mm.text())
	       except IndexError:
		    dom = ''
	      
	       gen = []
	       for m in grab.doc.select(u'//ul[@id="general"]/li'):
		    gen.append(m.text())
	       for z in grab.doc.select(u'//div[@id="specs"]/ul/li'):
		    gen.append(z.text())
	     
		    
	       try:
		    categ = grab.doc.select(u'//div[@id="breadcrumb"]').text()
	       except IndexError:
		    categ = ''
			      
	       clearText = re.sub(u"[^a-zA-Z0-9.,\-\s]", "", ray)
	       clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText)
	       
	       #Text = re.sub(u"[^a-zA-Z0-9.,\-\s]", "", dom)
	       #Text = re.sub(u"[.,\-\s]{3,}", " ", Text)
	       
	       projects = {}
		    
	       projects = {'name': sub,
		           'description': clearText,
		           'description_new': dom,
		           'price': punkt,
		           'images': ter,
		           'url': task.url,
		           'option': gen,
		           'category': categ,
		           'category_id': uliza} 
	       
	       yield Task('write',project=projects,grab=grab,refresh_cache=True)
		 
	  def task_write(self,grab,task):
	       print('*'*50)
	       print  task.project['name']
	       #print  task.project['description']
	       print  task.project['price']
	       #print  task.project['images']
	       print  task.project['category_id']
	       #print  task.project['description_new']
	       #print  task.project['option']
	       print  task.project['category']
	       print('*'*50)
	       print 'Ready - '+str(self.result)+' ** '+str(p+1)+'/'+str(len(urls))
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       self.records.insert(task.project)
	       print('*'*50)	       
	       self.result =self.result+1
	 
     bot = Cian_Zem(thread_number=5,network_try_limit=2000)
     bot.load_proxylist('/home/oleg/pars/proxy/ivan.txt','text_file')
     bot.create_grab_instance(timeout=500, connect_timeout=5000)
     try:
	  bot.run()
     except KeyboardInterrupt:
	  pass
     bot.client.close()
     print('Done!') 







