#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import grab.spider.queue_backend
import grab.spider.queue_backend.memory
import grab.transport
import grab.transport.curl
import logging
import time
import re
from datetime import datetime
import xlsxwriter
#from easygui import fileopenbox,msgbox,integerbox,ynbox
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logging.basicConfig(level=logging.DEBUG,format=' %(message)s')


name =open('adres.txt').read().splitlines()
for li in name:
       nums=len(name)       
class Gis(Spider):
       
       #initial_urls=['https://2gis.ru/countries/global/']
       def prepare(self):
              #self.rb = xlrd.open_workbook(name+'.xlsx')
              #self.sheet = self.rb.sheet_by_index(1)
              self.workbook = xlsxwriter.Workbook(u'Координаты_'+datetime.today().strftime('%d.%m.%Y')+'_.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"Адрес")
              self.ws.write(0,1, u"LON")
              self.ws.write(0,2, u"LAT")
              self.row= 1
              
       def task_generator(self):
              
              for line in name:
                     num=line.strip()
                     yield Task ('post',url='https://maps.google.com/maps/api/geocode/json?address='+num+'&sensor=false',num=num,network_try_count=100)
                     
       def task_post(self,grab,task):
                                  
              try:
                     try:
                            try:
                                   lat = grab.response.json["results"][0]["geometry"]["location"]["lat"]
                            except (TypeError,KeyError,ValueError,IndexError):
                                   lat= grab.response.json["results"][0]["geometry"]["viewport"]["southwest"]["lat"]
                     except (TypeError,KeyError,ValueError,IndexError):
                            lat= grab.response.json["results"][0]["geometry"]["viewport"]["northeast"]["lat"]
              except (TypeError,KeyError,ValueError,IndexError):
                     lat= ''
                     
              try:
                     try:
                            try:
                                   lng = grab.response.json["results"][0]["geometry"]["location"]["lng"]
                            except (TypeError,KeyError,ValueError,IndexError):
                                   lng= grab.response.json["results"][0]["geometry"]["viewport"]["southwest"]["lng"]
                     except (TypeError,KeyError,ValueError,IndexError):
                            lng= grab.response.json["results"][0]["geometry"]["viewport"]["northeast"]["lng"]
              except (TypeError,KeyError,ValueError,IndexError):
                     lng= ''
                     
              projects = {'adres': task.num,
                          'lat': lat,
                          'lng':lng}
                          
             
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
             
              print('*'*50)
              print  task.project['adres']
              print  task.project['lat']
              print  task.project['lng']              
              
              
              #self.ws.write(self.row, 0, task.project['nomer'])
              #self.ws.write(self.row, 1, task.project['status'])
              #self.ws.write(self.row, 2, task.project['data'])
              #self.ws.write(self.row, 3, task.project['category'])
              #self.ws.write(self.row, 4, task.project['ploshad'])
              #self.ws.write(self.row, 5, task.project['forma'])
              #self.ws.write(self.row, 6, task.project['price'])
              #self.ws.write(self.row, 7, task.project['data1'])
              #self.ws.write(self.row, 8, task.project['adress'])
              #self.ws.write(self.row, 9, task.project['data2'])
              #self.ws.write(self.row, 10, task.project['fio'])
              #self.ws.write(self.row, 11, task.project['lat'])
              #self.ws.write(self.row, 12, task.project['lng'])
              #self.ws.write(self.row, 13, task.project['gaz'])
              #self.ws.write_string(self.row, 14, task.project['url']) 
              #self.ws.write(self.row, 15, datetime.today().strftime('%d.%m.%Y')) 
              #print('*'*50)
              print 'Ready - '+str(self.row)+'/'+str(nums)
              print 'Tasks - %s' % self.task_queue.size()
              print('*'*50) 
              self.row+= 1              
                     
                     #if self.row > 15:
                            #self.stop()                      
              
              
bot = Gis(thread_number=1, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file',proxy_type='http',  timeout=5)
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 2 сек...')
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
#msgbox("ГОТОВО!!!!")
