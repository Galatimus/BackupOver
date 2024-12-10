#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import json
import re
import collections
import pymongo
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import InvalidOperation
import math
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



i = 10
l= open('../city.txt').read().splitlines()
dc = len(l)
page = l[i]

projects = {}

url_base = 'mongodb://oleg:walter2005@cluster0-shard-00-00-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-01-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-02-cfwsy.gcp.mongodb.net:27017/landly?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'

while True:
     print '**********',i+1,'/',dc,'**********'
     class Domofond_Com(Spider):
	  def prepare(self):
	       #self.link = 'https://www.zillow.com/'+page.split(',')[0]+'-'+page.split(',')[1].lower()+'/'
	       self.link = 'http://www.zipcodeapi.com/rest/FbwO9OZpIHPr2eQ3sstLxZR9RGStVilmmsc1d2omDQ66djG9DNZgeGf0nhOYDdDS/city-zips.json/'+page.split(',')[0]+'/'+page.split(',')[1]+'/'
	       self.lin = []
	       self.zipcode = []
	       self.tobase = []	
	       self.dubl = []
	       print 'Request to base ...'
	       self.client = MongoClient(url_base)
	       self.db = self.client.landly
	       for entry in self.db.zillow.find():
		    self.tobase.append(entry["zpid"])
	       print 'Records IS:',str(len(self.tobase)),'>>',str(len(list(set(self.tobase))))
	       self.dubl = [item for item, count in collections.Counter(self.tobase).items() if count > 1]
	       print 'duplicate is >>',len(self.dubl)
	       self.dubl.sort()	
	       for i in range(len(self.dubl)):
		    print str(self.dubl[i]) + ' is a duplicate',str(i),'/',str(len(self.dubl))
		    self.db.zillow.delete_one({'zpid': self.dubl[i]})
		    self.tobase.remove(self.dubl[i])
	       print 'Records NEW IS :',str(len(self.tobase)) 
	       self.client.close
	       time.sleep(2)
	       for p in range(1,50):
		    try:
			 time.sleep(2)
			 g = Grab(timeout=20, connect_timeout=50)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
			 #g.proxylist.load_url('http://lum-customer-landly-zone-zone1:e7qhy6dhu0fs@zproxy.lum-superproxy.io:22225',proxy_type='http')
			 g.go(self.link)
			 self.zipcode = g.doc.json["zip_codes"]
			 print('*'*10)
			 print len(self.zipcode)
			 print('*'*10)
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print p,'Change proxy'
			 #g.change_proxy()
			 del g
			 continue
	       else:
		    self.pag = 1
		    self.num=1
	       

	  def task_generator(self):
	       for x in range(len(self.zipcode)):
		    for p in range(1,10):
		         yield Task ('post',url='https://www.zillow.com/'+page.split(',')[0].lower()+'-'+page.split(',')[1].lower()+'-'+self.zipcode[x]+'/'+str(p)+'_p/',refresh_cache=True,network_try_count=10000000)
		    

	
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//a[@class="list-card-link list-card-info"]'):
		    yield Task('item', url=grab.make_url_absolute(elem.attr('href')),refresh_cache=True, network_try_count=10000000)


	  def task_item(self, grab, task):
	       try:
		    try:
			 street = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['address']['streetAddress']
		    except IndexError:
			 street = grab.doc.select(u'//h1[@class="ds-address-container"]/span[1]').text().replace(',','')
	       except IndexError:
		    street = ''
	       try:
		    try:
			 ray =  json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['address']['addressLocality']
		    except IndexError:
			 ray =  grab.doc.select(u'//h1[@class="ds-address-container"]/span[2]').text().split(', ')[0]
	       except IndexError:
		    ray = ''
	       try:
		    try:
			 punkt= json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['address']['addressRegion']
		    except IndexError:
			 punkt= grab.doc.select(u'//h1[@class="ds-address-container"]/span[2]').text().split(', ')[1].split(' ')[0]
	       except IndexError:
		    punkt = ''
     
	       try:
		    try:
			 ter = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['address']['postalCode']
		    except IndexError:
			 ter = grab.doc.select(u'//h1[@class="ds-address-container"]/span[2]').text().split(', ')[1].split(' ')[1]
	       except IndexError:
		    ter =''
     
	       try:
		    try:
		         uliza = grab.doc.rex_text(u'latitude":(.*?),')
		    except IndexError:
			 uliza = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['geo']['latitude']
	       except IndexError:
		    uliza = ''
	       try:
		    try:
		         dom = grab.doc.rex_text(u'longitude":(.*?)}')
		    except IndexError:
			 dom = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['geo']['longitude']
	       except IndexError:
		    dom = ''       
	       try:
		    try:
			 trassa = grab.doc.select(u'//div[@class="ds-overview-section"][2]/div').text()
		    except IndexError:
			 trassa = grab.doc.select(u'//meta[@name="description"]').attr('content')
	       except IndexError:
		    trassa = ''       
	       try:
		    udal = grab.doc.select(u'//span[contains(text(),"Year built:")]/following-sibling::span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    udal = ''
	       try:
		    try:
		         try:
		              pr = grab.doc.select(u'//span[contains(text(),"Total interior livable area:")]').text()
		         except IndexError:
			      pr = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[2]
		    except IndexError:
			 pr = grab.doc.select(u'//h3[@class="ds-bed-bath-living-area-container"]/span[4]').text()
	       except IndexError:
		    pr = '' 
     
	       try:
		    try:
		         opis = grab.doc.select(u'//h3[@class="ds-bed-bath-living-area-container"]/span[1]').text()
		    except IndexError:
			 opis = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[0]
	       except IndexError:
		    opis = ''
	       try:
		    try:
		         try:
		              et = grab.doc.select(u'//span[contains(text(),"Bathrooms:")]').text()
		         except IndexError:
			      et = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[2]').text())['description'].split(', ')[1]
		    except IndexError:
			 et = grab.doc.select(u'//h3[@class="ds-bed-bath-living-area-container"]/button/span').text()
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
		    et3 = []
		    for em in grab.doc.select(u'//picture[@class="media-stream-photo"]/img'):
			 urr = em.attr('src')
			 et3.append(urr)
	       except IndexError:
		    et3 = ''
	       try:
		    et4 = []
		    et44 = []
		    et444 = []
		    ett44 = []
		    for n in grab.doc.select(u'//div[@class="ds-nearby-schools-info-section"]/a'):
			 ur = n.text()
			 et4.append(ur)
		    for gr in grab.doc.select(u'//ul[@class="ds-school-info-section"]/li[1]/span[2]'):
			 urr = gr.text()
			 et44.append(urr)
		    for di in grab.doc.select(u'//ul[@class="ds-school-info-section"]/li[2]/span[2]'):
			 urd = di.text()
			 et444.append(urd)
		    for rt in grab.doc.select(u'//div[@class="ds-school-rating"]/div'):   
			 urt = rt.text()
			 ett44.append(urt)	       
	       except IndexError:
		    et4 = ''	
	       try:
		    et5 = grab.doc.select(u'//span[@class="ds-estimate-value"]').text().replace('None','')
	       except IndexError:
		    et5 = ''
	       try:
		    try:
			 et6 = grab.doc.select(u'//span[contains(text(),"Type:")]/following-sibling::span').text()
		    except IndexError:
			 et6 = json.loads(grab.doc.select(u'//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').text())['@type']
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
		    try:
		         et8 = grab.doc.select(u'//div[contains(text(),"One Year Forecast")]/following-sibling::div/span').text()
		    except IndexError:
			 et8 = grab.doc.rex_text(u'regionForecastRate":"(.*?)"}')
	       except IndexError:
		    et8 = ''
	       try:
		    et9 = grab.doc.select(u'//div[contains(text(),"Time on Zillow")]/following-sibling::div').text()
	       except IndexError:
		    et9 = ''
	       try:
	            et10 = []
		    for s in grab.doc.select(u'//h6[contains(text(),"Similar homes")]/following::div[1]/div/a/div/div/div[2]/div[2]'):
			 urs = s.text()
			 et10.append(urs)
	       except IndexError:
		    et10 = ''
	       try:
		    et11 = grab.doc.select(u'//span[contains(text(),"Heating:")]/following-sibling::span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et11 = ''
	       try:
		    et12 = grab.doc.select(u'//span[contains(text(),"Cooling:")]/following-sibling::span').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et12 = ''
	       try:
		    et13 = grab.doc.select(u'//span[contains(text(),"Parking:")]/following-sibling::span').text().replace('No Data','').replace('None','')
	       except IndexError:
	            et13 = ''	  
	       try:
	            et14 = grab.doc.select(u'//span[contains(text(),"Price/sqft:")]/following-sibling::span').text().replace('No Data','').replace('None','')
	       except IndexError:
	            et14 = ''     
	       try:
		    try:
	                 et15 = grab.doc.select(u'//h4[contains(text(),"Neighborhood:")]').text().split(': ')[1]
		    except IndexError:
			 et15 = grab.doc.rex_text(u'Neighborhood:(.*?)<')
	       except IndexError:
		    et15 = ''
	       try:
		    try:
	                 et16 = grab.doc.select(u'//div[@class="ds-chip"]/div/div[@class="ds-mortgage-row"]/div/span[2]/text()').text()
		    except IndexError:
			 et16 = grab.doc.select(u'//span[contains(text(),"Estimated monthly cost")]/preceding-sibling::h4').text()
	       except IndexError:
	            et16 = ''
	       try:
		    try:
		         et17 = grab.doc.rex_text(u'Major remodel year:(.*?)span')
		    except IndexError:
		         et17 = grab.doc.select(u'//span[contains(text(),"Major remodel year:")]').text()
	       except IndexError:
		    et17 = ''
		    
	       try:
		    try:
	                 et18 = grab.doc.rex_text(u'Appliances included in sale:<!-- -->(.*?)<')
	            except IndexError:
		         et18 = grab.doc.select(u'//span[contains(text(),"Appliances included in sale:")]').text().split(': ')[1]
	       except IndexError:
	            et18 = ''	       
	       #print et18
	       
	       try:
		    try:
			 et19 = grab.doc.rex_text(u'Flooring:<!-- -->(.*?)<')
		    except IndexError:
			 et19 = grab.doc.select(u'//span[contains(text(),"Flooring:")]').text().split(': ')[1]
	       except IndexError:
		    et19 = ''	       
	       #print et19
	       
	       try:
		    try:
			 item20 = grab.doc.rex_text(u'Total interior livable area:<!-- -->(.*?)<')
		    except IndexError:
			 item20 = grab.doc.select(u'//span[contains(text(),"Total interior livable area:")]').text().split(': ')[1]
	       except IndexError:
	            item20 = ''	       
	       #print item20
	       
	       try:
		    try:
			 item21 = grab.doc.rex_text(u'Fireplace:<!-- -->(.*?)<')
		    except IndexError:
			 item21 = grab.doc.select(u'//span[contains(text(),"Fireplace:")]').text().split(': ')[1]
	       except IndexError:
		    item21 = ''	       
	       #print item21
	       
	       try:
		    try:
			 item22 = grab.doc.rex_text(u'Stories:<!-- -->(.*?)<')
	            except IndexError:
			 item22 = grab.doc.select(u'//span[contains(text(),"Stories:")]').text().split(': ')[1]
	       except IndexError:
		    item22 = ''	       
	       #print item22
	       
	       try:
		    try:
			 item23 = grab.doc.rex_text(u'Private pool:<!-- -->(.*?)<')
		    except IndexError:
			 item23 = grab.doc.select(u'//span[contains(text(),"Private pool:")]').text().split(': ')[1]
	       except IndexError:
	            item23 = ''	       
	       #print item23
	       
	       try:
		    try:
			 item24 = grab.doc.rex_text(u'Exterior features:<!-- -->(.*?)<')
		    except IndexError:
			 item24 = grab.doc.select(u'//span[contains(text(),"Exterior features:")]').text().split(': ')[1]
	       except IndexError:
		    item24 = ''
		    
	       try:
	            item25 = grab.doc.select(u'//title').text().split('MLS #')[1].split(' | Zillow')[0]
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
	                   'street': street,
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
	                   'stories': re.sub(u'[^\d]','',item22),
	                   'private pool': item23,
	                   'exterior features': item24,
		           'status': et2,
		           'images': et3,
	                   'appliances': et18.split(', '),
		           'schools': [{'data': {'Grades': et44,'Distance': et444},'name': et4,'rating': ett44}],
		           'url': task.url,
		           'zestimate': et5,
	                   'zpid': 'Z'+re.sub(u'[^\d]','',task.url.split('/')[5]),
		           'timeonzillow': et9,
			   'similarhouses': et10,
			   'neighborhood': et15}
	       
	       yield Task('write',project=projects,grab=grab)
	  
	       
	  def task_write(self,grab,task):
	       
	       #try:
		    #if len(self.db.houses.find_one({"zpid" : task.project['zpid']})['similarhouses']) == 0:
			 #print task.project['similarhouses']
			 #self.db.houses.insert_one({'zpid': task.project['zpid'], 'similarhouses': task.project['similarhouses']})
	       #except TypeError:
		    #pass
	       
	       if task.project['description'] <> '' :
		    if task.project['zpid'] not in self.tobase:
			 print('*'*10)
			 print  task.project['description']
			 print  task.project['zpid'] 
			 print  task.project['mls-id'] 
			 self.lin.append(task.project)
			 print('*'*10)
			 print 'Ready - '+str(len(self.lin))#+'/'+str(self.num)
			 logger.debug('Tasks - %s' % self.task_queue.size()) 
			 print '***',i+1,'/',dc,'***'
			 print('*'*10)
			 
			 if len(self.lin) > 2500:
			      self.stop() 
		    else:
			 print('*'*10)
			 print task.project['zpid'],'<<<IS EXITS!!!>>>'
			 logger.debug('Tasks - %s' % self.task_queue.size()) 
			 print('*'*10)
	       else:
		    print('*'*10)
		    logger.debug('Tasks - %s' % self.task_queue.size()) 
		    print '***',i+1,'/',dc,'***'
		    print('*'*10)
	
     
     bot = Domofond_Com(thread_number=4, network_try_limit=100000000)
     bot.load_proxylist('../tipa.txt','text_file')
     #bot.load_proxylist('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt','url')
     bot.create_grab_instance(timeout=5, connect_timeout=5)
     try:
	  bot.run()
     except KeyboardInterrupt:
	  pass
     print('sleep 2 ...')
     time.sleep(2)    
     print len(bot.lin)
     client = MongoClient(url_base)
     db = client.get_database('landly')
     records = db.zillow
     try:
          records.insert(bot.lin)
     except InvalidOperation:
	  pass
	  #time.sleep(5)
	  #print('Againe')
	  #continue
     client.close()
     print('Record Done!')
     time.sleep(2)     
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  break     

       
     
     
     