#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import time
from datetime import datetime,timedelta
import xlsxwriter

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'Brsn_Жилье.xlsx') 

l= ['http://www.brsn.ru/kvartira.html','http://www.brsn.ru/arenda-kvartir.html']
	       
class Cian_Kv(Spider):



     def prepare(self):
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	  self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  self.ws.write(0, 4, u"УЛИЦА")
	  self.ws.write(0, 5, u"ДОМ")
	  self.ws.write(0, 6, u"ОРИЕНТИР")
	  self.ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
	  self.ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
	  self.ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
	  self.ws.write(0, 10, u"ТИП_ОБЪЕКТА")
	  self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  self.ws.write(0, 12, u"СТОИМОСТЬ")
	  self.ws.write(0, 13, u"ЦЕНА_М2")
	  self.ws.write(0, 14, u"КОЛИЧЕСТВО_КОМНАТ")
	  self.ws.write(0, 15, u"ПЛОЩАДЬ_ОБЩАЯ")
	  self.ws.write(0, 16, u"ПЛОЩАДЬ_ЖИЛАЯ")
	  self.ws.write(0, 17, u"ПЛОЩАДЬ_КУХНИ")
	  self.ws.write(0, 18, u"ПЛОЩАДЬ_КОМНАТ")
	  self.ws.write(0, 19, u"ЭТАЖ")
	  self.ws.write(0, 20, u"ЭТАЖНОСТЬ")
	  self.ws.write(0, 21, u"МАТЕРИАЛ_СТЕН")
	  self.ws.write(0, 22, u"ГОД_ПОСТРОЙКИ")
	  self.ws.write(0, 23, u"РАСПОЛОЖЕНИЕ_КОМНАТ")
	  self.ws.write(0, 24, u"БАЛКОН")
	  self.ws.write(0, 25, u"ЛОДЖИЯ")
	  self.ws.write(0, 26, u"САНУЗЕЛ")
	  self.ws.write(0, 27, u"ОКНА")
	  self.ws.write(0, 28, u"СОСТОЯНИЕ")
	  self.ws.write(0, 29, u"ВЫСОТА_ПОТОЛКОВ")
	  self.ws.write(0, 30, u"ЛИФТ")
	  self.ws.write(0, 31, u"РЫНОК")
	  self.ws.write(0, 32, u"КОНСЬЕРЖ")
	  self.ws.write(0, 33, u"ОПИСАНИЕ")
	  self.ws.write(0, 34, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 35, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  self.ws.write(0, 36, u"ТЕЛЕФОН")
	  self.ws.write(0, 37, u"КОНТАКТНОЕ_ЛИЦО")
	  self.ws.write(0, 38, u"КОМПАНИЯ")
	  self.ws.write(0, 39, u"ДАТА_РАЗМЕЩЕНИЯ_ОБЪЯВЛЕНИЯ")
	  self.ws.write(0, 40, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 41, u"ТИП_ПРОДАЖИ")
	  self.ws.write(0, 42, u"МЕБЕЛЬ")
	  self.result= 1
            
            
            
              
    
     def task_generator(self):
	  for line in l:#open('/home/oleg/CIAN/Links/Kv.txt').read().splitlines():
            yield Task ('post',url=line.strip(),network_try_count=100)
        
            
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select('//li[@class="pagination-next"]/a')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*100)
	       print '!!!','NO PAGE NEXT','!!!'
	       print('*'*100)
	       logger.debug('%s taskq size' % self.task_queue.size())
	    
        
       
       
        
            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//div[@class="photo-container"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       print ur
	       yield Task('item', url=ur,refresh_cache=True)
	  yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	    
        
        
     
     def task_item(self, grab, task):
	  
	  try:
               sub = u'Брянская область'#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[0]
          except IndexError:
               sub = ''
	  try:
               ray = grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"raion")]').text().replace(u'р-н ','')
          except DataNotFound:
               ray =''
	  try:
               #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').exists()==True:
                    #punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
               #else:
               punkt= grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"city")]').text()
          except IndexError:
               punkt = ''
		 
	  try:
               if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').exists()==True:
                    ter= grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[3].replace(u'улица','')
               else:
                    ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
          except IndexError:
               ter ='' 
	  try:
	       #try:
                    #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"улица")]').text()
	       #except DataNotFound:
	            #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"проспект")]').text()
               #except DataNotFound:
                    #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"шоссе")]').text()
               #except DataNotFound:
               uliza = re.sub(u'[\d]','',grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"street")]').text()).replace(',','')
          except DataNotFound:
               uliza = ''
	       
	  try:
	    dom = grab.doc.select(u'//div[@class="sttnmls_navigation text-center"]/a[contains(@href,"street")]').number()
	   #print rayon
	  except DataNotFound:
	      dom = ''
		
	    
	  try:
	    metro = grab.doc.select(u'//div[@class="object_descr_metro"]/a').text()
	    #print rayon
	  except DataNotFound:
	      metro = ''
	      
	  try:
	    metro_min = grab.doc.select(u'//span[@class="object_item_metro_comment"]').number()
	    #print rayon
	  except DataNotFound:
	      metro_min = ''
	      
	  try:
	       metro_tr = grab.doc.select(u'//span[@class="object_item_metro_comment"]').text().split(u'мин. ')[1]
          except IndexError:
	       metro_tr = ''
	       
	  try:
	       #if grab.doc.select(u'//div[@class="object_descr_title"]').text().find(u'комната') == 0:
                    #tip_ob = u'Комната'
	       #else:
               tip_ob = u'Квартира' 
	  except DataNotFound:
	       tip_ob = ''
	       
	  try:
	       oper = grab.doc.select(u'//h1').text().split(' ')[0].replace(u'Продам',u'Продажа').replace(u'Сдам',u'Аренда') 
	  except DataNotFound:
	       oper = ''
	      
	  try:
	       try: 
	            price =  grab.doc.select(u'//div[@class="pricecard"]').text().replace(' ','').replace(u'a',u' р.')
               except IndexError:
	            price =  grab.doc.select(u'//div[@class="pricecard rent month"]').text().replace(' ','').replace(u'a',u' р ')   
	  except IndexError:
	      price = ''
	      
	  try:
               price_m = grab.doc.select(u'//div[@class="priceqmcard"]').text()#.split(u'.')[0]
          except IndexError:
               price_m = ''
		
	  try:
	    kol_komnat = grab.doc.select(u'//h1').number()
	   #print rayon
	  except DataNotFound:
	      kol_komnat = ''

	  

	  try:
	    plosh_ob = grab.doc.rex_text(u'площадь: <b>(.*?)</b> кв.м').split('/')[0]+u' м2'
	     #print rayon
	  except IndexError:
	     plosh_ob = ''

	  try:
	    plosh_gil = grab.doc.rex_text(u'площадь: <b>(.*?)</b> кв.м').split('/')[1]+u' м2'
	     #print rayon
	  except IndexError:
	     plosh_gil = ''
		
	  try:
	    plosh_kuh = grab.doc.rex_text(u'площадь: <b>(.*?)</b> кв.м').split('/')[2]+u' м2'
	     #print rayon
	  except IndexError:
	     plosh_kuh = ''
	     
	  try:
	       plosh_com = grab.doc.select(u'//th[contains(text(),"Площадь комнат:")]/following-sibling::td').text().replace(u'–','')
          except DataNotFound:
	       plosh_com = ''
	       
	  try:
	    et = grab.doc.rex_text(u'<b>(.*?)</b>-этаж')
	    #print price + u' руб'	    
	  except IndexError:
	       et = '' 
	      
	  try:
	    etagn =grab.doc.rex_text(u'-этаж <b>(.*?)</b>-этажного ')
	    #print price + u' руб'	    
	  except IndexError:
	       etagn = ''
		
	  try:
	    mat = grab.doc.rex_text(u'</b>-этажного (.*?)дома')
	    #print rayon
	  except IndexError:
	      mat = '' 
	      
	  #try:
	    #god = grab.doc.select(u'//div[contains(text(),"Год постройки/сдачи:")]/following-sibling::div[@class="propertyValue"]').text()
	  #except DataNotFound:
	      #god = ''
		
	  try:
	    balkon = grab.doc.select(u'//th[contains(text(),"Балкон:")]/following-sibling::td[contains(text(),"балк")]').text()#.replace(u'нет','')
	    #print rayon
	  except DataNotFound:
	      balkon = ''
	      
	  try:
	    lodg = grab.doc.select(u'//th[contains(text(),"Балкон:")]/following-sibling::td[contains(text(),"лодж")]').text()
	    #print rayon
	  except DataNotFound:
	      lodg = ''
	      
	  try:
	    sanuzel = grab.doc.select(u'//th[contains(text(),"Санузел:")]/following-sibling::td').text().replace(u'нет','')
	  except DataNotFound:
	      sanuzel = ''
		
		
	  try:
	    okna = grab.doc.select(u'//th[contains(text(),"Вид из окна:")]/following-sibling::td').text()
	  except DataNotFound:
	      okna = ''
	      
	  #try:
	    #potolki = grab.doc.select(u'//div[contains(text(),"Высота потолков:")]/following-sibling::div[@class="propertyValue"]').text()
	  #except DataNotFound:
	      #potolki = ''
	      
	  try:
	    lift = grab.doc.select(u'//th[contains(text(),"Лифт:")]/following-sibling::td').text().replace(u'нет','')
	  except DataNotFound:
	     lift = ''
	     
	  try:
	    rinok = grab.doc.select(u'//th[contains(text(),"Тип дома:")]/following-sibling::td').text().split(', ')[0]
	  except DataNotFound:
	      rinok = ''
	      
	  try:
	    kons = re.sub(u'^.*(?=консьерж)','', grab.doc.select(u'//*[contains(text(), "консьерж")]').text())[:8].replace(u'консьерж',u'есть')
	  except DataNotFound:
	      kons = ''
		
	  try:
	     opis = grab.doc.select(u'//div[@id="dopinfo"]/p').text() 
	  except DataNotFound:
	      opis = ''
	   
	  try:
	       phone = grab.doc.rex_text(u'tel:(.*?)">')
	  except (AttributeError,DataNotFound):
	      phone = ''
	      
	  try:
	    lico = grab.doc.select(u'//img[@class="thumbnail"][contains(@src,"components")]/following::b[1]').text()
	  except IndexError:
	      lico = ''
	       
	  try:
	    comp = grab.doc.select(u'//img[@class="thumbnail"][contains(@src,"agency")]/following::b[1]').text()
	    #print rayon
	  except DataNotFound:
	      comp = ''
	       
	  try:
               conv = [(u' августа ',u'.08.'), (u' июля ',u'.07.'),
	       (u' мая ',u'.05.'),(u' июня ',u'.06.'),
	       (u' марта ',u'.03.'),(u' апреля ',u'.04.'),
	       (u' января ',u'.01.'),(u' декабря ',u'.12.'),
	       (u' сентября ',u'.09.'),(u' ноября ',u'.11.'),
	       (u' февраля ',u'.02.'),(u' октября ',u'.10.')] 
	       dt= grab.doc.select(u'//b[contains(text(),"Обновлено:")]/following-sibling::span').text()#.split(', ')[0]
	       data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
		   #print data
          except DataNotFound:
               data = ''
	       
	  
	       
	  try:
	    tip_pr = grab.doc.select(u'//th[contains(text(),"Тип продажи:")]/following-sibling::td').text()
	    #print rayon
	  except DataNotFound:
	      tip_pr = ''
	      
	      
	  
	      
         
      
	  projects = {'sub': sub,
	              'rayon': ray,
	              'punkt': punkt,
	              'teritor': ter,
	              'ulica': uliza,
	              'dom': dom,
	              'metro': metro,
	              'udall': metro_min,
	              'tran': metro_tr,
	              'object': tip_ob,
	              'cena': price,
	              'cena_m': price_m,
	              'col_komnat': kol_komnat,
	              'plosh_ob':plosh_ob,
	              'plosh_gil': plosh_gil,
	              'plosh_kuh': plosh_kuh,
	              'plosh_com': plosh_com,
	              'etach': et,
	              'etashost': etagn,
	              'material': mat,
	              'balkon': balkon,
	              'logia': lodg,
	              'uzel':sanuzel,
	              'okna': okna,
	              'lift':lift,
	              'rinok': rinok,
	              'kons':kons,
	              'opis':opis,
	              'url':task.url,
	              'phone':phone,
	              'lico':lico,
	              'company':comp,
	              'data':data,
	              'tip_prod':tip_pr,
	              'oper':oper
	              }
	
	
	
	  yield Task('write',project=projects,grab=grab)
	
	
	
	
	
	
     def task_write(self,grab,task):
	  
	  print('*'*50)	       
	  print  task.project['sub']
	  print  task.project['rayon']
	  print  task.project['punkt']
	  print  task.project['teritor']
	  print  task.project['ulica']
	  print  task.project['dom']
	  print  task.project['metro']
	  print  task.project['udall']
	  print  task.project['tran']
	  print  task.project['object']
	  print  task.project['cena']
	  print  task.project['cena_m']
	  print  task.project['col_komnat']
	  print  task.project['plosh_ob']
	  print  task.project['plosh_gil']
	  print  task.project['plosh_kuh']
	  print  task.project['plosh_com']
	  print  task.project['etach']
	  print  task.project['etashost']
	  print  task.project['material']
	  print  task.project['balkon']
	  print  task.project['logia']
	  print  task.project['uzel']
	  print  task.project['okna']
	  print  task.project['lift']
	  print  task.project['rinok']
	  print  task.project['kons']
	  print  task.project['opis']
	  print  task.project['url']
	  print  task.project['phone']
	  print  task.project['lico']
	  print  task.project['company']
	  print  task.project['data']
	  print  task.project['oper']
	  print  task.project['tip_prod']
    
	  self.ws.write(self.result, 0,task.project['sub'])
	  self.ws.write(self.result, 1,task.project['rayon'])
	  self.ws.write(self.result, 2,task.project['punkt'])
	  self.ws.write(self.result, 3,task.project['teritor'])
	  self.ws.write(self.result, 4,task.project['ulica'])
	  self.ws.write(self.result, 5,task.project['dom'])
	  self.ws.write(self.result, 7,task.project['metro'])
	  self.ws.write(self.result, 8,task.project['udall'])
	  self.ws.write(self.result, 9,task.project['tran'])
	  self.ws.write(self.result, 10,task.project['object'])
	  self.ws.write(self.result, 11,task.project['oper'])
	  self.ws.write(self.result, 12, task.project['cena'])
	  self.ws.write(self.result, 13, task.project['cena_m'])
	  self.ws.write(self.result, 14, task.project['col_komnat'])
	  self.ws.write(self.result, 15, task.project['plosh_ob'])
	  self.ws.write(self.result, 16, task.project['plosh_gil'])
	  self.ws.write(self.result, 17, task.project['plosh_kuh'])
	  self.ws.write(self.result, 18, task.project['plosh_com'])
	  self.ws.write(self.result, 19, task.project['etach'])
	  self.ws.write(self.result, 20, task.project['etashost'])
	  self.ws.write(self.result, 21, task.project['material'])
	  self.ws.write(self.result, 24, task.project['balkon'])
	  self.ws.write(self.result, 25, task.project['logia'])
	  self.ws.write(self.result, 26, task.project['uzel'])
	  self.ws.write(self.result, 27, task.project['okna'])
	  self.ws.write(self.result, 30, task.project['lift'])
	  self.ws.write(self.result, 31, task.project['rinok'])
	  self.ws.write(self.result, 32, task.project['kons'])
	  self.ws.write(self.result, 33, task.project['opis'])
	  self.ws.write(self.result, 34, u'Брянский сервер недвижимости')
	  self.ws.write_string(self.result, 35, task.project['url'])
	  self.ws.write(self.result, 36, task.project['phone'])
	  self.ws.write(self.result, 37, task.project['lico'])
	  self.ws.write(self.result, 38, task.project['company'])
	  self.ws.write(self.result, 39, task.project['data'])
	  self.ws.write(self.result, 40, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 41, task.project['tip_prod'])
	  
	  print('*'*50)
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  print('*'*50)
	  self.result+= 1
	  #if self.result > 100:
	       #self.stop()

     
bot = Cian_Kv(thread_number=5,network_try_limit=2000)
#bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
#bot.proxy_auto_change
#bot.setup_grab(proxy='localhost:8118', proxy_type='HTTP')
#bot.setup_grab(proxy='185.39.149.164:40165', proxy_userpwd='cHWT9uREaJ:galatimus@mail.ru', proxy_type='HTTP')
#bot.setup_queue(backend='memory')
#bot.setup_grab(connect_timeout=500, timeout=1500)
bot.run()
workbook.close()
print('Done!')

     
     