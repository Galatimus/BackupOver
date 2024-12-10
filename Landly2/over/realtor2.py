#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
import re
from grab import Grab
import time
from datetime import datetime,timedelta
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Domofond_Com(Spider):
     def prepare(self):
	  self.result= 1
	   
     def task_generator(self):
	  l= open('realtor.txt').read().splitlines()
          self.dc = len(l)
          print self.dc	 
          for line in l:
	       #g = Grab(url=line,timeout=20, connect_timeout=50)
	       #g.setup(proxy='http://lum-customer-landly-zone-zone1:e7qhy6dhu0fs@zproxy.lum-superproxy.io:22225', proxy_type='http')
	       yield Task ('item',url=line,refresh_cache=True,network_try_count=10000)
	       #del g
	       time.sleep(5)
   
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//span[@itemprop="streetAddress"]').text().replace(',','')
	  except IndexError:
	       sub = ''
	  try:
	       ray =  grab.doc.select(u'//span[@itemprop="addressLocality"]').text()
	  except IndexError:
	       ray = ''
	  try:
	       punkt= grab.doc.select(u'//span[@itemprop="addressRegion"]').text()
	  except IndexError:
	       punkt = ''

	  try:
	       ter = grab.doc.select(u'//span[@itemprop="postalCode"]').text()
	  except IndexError:
	       ter =''

	  try:
	       uliza = grab.doc.select(u'//meta[@itemprop="latitude"]').attr('content')
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//meta[@itemprop="longitude"]').attr('content')
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//p[@id="ldp-detail-romance"]').text()
	  except IndexError:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//span[contains(text(),"Year built:")]/following-sibling::span').text()
	  except IndexError:
	       udal = ''
	  try:
	       price = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[2]
	  except IndexError:
	       price = '' 

	  try:
	       opis = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[0]
	  except IndexError:
	       opis = ''
	  try:
	       et = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[1]
	  except IndexError:
	       et = ''
	  try:
	       et1 = grab.doc.select(u'//span[@class="ds-value"]').text()
	  except IndexError:
	       et1 = ''
	  try:
	       et2 = grab.doc.select(u'//span[@class="ds-status-details"]').text()
	  except IndexError:
	       et2 = ''
	  try:
	       lin = []
	       for em in grab.doc.select(u'//picture[@class="media-stream-photo"]/img'):
		    urr = em.attr('src')
		    lin.append(urr)
	       et3 = ", ".join(lin) 
	  except IndexError:
	       et3 = ''
	  try:
	       li = []
	       for m in grab.doc.select(u'//div[@class="ds-nearby-schools-info-section"]/a'):
		    ur = m.text()
		    li.append(ur)
	       et4 = ", ".join(li)
	  except IndexError:
	       et4 = ''	
	  try:
	       et5 = grab.doc.select(u'//span[@class="ds-estimate-value"]').text()
	  except IndexError:
	       et5 = ''
	  try:
	       try:
		    et6 = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['@type']
	       except IndexError:
		    et6 = grab.doc.select(u'//span[contains(text(),"Type:")]/following-sibling::span').text()
	  except IndexError:
	       et6 =''
	  try:
	       try:
		    et7 = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[3]
	       except IndexError:
		    et7 = grab.doc.select(u'//span[contains(text(),"Lot:")]/following-sibling::span').text()
	  except IndexError:
	       et7 = ''
	  try:
	       et8 = grab.doc.rex_text(u'regionForecastRate":"(.*?)"}')
	  except IndexError:
	       et8 = ''
	  try:
	       et9 = grab.doc.select(u'//div[contains(text(),"Time on Zillow")]/following-sibling::div').text()
	  except IndexError:
	       et9 = ''
	  #try:
	       #et10 = grab.doc.select(u'//span[contains(text(),"Страна производства")]/following-sibling::span').text()
	  #except IndexError:
	       #et10 = ''
	  #try:
	       #et11 = grab.doc.select(u'//span[contains(text(),"Застежка")]/following-sibling::span').text()
	  #except IndexError:
	       #et11 = ''
	  #try:
	       #et12 = grab.doc.select(u'//span[contains(text(),"Капюшон")]/following-sibling::span').text()
	  #except IndexError:
	       #et12 = ''

	 
	  phone = ''
	  
   
	  projects = {'street': sub,
                    'city': ray,
                    'state': punkt,
                    'zipcode': ter,
                    'latitude': uliza,
                    'longitude': dom,
                    'description': trassa, 
                    'yearBuilt': udal,              
                    'livingArea': price,                      
                    'bedrooms': opis,
                    'bathrooms': et,
                    'price': et1,
                    'status': et2,
                    'photos': et3,
                    'schools': et4,
                    'url': task.url,
                    'zestimate': et5,
                    'type': et6,
                    'lotSize': et7,
                    'forecast': et8,
                    'time': et9}
		    #'et10': et10,
		    #'et11': et11,
		    #'url': task.url,
		    #'et12': et12,
		    #'opis': opis,
		    #'cena': price }
	  
	  yield Task('write',project=projects,grab=grab)
     
	  
     def task_write(self,grab,task):
	  #time.sleep(1)
	  print('*'*100)
	  print  task.project['street']
	  print  task.project['city']
	  print  task.project['state']
	  print  task.project['zipcode']
	  print  task.project['latitude']
	  print  task.project['longitude']
	  print  task.project['description']
	  print  task.project['yearBuilt']
	  print  task.project['livingArea']
	  print  task.project['price']
	  print  task.project['bedrooms']
	  print  task.project['bathrooms']
	  print  task.project['status']
	  print  task.project['photos']
	  print  task.project['schools']
	  print  task.project['url']
	  print  task.project['zestimate']
	  print  task.project['type']
	  print  task.project['lotSize']
	  print  task.project['forecast']
	  print  task.project['time']

     
	  
	  

	  
	  print('*'*10)
	  print 'Ready - '+str(self.result)+'/'+str(self.dc)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print('*'*10)
	  self.result+= 1
   

bot = Domofond_Com(thread_number=5, network_try_limit=100000)
#bot.load_proxylist('../ivan.txt','text_file')
bot.load_proxylist('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt','url')
bot.create_grab_instance(timeout=500, connect_timeout=500)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Спим 2 сек...')
time.sleep(1)
print('Сохранение...')
print('Done!')
 

       
     
     
     