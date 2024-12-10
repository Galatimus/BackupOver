#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import xlsxwriter
import time
import os
import random
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'0001-0002_00_C_004-0002_NGS.xlsx') 
   

class Ngs_Com(Spider):
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
	  self.ws.write(0, 12, u"ПЛОЩАДЬ")
	  self.ws.write(0, 13, u"ЭТАЖ")
	  self.ws.write(0, 14, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 15, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 16, u"МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 17, u"ВЫСОТА_ПОТОЛКА")
	  self.ws.write(0, 18, u"СОСТОЯНИЕ")
	  self.ws.write(0, 19, u"БЕЗОПАСНОСТЬ")
	  self.ws.write(0, 20, u"ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 21, u"ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 22, u"КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 23, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 24, u"ТЕПЛОСНАБЖЕНИЕ")
	  self.ws.write(0, 25, u"ОПИСАНИЕ")
	  self.ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 28, u"ТЕЛЕФОН")
	  self.ws.write(0, 29, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 30, u"КОМПАНИЯ")
	  self.ws.write(0, 31, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 32, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 33, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 34, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 35, u"МЕСТОПОЛОЖЕНИЕ") 
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  l= open('ngs_com.txt').read().splitlines()
          self.dc = len(l)
          print self.dc
          for line in l:
	       yield Task ('item',url=line,network_try_count=100)

     def task_item(self, grab, task):
	  
	  try:
	       if 'ngs' in task.url:
		    sub = u'Новосибирская область' 
	       elif 'e1' in task.url:
		    sub = u'Свердловская область' 
	  except IndexError:
	       sub = ''	  
	  
	  try:
	       r = grab.doc.select(u'//p[@class="card__address"]').text()
	       t=0
	       for w in r.split(', '):
		    t+=1
		    if w.find(u' район')>=0:
			 ray= r.split(', ')[t-1]
			 break
		    else:
			 ray = ''
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//p[@class="card__address"]').text().replace(ray,'').replace(',','')
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//p[@class="card__reference-point"]').text().replace(u'Ориентир — ','')
	  except IndexError:
	       ter =''
	       
	  try:
	       z = grab.doc.select(u'//p[@class="card__address"]').text()
	       a=0
	       for i in z.split(', '):
		    a+=1
		    if i.find(u'ул. ')>=0:
			 uliza= z.split(', ')[a-1]
			 break
		    else:
			 uliza = ''
	  except IndexError:
	       uliza = ''
	       
	       
	  try:
	       d = grab.doc.select(u'//p[@class="card__address"]').text()
	       m=0
	       for h in d.split(', '):
		    m+=1
		    if h.find(u'д. ')>=0:
			 dom= d.split(', ')[m-1].replace(u'д. ','')
			 break
		    else:
			 dom = ''
	  except IndexError:
	       dom = ''  
	  try:
	       trassa = grab.doc.select(u'//li[@class="sas-breadcrumbs__item"]/a[contains(@href,"type")]').text()
		#print rayon
	  except DataNotFound:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//td[contains(text(),"Класс:")]/following-sibling::td').text()
	  except DataNotFound:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//p[@class="card__cost"]').text()
	  except DataNotFound:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//dd[@class="sms-card-list__value"]').text()
	  except DataNotFound:
	       plosh = ''
	  try:
	       vid = grab.doc.select(u'//td[contains(text(),"Тип:")]/following-sibling::td').text()
	  except DataNotFound:
	       vid = '' 
	  try:
	       et = grab.doc.select(u'//dt[contains(text(),"Этаж")]/following-sibling::dd').text()
	  except IndexError:
	       et = ''
	  try:
	       et2 = grab.doc.select(u'//td[contains(text(),"Этаж/этажей:")]/following-sibling::td').text().split('/')[1]
	  except IndexError:
	       et2 = ''
	  
	  try:
	       mat = grab.doc.select(u'//p[@class="card__price"]').text().replace(u' м2','')
	  except IndexError:
	       mat = ''
	  try:
	       godp = grab.doc.select(u'//dt[contains(text(),"Год постройки")]/following-sibling::dd').text()
	  except IndexError:
	       godp = ''	       
	       
	       
	  try:
	       ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
	  except DataNotFound:
	       ohrana =''
	  try:
	       gaz = re.sub(u'^.*(?=газ)','', grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
	  except DataNotFound:
	       voda =''
	  try:
	       kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	  except DataNotFound:
	       kanal =''
	  try:
	       elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	  except DataNotFound:
	       elek =''
	  try:
	       teplo = grab.doc.select(u'//p[@class="card__address"]').text()
	  except IndexError:
	       teplo =''
	       
	  try:
	       oper = grab.doc.select(u'//h1').text().split(' - ')[1].split(' ')[0].replace(u'Продам',u'Продажа').replace(u'Сдам',u'Аренда') 
	  except IndexError:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="card__comments-section"]').text().replace(u'Комментарий ','') 
	  except IndexError:
	       opis = ''
	       
	  try:
	       phone = re.sub('[^\d]','',grab.doc.select(u'//div[@class="card__phones-container"]/span').text()+str(random.randint(100,999)))
	  except IndexError:
	       phone = ''
	       
	  try:
	       try: 
		    lico = grab.doc.select(u'//span[@class="card__author-name"]').text()
	       except IndexError:
		    lico = grab.doc.select(u'//a[@class="re-link card__author-name card__author-name_has-count-bubble"]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//strong[@class="organization-informer__title"]/a').text()
	  except IndexError:
	       comp = ''
	       
	  try:
	       data= grab.doc.select(u'//span[@class="card__publication-date"][2]').text()
	  except IndexError:
	       data = ''
	  try:
	       data1 = grab.doc.select(u'//span[@class="card__publication-date"][1]').text()
	  except IndexError:
	       data1 = ''	       
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt.replace(uliza,'').replace(dom,'').replace(u'д. ',''),
                      'teritor': ter,
                      'ulica': uliza,
                      'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
                      'et': et,
                      'ets': et2,
                      'mat': mat,
                      'god':godp,
                      'vid': vid,
                      'ohrana':ohrana,
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
                      'data1':data1,
                      'oper':oper
                      }
	  
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
	    
     def task_write(self,grab,task):
	  if task.project['teplo'] <> '':
	       print('*'*50)
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['punkt']
	       print  task.project['teritor']
	       print  task.project['ulica']
	       print  task.project['dom']
	       print  task.project['trassa']
	       print  task.project['udal']
	       print  task.project['cena']
	       print  task.project['plosh']
	       print  task.project['et']
	       print  task.project['ets']
	       print  task.project['mat']
	       print  task.project['god']
	       print  task.project['vid']
	       print  task.project['ohrana']
	       print  task.project['gaz']
	       print  task.project['voda']
	       print  task.project['kanaliz']
	       print  task.project['electr']
	       print  task.project['opis']
	       print task.project['url']
	       print  task.project['phone']
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.project['data']
	       print  task.project['data1']
	       print  task.project['teplo']
	       
	       #global result
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 6, task.project['teritor'])
	       self.ws.write(self.result, 4, task.project['ulica'])
	       self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 9, task.project['trassa'])
	       self.ws.write(self.result, 10, task.project['udal'])
	       self.ws.write(self.result, 33, task.project['oper'])
	       self.ws.write(self.result, 11, task.project['cena'])
	       self.ws.write(self.result, 12, task.project['plosh'])
	       self.ws.write(self.result, 13, task.project['et'])
	       self.ws.write(self.result, 14, task.project['ets'])
	       self.ws.write(self.result, 15, task.project['god'])
	       self.ws.write(self.result, 34, task.project['mat'])	  
	       self.ws.write(self.result, 18, task.project['vid'])
	       self.ws.write(self.result, 20, task.project['gaz'])
	       self.ws.write(self.result, 21, task.project['voda'])
	       self.ws.write(self.result, 22, task.project['kanaliz'])
	       self.ws.write(self.result, 23, task.project['electr'])
	       self.ws.write(self.result, 35, task.project['teplo'])
	       self.ws.write(self.result, 19, task.project['ohrana'])	       
	       self.ws.write(self.result, 25, task.project['opis'])
	       self.ws.write(self.result, 26, u'НГС.НЕДВИЖИМОСТЬ')
	       self.ws.write_string(self.result, 27, task.project['url'])
	       self.ws.write(self.result, 28, task.project['phone'])
	       self.ws.write(self.result, 29, task.project['lico'])
	       self.ws.write(self.result, 30, task.project['company'])
	       self.ws.write(self.result, 31, task.project['data'])
	       self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
	       self.ws.write(self.result, 34, task.project['data1'])
	       print('*'*50)
	       #print task.sub
	       
	       print 'Ready - '+str(self.result)+'/'+str(self.dc)
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print  task.project['oper']
	       print('*'*50)	       
	       self.result+= 1
	       
	       #if self.result >= 5:
		    #self.stop()	       
	       
	 

     
bot = Ngs_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=500)
bot.run()
print('Wait 2 sec...')
time.sleep(1)
print('Save it...')
workbook.close()
print('Done')
 
     
     
     
     
     
     
     
