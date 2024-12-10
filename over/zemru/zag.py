#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from datetime import datetime,timedelta
import time
import re
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



logging.basicConfig(level=logging.DEBUG)







workbook = xlsxwriter.Workbook(u'ZemRu_Загород.xlsx')


class Zemru_Zag(Spider):


     def prepare(self):
	  self.ws = workbook.add_worksheet(u'ZemRu_Загород')
	  
	  self.ws.write(0, 0, "СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, "МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, "НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, "ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, "УЛИЦА")
	  self.ws.write(0, 5, "ДОМ")
	  self.ws.write(0, 6, "ОРИЕНТИР")
	  self.ws.write(0, 7, "ТРАССА")
	  self.ws.write(0, 8, "УДАЛЕННОСТЬ")
	  self.ws.write(0, 9, "КАДАСТРОВЫЙ_НОМЕР_ЗЕМЕЛЬНОГО_УЧАСТКА")
	  self.ws.write(0, 10, "ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, "ОПЕРАЦИЯ")
	  self.ws.write(0, 12, "СТОИМОСТЬ")
	  self.ws.write(0, 13, "ЦЕНА_М2")
	  self.ws.write(0, 14, "ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 15, "КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 16, "ЭТАЖНОСТЬ")
	  self.ws.write(0, 17, "МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 18, "ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 19, "ПЛОЩАДЬ_УЧАСТКА")
	  self.ws.write(0, 20, "ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  self.ws.write(0, 21, "ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 22, "ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 23, "КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 24, "ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 25, "ТЕПЛОСНАБЖЕНИЕ")
	  self.ws.write(0, 26, "ЛЕС")
	  self.ws.write(0, 27, "ВОДОЕМ")
	  self.ws.write(0, 28, "БЕЗОПАСНОСТЬ")
	  self.ws.write(0, 29, "ОПИСАНИЕ")
	  self.ws.write(0, 30, "ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 31, "ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 32, "ТЕЛЕФОН")
	  self.ws.write(0, 33, "КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 34, "КОМПАНИЯ")
	  self.ws.write(0, 35, "ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 36, "ДАТА_ПАРСИНГА")
	  self.result= 1
	  
	  
     
     
     
     
     
     def task_generator(self):
	  for x in range(1,3):
	       yield Task ('post',url='http://base.zem.ru/all/?page=%d'% x+'&cat=2',network_try_count=100)
          for x in range(1,94):
               yield Task ('post',url='http://base.zem.ru/all/?page=%d'% x+'&cat=5',network_try_count=100) 
         
       
     
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="b-special-lots__item__information__link-title-text"]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur	      
	       yield Task('item',url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	  
               
               
               
               
     def task_item(self, grab, task):
	  try:
	       
	       sub = grab.doc.select(u'//span[contains(text(),"Область/Край")]/following-sibling::span').text()
	  except IndexError:
	       sub =''
          try:
               ray =  grab.doc.select(u'//span[contains(text(),"Регион")]/following-sibling::span[contains(text(),"район")]').text()
          except IndexError:
	       ray=''
          try:
               punkt = grab.doc.select(u'//span[contains(text(),"Населённый пункт")]/following-sibling::span').text()
          except IndexError:
               punkt = ''
          try:
               tip = grab.doc.select(u'//span[contains(text(),"Объект")]/following-sibling::span').text().replace(';','')
          except IndexError:
               tip = ''	       
	  try:
	       oper = grab.doc.select('//span[@class="b-title__lot__sale"]').text()
	  except IndexError:
	       oper = ''
	  try:
	       price = grab.doc.select(u'//span[@class="b-sidebar-info__object__cost__value"]').text()
          except IndexError:
               price = ''
          try:
               plosh = grab.doc.select(u'//span[contains(text(),"Площадь дома")]/following-sibling::span').text()
          except IndexError:
	       plosh = ''
          try:
               plosh_uch = grab.doc.select(u'//span[contains(text(),"Площадь участка")]/following-sibling::span').text()
          except IndexError:
               plosh_uch = '' 	       
          
          try:
               gaz = grab.doc.select(u'//span[contains(text(),"Газоснобжение")]/following-sibling::span').text()
          except IndexError:
               gaz =''
          try:
               voda = grab.doc.select(u'//span[contains(text(),"Водоснабжение")]/following-sibling::span').text()
          except IndexError:
               voda =''
          try:
               kanal = grab.doc.select(u'//span[contains(text(),"Канализация")]/following-sibling::span').text()
          except IndexError:
               kanal =''
          try:
               elek =  grab.doc.select(u'//span[contains(text(),"Электроснабжение")]/following-sibling::span').text()
          except IndexError:
               elek =''
          try:
               teplo = grab.doc.select(u'//span[contains(text(),"Отопление")]/following-sibling::span').text()
          except IndexError:
               teplo =''
          try:
               opis = grab.doc.select(u'//div[@class="b-object__description__text"]').text() 
          except IndexError:
               opis = ''
          try:
               phone = re.sub('[^\d\,\+]', u'',grab.doc.select(u'//span[contains(text(),"Телефон:")]/following-sibling::span').text())
          except IndexError:
               phone = ''
          try:
               lico = grab.doc.select(u'//span[contains(text(),"Лот создал")]/following-sibling::span').text()
          except IndexError:
               lico = ''
          try:
               comp = grab.doc.select(u'//a[@class="b-sidebar-vendor-link"]').text()
          except IndexError:
               comp = ''
	       
	  try:
	       data = grab.doc.select(u'//span[contains(text(),"Дата публикации")]/following-sibling::span').text()
	  except IndexError:
	       data = ''
	  
	       
	       
	       
	       
	       
          
                       
	  projects = {'url': task.url,
	              'sub': sub,
	              'rayon': ray,
	              'punkt': punkt,
	              'tip_ob':tip,
	              'plosh_uch': plosh_uch,
	              'cena': price,
	              'plosh':plosh,
	              'gaz': gaz,
	              'voda': voda,
	              'kanaliz': kanal,
	              'electr': elek,
	              'teplo': teplo,
	              'opis':opis,
	              'phone':phone,
	              'lico':lico,
	              'company':comp,
	              'data':data,
	              'oper':oper
	                 }
     
     
	  yield Task('write',project=projects,grab=grab)
          
          
          
          
          
     def task_write(self,grab,task):
	  
	       
	  print('*'*50)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['tip_ob']
	  print  task.project['plosh_uch']
	  print  task.project['cena']
	  print  task.project['plosh']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['opis']
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['data']
	  print  task.project['oper']
	  
	  
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  #self.ws.write(self.result, 3, task.project['teritor'])
	  #self.ws.write(self.result, 4, task.project['ulica'])
	  #self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 19, task.project['plosh_uch'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  self.ws.write(self.result, 11, task.project['oper'])
	  self.ws.write(self.result, 10, task.project['tip_ob'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 21, task.project['gaz'])
	  self.ws.write(self.result, 22, task.project['voda'])
	  self.ws.write(self.result, 23, task.project['kanaliz'])
	  self.ws.write(self.result, 24, task.project['electr'])
	  self.ws.write(self.result, 25, task.project['teplo'])
	  self.ws.write(self.result, 29, task.project['opis'])
	  self.ws.write(self.result, 30, u'ZEM.RU')
	  self.ws.write_string(self.result, 31, task.project['url'])
	  self.ws.write(self.result, 32, task.project['phone'])
	  self.ws.write(self.result, 33, task.project['lico'])
	  self.ws.write(self.result, 34, task.project['company'])
	  self.ws.write(self.result, 35, task.project['data'])
	  self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	  
	      
	  print('*'*50)
	  print 'Ready - '+str(self.result)
	  print 'Tasks - %s' % self.task_queue.size()
	  print('*'*50)	       
	  self.result+= 1
	  
	  
	  
	  
	  #if self.result > 100:
               #self.stop()	  
	  

    
bot = Zemru_Zag(thread_number=1, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=500)
bot.run()
workbook.close()
print('Done!') 


     
     
