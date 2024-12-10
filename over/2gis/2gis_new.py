#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
#from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
import xlrd
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

name ='0616'

class Gis(Spider):
       
       #initial_urls=['https://2gis.ru/countries/global/']
       
       def prepare(self):
              self.rb = xlrd.open_workbook(name+'.xlsx',on_demand=True)
              self.sheet = self.rb.sheet_by_index(0)
              self.workbook = xlsxwriter.Workbook(name+' tip'+'.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"Тип объекта")
              self.row= 1
              
       def task_generator(self):
              yield Task ('post',url='https://2gis.ru/countries/global/',network_try_count=100)
                                          
       def task_post(self,grab,task):
              for ul in range(1,self.sheet.nrows):
                     punkt= self.sheet.cell_value(ul,3)#.replace(', ',',')
                     uliza= self.sheet.cell_value(ul,5)#.replace(', ',',')
                     dom= str(self.sheet.cell_value(ul,6)).replace('.0','')#.replace(' ','')
                     try:
                            try:
                                   pg = grab.doc.select(u'//header[@class="world__sectionHeader"]/following-sibling::ul/li/h2/a[contains(text(),"'+punkt+'")]')
                                   url_gis=re.sub(r'\s+', ' ', pg.attr('href')+'/search/'+uliza+' '+dom)
                                   print url_gis
                                   yield Task ('save',url= url_gis,refresh_cache=True,network_try_count=100)
                            except IndexError:
                                   pg1 = grab.doc.select(u'//header[@class="world__sectionHeader"]/following-sibling::ul/li/h2/following-sibling::ul/li[contains(text(),"'+punkt+'")]/preceding::h2[1]/a')
                                   url_gis1= re.sub(r'\s+', ' ',pg1.attr('href')+'/search/'+punkt+' '+uliza+' '+dom)
                                   print url_gis1                                   
                                   yield Task ('save',url= url_gis1,refresh_cache=True,network_try_count=100)
                     except IndexError:
                            yield Task ('save',grab=grab,refresh_cache=True,network_try_count=100)
                      
                                                 
       def task_save(self,grab,task):
              try:
                     tip_zd= grab.doc.select(u'//div[@class="miniCard__desc"]/following-sibling::div[@class="miniCard__additional"]').text()
              except IndexError:
                     tip_zd=''
                     
                     
              self.ws.write(self.row, 0, tip_zd)
              print('*'*50)
              print task.url
              print tip_zd
              print self.row,'/',self.sheet.nrows
              logger.debug('Tasks - %s' % self.task_queue.size())
              
              print('*'*50)
              self.row+=1
                     
             
              
bot = Gis(thread_number=5, network_try_limit=100000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
#bot.initial_urls=['https://2gis.ru/countries/global/']
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 2 сек...')
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
