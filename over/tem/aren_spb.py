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
              self.workbook = xlsxwriter.Workbook(u'Arendator_SPB_Офисные_помещения_Аренда.xlsx')
              self.ws = self.workbook.add_worksheet(u'Arendator_SPB')
              self.ws.write(0, 0, u"Тип_помещения")
              self.ws.write(0, 1, u"Здание/Тип здания/Тип строения")
              self.ws.write(0, 2, u"Класс")
              self.ws.write(0, 3, u"Адрес")
              self.ws.write(0, 4, u"Район")
              self.ws.write(0, 5, u"Метро")
              self.ws.write(0, 6, u"Предлагаемая_площадь,кв.м")
              self.ws.write(0, 7, u"Этаж")
              self.ws.write(0, 8, u"Этажность")
              self.ws.write(0, 9, u"Мин._срок")
              self.ws.write(0, 10, u"Предоплата")
              self.ws.write(0, 11, u"Тип договора")
              self.ws.write(0, 12, u"Ставка,руб./кв.м/мес.")
              self.ws.write(0, 13, u"Арендная плата,руб./мес")
              self.ws.write(0, 14, u"Планировка")
              self.ws.write(0, 15, u"Отделка/Состояние отделки")
              self.ws.write(0, 16, u"Условия отделки")
              self.ws.write(0, 17, u"Наличие мебели")
              self.ws.write(0, 18, u"ОПИСАНИЕ")
              self.ws.write(0, 19, u"ИСТОЧНИК")
              self.ws.write(0, 20, u"ССЫЛКА")
              self.ws.write(0, 21, u"ДАТА ПУБЛИКАЦИИ(РАЗМЕЩЕНО)")
              self.ws.write(0, 22, u"ДАТА ОБНОВЛЕНИЯ")
                 
              
              
              
              
              
              
           	       
              self.result= 1
       def task_generator(self):
              for x in range(1,2651):#2651
                     yield Task ('post',url='http://www.office.arendator-spb.ru/arenda-ofisa/page%d'%x+'.html',refresh_cache=True,network_try_count=100)
              #for x in range(1,2):#13
                     #yield Task ('post',url='http://realty.dmir.ru/spb/sale/prodazha-torgovyh-pomeshceniy-v-sankt-peterburge/?mode=tbl&page=%d'% x,refresh_cache=True,network_try_count=1000)
                                          
       def task_post(self,grab,task):
              for elem in grab.doc.select(u'//a[contains(text(),"Подробнее>>")]'):
                     ur = grab.make_url_absolute(elem.attr('href'))  
                     #print ur	      
                     yield Task('item',url=ur,refresh_cache=True,network_try_count=100)
                           
                     
       def task_item(self, grab, task):
                       
              try:
                     tip = grab.doc.select(u'//span[contains(text(),"Тип помещения:")]/following-sibling::text()').text()
              except IndexError:
                     tip = ''
              
              try:
                     try:
                            tip_str = grab.doc.select(u'//strong[contains(text(),"Здание:")]/following-sibling::span').text()#.replace(u'тип строения','')
                     except IndexError:
                            tip_str = grab.doc.select(u'//strong[contains(text(),"Тип здания:")]/following-sibling::span').text()  
              except IndexError:
                     tip_str = ''
                     
              try:
                     klass = grab.doc.select(u'//strong[contains(text(),"Здание:")]/following-sibling::span').text().split(u'(класс ')[1].replace(u')','')
              except IndexError:
                     klass = ''                     
              try:
                     metro = grab.doc.select(u'//a[contains(@href,"metro")]').text()
              except IndexError:
                     metro = ''                     
              try:
                     ray = grab.doc.select(u'//div[@class="b_breadcrumbs"]/a[contains(text(),"район")]').text()
              except IndexError:
                     ray = ''
              
              try:
                     adress = re.sub(r'\s+', ' ',grab.doc.select(u'//strong[contains(text(),"Адрес:")]/following-sibling::span').text())
              except IndexError:
                     adress = ''
       
                                   
                     
              try:
                     plosh = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::span').text()
              except IndexError:
                     plosh = ''
              try:
                     cena_pr = grab.doc.select(u'//small[contains(text(),"цена -")]/following-sibling::span[1]').text()
              except IndexError:
                     cena_pr =''
              try:
                     cena_kv = grab.doc.select(u'//small/span[1]').text()
              except IndexError:
                     cena_kv =''                      
                                          
              try:
                     #try:
                            #pred = grab.doc.rex_text(u'предоплата: (.*?);')[:10]
                     #except IndexError:
                     pred = grab.doc.select(u'//span[contains(text(),"Отделка:")]/following-sibling::text()').text()  
              except IndexError:
                     pred = ''                     
       
              try:
                     remont = grab.doc.select(u'//span[contains(text(),"Планировка:")]/following-sibling::text()').text()#.replace(u'тип договора ','') 
              except IndexError:
                     remont = ''
              try:
                     sost = grab.doc.select(u'//span[contains(text(),"Условия отделки:")]/following-sibling::text()').text()#.replace(u'тип договора ','') 
              except IndexError:
                     sost = '' 
                     
              try:
                     meb = grab.doc.select(u'//span[contains(text(),"Наличие мебели:")]/following-sibling::text()').text()#.replace(u'тип договора ','') 
              except IndexError:
                     meb = ''                     
              try:
                     etag = grab.doc.select(u'//strong[contains(text(),"Этаж:")]/following-sibling::text()').text()
              except IndexError:
                     etag = ''
              try:
                     etagn = grab.doc.select(u'//strong[contains(text(),"Мин. срок:")]/following-sibling::text()').text()
              except IndexError:
                     etagn = ''                     
              try:
                     opis = grab.doc.select(u'//div[@id="b_full"]').text() 
              except IndexError:
                     opis = ''
              try:
                     data = grab.doc.select(u'//li[contains(text(),"дата обновления:")]').text().split(': ')[1].split(', ')[0].replace(u' Июл ','.07.')
              except IndexError:
                     data = ''                     
       
             
              
       
              
       
              projects = {'tip': tip,
                          'tip_str': tip_str,
                          'klass':klass,
                          'rayon': ray,
                          'metro': metro,
                          'adress': adress,
                          'plosh':plosh,
                          'cena_pr': cena_pr,
                          'cena_kv': cena_kv,
                          'sost': sost,
                          'mebel': meb,
                          'poryadok': pred,
                          'remont': remont,
                          'et': etag,
                          'ets': etagn,
                          'url': task.url,
                          'opis': opis,
                          'data': data}
                     
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
              print('*'*100)
              print  task.project['tip']
              print  task.project['tip_str']
              print  task.project['klass']
              print  task.project['rayon']
              print  task.project['metro']             
              print  task.project['adress']
              print  task.project['plosh']             
              print  task.project['cena_pr']
              print  task.project['cena_kv']
              print  task.project['sost']
              print  task.project['mebel']
              print  task.project['poryadok']
              print  task.project['remont']
              print  task.project['et']
              print  task.project['ets']
              print  task.project['opis']
              print  task.project['data']
              print  task.project['url']
             
       
              self.ws.write(self.result,0, task.project['tip'])              
              self.ws.write(self.result,1, task.project['tip_str'])
              self.ws.write(self.result,2, task.project['klass'])              
              self.ws.write(self.result,3, task.project['adress'])
              self.ws.write(self.result,4, task.project['rayon'])
              self.ws.write(self.result,5, task.project['metro'])
              self.ws.write(self.result,6, task.project['plosh'])             
              self.ws.write(self.result,7, task.project['et'])                  
              self.ws.write(self.result,9, task.project['ets'])
              #self.ws.write(self.result,9, task.project['poryadok'])
              self.ws.write(self.result,15,task.project['poryadok'])
              self.ws.write(self.result,14,task.project['remont'])
              self.ws.write(self.result,12,task.project['cena_kv'])
              self.ws.write(self.result,13,task.project['cena_pr'])
              self.ws.write(self.result,16, task.project['sost'])
              self.ws.write(self.result,17, task.project['mebel'])
              self.ws.write(self.result,18, task.project['opis'])
              self.ws.write(self.result,19, u'Петербургский арендатор')
              self.ws.write_string(self.result,20, task.project['url'])
              self.ws.write(self.result,22, task.project['data'])
              
              
       
       
       
       
              print('*'*100)
              print 'Ready - '+str(self.result)
              logger.debug('Tasks - %s' % self.task_queue.size()) 
              print('*'*100)
              self.result+= 1
              
              
              #if self.result > 100:
                     #self.stop()
              
              
              
bot = bcinform(thread_number=3, network_try_limit=100000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print(u'Спим 3 сек...')
time.sleep(3)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
