#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import pymongo
from pymongo import MongoClient
from pymongo.errors import InvalidOperation,DuplicateKeyError
import re
import collections
import math
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



i =0
l= open('redfin.txt').read().splitlines()
dc = len(l)
page = l[i]

url_base = 'mongodb://oleg:walter2005@cluster0-shard-00-00-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-01-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-02-cfwsy.gcp.mongodb.net:27017/landly?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'

#url_base = 'mongodb://127.0.0.1:27017'


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class Domofond_Com(Spider):
	  def prepare(self):
	       self.link = page
	       self.lin = []
	       self.tobase = []	
	       self.dubl = []
	       print 'Request to base ...'
	       self.client = MongoClient(url_base)
	       self.db = self.client.landly
	       for entry in self.db.redfin2.find():
		    self.tobase.append(entry["fpid"])
	       print 'Records IS :',str(len(self.tobase)),'>>',str(len(list(set(self.tobase))))
	       self.dubl = [item for item, count in collections.Counter(self.tobase).items() if count > 1]
               print 'duplicate is >>',len(self.dubl)
	       self.dubl.sort()
	       for i in range(len(self.dubl)):
		    print str(self.dubl[i]) + ' is a duplicate',str(i),'/',str(len(self.dubl))
		    self.db.redfin2.delete_one({'rpid': self.dubl[i]})
		    self.tobase.remove(self.dubl[i])
	       print 'Records NEW IS :',str(len(self.tobase))
	       self.client.close
	       time.sleep(2)
	       for p in range(1,51):
		    try:
			 time.sleep(2)
			 g = Grab(timeout=20, connect_timeout=50)
			 #g.proxylist.load_file(path='../ivan.txt',proxy_type='http')
			 g.proxylist.load_url('http://lum-customer-landly-zone-zone1:e7qhy6dhu0fs@zproxy.lum-superproxy.io:22225')
			 g.go(self.link)
			 
			 try:
			      self.num = re.sub('[^\d]','',g.doc.select(u'//div[@class="homes summary"]').text().split(' of ')[1])
			 except IndexError:
			      self.num = re.sub('[^\d]','',g.doc.rex_text(u'of (.*?) Homes'))
		         try:
			      self.pag = int(math.ceil(float(int(self.num))/float(20)))
			 except OverflowError:
			      self.num = 1
			      self.pag = 1
			      
			 if self.pag > 17:
			      self.pag = 17
			 else:
			      self.pag = self.pag
			      
			 print('*'*50)
			 print self.num
			 print self.pag
			 print('*'*50)
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print p,'Change proxy'
			 del g
			 continue
	       else:
		    self.num = 1
		    self.pag = 1
	      	
	  def task_generator(self):
	       for x in range(1,self.pag+1):
		    yield Task ('post',url=self.link+'/page-'+str(x),refresh_cache=True,network_try_count=10000000)
	       #yield Task ('post',url=self.link,refresh_cache=True,network_try_count=100)
	
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//div[@class="homecardv2"]/following-sibling::a'):
		    yield Task('item', url=grab.make_url_absolute(elem.attr('href')),refresh_cache=True, network_try_count=10000000)


	
	  def task_item(self, grab, task):
	       try:
		    sub = grab.doc.select(u'//span[@class="street-address"]').text()
	       except IndexError:
		    sub = ''
	       try:
		    ray =  grab.doc.select(u'//span[@class="locality"]').text()
	       except IndexError:
		    ray = ''
	       try:
		    punkt= grab.doc.select(u'//span[@class="region"]').text()
	       except IndexError:
		    punkt = ''
     
	       try:
		    ter = grab.doc.select(u'//span[@class="postal-code"]').text()
	       except IndexError:
		    ter =''
     
	       try:
		    uliza = grab.doc.rex_text(u'latitude":(.*?),')
	       except IndexError:
		    uliza = ''
	       try:
		    dom = grab.doc.rex_text(u'longitude":(.*?)}')
	       except IndexError:
		    dom = ''       
	       try:
		    trassa = grab.doc.select(u'//div[@class="sectionContent"]/div').text()
	       except IndexError:
		    trassa = ''       
	       try:
		    udal = grab.doc.select(u'//span[contains(text(),"Built")]/following-sibling::span').text()
	       except IndexError:
		    udal = ''
		    
	       try:    
		    try:
			 pr = grab.doc.select(u'//div[@class="info-block sqft"]/span/span[@class="statsValue"]').text()
		    except IndexError:
			 pr = grab.doc.select(u'//span[contains(text(),"Total Sq. Ft.")]/following-sibling::div').text()
	       except IndexError:
		    pr = '' 
	  
	       try:
		    try:
		         opis = grab.doc.select(u'//div[@data-rf-test-id="abp-beds"]/div').text()
		    except IndexError:
			 opis = grab.doc.select(u'//span[contains(text(),"Beds")]/following-sibling::div').text()
	       except IndexError:
		    opis = ''
	       try:
		    try:
		         et = grab.doc.select(u'//div[@data-rf-test-id="abp-baths"]/div').text()
		    except IndexError:
			 et = grab.doc.select(u'//span[contains(text(),"Baths")]/following-sibling::div').text()
	       except IndexError:
		    et = ''
	       try:
		    et1 = grab.doc.select(u'//div[@class="info-block price"]/div/div').text()
	       except IndexError:
		    et1 = ''
	       try:
		    et2 = grab.doc.select(u'//span[@class="status-container"]/span/span[2]/div/span').text()
	       except IndexError:
		    et2 = ''
	       try:
		    et3 = []
		    for em in grab.doc.select(u'//img[contains(@src,"media")]'):
			 urr = em.attr('src').replace('genLdpUgcThumb','genLdpUgcMediaBrowserUrl')
			 et3.append(urr)
		    for m in grab.doc.select(u'//img[contains(@src,"mbpaddedwide")]'):
			 u = m.attr('src')
			 et3.append(u)		    
	       except IndexError:
		    et3 = ''
	       try:
		    et4 = []
		    et44 = []
		    et444 = []
		    ett44 = []
		    for n in grab.doc.select(u'//div[@data-rf-test-name="school-name"]'):
			 ur = n.text()
			 et4.append(ur)
		    for gr in grab.doc.select(u'//div[@data-rf-test-name="school-name"]/following-sibling::div[1]'):
			 urr = gr.text().split(' • ')[1]
			 et44.append(urr)
		    for di in grab.doc.select(u'//td[@class="distance-col"][contains(text(),"mi")]'):
			 urd = di.text()
			 et444.append(urd)
		    for rt in grab.doc.select(u'//div[@class="rating"]'):   
			 urt = rt.text()
			 ett44.append(urt)	       
	       except IndexError:
		    et4 = ''	
	       #try:
		    #et5 = grab.doc.select(u'//div[@class="RedfinEstimateValueHeader"]/div').text().replace('None','')
	       #except IndexError:
	       et5 = ''
	       try:
		    try:
			 et6 = grab.doc.select(u'//span[contains(text(),"Style")]/following-sibling::div').text()
		    except IndexError:
			 et6 = grab.doc.rex_text(u'propertyTypeName\":\"(.*?)\"')
	       except IndexError:
		    et6 =''
	       try:
		    try:
			 et7 = grab.doc.select(u'//span[contains(text(),"Lot Size")]/following-sibling::div').text()
		    except IndexError:
			 et7 = grab.doc.select(u'//span[contains(text(),"Lot Size")]/following-sibling::span').text()
	       except IndexError:
		    et7 = ''
	       #try:
		    #try:
			 #et8 = grab.doc.select(u'//div[contains(text(),"One Year Forecast")]/following-sibling::div/span').text()
		    #except IndexError:
			 #et8 = grab.doc.rex_text(u'regionForecastRate":"(.*?)"}')
	       #except IndexError:
	       et8 = ''
	       
	       try:
		    et9 = grab.doc.select(u'//span[contains(text(),"On Redfin:")]/following-sibling::span[contains(text(),"days")]').text()
	       except IndexError:
		    et9 = ''
	       try:
		    et10 = []
		    for s in grab.doc.select(u'//div[@class="similars"]/div/div/div/a'):
			 urs = s.attr('title')
			 et10.append(urs)
	       except IndexError:
		    et10 = ''
	       try:
		    et11 = grab.doc.select(u'//h3[contains(text(),"Heating & Cooling")]/following-sibling::li[2]/span/span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et11 = ''
	       try:
		    et12 = grab.doc.select(u'//h3[contains(text(),"Heating & Cooling")]/following-sibling::li[1]/span/span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et12 = ''
	       try:
		    et13 = grab.doc.select(u'//h3[contains(text(),"Garage & Parking")]/following-sibling::li/span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et13 = ''	  
	       try:
		    et14 = grab.doc.select(u'//div[@data-rf-test-id="abp-priceperft"]').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et14 = ''     
	       try:
		    try:
			 et15 = grab.doc.select(u'//h2[contains(text(),"Neighborhood")]/span/span[2]').text()
		    except IndexError:
			 et15 = grab.doc.rex_text(u'Neighborhood:(.*?)<')
	       except IndexError:
		    et15 = ''
	       try:
		    et16 = grab.doc.rex_text(u'rent for (.*?).')
	       except IndexError:
		    et16 = ''
	       try:
		    et17 = grab.doc.select(u'//span[contains(text(),"Year Renovated")]/following-sibling::div').text()
	       except IndexError:
	            et17 = ''
	  
	       try:
		    et18 = grab.doc.select(u'//h3[contains(text(),"Kitchen Features")]/following-sibling::li/span/span').text()
	       except IndexError:
		    et18 = ''	       
	       #print et18
	  
	       try:
		    et19 = grab.doc.select(u'//span[contains(text(),"Flooring")]').text()
	       except IndexError:
		    et19 = ''	       
	       #print et19
	  
	       try:
		    item20 = pr
	       except IndexError:
		    item20 = ''	       
	       #print item20
	  
	       try:
		    item21 = grab.doc.select(u'//span[contains(text(),"Fireplace")]').text()
	       except IndexError:
		    item21 = ''	       
	       #print item21
	  
	       try:
		    item22 = grab.doc.select(u'//span[contains(text(),"Stories")]/following-sibling::div').text()
	       except IndexError:
		    item22 = ''	       
	       #print item22
	  
	       #try:
		    #try:
			 #item23 = grab.doc.rex_text(u'Private pool:<!-- -->(.*?)<')
		    #except IndexError:
			 #item23 = grab.doc.select(u'//span[contains(text(),"Private pool:")]').text().split(': ')[1]
	       #except IndexError:
	       item23 = ''
	  
	       try:
		    item24 = grab.doc.select(u'//h3[contains(text(),"Interior Features")]/following-sibling::li').text()
	       except IndexError:
		    item24 = ''
	  
	       try:
		    item25 = grab.doc.select(u'//title').text().split('MLS# ')[1].split(' | ')[0]
	       except IndexError:
		    item25 = ''
	       
	       temp = {'atAGlanceFacts':[]} 
	  
	       temp['atAGlanceFacts'].append({'factLabel': 'Year built','factValue': udal})
	       temp['atAGlanceFacts'].append({'factLabel': 'Remodeled year','factValue': re.sub(u'[^\d]','',et17)})
	       temp['atAGlanceFacts'].append({'factLabel': 'Heating','factValue': et11})
	       temp['atAGlanceFacts'].append({'factLabel': 'Cooling','factValue': et12})
	       temp['atAGlanceFacts'].append({'factLabel': 'Parking','factValue': et13})
	       temp['atAGlanceFacts'].append({'factLabel': 'lotsize','factValue': et7})
	       temp['atAGlanceFacts'].append({'factLabel': 'Price/sqft','factValue': et14})
	  
	       projects = {'city': ray,
		           'country': 'USA',
		           'state': punkt,
		           'street': sub,
		           'zipcode': ter,
		           'lat': uliza,
		           'lon': dom,
		           'baths': et,
		           'beds': opis,
		           'sqft': pr,
		           '1-year-forecast': et8,
		           'rent': et16,
		           'propertyType': et6,
		           'homeFacts': temp,
		           'description': trassa, 
		           'price': et1,
		           'mls-id': item25,
		           'flooring': et19,
		           'total-interior-livable-area': item20,
		           'fireplace': item21,
		           'stories': item22,
		           'private pool': item23,
		           'exterior features': item24,
		           'status': et2,
		           'images': et3,
		           'appliances': et18.split(', '),
		           'schools': [{'data': {'Grades': et44,'Distance': et444},'name': et4,'rating': ett44}],
		           'url': task.url,
		           'zestimate': et5,
		           'fpid': 'RF'+task.url.split('home/')[1],
		           'timeonredfin': et9,
		           'similarhouses': et10,
		           'neighborhood': et15}
	       
	       yield Task('write',project=projects,grab=grab)
	  
	       
	  def task_write(self,grab,task):
	       if task.project['fpid'] not in self.tobase:
		    print('*'*10)
		    print  task.project['description']
		    print  task.project['fpid'] 
		    print  task.project['mls-id']
		    #print  task.project['images']
		    self.lin.append(task.project)
		    print('*'*10)
		    print 'Ready - '+str(len(self.lin))+'/'+str(self.num)
		    logger.debug('Tasks - %s' % self.task_queue.size()) 
		    print '***',i+1,'/',dc,'***'
		    print('*'*10)
	       else:
		    print('*'*10)
		    print task.project['fpid'],'<<<IS EXITS!!!>>>'
		    logger.debug('Tasks - %s' % self.task_queue.size())
		    print('*'*10) 	       
	
     
     bot = Domofond_Com(thread_number=3, network_try_limit=100000000)
     bot.load_proxylist('../ivan.txt','text_file')
     #bot.load_proxylist('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt','url',proxy_type='http')
     bot.create_grab_instance(timeout=500, connect_timeout=500)
     try:
	  bot.run()
     except KeyboardInterrupt:
	  pass
     print('sleep 2 ...')
     time.sleep(2)    
     print len(bot.lin)
     client = MongoClient(url_base)
     db = client.landly
     records = db.redfin2 
     try:
          records.insert(bot.lin)
     except InvalidOperation:
	  pass
     client.close()
     print('Record Done!')
     time.sleep(2)
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  break     

       
     
     
     