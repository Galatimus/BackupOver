#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import logging
import time
from sub import conv
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class mallru(Spider):
       def prepare(self):
              self.workbook = xlsxwriter.Workbook(u'Mallru_ТЦ.xlsx')
              self.ws = self.workbook.add_worksheet(u'mallru')
              self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
              self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
              self.ws.write(0, 2, u"ПОСЕЛЕНИЕ")
              self.ws.write(0, 3, u"ОРИЕНТИР")
              self.ws.write(0, 4, u"НАСЕЛЕННЫЙ_ПУНКТ")
              self.ws.write(0, 5, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
              self.ws.write(0, 6, u"АДРЕС")
              self.ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
              self.ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
              self.ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
              self.ws.write(0, 10, u"МАСШТАБ")
              self.ws.write(0, 11, u"ТИП ПОСТРОЙКИ")
              self.ws.write(0, 12, u"НАИМЕНОВАНИЕ ОБЪЕКТА")
              self.ws.write(0, 13, u"КЛАСС ОБЪЕКТА")
              self.ws.write(0, 14, u"ОБЩАЯ ПЛОЩАДЬ ОБЪЕКТА")
              self.ws.write(0, 15, u"КОЛИЧЕСТВО ЭТАЖЕЙ")
              self.ws.write(0, 16, u"НДС")
              self.ws.write(0, 17, u"КУ")
              self.ws.write(0, 18, u"ЭКСПЛУАТАЦИОННЫЕ РАСХОДЫ")
              self.ws.write(0, 19, u"ГОД ПОСТРОЙКИ")
              self.ws.write(0, 20, u"ПАРКОВКА")
              self.ws.write(0, 21, u"ОХРАНА")
              self.ws.write(0, 22, u"ЯКОРНЫЕ АРЕНДАТОРЫ")
              self.ws.write(0, 23, u"ДЕВЕЛОПЕР")
              self.ws.write(0, 24, u"ОПИСАНИЕ")
              self.ws.write(0, 25, u"ИСТОЧНИК_ИНФОРМАЦИИ")
              self.ws.write(0, 26, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
              self.ws.write(0, 27, u"КОНТАКТЫ")
              self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")            
              self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
              self.ws.write(0, 30, u"ДАТА_ПАРСИНГА")	       
              self.result= 1
       def task_generator(self):
              yield Task ('post',url='http://www.mallru.ru/malls',refresh_cache=True,network_try_count=100)
              
              
       def task_post(self,grab,task):
              for elem in grab.doc.select(u'//h3/a'):
                     ur = grab.make_url_absolute(elem.attr('href'))  
                     #print ur	      
                     yield Task('item',url=ur,network_try_count=100)
              yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
       def task_page(self,grab,task):
              try:
                     pg = grab.doc.select(u'//span[@id="pagination"]/strong/following-sibling::a[1]')
                     u = grab.make_url_absolute(pg.attr('href'))
                     yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
              except IndexError:
                     print('*'*100)
                     print '!!','NO PAGE NEXT','!!'
                     print('*'*100)
                     logger.debug('%s taskq size' % self.task_queue.size())              
                     
       def task_item(self, grab, task):
              try:
                     dt= grab.doc.rex_text(u'<p>г. (.*?)<br/>')
                     sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
              except IndexError: 
                     sub=''
             
              try:
                     punkt = grab.doc.rex_text(u'<p>г. (.*?)<br/>')
              except IndexError:
                     punkt = ''                     
              try:
                     adress = grab.doc.rex_text(u'<p>г. (.*?)</p>').replace(u'<br/>',',')
              except IndexError:
                     adress = ''
                     
              try:
                     metro = grab.doc.rex_text(u'Станция метро «(.*?)»')
              except IndexError:
                     metro = ''
            
              
              try:
                     name = grab.doc.select(u'//h1').text()
              except IndexError:
                     name = ''
              try:
                     plosh_ob = grab.doc.select(u'//td[contains(text(),"Общая площадь")]/following-sibling::td').text()
              except IndexError:
                     plosh_ob = ''
              
              try:
                     et = grab.doc.select(u'//td[contains(text(),"Количество этажей")]/following-sibling::td').number()
              except IndexError:
                     et = ''
       
                                   
                     
              try:
                     park = grab.doc.select(u'//td[contains(text(),"Парковка")]/following-sibling::td').text()
              except IndexError:
                     park = ''
       
              try:
                     yakor = grab.doc.select(u'//td[contains(text(),"Якоря")]/following-sibling::td').text()
              except IndexError:
                     yakor = ''
              try:
                     devel = grab.doc.select(u'//td[contains(text(),"Девелопер")]/following-sibling::td').text()
              except IndexError:
                     devel = ''                     
       
              try:
                     opis = grab.doc.select(u'//h3[contains(text(),"Дополнительное описание")]/following-sibling::p').text() 
              except IndexError:
                     opis = ''
              
       
             
              
       
              
       
              projects = {'url': task.url,
                          'sub': sub,
                          'punkt': punkt,
                          'adress': adress,
                          'metro': metro,
                          'name': name,
                          'plosh_ob': plosh_ob,
                          'et': et,
                          'park': park,
                          'yakor':yakor,
                          'opis': opis,
                          'devel': devel
                           }
                     
              yield Task('write',project=projects,grab=grab)
              
       def task_write(self,grab,task):
              print('*'*100)
              print  task.project['sub']
              print  task.project['punkt']
              print  task.project['adress']
              print  task.project['metro']
              print  task.project['name']
              print  task.project['plosh_ob']
              print  task.project['et']             
              print  task.project['park']
              print  task.project['yakor']             
              print  task.project['opis']
              print  task.project['url']
              print  task.project['devel']
             
       
              self.ws.write(self.result,0, task.project['sub'])              
              self.ws.write(self.result,4, task.project['punkt'])
              self.ws.write(self.result,6, task.project['adress'])              
              self.ws.write(self.result,7, task.project['metro'])
              #self.ws.write(self.result,11, task.project['tip'])
              self.ws.write(self.result,12, task.project['name'])
              self.ws.write(self.result,14, task.project['plosh_ob'])             
              self.ws.write(self.result,15, task.project['et'])                  
              self.ws.write(self.result,20, task.project['park'])
              self.ws.write(self.result,22, task.project['yakor'])
              self.ws.write(self.result,23, task.project['devel'])
              self.ws.write(self.result,25, u'МОЛЛРУ.РУ')
              self.ws.write_string(self.result,26, task.project['url'])
              #self.ws.write(self.result,27, task.project['phone'])
              self.ws.write(self.result,24, task.project['opis'])
              self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
              
       
       
       
       
              print('*'*100)
              print 'Ready - '+str(self.result)
              logger.debug('Tasks - %s' % self.task_queue.size()) 
              print('*'*100)
              self.result+= 1
              
              
              #if self.result > 50:
                     #self.stop()	              
              
              
              
bot = mallru(thread_number=5, network_try_limit=1000)
bot.load_proxylist('../../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print(u'Спим 3 сек...')
time.sleep(3)
print(u'Сохранение...')
bot.workbook.close()
print('Done!')
