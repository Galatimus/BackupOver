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
              self.workbook = xlsxwriter.Workbook(u'Координаты_банки.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"Адрес")
              self.ws.write(0,1, u"LON")
              self.ws.write(0,2, u"LAT")
              self.row= 1
              
       def task_generator(self):
              
              for line in name:
                     num=line.strip()
                     yield Task ('post',url='https://geocode-maps.yandex.ru/1.x/?geocode='+num,num=num,network_try_count=100)
                     
       def task_post(self,grab,task):
                                  
              try:
                     lat= grab.doc.rex_text(u'<pos>(.*?)</pos>').split(' ')[0]
              except (TypeError,KeyError,ValueError,IndexError):
                     lat= ''
                     
              try:
                     lng= grab.doc.rex_text(u'<pos>(.*?)</pos>').split(' ')[1]
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
              
              self.ws.write(self.row, 0, task.project['adres'])
              self.ws.write(self.row, 1, task.project['lat'])
              self.ws.write(self.row, 2, task.project['lng'])              
              
              print 'Ready - '+str(self.row)+'/'+str(nums)
              print 'Tasks - %s' % self.task_queue.size()
              print('*'*50) 
              self.row+= 1              
                     
              #if self.row > 15:
                     #self.stop()                      
              
              
bot = Gis(thread_number=5, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file',proxy_type='http',  timeout=5)
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 2 сек...')
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
#msgbox("ГОТОВО!!!!")
