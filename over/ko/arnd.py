#!/usr/bin/python
# -*- coding: utf-8 -*-

from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
#from sub import conv
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



i = 0
l= open('Kat.txt').read().splitlines()
page = l[i]


while True:
       print '********************************************',i+1,'/',len(l),'*******************************************'
       class Arendator(Spider):
              def prepare(self):
                     self.f = page
                     #self.link =l[i]
                     #self.count =1
                     self.workbook = xlsxwriter.Workbook(u'aren/Arendator_Объекты_'+str(i+1)+'.xlsx')
                     #self.workbook1 = xlsxwriter.Workbook(u'aren/Arendator_Предложения_'+str(i+1)+'.xlsx')
                     self.ws = self.workbook.add_worksheet(u'Объекты')
                     #self.ws1 = self.workbook1.add_worksheet(u'Предложения')
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
                     #****************************************
                     #self.ws1.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
                     #self.ws1.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН")
                     #self.ws1.write(0, 2, u"ОРИЕНТИР")
                     #self.ws1.write(0, 3, u"НАСЕЛЕННЫЙ_ПУНКТ")
                     #self.ws1.write(0, 4, u"НАИМЕНОВАНИЕ ОБЪЕКТА")
                     #self.ws1.write(0, 5, u"ОПЕРАЦИЯ")
                     #self.ws1.write(0, 6, u"НАЗНАЧЕНИЕ ОБЪЕКТА")
                     #self.ws1.write(0, 7, u"ЭТАЖ")
                     #self.ws1.write(0, 8, u"ПЛОЩАДЬ ПОМЕЩЕНИЯ")
                     #self.ws1.write(0, 9, u"ЦЕНА ПРОДАЖИ")
                     #self.ws1.write(0, 10, u"АРЕНДНАЯ_СТАВКА_РУБ/МЕС")
                     #self.ws1.write(0, 11, u"ЦЕНА_КВ.М._РУБ")
                     #self.ws1.write(0, 12, u"ИСТОЧНИК_ИНФОРМАЦИИ")
                     #self.ws1.write(0, 13, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
                     #self.ws1.write(0, 14, u"ДАТА_РАЗМЕЩЕНИЯ")            
                     #self.ws1.write(0, 15, u"ДАТА_ОБНОВЛЕНИЯ")
                     #self.ws1.write(0, 16, u"ДАТА_ПАРСИНГА")
                     self.result= 1
                     #self.result1= 1
                     #else:
                            #self.result+= 1
                            #self.result1+= 1 
                     
              def task_generator(self):
                     yield Task ('post',url=self.f,refresh_cache=True,network_try_count=100)

                            
              def task_post(self,grab,task):
                     
                     for elem in grab.doc.select(u'//a[@class="objects-list__box object-box"]'):
                            ur = grab.make_url_absolute(elem.attr('href'))
                            #print ur
                            yield Task('item',url=ur,refresh_cache=True,network_try_count=100)
                            #yield Task('post2',url=ur,refresh_cache=True,network_try_count=100)
                     yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
                     
              def task_page(self,grab,task): 
                     try:
                            pg = grab.doc.select(u'//a[contains(@title,"Следующая страница")]')
                            u = grab.make_url_absolute(pg.attr('href'))
                            yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
                     except DataNotFound:
                            print('*'*100)
                            print '!!','NO PAGE NEXT','!!'
                            print('*'*100)
                            logger.debug('%s taskq size' % self.task_queue.size())
                            

                            
             
                            
              def task_item(self, grab, task):

                     try:
                            ray =  grab.doc.select(u'//a[contains(@title,"округу")]').text() 
              
                     except IndexError:
                            ray = ''
                     try:
                            p = grab.doc.select(u'//div[@class="geo-address"]').text()
                            if p.find(u'Санкт-Петербург')>=0:
                                   punkt = grab.doc.select(u'//div[@class="geo-address"]').text().split(',')[0][3:]
                            elif p.find(u'Москва')>=0:
                                   punkt = grab.doc.select(u'//div[@class="geo-address"]').text().split(',')[0][3:]
                            else:
                                   punkt = grab.doc.select(u'//div[@class="geo-address"]').text().split(' (')[0][3:]#.split(')')[0]
                     except IndexError:
                            punkt = '' 
                            
                     try:
                            ter = grab.doc.select(u'//a[contains(@title,"району")]').text()
                     except IndexError:
                            ter = ''                     
                     try:
                            adress = grab.doc.select(u'//div[@class="geo-address"]').text().replace(u' (на карте)','')
                     except IndexError:
                            adress = ''
                            
                     try:
                            metro = grab.doc.select(u'//i[@class="geo-metro-link"]').text()
                     except IndexError:
                            metro = ''
                     try:
                            metro_min = grab.doc.select(u'//div[@class="geo-metro-list-item"]').number()
                     except IndexError:
                            metro_min = ''
                     try:
                            metro_kak = grab.doc.select(u'//dt[contains(text(),"Этажность")]/following-sibling::dd[1]').text()
                     except IndexError:
                            metro_kak = ''
                     try:
                            mash = grab.doc.select(u'//dt[contains(text(),"Масштаб торгового комплекса")]/following-sibling::dd[1]').text()
                     except IndexError:
                            mash = ''                     
                     try:
                            tip = grab.doc.select(u'//dt[contains(text(),"Назначение")]/following-sibling::dd/a').text().split(' (')[0]
                     except IndexError:
                            tip = ''                     
                     
                     try:
                            name = grab.doc.select(u'//h1').text()
                     except IndexError:
                            name = ''
                     try:
                            klass = grab.doc.select(u'//dt[contains(text(),"Класс офисного здания")]/following-sibling::dd[1]').text()
                     except IndexError:
                            klass = ''
                     try:
                            plosh_ob = grab.doc.select(u'//dt[contains(text(),"Общая площадь")]/following-sibling::dd[1]').text()
                     except IndexError:
                            plosh_ob = ''                     
                     
                          
                     try:
                            yakor = grab.doc.select(u'//dt[contains(text(),"Год постройки")]/following-sibling::dd[1]').text()
                     except IndexError:
                            yakor = ''
                     try:
                            rashodi = grab.doc.select(u'//dt[contains(text(),"Девелопер")]/following-sibling::dd[1]/a').text()
                     except IndexError:
                            rashodi = ''                     
                            
                     try:
                            park = grab.doc.select(u'//h3[contains(text(),"Парковка")]/following-sibling::dt[1]').text()
                     except IndexError:
                            park = ''
              
                     try:
                            ohrana = grab.doc.select(u'//dt[contains(text(),"Охрана")]/following-sibling::dd[1]').text()
                     except IndexError:
                            ohrana = ''
              
                     try:
                            opis = grab.doc.select(u'//div[@class="content"]/p[2]').text() 
                     except IndexError:
                            opis = ''
                     try:
                            phone = re.sub('[^\d\,\+]','',grab.doc.select(u'//span[@class="begin"]').text())
                     except IndexError:
                            phone = ''
              
                    
                     try:
                            conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
                                    (u' мая ',u'.05.'),(u' июня ',u'.06.'),
                                    (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
                                    (u' января ',u'.01.'),(u' декабря ',u'.12.'),
                                    (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
                                    (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
                            d = grab.doc.select(u'//span[@class="grey-text"][2]').text()
                            data = reduce(lambda d, r: d.replace(r[0], r[1]), conv, d)[:-6]
                     except IndexError:
                            data = ''
                     projects = {'url': task.url,
                                 'rayon': ray,
                                 'punkt': punkt,
                                 'ter':ter,
                                 'adress': adress,
                                 'metro': metro,
                                 'metro_min': metro_min,
                                 'metro_kak': metro_kak,
                                 'mashtab': mash,
                                 'tip': tip,
                                 'name': name,
                                 'klass': klass,
                                 'plosh': plosh_ob,
                                 'yakor': yakor,
                                 'park': park,
                                 'ohrana':ohrana,
                                 'rashodi': rashodi,
                                 'opis': opis,
                                 'phone': phone,
                                 'dataraz': data}
                     
                     try:
              
                            link = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode='+adress
                            yield Task('subject',url=link,project=projects,refresh_cache=True,network_try_count=100)
                     except IndexError:
                            yield Task('subject',grab=grab,project=projects)
                            
                            
              def task_subject(self, grab, task):
                     try:
                            sub = grab.doc.json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][2]["name"]
                     except (IndexError,KeyError,AttributeError):
                            sub = ''	              
                            
                     yield Task('write',project=task.project,sub=sub,grab=grab)
                     
              def task_write(self,grab,task):
                     print('*'*100)
                     print  task.sub
                     print  task.project['rayon']
                     print  task.project['punkt']
                     print  task.project['ter']
                     print  task.project['adress']
                     print  task.project['metro']
                     print  task.project['metro_min']
                     print  task.project['metro_kak']
                     print  task.project['mashtab']
                     print  task.project['tip']
                     print  task.project['name']
                     print  task.project['klass']
                     print  task.project['plosh']
                     print  task.project['yakor']
                     print  task.project['park']
                     print  task.project['ohrana']
                     print  task.project['rashodi']
                     print  task.project['opis']
                     print  task.project['url']
                     print  task.project['phone']
                     print  task.project['dataraz']
                     #----------------------------
                     self.ws.write(self.result,0, task.sub)
                     self.ws.write(self.result,1, task.project['rayon'])
                     self.ws.write(self.result,4, task.project['punkt'])
                     self.ws.write(self.result,5, task.project['ter'])
                     self.ws.write(self.result,6, task.project['adress'])
                     self.ws.write(self.result,8, task.project['metro_min'])
                     self.ws.write(self.result,7, task.project['metro'])
                     self.ws.write(self.result,15, task.project['metro_kak'])
                     self.ws.write(self.result,10, task.project['mashtab'])
                     self.ws.write(self.result,11, task.project['tip'])
                     self.ws.write(self.result,12, task.project['name'])
                     self.ws.write(self.result,13, task.project['klass'])
                     self.ws.write(self.result,14, task.project['plosh'])
                     self.ws.write(self.result,23, task.project['rashodi'])
                     self.ws.write(self.result,20, task.project['park'])
                     self.ws.write(self.result,21, task.project['ohrana'])
                     self.ws.write(self.result,19, task.project['yakor'])
                     self.ws.write(self.result,24, task.project['opis'])
                     self.ws.write(self.result,25, u'Arendator.ru')
                     self.ws.write_string(self.result,26, task.project['url'])
                     self.ws.write(self.result,27, task.project['phone'])
                     self.ws.write(self.result,28, task.project['dataraz'])
                     self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
                     print('*'*100)
                     print 'Ready - '+str(self.result)
                     logger.debug('Tasks - %s' % self.task_queue.size())
                     
                     print('*'*100)
                     self.result+= 1              
                     #***************************************************************
                     #if self.result >50:
                            #self.stop()                 
                     
                     
                     
       bot = Arendator(thread_number=5, network_try_limit=1000)
       bot.load_proxylist('../../tipa.txt','text_file')
       bot.create_grab_instance(timeout=50, connect_timeout=50)
       bot.run()
       print('Wait 2 sec...')
       time.sleep(2)
       print('Save it...')
       bot.workbook.close()
       print('Done!')
       i=i+1
       try:
              page = l[i]
       except IndexError:
              break        


