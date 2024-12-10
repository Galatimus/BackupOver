#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import grab.spider.queue_backend
import grab.spider.queue_backend.memory
import grab.transport
import grab.transport.curl
import logging
import time
from pyproj import Proj, transform
import re
from datetime import datetime
import xlsxwriter
#from easygui import fileopenbox,msgbox,integerbox,ynbox
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logging.basicConfig(level=logging.DEBUG)

#msg = 'Выбирете файл с номерами...'



#try:
       #n3 = fileopenbox(msg=msg, title='', filetypes= ["*.txt"],multiple=False)
       
       #kd = open(n3).read().splitlines()
#except IOError:
       #msgbox("The result is ")
       #exit()
       
#n5 = integerbox("Колличество потоков...1-5:", lowerbound = 1, upperbound = 5)


#n5 = ynbox('Прокси используем?', 'Title', ('Да', 'Нет'))
#if n5 == True:
       #n4 = fileopenbox(msg='Выбирете файл с прокси...', title='', filetypes= ["*.txt"],multiple=False)
#else:
       #n4=''
       
name =open('nums.txt').read().splitlines()
for li in name:
       nums=len(name)       
class Gis(Spider):
       
       #initial_urls=['https://2gis.ru/countries/global/']
       def prepare(self):
              #self.rb = xlrd.open_workbook(name+'.xlsx')
              #self.sheet = self.rb.sheet_by_index(1)
              self.workbook = xlsxwriter.Workbook(u'Кадастровые_номера_'+datetime.today().strftime('%d.%m.%Y')+'_.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"Кадастровый номер")
              self.ws.write(0,1, u"Статус")
              self.ws.write(0,2, u"Дата постановки на кадастровый учет")
              self.ws.write(0,3, u"Разрешенное использование")
              self.ws.write(0,4, u"Площадь:м2")
              self.ws.write(0,5, u"Форма собственности")
              self.ws.write(0,6, u"Кадастровая стоимость:ру.")
              self.ws.write(0,7, u"Дата обновления границ")
              self.ws.write(0,8, u"Местоположение)")
              self.ws.write(0,9, u"Дата опубликования на ПКК")
              self.ws.write(0,10, u"Кадастровый инженер")
              self.ws.write(0,11, u"Долгота")
              self.ws.write(0,12, u"Широта")              
              self.ws.write(0,13, u"Ссылка на сайт")
              self.ws.write(0,14, u"Дата парсинга")              
              self.inProj = Proj(init='epsg:3857')
              self.outProj = Proj(init='epsg:4326')             
              self.row= 1
              
       def task_generator(self):
              for line in name:
                     num=re.sub(r'(?<=:)0*','',line.strip())
                     yield Task ('post',url='http://pkk5.rosreestr.ru/api/features/1/'+num,refresh_cache=True,network_try_count=100,use_proxylist=False)
                     
       def task_post(self,grab,task):
              try:
                     nomer = grab.response.json["feature"]['attrs']['cn']
              except (ValueError,TypeError):
                     nomer =''              
              
              try:
                     status = grab.response.json["feature"]['attrs']['statecd']
              except (ValueError,TypeError):
                     status =''
              try:
                     data = grab.response.json["feature"]['attrs']['date_create']
              except (ValueError,TypeError):
                     data =''                      
              try:
                     cat = grab.response.json['feature']['attrs']['util_by_doc']
              except (ValueError,TypeError):
                     cat =''                      
              try:
                     plosh = grab.response.json["feature"]['attrs']['area_value']
              except (ValueError,TypeError):
                     plosh =''
              try:
                     kod = grab.response.json["feature"]['attrs']['fp']
              except (ValueError,TypeError):
                     kod =''                     
                     
             
              try:
                     data_ut = grab.response.json["feature"]['attrs']['adate']
              except (ValueError,TypeError):
                     data_ut =''
              try:
                     adres = grab.response.json['feature']['attrs']['address']
              except (ValueError,TypeError):
                     adres =''
                     
              try:
                     cena = grab.response.json["feature"]['attrs']['cad_cost']
              except (ValueError,TypeError):
                     cena =''                     
              try:
                     data_ob = grab.response.json["feature"]['attrs']['pubdate']
              except (ValueError,TypeError):
                     data_ob =''
              try:
                     try:
                            ingener = grab.response.json['feature']['attrs']['cad_eng_data']['ci_surname']
                     except (TypeError,KeyError,ValueError):
                            ingener = grab.response.json['feature']['attrs']['cad_eng_data']['co_name']
              except (TypeError,KeyError,ValueError):
                     ingener =''
                     
              try:
                     y = grab.response.json["feature"]['center']['y']
                     x = grab.response.json["feature"]['center']['x']
                     lat,lng = transform(self.inProj,self.outProj,x,y)
              except (TypeError,KeyError,ValueError):
                     lat =''                     
                     lng =''
                     
              projects = {'nomer': nomer,
                          'status': status,
                          'url': task.url,
                          'data': data,
                          'category': cat,
                          'ploshad': plosh,
                          'forma': kod,
                          'price': cena,
                          'data1': data_ut,
                          'adress': adres,
                          'data2': data_ob,
                          'fio':ingener,
                          'lat': lat,
                          'lng':lng}
                            #'gaz': gaz,
                            #'voda': voda,
                            #'kanaliz': kanal,
                            #'electr': elek,
                            #'teplo': teplo,
                            #'opis':opis,
                            #'phone':phone}
             
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
              if task.project['nomer'] <> '':
                     
                     print('*'*50)
                     print  task.project['nomer']
                     print  task.project['status']
                     print  task.project['data']
                     print  task.project['category']
                     print  task.project['ploshad']
                     print  task.project['forma']
                     print  task.project['price']
                     print  task.project['data1']
                     print  task.project['adress']
                     print  task.project['data2']
                     print  task.project['fio']
                     print  task.project['lat']
                     print  task.project['lng']              
                     
                     
                     self.ws.write(self.row, 0, task.project['nomer'])
                     self.ws.write(self.row, 1, task.project['status'])
                     self.ws.write(self.row, 2, task.project['data'])
                     self.ws.write(self.row, 3, task.project['category'])
                     self.ws.write(self.row, 4, task.project['ploshad'])
                     self.ws.write(self.row, 5, task.project['forma'])
                     self.ws.write(self.row, 6, task.project['price'])
                     self.ws.write(self.row, 7, task.project['data1'])
                     self.ws.write(self.row, 8, task.project['adress'])
                     self.ws.write(self.row, 9, task.project['data2'])
                     self.ws.write(self.row, 10, task.project['fio'])
                     self.ws.write(self.row, 11, task.project['lat'])
                     self.ws.write(self.row, 12, task.project['lng'])
                     self.ws.write_string(self.row, 13, task.project['url']) 
                     self.ws.write(self.row, 14, datetime.today().strftime('%d.%m.%Y')) 
                     print('*'*50)
                     print 'Ready - '+str(self.row)+'/'+str(nums)
                     print 'Tasks - %s' % self.task_queue.size()
                     print('*'*50) 
                     self.row+= 1              
                     
                     #if self.row > 5:
                            #self.stop()                      
              
              
bot = Gis(thread_number=2, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Pars/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 2 сек...')
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')

