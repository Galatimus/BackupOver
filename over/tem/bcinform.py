#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
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



workbook = xlsxwriter.Workbook(u'0001-0019_00_C_001-0217_BCINF.xlsx')


class Farpost_Com(Spider):
     def prepare(self):
	  #self.f = page
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
	  #self.r = conv     
	       
	  self.result= 1
	
	       
    
     def task_generator(self):
	  
	  
	  #for x in range(438):#438
	       #yield Task ('post',url='https://bcinform.moscow/arenda-ofisa/?p=%d'%x,refresh_cache=True,network_try_count=100)
	  for x1 in range(5):#1500
	       yield Task ('post',url='http://bcinform.ru/spb/?p=%d'%x1,refresh_cache=True,network_try_count=100)

	  
			      
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//h6[@class="nameSS"]/ancestor::a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)

     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//span[@class="nav-header__location"]').text()
	  except IndexError:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//h1').text()
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= sub #grab.doc.select(u'//span[@itemprop="addressLocality"]').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//span[@class="areaObjectCardEl"]/a[contains(text(),"р-н")]').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       
	       uliza = grab.doc.select(u'//span[@itemprop="streetAddress"]').text()
	  except IndexError:
	       uliza = ''
	       
          try:
               dom = grab.doc.select(u'//meta[@name="geo.position"]/@content').text().split(';')[0]
          except IndexError:
               dom = ''
	       
	  try:
	       trassa = grab.doc.select(u'//div[@class="areaObjectCardBlock"]/following-sibling::a[contains(text(),"БЦ")]').text()
		#print rayon
	  except IndexError:
	       trassa = ''
	       
	  try:
	       if punkt == u'Москва':
		    udal = grab.doc.select(u'//ul[@class="breadcrumb"]/li[2]/span/a').text()
	       else:
		    udal = grab.doc.select(u'//ul[@class="breadcrumb"]/li[3]/span/a').text()
	  except IndexError:
	       udal = ''
          try:
	       if punkt == u'Москва':
                    seg = grab.doc.select(u'//div[contains(text(),"Площадь")]/following-sibling::div').text().replace(u'Цена ','')
	       else:
		    seg = grab.doc.select(u'//div[contains(text(),"Площадь")]/following-sibling::div[2]').text()
          except IndexError:
               seg = ''	       
	       
	  try:
	       if punkt == u'Москва':
	            price = grab.doc.select(u'//div[@class="row"][2]/div[3]').text()
	       else:
		    price = grab.doc.select(u'//div[@class="row"][2]/div[4]').text()
	  except IndexError:
	       price = ''
	       
	  try:
	       plosh = grab.doc.select(u'//div[contains(text(),"Площадь")]/following::div[@class="row"][1]/div[2]').text()
	  except IndexError:
	       plosh = '' 
	  try:
	       ets = grab.doc.select(u'//div[contains(text(),"Этаж")]/following::div[@class="row"][1]/div[1]').number()
	  except IndexError:
	       ets = '' 

	  try:
	       ohrana = grab.doc.select(u'//meta[@name="geo.placename"]/@content').text()
	  except IndexError:
	       ohrana =''
	  try:
	       gaz = grab.doc.select(u'//meta[@name="geo.position"]/@content').text().split(';')[1]
	  except IndexError:
	       gaz =''
	  try:
	       voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
	  except IndexError:
	       voda =''
	  try:
	       elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	  except IndexError:
	       elek =''
	  try:
	       teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	  except IndexError:
	       teplo =''  
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="description"]').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
	       phone =re.sub('[^\d\+]','',grab.doc.select(u'//div[@id="objectNumberPhone"]/strong').text())
	       #phone = grab.doc.rex_text(u'telephone(.*?)showPhonesHideLink')
	  except IndexError:
	       phone = ''
	       
	  try:
	       lico = grab.doc.select(u'//span[@class="stationMetroObject"]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//span[@class="timeToStationMetroObject"]').number()
	  except IndexError:
	       comp = ''
	  try:
	       try:
	            oper = grab.doc.select(u'//h1').text().split(' ')[0]
	       except IndexError:
		    oper = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a[contains(@href,"garage")]').text().split(' ')[0]
	  except IndexError:
	       oper = ''
	       
	  try:
	       data= grab.doc.select(u'//div[@class="lastModify"]').text().replace(u'Данные обновлены ','').split(' ')[0].replace(u'-','.')
	  except IndexError:
	       data = ''
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
	              'segment': seg,
                      'cena': price,
                      'plosh':plosh,
	              'etah':ets,
                      'ohrana':ohrana,
                      'gaz': gaz,
                      'voda': voda,
                      'electr': elek,
                      'teplo': teplo,
                      'opis':opis,
                      'phone':phone,
                      'lico':lico,
                      'company':comp,
	              'operazia':oper,
                      'data':data }
	  
	  try:
	       if punkt == u'Москва':
	            link = 'http://bcinform.moscow/'+grab.doc.select(u'//div[@class="areaObjectCardBlock"]/following-sibling::a').attr('href')
	       else:
		    link = 'http://bcinform.ru/'+grab.doc.select(u'//div[@class="areaObjectCardBlock"]/following-sibling::a').attr('href')
	       gr = Grab()
	       gr.setup(url=link)
	       yield Task('class',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
	  except IndexError:
	       yield Task('class',grab=grab,project=projects)	  
	  
	  
     def task_class(self, grab, task):
	  try:
	       klass = grab.doc.select(u'//span[@class="classOfObject classObjectA"]/a').text()
	  except IndexError:
	       klass = ''
	  #print klass
	  yield Task('write',project=task.project,klass=klass,grab=grab)
            
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
	  print  task.project['cena']+' '+task.project['segment']
	  print  task.project['plosh']
	  print  task.project['etah']	  
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['electr']
	  print  task.project['teplo']
	  print  task.project['opis']
	  print  task.klass
	  print task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['data']
	  print  task.project['ohrana']

	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 33, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  #self.ws.write(self.result, 7, task.project['segment'])
	  self.ws.write(self.result, 8, task.project['trassa'])
	  self.ws.write(self.result, 9, task.project['udal'])
	  self.ws.write(self.result, 34, task.project['dom'])
	  self.ws.write(self.result, 11, task.project['cena']+' '+task.project['segment'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  self.ws.write(self.result, 15, task.project['etah'])
	  #self.ws.write(self.result, 15, task.project['god'])
	  #self.ws.write(self.result, 16, task.project['mat'])
	  self.ws.write(self.result, 10, task.klass)
	  #self.ws.write(self.result, 18, task.project['sostoyanie'])
	  self.ws.write(self.result, 24, task.project['ohrana'])
	  self.ws.write(self.result, 35, task.project['gaz'])
	  self.ws.write(self.result, 21, task.project['voda'])
	  #self.ws.write(self.result, 22, task.project['kanaliz'])
	  self.ws.write(self.result, 23, task.project['electr'])
	  self.ws.write(self.result, 27, task.project['company'])
	  self.ws.write(self.result, 19, u'БЦИнформ')
	  self.ws.write_string(self.result, 20, task.project['url'])
	  self.ws.write(self.result, 18, task.project['opis'])
	  self.ws.write(self.result, 21, task.project['phone'])
	  self.ws.write(self.result, 26, task.project['lico'])
	  self.ws.write(self.result, 30, task.project['data'])
	  self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 28, task.project['operazia'])
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  print  task.project['operazia']
	  print('*'*50)	       
	  self.result+= 1
	       
	       
	       
	  #if self.result > 5:
	       #self.stop()

     
bot = Farpost_Com(thread_number=1,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')
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







