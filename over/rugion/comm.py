#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import time
from PIL import Image
from cStringIO import StringIO
import pytesseract
import re
import os
import math
from grab import Grab
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'0001-0070_00_C_001-0002_FARPOS.xlsx')


     
     
class Region_Com(Spider):    
     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"СЕГМЕНТ")
	  self.ws.write(0, 8, u"ТИП_ПОСТРОЙКИ")
	  self.ws.write(0, 9, u"НАЗНАЧЕНИЕ_ОБЪЕКТА")
	  self.ws.write(0, 10, u"ПОТРЕБИТЕЛЬСКИЙ_КЛАСС")
	  self.ws.write(0, 11, u"СТОИМОСТЬ")
	  self.ws.write(0, 12, u"ИЗМЕНЕНИЕ_СТОИМОСТИ")
	  self.ws.write(0, 13, u"ДОПОЛНИТЕЛЬНЫЕ_КОММЕРЧЕСКИЕ_УСЛОВИЯ")
	  self.ws.write(0, 14, u"ПЛОЩАДЬ")
	  self.ws.write(0, 15, u"ЭТАЖ")
	  self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 17, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 18, u"ОПИСАНИЕ")
	  self.ws.write(0, 19, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 20, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 21, u"ТЕЛЕФОН")
	  self.ws.write(0, 22, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 23, u"КОМПАНИЯ")
	  self.ws.write(0, 24, u"МЕСТОПОЛОЖЕНИЕ")
	  self.ws.write(0, 25, u"МЕСТОРАСПОЛОЖЕНИЕ")
	  self.ws.write(0, 26, u"БЛИЖАЙШАЯ_СТАНЦИЯ_МЕТРО")
	  self.ws.write(0, 27, u"РАССТОЯНИЕ_ДО_БЛИЖАЙШЕЙ_СТАНЦИИ_МЕТРО")
	  self.ws.write(0, 28, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 29, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 30, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 31, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 32, u"КАДАСТРОВЫЙ_НОМЕР")
	  self.ws.write(0, 33, u"ЗАГОЛОВОК")
	  self.ws.write(0, 34, u"ШИРОТА_ИСХ")
	  self.ws.write(0, 35, u"ДОЛГОТА_ИСХ")
	  self.ws.write(0, 36, u"ТРАССА")
	  self.ws.write(0, 37, u"ПАРКОВКА")
	  self.result= 1        

     def task_generator(self):
	  for x in range(1,10):#52
	       yield Task ('post',url='http://domchel.ru/realty/sell/commerce/office/?page=%d'%x,refresh_cache=True,network_try_count=100)
       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//div[@class="rl_note"]/preceding-sibling::a'):
	       ur = elem.attr('href')  
	       #print ur	      
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
  
   
     def task_item(self, grab, task):
	  try:
	       punkt = 'Челябинск'#grab.doc.select(u'//li[contains(text(),"Ваш город:")]/a').text()
	  except DataNotFound:
	       punkt = ''
	       
	  try:
	       ter =  grab.doc.select(u'//span[contains(text(),"Район города:")]/following-sibling::text()').text()
	  except DataNotFound:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().find(u'м. ') > 0:
		    #uliza = grab.doc.select(u'//figure[@class="mb20 ml10"]/h1').text().split(',')[3]
	       #else:    
	       uliza = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text()
	  except IndexError:
	       uliza = ''
	       
	  try:
	       dom =  grab.doc.select(u'//div[@class="rl_menu_header"]/a[5]').text()
	  except IndexError:
	       dom = ''
	       
	  try:
	       tip = grab.doc.select(u'//span[contains(text(),"Тип помещения:")]/following-sibling::text()').text()
	  except IndexError:
	       tip = ''
	     
	  try:
	       orentir = grab.doc.select(u'//span[contains(text(),"Ориентир:")]/following-sibling::text()').text()
	       #print rayon
	  except DataNotFound:
	       orentir = ''
	     
	  
	     
	     
	  try:
	       try:
		    price = grab.doc.select(u'//span[contains(text(),"Цена общая:")]/following-sibling::text()').text()
	       except IndexError:
		    price = grab.doc.select(u'//span[contains(text(),"месяц:")]/following-sibling::text()').text()+'/мес.'
	  except IndexError:
	       price = ''
	       
	  try:
	       naz = grab.doc.select(u'//div[@class="title"]').text().split(', ')[0]
	  except IndexError:
	       naz = ''   
	     
	     
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Площадь")]/following-sibling::text()').text()
	    #print rayon
	  except DataNotFound:
	       plosh = ''

	  try:
	       ohrana = grab.doc.select(u'//li[contains(text(),"Ипотека")]').text()
	  except DataNotFound:
	       ohrana =''
	       
	       
	  try:
	       gaz = grab.doc.select(u'//span[contains(text(),"Этаж:")]/following-sibling::text()').text()
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//span[contains(text(),"Парковка, количество машиномест:")]/following-sibling::text()').text()
	  except DataNotFound:
	       voda =''
	       
	  try:
	       kanal = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text()
	  except DataNotFound:
	       kanal =''
	       
	  try:
	       elek = grab.doc.select(u'//div[@class="title"]').text()
	  except DataNotFound:
	       elek =''
	       
	  try:
	       con = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
	            (u' мая ',u'.05.'),(u' июня ',u'.06.'),
	            (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
	            (u' января ',u'.01.'),(u' декабря ',u'.12.'),
	            (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
	            (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
		       #d = grab.doc.select(u'//div[@class="createDate"]/text()').text()
	       d1 = grab.doc.rex_text(u'Опубликовано (.*?)&nbsp;&nbsp;')
	       teplo = reduce(lambda d1, r: d1.replace(r[0], r[1]), con, d1)[:10]
	  except DataNotFound:
	       teplo =''	 	     
	     
	  
	     
	  try:
	       opis = grab.doc.select(u'//span[contains(text(),"Дополнительная информация:")]/following-sibling::text()').text() 
	  except DataNotFound:
	       opis = ''
	     
	  try:
	       lico = grab.doc.select(u'//div[@class="field_info"][3]/div/following-sibling::text()[1]').text()
	   #print rayon
	  except DataNotFound:
	       lico = ''
	     
	  try:
	       com = grab.doc.select(u'//div[@class="field_info"][1]/a/b').text()
	   #print rayon
	  except DataNotFound:
	       com = ''
	     
	     
	  try:
	       conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
	               (u' мая ',u'.05.'),(u' июня ',u'.06.'),
	               (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
	               (u' января ',u'.01.'),(u' декабря ',u'.12.'),
	               (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
	               (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
	       #d = grab.doc.select(u'//div[@class="createDate"]/text()').text()
	       d = grab.doc.rex_text(u'<br>Обновлено (.*?)&nbsp;&nbsp;')
	       data = reduce(lambda d, r: d.replace(r[0], r[1]), conv, d)[:10]
	   #print rayon
	  except DataNotFound:
	       data = ''
	     
	 
	     
	     
	  try:
	   
	       phone_url = task.url.replace('detail','phone')
	       g2 = grab.clone(timeout=2000, connect_timeout=2000)
	       g2.go(phone_url)
	       im = Image.open(StringIO(g2.response.body))
	       x,y = im.size
	       phone = pytesseract.image_to_string(im.convert("RGB").resize((int(x*10), int(y*10)),Image.BICUBIC))
	       del g2
	       #phone = re.sub('[\s]', u'',pho)
	  except (AttributeError,DataNotFound,IOError):
	       phone = ''  
	     
	  
	     
	 
	 
	 
	 
	 
	  projects = {'sub': 'Челябинская область',
                       'uliza': uliza,
                       'dom': dom,
                       'punkt': punkt,
                       'terit':ter,  
                       'phone': phone,
                       'price': price,
                       'opis': opis,
                       'naz': naz,
                       'url': task.url,
                       'orentir': orentir,
                       'ploshad': plosh,
                       'tip': tip,
                       'gaz': gaz,
                       'voda':voda,
                       'elekt': elek,
                       'ohrana': ohrana,
                       'teplo': teplo,
                       'kanal': kanal,
                       'lico':lico,
                       'com':com,
                       'dataraz': data}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	 
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['uliza']
	  print  task.project['dom']
	  print  task.project['naz']
	  print  task.project['punkt']
	  print  task.project['terit']	      
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['opis']
	  print  task.project['price']
	 
	  print  task.project['orentir']	      
	  print  task.project['ploshad']	       
	  print  task.project['tip']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanal']
	  print  task.project['elekt']
	  print  task.project['teplo']
	  print  task.project['ohrana']
	  print  task.project['lico']
	  print  task.project['com']
	  print  task.project['dataraz']
	  
	  
	  
   
   
   
   
	  self.ws.write(self.result,0, task.project['sub'])
	  self.ws.write(self.result,4, task.project['uliza'])
	  self.ws.write(self.result,3, task.project['terit'])
	  self.ws.write(self.result,2, task.project['punkt'])
	  self.ws.write(self.result,7, task.project['dom']) 
	  self.ws.write(self.result,6, task.project['orentir'])
	  self.ws.write(self.result,8, task.project['tip'])
	  self.ws.write(self.result,9, task.project['naz'])
	  self.ws.write(self.result, 11, task.project['price'])
	  self.ws.write(self.result, 14, task.project['ploshad'])
	  self.ws.write(self.result, 15, task.project['gaz'])
	  self.ws.write(self.result, 37, task.project['voda'])
	  self.ws.write(self.result, 24, task.project['kanal'])
	  self.ws.write(self.result, 33, task.project['elekt'])
	  self.ws.write(self.result, 29, task.project['teplo'])
	  self.ws.write(self.result, 13, task.project['ohrana'])
	  self.ws.write(self.result, 18, task.project['opis'])
	  self.ws.write_string(self.result, 20, task.project['url'])
	  self.ws.write(self.result, 21, task.project['phone'])
	  self.ws.write(self.result, 22, task.project['lico'])
	  self.ws.write(self.result, 23, task.project['com'])
	  self.ws.write(self.result, 30, task.project['dataraz'])
	  self.ws.write(self.result, 19, 'Domchel')
	  self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 28, 'Продажа')
	  print('*'*100)	
	  print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  #print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  
	  #if int(self.result) >= int(self.num)-1:
	       #self.stop()

bot = Region_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
workbook.close()
print('Done')

