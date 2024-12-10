#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'ADVECS.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"№")
	  self.ws.write(0, 1, u"Район")
	  self.ws.write(0, 2, u"Метро")
	  self.ws.write(0, 3, u"До метро")
	  self.ws.write(0, 4, u"Адрес")
	  self.ws.write(0, 5, u"Название_ЖК")
	  self.ws.write(0, 6, u"Тип дома / Здание")
	  self.ws.write(0, 7, u"Тип сделки")
	  self.ws.write(0, 8, u"Этаж/Этажность")
	  self.ws.write(0, 9, u"Фонд")
	  self.ws.write(0, 10, u"Кол-во комнат")
	  self.ws.write(0, 11, u"Площадь общая")
	  self.ws.write(0, 12, u"Площадь жилая")
	  self.ws.write(0, 13, u"Площадь комнат")
	  self.ws.write(0, 14, u"Площадь кухни")
	  self.ws.write(0, 15, u"Санузлов")
	  self.ws.write(0, 16, u"Санузлы")
	  self.ws.write(0, 17, u"Балкон")
	  self.ws.write(0, 18, u"Пол")
	  self.ws.write(0, 19, u"Ремонт")
	  self.ws.write(0, 20, u"Вход")
	  self.ws.write(0, 21, u"Вид из окон")
	  self.ws.write(0, 22, u"Цена")
	  self.ws.write(0, 23, u"Бюджет")
	  self.ws.write(0, 24, u"Арендная плата")
	  self.ws.write(0, 25, u"Описание")
	  self.ws.write(0, 26, u"Источник")
	  self.ws.write(0, 27, u"Ссылка")
	  
	       
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  yield Task ('post',url='http://www.advecs.com/elite/',network_try_count=100)
	       
	       
     def task_post(self,grab,task):
	  for elem in grab.doc.select('//div[@class="inf"]/preceding-sibling::a'):
	       ur = grab.make_url_absolute(elem.attr('href'))
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True, network_try_count=100)	       
                
     def task_item(self, grab, task):
	  try:
	       #dt = grab.doc.select(u'//div[contains(text(),"Город:")]/span').text()
	       sub = u'Санкт-Петербург'#reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	  except DataNotFound:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//b[contains(text(),"Район")]/following-sibling::text()[1]').text().replace(': ','').replace(',','')
	     #print ray 
	  except DataNotFound:
	       ray = ''          
	  try:
	       #if  grab.doc.select(u'//em/a[2][contains(text(),"р-н")]').exists()==True:
	       punkt= grab.doc.select(u'//b[contains(text(),"Метро")]/following-sibling::text()[1]').text().split(' (')[0].replace(': ','').replace(',','')
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').exists()==True:
	       ter= grab.doc.select(u'//b[contains(text(),"Метро")]/following-sibling::text()[1]').text().split(' (')[1].replace(')','')
	       #else:
		    #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//div[@class="addr"]').text()#.split(', ')[0]
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//strong[contains(text(),"Здание:")]/following-sibling::text()[1]').text()
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//b[contains(text(),"Тип сделки")]/following-sibling::text()[1]').text().replace(': ','').replace(',','')
		#print rayon
	  except DataNotFound:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//strong[contains(text(),"Этаж:")]/following-sibling::text()[1]').text()
	  except DataNotFound:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//strong[contains(text(),"S общ.")]/following-sibling::text()[1]').text().replace('— ','')
	  except DataNotFound:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//strong[contains(text(),"S жил.")]/following-sibling::text()[1]').text().replace('— ','')
	  except DataNotFound:
	       plosh = ''
	  
	  try:
	       lin = []
               for em in grab.doc.select(u'//strong[contains(text(),"S комнат")]/following-sibling::text()'):
	            urr = em.text().replace('— ','')
	            lin.append(urr)
               et = "".join(lin).split('(')[0].split('сот')[0]
	  except IndexError:
	       et = ''
	  try:
	       et2 = grab.doc.select(u'//strong[contains(text(),"S кухни")]/following-sibling::text()[1]').text().replace('— ','')
	  except IndexError:
	       et2 = ''
	  
	  try:
	       mat = grab.doc.select(u'//strong[contains(text(),"Санузел:")]/following-sibling::text()[1]').number()
	  except IndexError:
	       mat = ''
          try:
               godp = grab.doc.select(u'//strong[contains(text(),"Балкон:")]/following-sibling::text()[1]').text()
          except IndexError:
               godp = ''	       
	       
	       
	  try:
	       ohrana = grab.doc.select(u'//strong[contains(text(),"Пол:")]/following-sibling::text()[1]').text()
	  except DataNotFound:
	       ohrana =''
	  try:
	       gaz = grab.doc.select(u'//strong[contains(text(),"Ремонт:")]/following-sibling::text()[1]').text()
	  except DataNotFound:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//strong[contains(text(),"Вход:")]/following-sibling::text()[1]').text()
	  except DataNotFound:
	       voda =''
	  try:
	       kanal = grab.doc.select(u'//strong[contains(text(),"Вид из окон:")]/following-sibling::text()[1]').text()
	  except DataNotFound:
	       kanal =''
	  try:
	       elek =  grab.doc.select(u'//div[@class="ss"]/b').text().split(', ')[1]
	  except DataNotFound:
	       elek =''
	  try:
	       teplo = re.sub('[^\d]', u'',grab.doc.select(u'//div[@class="ss"]/b').text().split(', ')[0])
	  except IndexError:
	       teplo =''
	       
	  try:
	       if 'мес' in price:
		    oper = u'Аренда'#grab.doc.select(u'//label[contains(text(),"Тип операции:")]/following-sibling::span').text().replace(u'Сдам',u'Аренда').replace(u'Спрос',u'Аренда').replace(u'Продам',u'Продажа') 
	       else:
		    oper = u'Продажа'
	  except IndexError:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="anons"]/div').text()#.replace(u'Описание','')  
	  except IndexError:
	       opis = ''
	       
	  try:
	       #try: 
	       phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//div[@class="serif bigFont"]').text())
	       #except IndexError:
		    #phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//a[@class="mobile"]/@href').text())
	  except IndexError:
	       phone = ''
	       
	  try:
	        
	       lico = grab.doc.select(u'//strong[contains(text(),"Агент")]/following-sibling::a[1]').text()
	       #except IndexError:
		    #lico = grab.doc.select(u'//td[contains(text(),"Агент:")]/following-sibling::td').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = u'Адвекс'#grab.doc.select(u'//div[@class="avtor"]/a[contains(@href, "firma")]/h4').text()#.split(' :: ')[0]
	  except IndexError:
	       comp = ''
	       
	  try:
	       data = re.sub('[^\d\.]', u'',grab.doc.select(u'//td[@id="right"]/div[1]').text().split(', ')[0])
	  except IndexError:
	       data = ''
	       
	  try:
	       vid = re.sub('[^\d\.]', u'',grab.doc.select(u'//td[@id="right"]/div[1]').text().split(', ')[1])
	  except DataNotFound:
	       vid = '' 	       
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
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
                      'oper':oper
                      }
          
	  yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     def task_write(self,grab,task):
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
	  print  task.project['ohrana']
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
	  print  task.project['vid']
	  print  task.project['oper']
	  
	  #global result
	  self.ws.write(self.result, 0,self.result)
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 6, task.project['dom'])
	  self.ws.write(self.result, 7, task.project['trassa'])
	  self.ws.write(self.result, 8, task.project['udal'])
	  #self.ws.write(self.result, 34, task.project['oper'])
	  self.ws.write(self.result, 11, task.project['cena'])
	  self.ws.write(self.result, 12, task.project['plosh'])
	  self.ws.write(self.result, 13, task.project['et'])
	  self.ws.write(self.result, 14, task.project['ets'])
	  self.ws.write(self.result, 17, task.project['god'])
	  self.ws.write(self.result, 15, task.project['mat'])	  
	  self.ws.write(self.result, 32, task.project['vid'])
	  self.ws.write(self.result, 19, task.project['gaz'])
	  self.ws.write(self.result, 20, task.project['voda'])
	  self.ws.write(self.result, 21, task.project['kanaliz'])
	  self.ws.write(self.result, 22, task.project['electr'])
	  self.ws.write(self.result, 10, task.project['teplo'])
	  self.ws.write(self.result, 18, task.project['ohrana'])	       
	  self.ws.write(self.result, 25, task.project['opis'])
	  self.ws.write(self.result, 26, u'АН "Адвекс"')
	  self.ws.write_string(self.result, 27, task.project['url'])
	  #self.ws.write(self.result, 28, task.project['phone'])
	  #self.ws.write(self.result, 29, task.project['lico'])
	  #self.ws.write(self.result, 30, task.project['company'])
	  #self.ws.write(self.result, 31, task.project['data'])
	  #self.ws.write(self.result, 33, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	  #if self.result >= 10:
	       #self.stop()	       	       
	 

     
bot = Cian_Zem(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
try:
     command = 'mount -t cifs //192.168.1.6/d /home/oleg/pars -o _netdev,sec=ntlm,auto,username=oleg,password=1122,file_mode=0777,dir_mode=0777'
     os.system('echo %s|sudo -S %s' % ('1122', command))
     time.sleep(10)
     workbook.close()
     print('Done')
except IOError:
     time.sleep(30)
     os.system('echo %s|sudo -S %s' % ('1122', 'mount -a'))
     time.sleep(10)
     workbook.close()
     print('Done!')
print('Done!') 







