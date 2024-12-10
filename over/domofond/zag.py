#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import re
import time
import random
from head import agents
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab(timeout=2, connect_timeout=2)

g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')


i = 53
l= open('Links/Zag_Prod.txt').read().splitlines()
dc = len(l)
page = l[i]
oper = u'Продажа'

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class Dmofond_Zag(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	       while True:
                    try:
                         time.sleep(2)
                         g.go(self.f)
			 for elem in g.doc.select(u'//ul[@class="pagination"]/li/a'):
			      self.last = elem.number()
                         self.sub = g.doc.rex_text(u'class="active">(.*?)</span>')
                         print self.sub,self.last 
                         break
                    except(GrabTimeoutError,GrabNetworkError, GrabConnectionError):
                         print g.config['proxy'],'Change proxy'
                         g.change_proxy()
                         continue
                    except DataNotFound:
                         time.sleep(1)
                         print g.config['proxy'],'Change > proxy'
                         g.change_proxy()
                         continue
		    except AttributeError:
			 self.last = 1 
	       self.workbook = xlsxwriter.Workbook(u'zag/Domofond_%s' % bot.sub + u'_Загород_'+oper+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Domofond_Загород')
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
	       self.result= 1
	       
    
	  def task_generator(self):
	       for x in range(1,self.last+1):
                    yield Task ('post',url=self.f+'?Page=%d'%x,refresh_cache=True,network_try_count=100)
        
	  def task_post(self,grab,task):
	       try:
		    num =  re.sub(u'^.*(?=из)', '', grab.doc.select('//p[@class="pull-left"]').text())
	       except DataNotFound:
		    num = ''
	       for elem in grab.doc.select('//a[@itemprop="sameAs"]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur	      
		    yield Task('item', url=ur,num=num,refresh_cache=True, network_try_count=100)
	       
	       
	  
     
	  
        
	  def task_item(self, grab, task):
	        
	       try:
	            if grab.doc.select(u'//span[@itemprop="address"]/following-sibling::p[contains(text(),"шоссе")]').exists()== False:
	                 punkt = grab.doc.select('//span[@itemprop="address"]/following-sibling::p').text()
	            else:
		         punkt = '' 
	       except DataNotFound:
		    punkt = '' 
		    
	       try:
		    trassa = grab.doc.select(u'//span[@itemprop="address"]/following-sibling::p[contains(text(),"шоссе")]').text()
	       except DataNotFound:
		    trassa =''
		    
               try:
                    udal = grab.doc.select(u'//strong[contains(text(),"Расстояние от центра:")]/following-sibling::text()').text().split(', ')[0]
               except IndexError:
                    udal = ''
		    
               try:
                    tip = grab.doc.select(u'//strong[contains(text(),"Тип объекта:")]/following-sibling::text()').text()
               except IndexError:
                    tip = ''		    
		    
	       
	       try:
		    price = grab.doc.select(u'//strong[contains(text(),"Цена:")]/following-sibling::text()').text()
		 #print price
	       except DataNotFound:
		    price =''
	       try:
                    price_sot = grab.doc.select(u'//strong[contains(text(),"Цена за м²:")]/following-sibling::text()').text()
               except DataNotFound:
                    price_sot =''		   
	       try: 
                    plosh_ob = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::text()').text().split('/ ')[0]+u'м2'
               except IndexError:
		    plosh_ob=''
               
               try:
                    ets = grab.doc.select(u'//strong[contains(text(),"Этажность:")]/following-sibling::text()').text()#.split('. ')[1].replace('(','').replace(')','')
               except IndexError:
                    ets =''
		    
               try:
                    mat = grab.doc.select(u'//strong[contains(text(),"Материал здания:")]/following-sibling::text()').text()
               except IndexError:
                    mat =''
		    
               try: 
                    plosh_uch = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::text()').text().split('/ ')[1]
               except IndexError:
                    plosh_uch='' 
	       try:
		    ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
		 #print ohrana
	       except DataNotFound:
		    ohrana =''
	       try:
		    gaz = re.sub(u'^.*(?=газ)','', grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
		 #print gaz
	       except DataNotFound:
		    gaz =''
	       try:
		    voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
		 #print voda
	       except DataNotFound:
		    voda =''
	       try:
		    kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
		 #print kanal
	       except DataNotFound:
		    kanal =''
	       try:
		    elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
		 #print elek
	       except DataNotFound:
		    elek =''
	       try:
		    teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	       except DataNotFound:
		    teplo =''
	       try:
		    opis = grab.doc.select(u'//p[@class="df_listingDescription"]').text() 
		 #print opis
	       except DataNotFound:
		    opis = ''
	       try:
		    lico = grab.doc.select(u'//*[contains(text(),"Частное лицо:")]/following-sibling::h6').text()
		 #print lico
	       except DataNotFound:
		    lico = ''
	       try:
		    comp = grab.doc.select(u'//*[contains(text(),"Компания:")]/following-sibling::h6').text()
		 #print comp
	       except DataNotFound:
		    comp = ''
	       
	       try:
	            try: 
	                 data = grab.doc.select(u'//strong[contains(text(),"Дата обновления объявления:")]/following-sibling::text()').text().replace('/','.')
	            except DataNotFound:
		         data = grab.doc.select(u'//strong[contains(text(),"Дата публикации объявления:")]/following-sibling::text()').text().replace('/','.') 
	       except DataNotFound:   
	            data = ''
		    
	       if grab.doc.select(u'//a[@class="btn btn-block btn-success"]/@data-url').exists()==True:
		    ListingId = str(grab.doc.select(u'//span[@class="active"]').number())
		    Token = grab.doc.rex_text(u'Token=(.*?)">')
		    headers ={'Accept': '*/*',
	                      'Accept-Encoding': 'gzip,deflate',
	                      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	                      'Cookie': 'sessid='+ListingId+'.'+Token,
	                      'Host': 'www.domofond.ru',
	                      'Referer': task.url,
	                      'User-Agent': agents[random.randint(0, len(agents)-1)], 
	                      'X-Requested-With': 'XMLHttpRequest'}
	  
		    g2 = grab.clone(headers=headers,proxy_auto_change=True)
		    print headers['User-Agent']
		    for p in range(1,21):
			 try:
	  
			      url1 = grab.doc.select(u'//a[@class="btn btn-block btn-success"]').attr('data-url')
			      g2.request(post='{"ListingId": %s, "Token": %s}' % (ListingId, Token),url=url1)
			      phone = re.findall('#(.*?)#',g2.response.body)[0]
			      print('*'*50+'  '+'Phone-OK'+'  '+'*'*50) 
			      break
			 except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
			      bot.change_proxy(task, grab)
			      print ('*'*50+'  '+'Change proxy'+' : '+str(p)+' / 20 '+'*'*50)
			      g2 = grab.clone(headers=headers,proxy_auto_change=True)
                    else:
			 phone = ''
			      
	       else:
		    phone = '' 
		    
	      
	       	     
	  
	       projects = {'sub': self.sub,
		           'punkt': punkt,
		           'trassa': trassa,
	                   'udall': udal,
		           'cena': price,
	                   'cena_sot': price_sot,
		           'plosh': plosh_ob,
	                   'tip': tip,
	                   'etash':ets,
	                   'material':mat,
	                   'plosh2': plosh_uch,
		           'ohrana':ohrana,
		           'gaz': gaz,
		           'voda': voda,
		           'kanaliz': kanal,
		           'electr': elek,
		           'teplo': teplo,
		           'opis': opis,
		           'url': task.url,
		           'phone': phone,
		           'lico':lico,
		           'company': comp,
		           'koll':task.num,
		           'data':data
		           }
          
	  
	       yield Task('write',project=projects,grab=grab)
	
     
	
	  def task_write(self,grab,task):
	       #time.sleep(1)
	       print('*'*50)
	       print  task.project['sub']
	       print  task.project['punkt']
	       print  task.project['trassa']
	       print  task.project['udall']
	       print  task.project['cena']
	       print  task.project['cena_sot']
	       print  task.project['plosh']
	       print  task.project['tip']
	       print  task.project['etash']
	       print  task.project['material']
	       print  task.project['plosh2']
	       print  task.project['ohrana']
	       print  task.project['gaz']
	       print  task.project['voda']
	       print  task.project['kanaliz']
	       print  task.project['electr']
	       print  task.project['teplo']
	       print  task.project['opis']
	       print  task.project['url']
	       print  task.project['phone']
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.project['data']
	  
	       
	       
     
	       self.ws.write(self.result, 0, task.project['sub'])
	       #self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 7, task.project['trassa'])
	       self.ws.write(self.result, 8, task.project['udall'])
	       self.ws.write(self.result, 10, task.project['tip'])
	       self.ws.write(self.result, 11, oper)
	       self.ws.write(self.result, 12, task.project['cena'])
	       self.ws.write(self.result, 13, task.project['cena_sot'])
	       self.ws.write(self.result, 14, task.project['plosh'])	       
	       self.ws.write(self.result, 20, task.project['ohrana'])
	       self.ws.write(self.result, 16, task.project['etash'])
	       self.ws.write(self.result, 17, task.project['material'])
	       self.ws.write(self.result, 19, task.project['plosh2'])
	       self.ws.write(self.result, 21, task.project['gaz'])
	       self.ws.write(self.result, 22, task.project['voda'])
	       self.ws.write(self.result, 23, task.project['kanaliz'])
	       self.ws.write(self.result, 24, task.project['electr'])
	       self.ws.write(self.result, 25, task.project['teplo'])
	       self.ws.write(self.result, 28, task.project['ohrana'])
	       self.ws.write(self.result, 29, task.project['opis'])
	       self.ws.write(self.result, 30, u'DOMOFOND.RU')
	       self.ws.write_string(self.result, 31, task.project['url'])
	       self.ws.write(self.result, 32, task.project['phone'])
	       self.ws.write(self.result, 33, task.project['lico'])
	       self.ws.write(self.result, 34, task.project['company'])
	       self.ws.write(self.result, 35, task.project['data'])
	       self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	       
	       print('*'*50)
	       
	       print 'Ready - '+str(self.result)+'/'+task.project['koll']
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
	       print '***',i+1,'/',dc,'***'
	       print oper
	       
	       print('*'*50)
	       
	       self.result+= 1
	       
	       #if self.result > 50:
		    #self.stop()
	 

     bot = Dmofond_Zag(thread_number=5, network_try_limit=1000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=500, connect_timeout=500)
     bot.run()
     print(u'Спим 2 сек...')
     time.sleep(2)
     print(u'Сохранение...')
     bot.workbook.close()
     print('Done!')
     time.sleep(1) 
     i=i+1
     try:
          page = l[i]
     except IndexError:
          if oper == u'Продажа':
               i = 0
	       l= open('Links/Zag_Arenda.txt').read().splitlines()
	       dc = len(l)
	       page = l[i]
	       oper = u'Аренда'
	  else:
	       break
       
     
     
     