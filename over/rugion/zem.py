#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import math
import time
import os
from PIL import Image
from cStringIO import StringIO
import pytesseract
import re
from grab import Grab
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')


page = 'http://domchel.ru/realty/sell/land/housing/'
oper = u'Продажа'
i = 44

class Region_Zem(Spider):
     def prepare(self):
	  self.f = page
		       
	       
	  self.workbook = xlsxwriter.Workbook('0001-0002_00_У_004-0004_DOMCH.xlsx')
	  self.ws = self.workbook.add_worksheet(u'Rugion_ЗЕМЛЯ')
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"ТРАССА")
	  self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	  self.ws.write(0, 9, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 10, u"СТОИМОСТЬ")
	  self.ws.write(0, 11, u"ЦЕНА_ЗА_СОТКУ")
	  self.ws.write(0, 12, u"ПЛОЩАДЬ")
	  self.ws.write(0, 13, u"КАТЕГОРИЯ_ЗЕМЛИ")
	  self.ws.write(0, 14, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	  self.ws.write(0, 15, u"ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 16, u"ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 17, u"КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 18, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 19, u"ТЕПЛОСНАБЖЕНИЕ")
	  self.ws.write(0, 20, u"ОХРАНА")
	  self.ws.write(0, 21, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  self.ws.write(0, 22, u"ОПИСАНИЕ")
	  self.ws.write(0, 23, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 24, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 25, u"ТЕЛЕФОН")
	  self.ws.write(0, 26, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 27, u"КОМПАНИЯ")
	  self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 30, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 31, u"ВИД_ПРАВА")
	  self.ws.write(0, 32, u"МЕСТОПОЛОЖЕНИЕ")
	  self.result= 1
	       
	    
	    
	    
	      
    
     def task_generator(self):
	  for x in range(1,int(i)+1):
	       yield Task ('post',url=self.f+'?page=%d'%x,network_try_count=100)
	  yield Task ('post',url='http://domchel.ru/realty/lease/land/housing/',network_try_count=100)
	  
	  
     def task_post(self,grab,task):
	  
	  for elem in grab.doc.select(u'//div[@class="rl_note"]/preceding-sibling::a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur	      
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)

     def task_item(self, grab, task):
	  try:
	       if grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().find(u'р-н') > 0:
		    ray = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text().split(', ')[0]
	       else:
		    ray =''
	     #print ray
	  except DataNotFound:
	       ray =''
	  try:
	       punkt = 'Челябинск'
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter =  grab.doc.select(u'//span[contains(text(),"Район города:")]/following-sibling::text()').text()
	     #print ter
	  except DataNotFound:
	       ter =''
	     
	  try:
	       orentir = grab.doc.select(u'//span[contains(text(),"Ориентир:")]/following-sibling::text()').text()
	       #print rayon
	  except DataNotFound:
	       orentir = ''
	  try:
	       price = grab.doc.select(u'//span[contains(text(),"Цена общая:")]/following-sibling::text()').text()
	   #print price + u' руб'	    
	  except DataNotFound:
	       price = ''
	       
	  try:
	       price_sot = grab.doc.select(u'//span[contains(text(),"сот.")]/following-sibling::text()').text()
	  except DataNotFound:
	       price_sot = ''		    
	     
	     
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Площадь")]/following-sibling::text()').text()
	    #print rayon
	  except DataNotFound:
	       plosh = ''
	     
	  
	     
	  try:
	       vid = grab.doc.select(u'//span[contains(text(),"Тип")]/following-sibling::text()').text().replace(u'Под ','')
	   #print rayon
	  except DataNotFound:
	       vid = ''
	     
	  try:
	       ohrana =re.sub(u'^.*(?=храна)','',grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
	  except DataNotFound:
	       ohrana =''
	       
	       
	  try:
	       gaz = re.sub(u'^.*(?=газ)','',grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = re.sub(u'^.*(?=вод)','',grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
	  except DataNotFound:
	       voda =''
	       
	  try:
	       kanal = grab.doc.select(u'//span[contains(text(),"Расположение")]/following-sibling::text()').text()
	  except DataNotFound:
	       kanal =''
	       
	  try:
	       elek = re.sub(u'^.*(?=лектричество)','',grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
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
	       #if  re.sub(u'[^\d]','',grab.doc.select(u'//div[@style="clear: both; margin-bottom: 15px"]/following-sibling::br//following-sibling::text()').text()).isdigit()==False:
	       lico = grab.doc.select(u'//div[@class="field_info"][3]/div/following-sibling::text()[1]').text()
	       #else:
		    #lico=''
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
	       prava = grab.doc.select(u'//span[contains(text(),"Форма собственности:")]/following-sibling::text()').text()
	   #print rayon
	  except DataNotFound:
	       prava = ''
	     
	     
	  try:
	   
	       phone_url = task.url.replace('detail','phone')
	       g2 = grab.clone(timeout=200, connect_timeout=200)
	       g2.go(phone_url)
	       im = Image.open(StringIO(g2.response.body))
	       x,y = im.size
	       phone = pytesseract.image_to_string(im.convert("RGB").resize((int(x*10), int(y*10)),Image.BICUBIC))
	       #phone = re.sub('[\s]', u'',pho)
	  except (AttributeError,DataNotFound,IOError):
	       phone = ''  
	     
	  
	     
	 
	 
	 
	 
	 
	  projects = {'sub': 'Челябинская область',
                       'rayon': ray,
                       'punkt': punkt,
                       'terit':ter,  
                       'phone': phone,
                       'price': price,
                       'opis': opis,
                       'price_sot': price_sot,
                       'url': task.url,
                       'orentir': orentir,
                       'ploshad': plosh,
                       'vid': vid,
                       'gaz': gaz,
                       'voda':voda,
                       'elekt': elek,
                       'ohrana': ohrana,
                       'teplo': teplo,
                       'kanal': kanal,
                       'lico':lico,
                       'com':com,
                       'dataraz': data,
                      'prava':prava}
   
   
   
	  yield Task('write',project=projects,grab=grab)
   

   
   
   
   
     def task_write(self,grab,task):
	 
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['terit']	      
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['opis']
	  print  task.project['price']
	  print  task.project['price_sot']
	  print  task.project['orentir']	      
	  print  task.project['ploshad']	       
	  print  task.project['vid']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['elekt']
	  print  task.project['ohrana']
	  print  task.project['lico']
	  print  task.project['com']
	  print  task.project['dataraz']
	  print  task.project['teplo']
	  print  task.project['prava']
	  print  task.project['kanal']
	  
	  
   
   
   
   
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	 
	  self.ws.write(self.result, 6, task.project['orentir'])
	 
	  self.ws.write(self.result, 10, task.project['price'])
	  self.ws.write(self.result, 12, task.project['ploshad'])
	 
	  self.ws.write(self.result, 14, task.project['vid'])
	  self.ws.write(self.result, 15, task.project['gaz'])
	  self.ws.write(self.result, 16, task.project['voda'])
	  self.ws.write(self.result, 32, task.project['kanal'])
	  self.ws.write(self.result, 18, task.project['elekt'])
	  self.ws.write(self.result, 28, task.project['teplo'])
	  self.ws.write(self.result, 20, task.project['ohrana'])
	  self.ws.write(self.result, 22, task.project['opis'])
	  self.ws.write_string(self.result, 24, task.project['url'])
	  self.ws.write(self.result, 25, task.project['phone'])
	  self.ws.write(self.result, 26, task.project['lico'])
	  self.ws.write(self.result, 27, task.project['com'])
	  self.ws.write(self.result, 29, task.project['dataraz'])
	  self.ws.write(self.result, 31, task.project['prava'])
	  self.ws.write(self.result, 23, re.findall('http://dom.(.*?)/',task.url)[0].replace('hel','domchel'))
	  self.ws.write(self.result, 30, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 9, oper)
	  print('*'*100)	
	  #print self.sub
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size()) 
	  print oper
	  print('*'*100)
	  self.result+= 1
	  
	  
	  #if int(self.result) >= int(self.num) - 1:
		    #self.stop()
   

bot = Region_Zem(thread_number=5,network_try_limit=1000)
#bot.setup_queue('mongo', database='Rugion',host='192.168.10.200')
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')   
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
bot.workbook.close()
print('Done')
     
