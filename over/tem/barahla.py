#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import time
import requests
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'barahla_Коммерческая.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet(u'barahla_Коммерческая')
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
	  for x in range(1,20):#2265
               yield Task ('post',url='https://comrent.ru/arenda-ofisa-v-moskve?page=%d'%x,network_try_count=100)
	  
                 
        
        
            
            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//a[@class="thumb"]'):
	       ur = grab.make_url_absolute(elem.attr('href')) 
	       print ur
	       #yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	 
        
        
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//input[@name="region"][2]/following-sibling::label[1]').text().encode('cp1251')
	  except IndexError:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//div[@class="mrk badr"]/a[contains(text(),"р-н")]').text()
	     #print ray 
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//input[@name="region"][1]/following-sibling::label[1]').text().encode('cp1251')
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text()," район")]').exists()==True:
	       ter= grab.doc.select(u'//div[@class="mrk badr"]/em/a[contains(text(),"р-н")]').text()#.split(', ')[3].replace(u'улица','')
	       #else:
		    #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//div[@class="mrk badr"]/a[2]').text()#.split(', ')[0]
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//div[@class="mrk badr"]/a[2]/following-sibling::text()').number()
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//legend[@class="obj"]/a').text().replace(u'Продажа ','').replace(u'Аренда ','').split(' (')[0]
		#print rayon
	  except DataNotFound:
	       trassa = ''       
	  try:
	       udal = u'Коммерческая недвижимость'#grab.doc.select(u'//td[contains(text(),"Класс:")]/following-sibling::td').text()
	  except DataNotFound:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//legend[@class="price"]').text()
	  except DataNotFound:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//div[@class="mrk barea"]').text()
	  except DataNotFound:
	       plosh = ''
	  try:
	       vid = grab.doc.select(u'//div[@class="ipoteka"]').text()
	  except DataNotFound:
	       vid = '' 
	  try:
	       et = grab.doc.select(u'//div[@class="mrk bfloor"]').text().split('/')[0]
	  except IndexError:
	       et = ''
	  try:
	       et2 = grab.doc.select(u'//div[@class="mrk bfloor"]').text().split('/')[1].split(' ')[0]
	  except IndexError:
	       et2 = ''
	  
	  try:
	       mat = grab.doc.select(u'//div[@class="chp"]').text()
	  except IndexError:
	       mat = ''
          try:
               godp = grab.doc.select(u'//title').text()
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
	       teplo = grab.doc.select(u'//div[@class="mrk badr"]').text()
	  except IndexError:
	       teplo =''
	       
	  try:
	       oper = grab.doc.select(u'//legend[@class="obj"]/a').text().split(' ')[0] 
	  except IndexError:
	       oper = ''               
	      
		    
	  try:
	       opis = grab.doc.select(u'//div[@class="app"]/p').text() 
	  except IndexError:
	       opis = ''
	       
	  try:
               #Id = grab.doc.select(u'//span[@class="show_phone"]/a').attr('data-id')
	       #print Id
	       #headers ={'Accept': '*/*',
		         #'Accept-Encoding': 'gzip,deflate,br',
	                 #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		         #'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		         #'Cookie': 'sessid='+Id,
		         #'Host': task.url.split('.net')[0]+'.net',
		         #'Referer': task.url,
		         #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0', 
		         #'X-Requested-With': 'XMLHttpRequest'}
	       #g2 = grab.clone()
	       #for p in range(1,25):
		    #try:
			 #url1 = task.url.split('.net')[0]+'.net'+'/ajax/show_phone/?id='+Id
			 #print url1
			 #g2.request(post='{},url=url1,headers=headers)
			 #phone = g2.response.body
			 #print phone
			 #print('*'*50+'  '+'Phone-OK'+'  '+'*'*50) 
			 #del g2
			 #break
		    #except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
			 #print 'Change proxy'+' : '+str(p)+' / 25'
			 #g2 = grab.clone()
	       #else:
		    #phone =''	  
	       
	       #try:
	       ad_id= grab.doc.select(u'//span[@class="show_phone"]/a').attr('data-id')
	       url_ph =  task.url.split('.net')[0]+'.net'+'/ajax/show_phone/?id='+ad_id
	       r= requests.post(url_ph,verify=True,timeout=15000)
	       phone = r.content
	       print phone
	       #except IndexError:
	       #phone = ''	       
	  except IndexError:
	       phone = ''
	       
	  try:
	       try: 
	            lico = grab.doc.select(u'//div[@class="mrk bface"]').text()
	       except IndexError:
		    lico = grab.doc.select(u'//td[contains(text(),"Агент:")]/following-sibling::td').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//div[@class="mrk bfirm"]').text()
	  except IndexError:
	       comp = ''
	       
	  try:
	       data= grab.doc.select(u'//div[@class="mrk bdate"]').text().split(' ')[0]
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
                      'phone':re.sub('[^\d\,\+]','',phone),
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
	  print  task.project['teplo']
	  print  task.project['oper']
	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 8, task.project['trassa'])
	  self.ws.write(self.result, 7, task.project['udal'])
	  self.ws.write(self.result, 28, task.project['oper'])
	  self.ws.write(self.result, 11, task.project['cena'])
	  self.ws.write(self.result, 14, task.project['plosh'])
	  self.ws.write(self.result, 15, task.project['et'])
	  self.ws.write(self.result, 16, task.project['ets'])
	  self.ws.write(self.result, 33, task.project['god'])
	  self.ws.write(self.result, 13, task.project['mat'])	  
	  self.ws.write(self.result, 13, task.project['vid'])
	  #self.ws.write(self.result, 20, task.project['gaz'])
	  #self.ws.write(self.result, 21, task.project['voda'])
	  #self.ws.write(self.result, 22, task.project['kanaliz'])
	  #self.ws.write(self.result, 23, task.project['electr'])
	  self.ws.write(self.result, 24, task.project['teplo'])
	  #self.ws.write(self.result, 19, task.project['ohrana'])	       
	  self.ws.write(self.result, 18, task.project['opis'])
	  self.ws.write(self.result, 19, u'INFOLINE')
	  self.ws.write_string(self.result, 20, task.project['url'])
	  self.ws.write(self.result, 21, task.project['phone'])
	  self.ws.write(self.result, 22, task.project['lico'])
	  self.ws.write(self.result, 23, task.project['company'])
	  self.ws.write(self.result, 29, task.project['data'])
	  self.ws.write(self.result, 31, datetime.today().strftime('%d.%m.%Y'))
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	  
	  #if self.result > 10:
	       #self.stop()	  
	       
	 

     
bot = Cian_Zem(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')
try:
     command = 'mount -t cifs //192.168.1.6/d /home/oleg/pars -o _netdev,sec=ntlm,auto,vers=1.0,username=oleg,password=1122,file_mode=0777,dir_mode=0777'
     os.system('echo %s|sudo -S %s' % ('1122', command))
     time.sleep(2)
     workbook.close()
     print('Done')
except IOError:
     time.sleep(30)
     os.system('echo %s|sudo -S %s' % ('1122', 'mount -a'))
     time.sleep(10)
     workbook.close()
     print('Done!')









