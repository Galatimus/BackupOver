#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import logging
import time
import json
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logging.basicConfig(level=logging.DEBUG)

#g = Grab(timeout=200, connect_timeout=200)
#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')

name =open('nums.txt').read().splitlines()

class Gis(Spider):
       
       #initial_urls=['https://2gis.ru/countries/global/']
       def prepare(self):
              
              self.workbook = xlsxwriter.Workbook(u'Кадастровые_номера_'+datetime.today().strftime('%d.%m.%Y')+'_.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"Кадастровый номер")
              self.ws.write(0,1, u"Статус объекта")
              self.ws.write(0,2, u"Дата постановки на кадастровый учет")
              self.ws.write(0,3, u"Категория земель")
              self.ws.write(0,4, u"Площадь")
              self.ws.write(0,5, u"Единица измерения (код)")
              self.ws.write(0,6, u"Кадастровая стоимость")
              self.ws.write(0,7, u"Дата утверждения стоимости")
              self.ws.write(0,8, u"Адрес (местоположение)")
              self.ws.write(0,9, u"Дата обновления информации")
              self.ws.write(0,10, u"ФИО кадастрового инженера")
              self.ws.write(0,11, u"Долгота")
              self.ws.write(0,12, u"Широта")
              self.ws.write(0,13, u"Вид разрешенного использования по документу")
              self.ws.write(0,14, u"URL")
              self.ws.write(0,15, u"Дата парсинга")              
             
              self.row= 1
              
       def task_generator(self):
              for line in name:
                     self.num=line.strip()
                     time.sleep(1)
                     yield Task ('zapros',url='https://rosreestr.ru/wps/portal/cc_information_online?KN='+self.num,network_try_count=100)
                     #yield Task('Kadr',url='http://getpkk.ru/1/'+self.num,refresh_cache=True,network_try_count=100)
                     yield Task('Kadr',url='http://getpkk.ru/1/'+re.sub(r'(?<=:)0*','',self.num),network_try_count=100)
                     #yield Task('vid',url='http://pkk5.rosreestr.ru/api/features/1/'+re.sub(r'(?<=:)0*','',self.num),network_try_count=100)       
       
       
       def task_Kadr(self,grab,task):
              kd = grab.doc.rex_text(u'var init_data = (.+?);')
              data = json.loads(kd)
              try:
                     self.adres = data['attrs']['address']
              except (TypeError,IndexError,ValueError,KeyError):
                     self.adres ='' 
              try:
                     self.cat = data['attrs']['util_by_doc']
              except (TypeError,IndexError,ValueError,KeyError):
                     self.cat=''                     
              try:
                     self.lat=  data['coordinates'][0][0][0][1]
              except (TypeError,IndexError,ValueError,KeyError):
                     self.lat=''
                     
              try:
                     self.lng=  data['coordinates'][0][0][0][0]
              except (TypeError,IndexError,ValueError,KeyError):
                     self.lng='' 
              try:
                     self.cena = data['attrs']['cad_cost']
              except (TypeError,IndexError,ValueError,KeyError):
                     self.cena =''                     
              
       #def task_vid(self,grab,task):
              #try:
                     #self.cat = grab.response.json['feature']['attrs']['util_by_doc']
              #except (TypeError,IndexError,ValueError,KeyError):
                     #self.cat=''
       
       
       
       
       
       def task_zapros(self,grab,task):
              g2 = grab.clone(timeout=20, connect_timeout=200)
              g2.doc.submit(make_request=True,submit_name='submit')
              #time.sleep(1)
              
              try:
                     ur = g2.make_url_absolute(g2.doc.select(u'//td[@class="td"][4]/a').attr('href'))
                     yield Task ('post',url=ur,refresh_cache=True,network_try_count=100)
              except IndexError:
                     yield Task ('post',grab=g2,refresh_cache=True,network_try_count=100)              
              #g2=grab
              
                     
       def task_post(self,grab,task):
              
                            
              
              
              try:
                     nomer = grab.doc.select(u'//td[contains(text(),"Кадастровый номер:")]/following::b[1]').text()
              except IndexError:
                     nomer =''              
              
              try:
                     status = grab.doc.select(u'//nobr[contains(text(),"Статус объекта:")]/following::b[1]').text()
              except IndexError:
                     status =''
              try:
                     data = grab.doc.select(u'//nobr[contains(text(),"Дата постановки на кадастровый учет:")]/following::b[1]').text()
              except IndexError:
                     data =''                      
              try:
                     cat = grab.doc.select(u'//nobr[contains(text(),"Категория земель:")]/following::b[1]').text()
              except IndexError:
                     cat =''                      
              try:
                     plosh = grab.doc.select(u'//nobr[contains(text(),"Площадь:")]/following::b[1]').text()
              except IndexError:
                     plosh =''
              try:
                     kod = grab.doc.select(u'//td[contains(text(),"Единица измерения (код):")]/following::b[1]').text()
              except IndexError:
                     kod =''                     
                     
             
              try:
                     data_ut = grab.doc.select(u'//nobr[contains(text(),"Дата утверждения стоимости:")]/following::b[1]').text()
              except IndexError:
                     data_ut =''
              #try:
                     #adres = grab.doc.select(u'//nobr[contains(text(),"Адрес (местоположение):")]/following::b[1]').text()
              #except IndexError:
                     #adres =''
              #try:
                     #cena = grab.doc.select(u'//nobr[contains(text(),"Кадастровая стоимость:")]/following::b[1]').text().replace(self.adres,'')
              #except IndexError:
                     #cena =''                     
              try:
                     data_ob = grab.doc.select(u'//nobr[contains(text(),"Дата обновления информации:")]/following::b[1]').text()
              except IndexError:
                     data_ob =''
              try:
                     ingener = grab.doc.select(u'//td[contains(text(),"ФИО кадастрового инженера:")]/following::b[1]').text()
              except IndexError:
                     ingener =''
                     
             
                     
              projects = {'nomer': nomer,
                          'status': status,
                          'url': task.url,
                          'data': data,
                          'category': cat,
                          'ploshad': plosh,
                          'edin_izm': kod,
                          'price': self.cena,
                          'data1': data_ut,
                          'adress': self.adres,
                          'data2': data_ob,
                          'fio':ingener,
                          'dol': self.lat,
                          'shir':self.lng,
                          'vid_is':self.cat}
                          
                     
              
              
              yield Task('write',project=projects,grab=grab)
                                          
              
              
       def task_write(self,grab,task):
              
              
              print('*'*50)
              print  task.project['nomer']
              print  task.project['status']
              print  task.project['data']
              print  task.project['category']
              print  task.project['ploshad']
              print  task.project['edin_izm']
              print  task.project['price']
              print  task.project['data1']
              print  task.project['adress']
              print  task.project['data2']
              print  task.project['fio']
              print  task.project['dol']
              print  task.project['shir']
              print  task.project['vid_is']
              
              self.ws.write(self.row, 0, task.project['nomer'])
              self.ws.write(self.row, 1, task.project['status'])
              self.ws.write(self.row, 2, task.project['data'])
              self.ws.write(self.row, 3, task.project['category'])
              self.ws.write(self.row, 4, task.project['ploshad'])
              self.ws.write(self.row, 5, task.project['edin_izm'])
              self.ws.write(self.row, 6, task.project['price'])
              self.ws.write(self.row, 7, task.project['data1'])
              self.ws.write(self.row, 8, task.project['adress'])
              self.ws.write(self.row, 9, task.project['data2'])
              self.ws.write(self.row, 10, task.project['fio'])
              self.ws.write(self.row, 11, task.project['dol'])
              self.ws.write(self.row, 12, task.project['shir'])
              self.ws.write(self.row, 13, task.project['vid_is'])
              self.ws.write_string(self.row, 14, task.project['url']) 
              self.ws.write(self.row, 15, datetime.today().strftime('%d.%m.%Y')) 
              print('*'*50)
              print 'Ready - '+str(self.row)+'/'+str(3813)
              print('*'*50) 
              self.row+= 1              
              
              if self.row > 25:
                     self.stop()                      
              
              
bot = Gis(thread_number=3, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Pars/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=500)
bot.run()
print(u'Спим 2 сек...')
time.sleep(2)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
