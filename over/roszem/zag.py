#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
import xlsxwriter
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)





class roszem(Spider):
     def prepare(self):
	  #self.f = page
	  #self.link =l[i]
	  self.workbook = xlsxwriter.Workbook(u'zag/Roszem_Загород.xlsx')
	  self.ws = self.workbook.add_worksheet(u'roszem')
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"ТРАССА")
	  self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	  self.ws.write(0, 9, u"КАДАСТРОВЫЙ_НОМЕР_ЗЕМЕЛЬНОГО_УЧАСТКА")
	  self.ws.write(0, 10, u"ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 12, u"СТОИМОСТЬ")
	  self.ws.write(0, 13, u"ЦЕНА_М2")
	  self.ws.write(0, 14, u"ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 15, u"КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 17, u"МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 18, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 19, u"ПЛОЩАДЬ_УЧАСТКА")
	  self.ws.write(0, 20, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  self.ws.write(0, 21, u"ГАЗОСНАБЖЕНИЕ")
	  self.ws.write(0, 22, u"ВОДОСНАБЖЕНИЕ")
	  self.ws.write(0, 23, u"КАНАЛИЗАЦИЯ")
	  self.ws.write(0, 24, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  self.ws.write(0, 25, u"ТЕПЛОСНАБЖЕНИЕ")
	  self.ws.write(0, 26, u"ЛЕС")
	  self.ws.write(0, 27, u"ВОДОЕМ")
	  self.ws.write(0, 28, u"БЕЗОПАСНОСТЬ")
	  self.ws.write(0, 29, u"ОПИСАНИЕ")
	  self.ws.write(0, 30, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 31, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 32, u"ТЕЛЕФОН")
	  self.ws.write(0, 33, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 34, u"КОМПАНИЯ")
	  self.ws.write(0, 35, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 36, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 37, u"ДОРОГА")
	  self.ws.write(0, 38, u"ВИД_ПРАВА")
	  self.ws.write(0, 39, u"МЕСТОПОЛОЖЕНИЕ")
	  
	  self.result= 1 
	  
	  
     def task_generator(self):
	  for x in range(1,210):#217
	       yield Task ('post',url='http://www.roszem.ru/search?page=%d'%x+'&sort=date_sort&type=Cottage',refresh_cache=True,network_try_count=100)
	  #yield Task ('post',url='http://www.roszem.ru/land/',refresh_cache=True,network_try_count=100) 
     
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//td[@class="photo"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur	      
	       yield Task('item',url=ur,network_try_count=100,use_proxylist=False)
	               
               
               
               
     def task_item(self, grab, task):
	  
	 
	  try:
               sub = grab.doc.select(u'//nav[@class="wrapper"]/a[3]').text().replace(u'г. ','')
	  except IndexError:
	       sub=''
          try:
               ray = grab.doc.select(u'//nav[@class="wrapper"]/a[contains(text(),"район")]').text()
          except IndexError:
               ray = ''
	       
          try:
               ra = grab.doc.select(u'//p[@class="location"]').text()
	       punkt = ra.split(', ')[len(ra.split(','))-1]
               if ra.find(u'шоссе')>=0:
                    trassa = ra.split(', ')[0].split(' (')[0]
                    ter=''
	       else:
                    ter = ra.split(', ')[0]
                    trassa=''
               i=0
               for w in ra.split(','):
                    i+=1
                    if w.find(u'км от города')>=0:
                         udal = ra.split(', ')[i-1].replace(u' города','')
                         break
               if w.find(u'км от города')<0:
		    udal =''
          except IndexError:
               ra = ''
	       ter=''
	       trassa=''
	       udal =''
	       punkt=''
          try:
               price = grab.doc.select(u'//p[@class="price"]').text()
          except IndexError:
               price = ''
          try:
               price_sot = grab.doc.select(u'//th[@class="price_per"][contains(text(),"Цена за сотку")]/following::p[@class="price"][2]').text()
          except IndexError:
               price_sot = ''
          try:
               plosh_ob = grab.doc.select(u'//p[@class="square t-center"]').text().split(' / ')[1]
          except IndexError:
               plosh_ob = ''
          try:
               et = grab.doc.select(u'//h3[contains(text(),"Дом")]').number()
          except IndexError:
               et = ''
          try:
	       m = grab.doc.select(u'//dt[contains(text(),"Технические данные:")]/following-sibling::dd').text()
	       t=0
	       for w in m.split(','):
	            t+=1
	            if w.find(u'стены')>=0:
		         mat = m.split(', ')[t-1].replace(u'стены ','')
		         break
	       if w.find(u'стены')<0:
	            mat =''
	  except IndexError:
	       mat = ''
          try:
               g = grab.doc.select(u'//dt[contains(text(),"Технические данные:")]/following-sibling::dd').text()
               t=0
               for w in g.split(','):
                    t+=1
                    if w.find(u'год постройки')>=0:
                         god = g.split(', ')[t-1].replace(u'год постройки ','')
                         break
               if w.find(u'год постройки')<0:
                    god =''
          except IndexError:
               god = ''
          try:
               plosh_uh = grab.doc.select(u'//p[@class="square t-center"]').text().split(' / ')[0]
          except IndexError:
               plosh_uh = ''	       
          try:
	       gaz = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"газ")]').text().replace(u'есть газ',u'есть').replace(u'нет газа','')
	  except IndexError:
	       gaz =''
	  try:
	       voda = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"водоснабжение")]').text().replace(u'есть водоснабжение',u'есть').replace(u'нет водоснабжения','')
	  except IndexError:
	       voda =''
	  try:
	       kanal = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"канализация")]').text().replace(u'есть канализация',u'есть').replace(u'нет канализации','')
	  except IndexError:
	       kanal =''
	  try:
	       elekt = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"электричество")]').text().replace(u'есть электричество',u'есть').replace(u'нет электричества','')
	  except IndexError:
	       elekt =''
          try:
               teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
          except IndexError:
               teplo =''
          try:
               ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
          except IndexError:
               ohrana =''
          try:
               les = grab.doc.select(u'//p[@class="location"]').text()
          except IndexError:
               les =''
          try:
               vodoem = re.sub(u'^.*(?=озер)','', grab.doc.select(u'//*[contains(text(), "озер")]').text())[:4].replace(u'озер',u'есть')
          except IndexError:
               vodoem =''
          try:
               opis = grab.doc.select(u'//h3[contains(text(),"Описание")]/following-sibling::p').text() 
          except IndexError:
               opis = ''
          try:
               phone = re.sub('[^\d\+\,]','',grab.doc.select(u'//dt[contains(text(),"Телефон")]/following-sibling::dd').text())
          except IndexError:
               phone = ''
          try:
               lico = grab.doc.select(u'//dt[contains(text(),"Продавец")]/following-sibling::dd').text()
          except IndexError:
               lico = ''
          try:
               data = re.sub(u'^.*Размещен ','',grab.doc.select(u'//p[@class="id"]').text()).replace(')','')
          except IndexError:
               data = ''
          try:
               doroga = grab.doc.select(u'//dt[contains(text(),"Транспортная доступность:")]/following-sibling::dd').text()
          except IndexError:
               doroga = ''
          try:
               pravo = grab.doc.select(u'//dt[contains(text(),"Вид права:")]/following-sibling::dd').text()
          except IndexError:
               pravo = ''
	       
	       
	       
                       
	  projects = {'url': task.url,
	              'sub':sub,
	              'rayon': ray,
	              'punkt': re.sub('[0-9]', u'',punkt).replace(u'км от города','').replace(u'(МКАД)','').replace(u'шоссе',''),
	              'teritory':re.sub('[0-9]', u'',ter).replace(u'км от города','').replace(u'(МКАД)',''),
	              'trassa': trassa,
	              'udal': udal,
	              'price': price,
	              'price_sot': price_sot,
	              'ploshad': plosh_ob,
	              'et': et,
	              'mat': mat,
	              'god_postr': god,
	              'ploshad1': plosh_uh,
	              'gaz': gaz,
	              'voda':voda,
	              'kanal': kanal,
	              'elekt': elekt,
	              'teplo': teplo,
	              'ohrana': ohrana,
	              'les': les,
	              'vodoem':vodoem,	              
	              'opis': opis,
	              'phone': phone,
	              'lico':lico,
	              'dataraz': data,
	              'doroga': doroga,
	              'pravo': pravo
	              }
		          
	       
	       
	  yield Task('write',project=projects,grab=grab)
          
          
          
          
          
     def task_write(self,grab,task):
	       
	  print('*'*100)
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritory']
	  print  task.project['trassa']
	  print  task.project['udal']
	  print  task.project['price']
	  print  task.project['price_sot']
	  print  task.project['ploshad']
	  print  task.project['et']
	  print  task.project['mat']
	  print  task.project['god_postr']
	  print  task.project['ploshad1']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanal']
	  print  task.project['elekt']	  
	  print  task.project['teplo']
          print  task.project['ohrana']
	  print  task.project['les']
	  print  task.project['vodoem']	  
          print  task.project['opis']
          print task.project['url']
          print  task.project['phone']
          print  task.project['lico']
          print  task.project['dataraz']
	  print  task.project['doroga']
	  print  task.project['pravo']	  
	      
	      
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritory'])
	  #self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 7, task.project['trassa'])
	  self.ws.write(self.result, 8, task.project['udal'])
	  #self.ws.write(self.result, 9, u'Продажа')
	  self.ws.write(self.result, 10, u'Коттедж')
	  self.ws.write(self.result, 11, u'Продажа')
	  self.ws.write(self.result, 12, task.project['price'])
	  self.ws.write(self.result, 13, task.project['price_sot'])
	  self.ws.write(self.result, 14, task.project['ploshad'])
	  #self.ws.write(self.result, 15, task.project['gaz'])
	  self.ws.write(self.result, 16, task.project['et'])
	  self.ws.write(self.result, 17, task.project['mat'])
	  self.ws.write(self.result, 18, task.project['god_postr'])
	  self.ws.write(self.result, 19, task.project['ploshad1'])
	  self.ws.write(self.result, 21, task.project['gaz'])
	  self.ws.write(self.result, 22, task.project['voda'])
	  self.ws.write(self.result, 23, task.project['kanal'])
	  self.ws.write(self.result, 24, task.project['elekt'])
	  self.ws.write(self.result, 25, task.project['teplo'])
	  self.ws.write(self.result, 39, task.project['les'])
	  self.ws.write(self.result, 27, task.project['vodoem'])
	  self.ws.write(self.result, 28, task.project['ohrana'])
	  self.ws.write(self.result, 29, task.project['opis'])
	  self.ws.write(self.result, 30, u'ROSZEM.RU')
	  self.ws.write_string(self.result, 31, task.project['url'])
	  self.ws.write(self.result, 32, task.project['phone'])
	  self.ws.write(self.result, 33, task.project['lico'])
	  self.ws.write(self.result, 35, task.project['dataraz'])
	  self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 37, task.project['doroga'])
	  self.ws.write(self.result, 38, task.project['pravo'])	  
	  
	 
	  print('*'*100)
	 
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  
	  print('*'*100)
	  self.result+= 1
	       
	       #if self.result > 10:
		    #self.stop()
          
               
               
          
          
    
    
    
bot = roszem(thread_number=3, network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
print('Сохранение...')
bot.workbook.close()
print('Done!')

