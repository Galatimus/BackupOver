#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import grab.spider.queue_backend
import grab.spider.queue_backend.memory
import grab.transport
import grab.transport.curl
import grab
import logging
from rosreestr import vid,cat,stat
import time
from pyproj import Proj, transform
import pyproj
import re
import xlrd
from datetime import datetime
import xlsxwriter
from easygui import fileopenbox,msgbox
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logging.basicConfig(level=logging.DEBUG)

name = fileopenbox(msg='Столбец-1, Лист-1', title='Выберите файл с номерами', filetypes= ["*.xlsx"])
if name ==None:
       sys.exit(0)
       

class Gis(Spider):
       
      
       def prepare(self):
              print u'Продолжаем...'
              
              self.rb = xlrd.open_workbook(name,on_demand=True)
              self.sheet = self.rb.sheet_by_index(0)
              self.workbook = xlsxwriter.Workbook(u'Кадастровые_номера_'+datetime.today().strftime('%d.%m.%Y')+'_.xlsx')
              self.ws = self.workbook.add_worksheet()
             
              self.ws.write(0,0, u"Кадастровый номер")
              self.ws.write(0,1, u"Статус")
              self.ws.write(0,2, u"Дата постановки на кадастровый учет")
              self.ws.write(0,3, u"Вид разрешенного использования")
              self.ws.write(0,4, u"Площадь:м2")
              self.ws.write(0,5, u"Вид разрешенного использования по документу")
              self.ws.write(0,6, u"Кадастровая стоимость:ру.")
              self.ws.write(0,7, u"Дата утверждения стоимости")
              self.ws.write(0,8, u"Адрес (местоположение)")
              self.ws.write(0,9, u"Дата опубликования на ПКК")
              self.ws.write(0,10, u"Кадастровый инженер")
              self.ws.write(0,11, u"Долгота")
              self.ws.write(0,12, u"Широта")
              self.ws.write(0,13, u"Категория земель")
              self.ws.write(0,14, u"URL")
              self.ws.write(0,15, u"Дата парсинга")
              self.ws.write(0,16, u"Номера файла") 
              
              
              self.inProj = pyproj.Proj(init='epsg:3857')
              #raw_input()
              self.outProj = pyproj.Proj(init='epsg:4326')
             
              self.row= 1
              
              
       def task_generator(self):
              for ul in range(1,self.sheet.nrows):                    
                     num = re.sub(r'(?<=:)0*','',self.sheet.cell_value(ul,0)).replace('::',':0:')
                     nums = self.sheet.cell_value(ul,0)
                     yield Task ('post',url='http://pkk5.rosreestr.ru/api/features/1/'+num,nums=nums,refresh_cache=True,network_try_count=100)              

                     
       def task_post(self,grab,task):
              try:
                     nomer = grab.response.json["feature"]['attrs']['cn']
              except (ValueError,TypeError):
                     nomer =''              
              
              try:
                     st = grab.response.json["feature"]['attrs']['statecd']
                     status = reduce(lambda st, r1: st.replace(r1[0], r1[1]), stat, st)
              except (ValueError,TypeError):
                     status =''
              try:
                     data = grab.response.json["feature"]['attrs']['date_create']
              except (ValueError,TypeError):
                     data =''                      
              try:
                     c = grab.response.json["feature"]['attrs']['util_code']
                     categ = reduce(lambda c, r2: c.replace(r2[0], r2[1]), vid, c)
              except (ValueError,TypeError,AttributeError):
                     categ =''                      
              try:
                     plosh = grab.response.json["feature"]['attrs']['area_value']
              except (ValueError,TypeError):
                     plosh =''
              try:
                     kod = grab.response.json["feature"]['attrs']['util_by_doc']
              except (ValueError,TypeError):
                     kod =''                     
                     
             
              try:
                     data_ut = grab.response.json["feature"]['attrs']['date_cost']
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
                     z = grab.response.json["feature"]['attrs']['category_type']
                     gaz = reduce(lambda z, r3: z.replace(r3[0], r3[1]), cat, z)
              except (TypeError,KeyError,ValueError):
                     gaz =''
                     
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
                          'category': categ,
                          'ploshad': plosh,
                          'forma': kod,
                          'price': cena,
                          'data1': data_ut,
                          'adress': adres,
                          'data2': data_ob,
                          'fio':ingener,
                          'lat': lat,
                          'lng':lng,
                          'gaz': gaz,
                          'fnums':task.nums}
                       
             
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
              #if task.project['nomer'] <> '':             
              #print('*'*50)
              #print  task.project['nomer']
              #print  task.project['status']
              #print  task.project['data']
              #print  task.project['category']
              #print  task.project['ploshad']
              #print  task.project['forma']
              #print  task.project['price']
              #print  task.project['data1']
              #print  task.project['adress']
              #print  task.project['data2']
              #print  task.project['fio']
              #print  task.project['gaz']
              #print  task.project['lat']
              print  task.project['fnums']              
              
              
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
              self.ws.write(self.row, 13, task.project['gaz'])
              self.ws.write_string(self.row, 14, task.project['url']) 
              self.ws.write(self.row, 15, datetime.today().strftime('%d.%m.%Y')) 
              self.ws.write(self.row, 16, task.project['fnums'])
              #print('*'*50)
              print u'Результат - '+str(self.row)+'/'+str(self.sheet.nrows)
              print('*'*50) 
              self.row+= 1              
              
              #if self.row > 15:
                     #self.stop()                      
              
              
bot = Gis(thread_number=5, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Pars/Proxy/tipa.txt','text_file',proxy_type='http',  timeout=5)
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
msgbox('Имя файла:'+ 'Кадастровые_номера_'+datetime.today().strftime('%d.%m.%Y'),title='Обработка завершена!')

