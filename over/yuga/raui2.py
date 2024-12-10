#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
import re
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



workbook = xlsxwriter.Workbook(u'com/Raui_Коммерческая_Аренда.xlsx')

operacia = u'Аренда'

class Farpost_Com(Spider):
     def prepare(self):
	  #self.f = page
	  for p in range(1,5):
	       try:
		    #time.sleep(1)
		    g = Grab()
		    g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
		    g.go('https://raui.ru/snyat-office-sklad')
		    print g.response.code
		    if g.response.code ==200:
			 self.num = re.sub('[^\d]','',g.doc.select(u'//a[@class="pagging__link dotts"]/following::li[1]/a/span').text())
			 print 'OK'
			 del g
			 break
	       except(GrabTimeoutError,GrabNetworkError,IndexError,KeyError,AttributeError,GrabConnectionError):
		    print g.config['proxy'],'Change proxy'
		    g.change_proxy()
		    del g
		    continue
      
	  
	  
	  print self.num
	  
	  
	  
	  self.ws = workbook.add_worksheet(u'raui')
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
	  for x in range(1,int(self.num)+1):
	       yield Task ('post',url='https://raui.ru/snyat-office-sklad?page=%d'%x,refresh_cache=True,network_try_count=100)
	  
	   
  
	       
			      
     def task_post(self,grab,task):    
	  for elem in grab.doc.select(u'//a[contains(text(),"Подробнее")]'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)

     def task_item(self, grab, task):
	 
	  try:
	       sub= grab.doc.select(u'//div[@class="breadcrumbs"]/div/a[2]').text()
	  except IndexError:
	       sub =''	 
	  try:
	       try:
	            ray = grab.doc.select(u'//div[@class="breadcrumbs"]/div/a[contains(text()," район")]').text()
	       except IndexError:
		    ray = grab.doc.select(u'//div[@class="breadcrumbs"]/div/a[contains(text()," округ ")]').text()
	  except IndexError:
	       ray = ''          
	  try:
	       if sub == u'Москва':
		    punkt= u'Москва'
	       elif sub == u'Санкт-Петербург':
	            punkt= u'Санкт-Петербург'
	       elif sub == u'Севастополь':
	            punkt= u'Севастополь'
	       else:
		    punkt= grab.doc.select(u'//div[@class="breadcrumbs"]/div/a[4]').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       ter= grab.doc.select(u'//div[contains(text(),"Район")]/following-sibling::div/span').text()
	  except IndexError:
	       ter =''
	       
	  try:
	       try:
	            uliza = grab.doc.select(u'//span[@class="right"]/a[contains(@href, "ulitsy")]').text()
	       except IndexError:
		    uliza = grab.doc.select(u'//span[@class="right"]/a[contains(@href, "goroda")]/following-sibling::text()').text().split(', ')[1]
          except IndexError:
	       uliza = ''
	       
          try:
	       try:
                    dom = grab.doc.select(u'//span[@class="right"]/a[contains(@href, "doma")]').text()
	       except IndexError:
		    dom = grab.doc.select(u'//span[@class="right"]/a[contains(@href, "goroda")]/following-sibling::text()').text().split(', ')[2]
          except (IndexError,AttributeError):
               dom = ''
	       
	  try:
	       trassa = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a').text().replace(u'Продажа ','').replace(u'Аренда ','')#.split(', ')[0]
		#print rayon
	  except IndexError:
	       trassa = ''
	       
	  try:
	       udal = grab.doc.select(u'//meta[@name="keywords"]').attr('content').split(u' снять')[0]
	  except IndexError:
	       udal = ''
          try:
               seg = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"flatType")]').text()#.split(', ')[1]
          except IndexError:
               seg = ''	       
	       
	  try:
               price = grab.doc.select(u'//div[@class="item__price"]').text()#.replace(u'a',u'р.')
	  except IndexError:
	       price = ''
	       
	  try:
	       plosh = grab.doc.select(u'//td[contains(text(),"Площадь:")]/following-sibling::td').text()
	  except IndexError:
	       plosh = '' 
	  try:
	       cena_za = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"priceFor")]').text().replace(u'квадратный метр',u'м2').replace(u'все помещение','')
	  except IndexError:
	       cena_za = '' 
	       
	  
	  try:
	       ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
	  except IndexError:
	       ohrana =''
	  try:
	       gaz = grab.doc.select(u'//span[contains(text(),"Те­ле­фон")]/following-sibling::span').text()
	  except IndexError:
	       gaz =''
	  try:
	       voda = re.findall('tel="(.*?)"',grab.response.body)[0]
	  except IndexError:
	       voda =''
	  try:
	       kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	  except IndexError:
	       kanal =''
	  try:
	       elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	  except IndexError:
	       elek =''
	  try:
	       teplo = grab.doc.select(u'//h1').text()
	  except IndexError:
	       teplo =''  
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="item-text"]').text() 
	  except IndexError:
	       opis = ''
	       
	 	       
	  
	  try:
	       #oper = grab.doc.select(u'//meta[@name="description"]').attr('content').split(' ')[0]
	       oper = operacia
	  except IndexError:
	       oper = ''
	       
	  try:
	       data= grab.doc.select(u'//meta[@property="article:published_time"]').attr('content')[:10].replace('-','.')
	  except IndexError:
	       data = ''
	       
	  id_phone = re.sub('[^\d]','',grab.doc.select(u'//div[@class="item__number"][contains(text(),"Объявление ")]').text())
	  
	  phone_url = 'https://raui.ru/ajax/item/contact?id='+id_phone 
	  
	  headers ={'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Content-Length': '10',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie': 'session=aqq75kqhsmbegk00crvocv86t2',
                    'Host': 'raui.ru',
                    'Referer': task.url,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0', 
                    'X-Requested-With': 'XMLHttpRequest'}
	  g2 = grab.clone(headers=headers,proxy_auto_change=True)
     
	  for ph in range(1,5):
	       try:               
		    #time.sleep(1)
		    g2.request(post=[('id', id_phone)],headers=headers,url=phone_url)
		    
		    #print g2.response.body
		    #phone =  re.sub('[^\d\+]','',re.findall('em class=(.*?)/em>',g2.response.body)[0]) 
		    phone =  re.sub('[^\d\+]','',g2.response.json["contacts"]["phone"])
		    print 'Phone-OK'
		    del g2
		    break  
	       except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError):
		    g2.change_proxy()
		    print 'Change proxy'+' : '+str(ph)+' / 5'
		    g2 = grab.clone(headers=headers,timeout=2, connect_timeout=2,proxy_auto_change=True) 
	  else:
	       try:
		    phone = grab.doc.select(u'//div[@class="item-contacts-values"]/div').text()
	       except IndexError:
		    phone = ''	 	  
		    
	  
						   
	       
	  projects = {'url': task.url,
                      'rayon': ray,
	              'sub': sub,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal.split(u' купить')[0],
	              'segment': seg,
                      'cena': price,
                      'plosh':plosh,
	              #'etah':ets,
	              #'god':god,
	              #'mat':mat,
	              #'sostoyanie':sost,
                      'cena_za': cena_za.replace(u' в ',u'/'),
                      'ohrana':ohrana,
	              'phone':phone,
                      'gaz': gaz,
                      'voda': voda,
                      'kanaliz': kanal,
                      'electr': elek,
                      'teplo': teplo,
                      'opis':opis,
                      'operazia':oper,
                      'data':data }
	  
	  
	  
	  yield Task('write',project=projects,grab=grab)
            
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
	  print  task.project['segment']
	  print  task.project['cena']
	  print  task.project['plosh']
	  #print  task.project['etah']
	  #print  task.project['god']
	  #print  task.project['mat']
	  #print  task.project['sostoyanie']
	  print  task.project['ohrana']
	  print  task.project['gaz']
	  print  task.project['voda']
	  print  task.project['kanaliz']
	  print  task.project['electr']
	  print  task.project['opis']
	  print task.project['url']
	  print  task.project['phone']
	  #print  self.phone
	  print  task.project['data']
          print  task.project['teplo'].replace(task.project['udal'],'')
	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 7, task.project['segment'])
	  self.ws.write(self.result, 8, task.project['trassa'])
	  self.ws.write(self.result, 9, task.project['udal'])
	  self.ws.write(self.result, 5 , task.project['dom'])
	  self.ws.write(self.result, 11, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  #self.ws.write(self.result, 22, self.lico)
	  #self.ws.write(self.result, 23, task.project['electr'])
	  self.ws.write(self.result, 21, task.project['phone'])
	  self.ws.write(self.result, 19, u'RAUI')
	  self.ws.write_string(self.result, 20, task.project['url'])
	  self.ws.write(self.result, 18, task.project['opis'])
	  self.ws.write(self.result, 21, task.project['gaz'])
	  self.ws.write(self.result, 24, task.project['teplo'].replace(task.project['udal'],''))
	  self.ws.write(self.result, 29, task.project['data'])
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
	       
	       
	       
	  #if self.result > 50:
	       #self.stop()

     
bot = Farpost_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
try:
     bot.run()
except KeyboardInterrupt:
     pass
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(2)
workbook.close()
print('Done')








