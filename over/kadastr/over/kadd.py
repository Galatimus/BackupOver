usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import xlsxwriter
import logging
import time
from rosreestr import vid,cat,stat
from grab.spider import Spider,Task
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyproj import Proj, transform
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

i = 0
ls= open('np.txt').read().splitlines()
dc = len(ls)


logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


while i < len(ls):
           print '********************************************************************************************'
           #profile =  webdriver.FirefoxProfile()
           profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ljpce52l.default/') #Gui2
           #profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/jcpr7q9q.default/')#Gui1
           profile.native_events_enabled = False
           driver  = webdriver.Firefox(firefox_profile=profile,timeout=60)
           driver.set_window_position(0,0)
           driver.set_window_size(1000,720)           
           print i+1,'/',dc     
           driver.get('http://pkk5.rosreestr.ru/#x=&y=&z=&type=1&zoomTo=1&app=search&opened=1&text=Республика Тыва,'+ls[i])    
           sub = ls[i]
           print sub
           time.sleep(5)           
           lin = []
           while True:
                      print '********************',len(lin),'**********************'
                      try:
                                 try:
                                            WebDriverWait(driver,200).until(EC.presence_of_element_located((By.XPATH,u'//div[@class="featureSet_list"]')))
                                            print "Page is ready!"
                                            time.sleep(2)
                                 except TimeoutException:
                                            print "Loading took too much time!"
                                            time.sleep(2)
                                            driver.find_element_by_xpath(u'//a[contains(@title,"Следующая страница")]').click()                                 
                               
                                 for link in driver.find_elements_by_xpath(u'//b[@class="pull-left"]'):
                                            url = re.sub(r'(?<=:)0*','',link.text).replace(u'::',':0:')   
                                            print url
                                            lin.append(url)
                                 
                                 driver.find_element_by_xpath(u'//a[contains(@title,"Следующая страница")]').click()
                                 time.sleep(2)
                      except NoSuchElementException:
                                 driver.close()
                                 break
           class Gis(Spider):
           
                      #initial_urls=['https://2gis.ru/countries/global/']
                      def prepare(self):
                                 #self.rb = xlrd.open_workbook(name+'.xlsx')
                                 #self.sheet = self.rb.sheet_by_index(1)
                                 self.workbook = xlsxwriter.Workbook(u'np/Np_%s' % sub + u'.xlsx')
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
           
           
                                 self.inProj = Proj(init='epsg:3857')
                                 self.outProj = Proj(init='epsg:4326')             
                                 self.row= 1
           
                      def task_generator(self):
           
                                 for line in lin:
                                            yield Task ('post',url='http://pkk5.rosreestr.ru/api/features/1/'+line.strip(),network_try_count=100)
           
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
                                             'gaz': gaz}
           
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
                                            print  task.project['gaz']
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
                                            self.ws.write(self.row, 13, task.project['gaz'])
                                            self.ws.write_string(self.row, 14, task.project['url']) 
                                            self.ws.write(self.row, 15, datetime.today().strftime('%d.%m.%Y')) 
                                            print('*'*50)
                                            print 'Ready - '+str(self.row)+'/'+str(len(lin))
                                            print 'Tasks - %s' % self.task_queue.size()
                                            print('*'*50) 
                                            self.row+= 1              
           
                                            #if self.row > 15:
                                                       #self.stop()                      
           
           
           bot = Gis(thread_number=5, network_try_limit=1000)
           bot.load_proxylist('/home/oleg/Pars/Proxy/tipa.txt','text_file',proxy_type='http',  timeout=5)
           bot.create_grab_instance(timeout=5000, connect_timeout=5000)
           bot.run()
           print(u'Спим 2 сек...')
           time.sleep(2)
           print(u'Сохранение...')
           bot.workbook.close()
           print('Done!')                      
           time.sleep(3)          
           i=i+1    
          



 

