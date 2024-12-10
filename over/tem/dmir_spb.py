#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import logging
import time
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class bcinform(Spider):
       def prepare(self):
              self.workbook = xlsxwriter.Workbook(u'Dmir_SPB.xlsx')
              self.ws = self.workbook.add_worksheet(u'Dmir_SPB')
              self.ws.write(0, 0, u"ТИП_ПОМЕЩЕНИЯ")
              self.ws.write(0, 1, u"АДРЕС")
              self.ws.write(0, 2, u"МЕТРО")
              self.ws.write(0, 3, u"РАЙОН_ГОРОДА")
              self.ws.write(0, 4, u"УДАЛЕННОСТЬ_ОТ_МЕТРО(пешком)")
              self.ws.write(0, 5, u"ПЛОЩАДЬ")
              self.ws.write(0, 6, u"ЦЕНА_ЗА_ОБЪЕКТ(руб)")
              self.ws.write(0, 7, u"ЦЕНА(руб./кв.м)")
              self.ws.write(0, 8, u"СТАВКА_АРЕНДЫ(руб./кв.м/мес.или/год)")
              self.ws.write(0, 9, u"ПОРЯДОК_ОПЛАТЫ")
              self.ws.write(0, 10, u"СОСТАЯНИЕ_ОТДЕЛКИ")
              self.ws.write(0, 11, u"ЭТАЖ_РАСПОЛОЖЕНИЯ")
              self.ws.write(0, 12, u"ОПИСАНИЕ")
              self.ws.write(0, 13, u"ДАТА_РАЗМЕЩЕНИЯ_ОБЪЯВЛЕНИЯ")
           	       
              self.result= 1
       def task_generator(self):
              for x in range(1,22):#22
                     yield Task ('post',url='http://realty.dmir.ru/spb/rent/arenda-torgovyh-pomeshceniy-v-sankt-peterburge/?mode=tbl&page=%d'% x,refresh_cache=True,network_try_count=1000)
              for x in range(1,13):#13
                     yield Task ('post',url='http://realty.dmir.ru/spb/sale/prodazha-torgovyh-pomeshceniy-v-sankt-peterburge/?mode=tbl&page=%d'% x,refresh_cache=True,network_try_count=1000)
                                          
       def task_post(self,grab,task):
              for elem in grab.doc.select(u'//td/input[@type="hidden"]/following-sibling::a'):
                     ur = grab.make_url_absolute(elem.attr('href'))  
                     #print ur	      
                     yield Task('item',url=ur,network_try_count=1000)
                           
                     
       def task_item(self, grab, task):
                       
              try:
                     tip = u'Торговое помещение'
              except IndexError:
                     tip = ''
              
              try:
                     adress = grab.doc.select(u'//h2[@class="subtitle"]/small').text()
              except IndexError:
                     adress = ''
              try:
                     metro = grab.doc.select(u'//th[contains(text(),"метро:")]/following-sibling::td').text().split(', ')[0]
              except IndexError:
                     metro = ''                     
              try:
                     ray = grab.doc.select(u'//dt[contains(text(),"Район")]/following-sibling::dd[1]').text()
              except IndexError:
                     ray = ''
              
              try:
                     udal = grab.doc.select(u'//th[contains(text(),"метро:")]/following-sibling::td').text().split(', ')[1].split('. ')[0]
              except IndexError:
                     udal = ''
       
                                   
                     
              try:
                     plosh = grab.doc.select(u'//li[contains(text(),"общая площадь")]').text().replace(u' общая площадь','')
              except IndexError:
                     plosh = ''
              try:
                     cena_pr = grab.doc.select(u'//p[@class="kn-obj-info b-franchise-hide-mobile"]').text()
              except IndexError:
                     cena_pr =''
              try:
                     cena_kv = grab.doc.select(u'//span[@id="price_offer"]/sup/ancestor::span').text()
              except IndexError:
                     cena_kv =''                      
              try:
                     cena_ar = grab.doc.select(u'//span[@id="price_offer"][contains(text(),"месяц")]').text()
              except IndexError:
                     cena_ar = ''
                     try:
                            cena_pr = grab.doc.select(u'//span[@id="price_offer"]').text()
                     except IndexError:
                            cena_pr =''                            
              try:
                     poryadok = grab.doc.select(u'//dt[contains(text(),"Порядок оплаты")]/following-sibling::dd[1]').text()
              except IndexError:
                     poryadok = ''                     
       
              try:
                     remont = grab.doc.select(u'//li[contains(text(),"состояние")]/b').text() 
              except IndexError:
                     remont = ''
              try:
                     etag = grab.doc.select(u'//ul[@id="flat_data"]/li[contains(text(),"этаж")]').number()
              except IndexError:
                     etag = ''
              try:
                     opis = grab.doc.select(u'//div[@class="mb20 objectDesc"]').text() 
              except IndexError:
                     opis = ''
              try:
                     data = grab.doc.select(u'//dt[contains(text(),"Размещено")]/following::span[1]').text()
              except IndexError:
                     data = ''                     
       
             
              
       
              
       
              projects = {'tip': tip,
                          'adress': adress,
                          'rayon': ray,
                          'metro': metro,
                          'udal': udal,
                          'plosh':plosh,
                          'cena_pr': cena_pr,
                          'cena_kv': cena_kv,
                          'cena_ar': cena_ar,
                          'poryadok': poryadok,
                          'remont': remont,
                          'et': etag,
                          'opis': opis,
                          'data': data}
                     
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
              print('*'*100)
              print  task.project['tip']
              print  task.project['adress']
              print  task.project['rayon']
              print  task.project['metro']             
              print  task.project['udal']
              print  task.project['plosh']             
              print  task.project['cena_pr']
              print  task.project['cena_kv']
              print  task.project['cena_ar']
              print  task.project['poryadok']
              print  task.project['remont']
              print  task.project['et']
              print  task.project['opis']
              print  task.project['data']              
             
       
              self.ws.write(self.result,0, task.project['tip'])              
              self.ws.write(self.result,1, task.project['adress'])
              self.ws.write(self.result,2, task.project['metro'])              
              self.ws.write(self.result,3, task.project['rayon'])
              self.ws.write(self.result,4, task.project['udal'])
              self.ws.write(self.result,5, task.project['plosh'])
              self.ws.write(self.result,6, task.project['cena_pr'])             
              self.ws.write(self.result,7, task.project['cena_kv'])                  
              self.ws.write(self.result,8, task.project['cena_ar'])
              self.ws.write(self.result,9, task.project['poryadok'])
              self.ws.write(self.result,10,task.project['remont'])
              self.ws.write(self.result,11,task.project['et'])
              self.ws.write(self.result,12,task.project['opis'])
              self.ws.write(self.result,13,task.project['data'])
              
              
       
       
       
       
              print('*'*100)
              print 'Ready - '+str(self.result)
              logger.debug('Tasks - %s' % self.task_queue.size()) 
              print('*'*100)
              self.result+= 1
              
              
              #if self.result > 5:
                     #self.stop()	              
              
              
              
bot = bcinform(thread_number=2, network_try_limit=100000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 3 сек...')
time.sleep(3)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
