#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Domofond_Com(Spider):
     def prepare(self):
	  self.lin = []
	   
     def task_generator(self):
	  yield Task ('post',url='https://www.zillow.com/browse/homes/',refresh_cache=True,network_try_count=1000)

   
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//h2[contains(text(),"United States")]/following-sibling::ul/li/a'):
	       yield Task('homes',url=grab.make_url_absolute(elem.attr('href')),refresh_cache=True,network_try_count=1000)
   
     def task_homes(self,grab,task):
	  for el in grab.doc.select(u'//section[@class="zsg-content-component"]/ul/li/a[1]'):
	       yield Task('zip',url=grab.make_url_absolute(el.attr('href')),refresh_cache=True,network_try_count=1000)
	       
     def task_zip(self,grab,task):
	  for z in grab.doc.select(u'//section[@class="zsg-content-component"]/ul/li/a'):
	       zi = grab.make_url_absolute(z.attr('href'))
	       if 'homedetails' in zi:
		    self.lin.append(zi)
	       else:
		    yield Task('zipgo',url=zi ,refresh_cache=True,network_try_count=1000)
	       
     def task_zipgo(self,grab,task):
	  for rel in grab.doc.select(u'//section[@class="zsg-content-component"]/ul/li/a'):
	       urll = grab.make_url_absolute(rel.attr('href'))
	       if 'homedetails' in urll:
		    self.lin.append(urll)
	       else:
	            yield Task('real',url=urll,refresh_cache=True,network_try_count=1000)
	       
     def task_real(self,grab,task):
	  for real in grab.doc.select(u'//section[@class="zsg-content-component"]/ul/li/a'):
	       new = grab.make_url_absolute(real.attr('href'))  
	       #print new
	       self.lin.append(new)
	  print('*'*10)
	  print 'Ready - '+str(len(self.lin))
	  print('*'*10)
	       
bot = Domofond_Com(thread_number=3, network_try_limit=100000)
bot.load_proxylist('../tipa.txt','text_file')
#bot.load_proxylist('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt','url')
bot.create_grab_instance(timeout=500, connect_timeout=500)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Спим 2 сек...')
time.sleep(1)
print('Сохранение...')
links = open('ready/Zillow_off2.txt', 'a')
for item in bot.lin:
     links.write("%s\n" % item)
links.close()
time.sleep(1) 
print('Done!')
 

       
     
     
     