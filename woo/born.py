#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
from woocommerce import API
import json,codecs
#from googletrans import Translator
from mtranslate import translate
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Bornpretty.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
          
	  #self.wcapi = API(
	       #url='http://192.168.1.4/waltershop/',
	       #consumer_key='ck_7684ba7bd2b7666985eaa0ebc8aec7ab8560fe0d',
	       #consumer_secret='cs_60bf49fc1e3cfde2244dc90fc0a10dc278556d64',    
	       #wp_api=True,
	       #version="wc/v3",
	       ##query_string_auth=True,
	       #timeout=3000
	       #)
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Имя")
	  self.ws.write(0, 1, u"Описание")
	  self.ws.write(0, 2, u"Категории")
	  self.ws.write(0, 3, u"Изображения")
	  self.ws.write(0, 4, u"Базовая цена")
	  self.ws.write(0, 5, u"Артикул")
	  self.ws.write(0, 6, u"Цвет")
	  self.ws.write(0, 7, u"Объем")
	  self.ws.write(0, 8, u"Количество")
	  self.ws.write(0, 9, u"Тип Товара")

	       
	  self.result= 1
	  #self.trans= Translator(service_urls=['translate.google.com', 'translate.google.co.kr'], user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0', proxies=None, timeout=300)
	
	       
    
     def task_generator(self):
	  for x in range(1,29):
               yield Task ('post',url='https://www.bornprettystore.com/show.php?page=%d'%x,refresh_cache=True,network_try_count=100)


	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//p[@class="p1"]/preceding-sibling::a'):
	       ur = grab.make_url_absolute(elem.attr('href')) 
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)	       
                
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//p[@class="p1"]').text().replace('BORN PRETTY ','')
	  except IndexError:
	       sub = ''
	  try:
               ray = ' '.join([ t for t in  grab.doc.select(u'//div[@class="description_frame"]').html().split(' ') if t ])
	       #ray = grab.doc.select(u'//div[@class="description_frame"]').html()
	  except IndexError:
	       ray = ''
	  try:
	       try:
	            punkt= re.findall(u'Color: (.*?)<',ray)[0]
	       except IndexError:
		    punkt= re.findall(u'Color:(.*?)<',ray)[0]
	  except IndexError:
	       punkt = 'As the pictures show'
	       
	  try:
	       try:
		    try:
			 try:
	                      ob= re.findall(u'Capacity: (.*?)<',ray)[0]
			 except IndexError:
			      ob= re.findall(u'Volume:(.*?)<',ray)[0]
		    except IndexError:
			 ob= re.findall(u'Capacity:(.*?)<',ray)[0]
	       except IndexError:
		    ob= re.findall(u'Volume: (.*?)<',ray)[0]
          except IndexError:
	       ob = ''
	       
	  try:
	       try:
	            quin = re.findall(u'Quantity: (.*?)<',ray)[0]
	       except IndexError:
		    quin = re.findall(u'Quantity:(.*?)<',ray)[0]
	  except IndexError:
	       quin = ''
	       
	  try:
	       try:
	            tip = re.findall(u'Type: (.*?)<',ray)[0]
	       except IndexError:
		    tip = re.findall(u'Type:(.*?)<',ray)[0]
	  except IndexError:
	       tip = ''	  
	       
	  try:
	       art= re.sub(u'[^\d]','',grab.doc.select(u'//p[@class="p2 productid"]').text())
	  except IndexError:
	       art = ''	  
	  
	  try:
	       udal = grab.doc.select(u'//p[@class="p4"]/span[1]').text().replace('USD $','')
	  except IndexError:
	       udal = ''
	       
	  try:
	       shot = grab.doc.select(u'//div[@id="pro_detail"]/p').text().split('>')
	       shot.pop()
	  except IndexError:
	       shot = ''
	       
	  lin = []
	  for em in grab.doc.select(u'//div[@id="showArea"]/a'):
	       urr = em.attr('rel').split('!')[0].replace(':8443','')
	       lin.append(urr)  
          #try:
	       #ob = translate(ob,"ru","auto")
	  #except KeyError:
	       #ob = ''
	  #try:
	       #punkt = translate(punkt,"ru","auto")
	  #except KeyError:
	       #punkt = ''
	  #try:
	       #quin = translate(quin,"ru","auto")
	  #except KeyError:
	       #quin = ''
	  #try:
	       #tip = translate(tip,"ru","auto")
	  #except KeyError:
	       #tip = ''

    
	  projects = {'name': sub,
	              'description': re.sub('<[^<]+?>', '', ray),
	              'price': str(round(float(udal),2)*120),
	              'productid': art,
	              'color': punkt,
	              'obem': ob,
	              'col': quin,
	              'images':lin,
	              'category':'>'.join(shot).replace('BORN PRETTY > ','').replace('BP ','').replace(' & ',' ').lower(),
	              'type': tip,
	              'category_id': self.result} 
   
	   
	  
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
	  
     def task_write(self,grab,task):
	  print('*'*50)
	  #parent = task.project['category'].split(' > ')[0].strip()
	  #try:
	       #child = task.project['category'].split(' > ')[1].strip()
	  #except IndexError:
	       #child = ''
	       
	  #categories = self.wcapi.get("products/categories").json()
	  #cat_categories = [x for x in categories if x['name'] == parent]
	  #parent_id = None
	  #if not cat_categories:        
	       #try:
		    #response = self.wcapi.post("products/categories", {'name': parent})
		    #parent_id = response.json()['id']
	       #except KeyError:
	            #print 'no'
		    #pass
	       #print 'Create new parent category...is', parent_id
	  #else:
	       #parent_id = cat_categories[0]['id']    
	       #print 'parent Category...is',parent_id,' - ',parent 
	       
	  #if  child <>'':
	       #child_categories = [x for x in self.wcapi.get("products/categories").json() if x['name'] == child]
	       #child_id = None
	       #if not child_categories:        
		    #try:
			 #resp = self.wcapi.post("products/categories", {'name': child,'parent': parent_id})
			 #child_id = resp.json()['id']
		    #except KeyError:
			 #print 'no'
			 #pass
		    #print 'Create new child category...is', child_id
	       #else:
		    #child_id = child_categories[0]['id']    
		    #print 'child Category...is',child_id,' - ',child	  
	  
	  #else:
	       #child_id = parent_id
	  
	  #color_names = ['Orange', 'Brown', 'Black', 'White']
	       
	  #data = {}
	  #data = {
               #"name": task.project['name'],
               #"type": "simple",
               #"regular_price": task.project['price'],
               #"description": task.project['description'],
               ##"short_description": task.project['shotd'],
               #"categories": [{"id": child_id}],
	       #"sku": task.project['productid'],
	       ##"variations": [variation_data[1]],
               ##"weight": color,
               ##"length": sz,
               ##"width": strana,
               ##"height": sez,
               #"images": [{"src": task.project['images'][i]} for i in range(len(task.project['images']))],
               #'attributes' : [
                              #{'name' : 'Цвет','position' : 0,'visible' : True,'variation' : True,'options' : task.project['color']},
                              #{'name': 'Объем','position' : 0,'visible' : True,'variation' : True,'options' : task.project['obem']},
                              #{'name': 'Количество','position' : 0,'visible' : True,'variation' : True,'options' : task.project['col']},
                              #{'name': 'Тип','position' : 0,'visible' : True,'variation' : True,'options' : task.project['type']},
               ###{'name': 'Страна производства','position' : 0,'visible' : True,'variation' : True,'options' : strana},
               #]               
          #}	  
	       
	  print  task.project['name']
	  print  task.project['productid']
	  #print  task.project['description']
	  print  task.project['price']
	  print task.project['images']
	  print  task.project['category'].strip()
	  print  task.project['color']
	  print  task.project['obem']
	  print  task.project['col']
	  print  task.project['type']
	  #print(self.wcapi.post("products",data).json())
	  #time.sleep(5)
	  #r = self.wcapi.post("products",data)
	  #r.json()

	  self.ws.write(self.result, 0, task.project['name'])
	  self.ws.write_string(self.result, 1, task.project['description'])
	  self.ws.write(self.result, 2, task.project['category'].strip())
	  self.ws.write_string(self.result, 3, '|'.join(task.project['images']))
	  self.ws.write(self.result, 4, task.project['price'])
	  self.ws.write(self.result, 5, task.project['productid'])
	  self.ws.write_string(self.result, 6, task.project['color'])
	  self.ws.write_string(self.result, 7, task.project['obem'])
	  self.ws.write_string(self.result, 8, task.project['col'])
	  self.ws.write_string(self.result, 9, task.project['type'])
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)+' ****** '#+'Status is : '+str(r.status_code)
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)	       
	  self.result =self.result+1

	  
	 

     
bot = Cian_Zem(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('../ivan.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
try:
     bot.run()
except KeyboardInterrupt:
     pass
workbook.close()
print('Done!') 







