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
from geopy.distance import geodesic
import json
import collections
import math
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



i = 190
l= open('../city.txt').read().splitlines()
dc = len(l)
page = l[i]

url_base = 'mongodb://oleg:walter2005@cluster0-shard-00-00-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-01-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-02-cfwsy.gcp.mongodb.net:27017/landly?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'

#url_base = 'mongodb://127.0.0.1:27017'


while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class Domofond_Com(Spider):
	  def prepare(self):
	       self.link = 'https://www.trulia.com/'+page.split(',')[1]+'/'+page.split(',')[0].replace(' ','_')+'/'
	       self.lin = []
	       self.tobase = []	
	       self.dubl = []
	       print 'Request to base ...'
	       self.client = MongoClient(url_base)
	       self.db = self.client.landly
	       for entry in self.db.trulia.find():
		    self.tobase.append(entry["tpid"])
	       print 'Records IS :',str(len(self.tobase)),'>>',str(len(list(set(self.tobase))))
	       self.dubl = [item for item, count in collections.Counter(self.tobase).items() if count > 1]
               print 'duplicate is >>',len(self.dubl)
	       self.dubl.sort()
	       for i in range(len(self.dubl)):
		    print str(self.dubl[i]) + ' is a duplicate',str(i),'/',str(len(self.dubl))
		    self.db.trulia.delete_one({'tpid': self.dubl[i]})
		    self.tobase.remove(self.dubl[i])
	       print 'Records NEW IS :',str(len(self.tobase))
	       self.client.close
	       time.sleep(2)
	       for p in range(1,51):
		    try:
			 time.sleep(2)
			 g = Grab(timeout=20, connect_timeout=50)
			 g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
			 #g.proxylist.load_url('http://127.0.0.1:24000')
			 g.go(self.link)
			 try:
			      self.num = re.sub('[^\d]','',g.doc.select(u'//h1/following-sibling::h2').text())
			 except IndexError:
			      self.num = re.sub('[^\d]','',g.doc.select(u'//meta[@name="description"]').attr('content').split(', ')[0])
			 self.pag = int(math.ceil(float(int(self.num))/float(30)))
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
		    yield Task ('post',url=self.link+str(x)+'_p/',refresh_cache=True,network_try_count=10000000)
	       #yield Task ('post',url=self.link,refresh_cache=True,network_try_count=100)
	
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//div[@data-testid="home-card-sale"]/a'):
		    yield Task('item', url=grab.make_url_absolute(elem.attr('href')),refresh_cache=True, network_try_count=10000000)


	
	  def task_item(self, grab, task):
	       try:
		    sub = grab.doc.select(u'//title').text().split(', ')[0]
	       except IndexError:
		    sub = ''
	       try:
		    ray =  json.loads(grab.doc.select(u'//script[@data-testid="hdp-seo-residence-schema"]').text())['address']['addressLocality']
		    #print ray
	       except (IndexError,KeyError,TypeError):
		    ray = ''
	       try:
		    punkt= json.loads(grab.doc.select(u'//script[@data-testid="hdp-seo-residence-schema"]').text())['address']['addressRegion']
	       except (IndexError,KeyError,TypeError):
		    punkt = ''
     
	       try:
		    ter = json.loads(grab.doc.select(u'//script[@data-testid="hdp-seo-residence-schema"]').text())['address']['postalCode']
	       except (IndexError,KeyError,TypeError):
		    ter =''
     
	       try:
		    uliza = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['location']['coordinates']['latitude']
	       except (IndexError,KeyError,TypeError):
		    uliza = ''
	       try:
		    dom = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['location']['coordinates']['longitude']
	       except (IndexError,KeyError,TypeError):
		    dom = ''       
	       try:
		    trassa = grab.doc.select(u'//div[@data-testid="home-description-text-description-text"]/div/p').text()
	       except IndexError:
		    trassa = ''       
	       try:
		    udal = grab.doc.select(u'//li[contains(text(),"Built in")]').text()
	       except IndexError:
		    udal = ''
		    
	       try:    
		    pr = grab.doc.select(u'//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"sqft")]').text()
	       except IndexError:
		    pr = '' 
	  
	       try:
	            opis = grab.doc.select(u'//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"Beds")]').text()
	       except IndexError:
		    opis = ''
	       try:
	            et = grab.doc.select(u'//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"Baths")]').text()
	       except IndexError:
		    et = ''
	       try:
		    et1 = grab.doc.select(u'//h3[@data-testid="on-market-price-details"]/div').text()
	       except IndexError:
		    et1 = ''
	       try:
		    et2 = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['_page']['tracking']['listingStatus']
	       except (IndexError,KeyError,TypeError):
		    et2 = ''
	       try:
		    et3 = re.findall(r'largeSrc":"(.*?)"',grab.doc.body)
	       except IndexError:
		    et3 = ''
	       try:
		    et4 = []
		    et44 = []
		    et444 = []
		    ett44 = []
		    origin = (uliza, dom)
		    for n in json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['assignedSchools']['schools']:
                         et4.append(n['name'])
		    for gr in json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['assignedSchools']['schools']:
			 et44.append(gr['gradesRange'])
		    for di in json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['assignedSchools']['schools']:
			 dist = (di['latitude'], di['longitude'])
			 et444.append(str(round(geodesic(origin, dist).miles,2))+'mi')
		    for rt in json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['assignedSchools']['schools']:   
			 ett44.append(str(rt['providerRating']['rating'])+'/'+str(rt['providerRating']['maxRating'])) 
	       except (IndexError,KeyError,TypeError):
		    et4 = ''	
	       #try:
		    #et5 = grab.doc.select(u'//div[@data-testid="summary-mortgage-estimate"]').text().replace('None','')
	       #except IndexError:
	       et5 = ''
	       try:
		    et6 = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['_page']['tracking']['propertyType']
	       except (IndexError,KeyError,TypeError):
		    et6 =''
	       try:
		    try:
			 et7 = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['_page']['branchBanner']['bannerViewData']['data']['floorSpace']
		    except (IndexError,KeyError,TypeError):
			 et7 = grab.doc.select(u'//li[contains(text(),"Lot Size:")]').text().split(': ')[1]
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
		    et9 = grab.doc.select(u'//li[contains(text(),"Days on Trulia")]').text().replace(' on Trulia','')
	       except IndexError:
		    et9 = ''
	       try:
		    et10 = []
		    for s in json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['homeDetails']['similarHomes']['homes']:
			 et10.append(s['location']['fullLocation'])
	       except (IndexError,KeyError,TypeError):
		    et10 = ''
	       try:
		    et11 = grab.doc.select(u'//li[contains(text(),"Heating")]').text().split(': ')[1].replace('No Data','').replace('None','')
	       except IndexError:
		    et11 = ''
	       try:
		    et12 = grab.doc.select(u'//li[contains(text(),"Cooling System")]').text().split(': ')[1].replace('No Data','').replace('None','')
	       except IndexError:
		    et12 = ''
	       try:
		    et13 = grab.doc.select(u'//li[contains(text(),"Parking")]').text().split(': ')[1].replace('No Data','').replace('None','')
	       except IndexError:
		    et13 = ''	  
	       try:
		    et14 = grab.doc.select(u'//li[contains(text(),"/sqft")]').text().replace('No Data','').replace('None','')
	       except IndexError:
		    et14 = ''     
	       try:
		    try:
			 et15 = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['_page']['tracking']['listingNeighborhood']
		    except (IndexError,KeyError,TypeError):
			 et15 = grab.doc.rex_text(u'neighborhood":"(.*?)"')
	       except IndexError:
		    et15 = ''
	       #try:
		    #et16 = grab.doc.rex_text(u'rent for (.*?).')
	       #except IndexError:
	       et16 = ''
	       try:
		    et17 = grab.doc.select(u'//li[contains(text(),"Year Updated")]').text().split(': ')[1].replace('No Data','').replace('None','')
	       except IndexError:
	            et17 = ''
	  
	       try:
		    et18 = grab.doc.select(u'//li[contains(text(),"Floors")]').text().split(': ')[1]
	       except IndexError:
		    et18 = ''	       
	       #print et18
	  
	       try:
		    et19 = grab.doc.select(u'//li[contains(text(),"Pool")]').text().replace('Pool','yes')
	       except IndexError:
		    et19 = ''	       
	       #print et19
	  
	       try:
		    item20 = pr
	       except IndexError:
		    item20 = ''	       
	       #print item20
	  
	       try:
		    item21 = grab.doc.select(u'//li[contains(text(),"Fireplace")]').text().replace('Fireplace','yes')
	       except IndexError:
		    item21 = ''	       
	       #print item21
	  
	       try:
		    item22 = grab.doc.select(u'//li[contains(text(),"Stories:")]').text().split(': ')[1]
	       except IndexError:
		    item22 = ''	       
	       #print item22
	  
	       try:
		    try:
		         item23 = re.sub(u'[^\d]','',grab.doc.rex_text(u'listingID(.*?)maloneID'))
		    except IndexError:
			 item23 = json.loads(grab.doc.select(u'//script[@id="__NEXT_DATA__"]').text())['props']['_page']['tracking']['listingID']
	       except (IndexError,KeyError,TypeError):
	            item23 = ''

	  
	       try:
		    item24 = grab.doc.select(u'//h3[contains(text(),"Interior Features")]/following-sibling::li').text()
	       except IndexError:
		    item24 = ''
	  
	       try:
		    item25 = grab.doc.select(u'//title').text().split('MLS# ')[1].split(' - ')[0].replace(' | Trulia','')
	       except IndexError:
		    item25 = ''
		    
		    

     
	      
	       
	       temp = {'atAGlanceFacts':[]} 
	  
	       temp['atAGlanceFacts'].append({'factLabel': 'Year built','factValue': re.sub(u'[^\d]','',udal)})
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
		           'lat': str(uliza),
		           'lon': str(dom),
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
		           'flooring': '',
		           'total-interior-livable-area': item20,
		           'fireplace': item21,
		           'stories': item22,
		           'private pool': et19,
		           'exterior features': item24,
		           'status': et2,
		           'images': et3,
		           'appliances': et18.split(', '),
		           'schools': [{'data': {'Grades': et44,'Distance': et444},'name': et4,'rating': ett44}],
		           'url': task.url,
		           'zestimate': et5,
		           'tpid': 'T'+item23,
		           'timeontrulia': et9,
		           'similarhouses': et10,
		           'neighborhood': et15}
	       
	       yield Task('write',project=projects,grab=grab)
	  
	       
	  def task_write(self,grab,task):
	       if task.project['description'] <> '' :
		    if task.project['tpid'] not in self.tobase:
			 print('*'*10)
			 print  task.project['description']
			 print  task.project['tpid'] 
			 print  task.project['mls-id']
			 print  task.project['neighborhood']
			 self.lin.append(task.project)
			 print('*'*10)
			 print 'Ready - '+str(len(self.lin))+'/'+str(self.num)
			 logger.debug('Tasks - %s' % self.task_queue.size()) 
			 print '***',i+1,'/',dc,'***'
			 print('*'*10)
		    else:
			 print('*'*10)
			 print task.project['tpid'],'<<<IS EXITS!!!>>>'
			 logger.debug('Tasks - %s' % self.task_queue.size())
			 print('*'*10) 	       
	       else:
		    print('*'*10)
		    logger.debug('Tasks - %s' % self.task_queue.size()) 
		    print '***',i+1,'/',dc,'***'
		    print('*'*10)	
     
     bot = Domofond_Com(thread_number=4, network_try_limit=100000000)
     bot.load_proxylist('../ivan.txt','text_file')
     #bot.load_proxylist('http://127.0.0.1:24000','url',proxy_type='http',auto_change = False)
     #bot.create_grab_instance(timeout=5, connect_timeout=5)
     try:
	  bot.run()
     except KeyboardInterrupt:
	  pass
     print('sleep 2 ...')
     time.sleep(2)    
     print len(bot.lin)
     client = MongoClient(url_base)
     db = client.landly
     records = db.trulia 
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

       
     
     
     