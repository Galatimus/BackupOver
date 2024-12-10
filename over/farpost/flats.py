#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
import requests
import time
from datetime import datetime,timedelta
import xlsxwriter
from sub import conv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)







class Upn_Kv(Spider):
     def prepare(self):
	  self.workbook = xlsxwriter.Workbook(u'kv/Farpost_Жилье.xlsx')
	  self.ws = self.workbook.add_worksheet()
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
	  self.ws.write(0, 39, u"ДАТА_РАЗМЕЩЕНИЯ")
	  self.ws.write(0, 40, u"ДАТА_ОБНОВЛЕНИЯ")
	  self.ws.write(0, 41, u"ДАТА_ПАРСИНГА")
	  self.ws.write(0, 42, u"МЕСТОПОЛОЖЕНИЕ")
	  self.result= 1
       
       
       
	 

     def task_generator(self):
	  yield Task ('post1',url='http://www.farpost.ru/realty/sell_flats/',refresh_cache=True,network_try_count=100)
	  yield Task ('post1',url='http://www.farpost.ru/realty/rent_flats/',refresh_cache=True,network_try_count=100)
	  
	  for x in range(1,468):#92
               yield Task ('post',url='http://www.farpost.ru/realty/sell_flats/?page=%d'%x,refresh_cache=True, network_try_count=100)
          for x1 in range(1,63):#92
	       yield Task ('post',url='http://www.farpost.ru/realty/rent_flats/?page=%d'%x1,refresh_cache=True, network_try_count=100)
          
	   
       
     def task_post(self,grab,task):
	  links = grab.doc.select(u'//a[@class="bulletinLink"]')
	  for elem in links:
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	       
     def task_post1(self,grab,task):
	  for el in grab.doc.select(u'//div[@class="image"]/a[contains(@href,"html")]'):
	       ur1 = grab.make_url_absolute(el.attr('href'))  
	       #print ur1
	       yield Task('item', url=ur1,refresh_cache=True,network_try_count=100,use_proxylist=False)     

     def task_item(self, grab, task):
	  try:
	       dt = grab.doc.select(u'//td[@class="col_city"]/a').attr('data-user-city-name')
	       if 'район'in dt:
		    sub ='Приморский край'
	       else:
		    sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(u' край ',' ').replace(u' областьская ',' ').replace(u' крайий ',' ').replace(u' крайский ',' ')
	  except IndexError:
	       sub = ''	  
	  
	  
	  try:
	       r = grab.doc.select(u'//td[@class="col_city"]/a').text()
               if "район" in r:
	            ray = r
               else:
	            ray=''
	  except (IndexError,TypeError):
	       ray = ''          
	  try:
	       p= grab.doc.select(u'//td[@class="col_city"]/a').text()
	       if 'район'in p:
	            punkt = ''
	       else:
	            punkt=p
	  except (IndexError,TypeError):
	       punkt = ''
	  try:
	       ter= grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"district-street")]').text()
	  except (IndexError,TypeError):
	       ter =''
	  try:
	       uliza = re.split('\d+',grab.doc.select(u'//div[contains(text(),"Адрес")]/following-sibling::div').text().replace(u'Подробности о доме →',''))[0]
	       #uliza = ul['fullName']
	  except (IndexError,TypeError):
	       uliza = ''
	  try:
	       m = grab.doc.select(u'//div[contains(text(),"Адрес")]/following-sibling::div').text().replace(u'Подробности о доме →','')
	       dom=re.split('\W+', m,1)[1]
	  except (IndexError,AttributeError):
	       dom = ''
		
	  try:
	       orentir = grab.doc.select(u'//a[@class="breadcrumbs-list__link"][contains(@href,"microdistrict")]').text()
	  except IndexError:
	       orentir = ''              
	    
	  try:
	       metro = grab.doc.select(u'//div[@id="breadcrumbs"]/div/span[5]/a').text().split(' ')[0]
	    #print rayon
	  except IndexError:
	       metro = ''
	      
	  try:
	       metro_min = grab.doc.select(u'//span[@class="card-living-content-location-metro__text _time"]').number()
	    #print rayon
	  except IndexError:
	       metro_min = ''
	      
	  try:
	       metro_tr = grab.doc.select(u'//span[@class="card-living-content-location-metro__text _time"]').text().split(u'минут ')[1]
	  except IndexError:
	       metro_tr = ''
	       
	  try:
	       tip=grab.doc.select(u'//div[contains(text(),"Вид квартиры")]/following-sibling::div').text()
	       if 'Комната' in tip:
		    tip_ob = 'Комната'
	       else:
		    tip_ob='Квартира'
	  except IndexError:
	       tip_ob = ''

	  try:
	       price = grab.doc.select(u'//span[@class="inplace"][contains(@data-field,"price")]').text()
	  except IndexError:
	       price = ''
	      
	  try:
	       price_m = grab.doc.select(u'//li[@class="card-living-content-deal-params__item"][1]').text()
	  except IndexError:
	       price_m = ''
		
	  try:
	       kol_komnat = re.sub('[^0-9]','',grab.doc.select(u'//div[contains(text(),"Вид квартиры")]/following-sibling::div').text())
	   #print rayon
	  except IndexError:
	       kol_komnat = ''

	  

	  try:
	       plosh_ob = grab.doc.select(u'//div[contains(text(),"Общая площадь")]/following-sibling::div').text()
	     #print rayon
	  except IndexError:
	       plosh_ob = ''

	  try:
	       plosh_gil = grab.doc.select(u'//span[contains(text(),"Жилая площадь")]/following-sibling::span').text()
	     #print rayon
	  except IndexError:
	       plosh_gil = ''
		
	  try:
	       plosh_kuh = grab.doc.select(u'//span[contains(text(),"Кухня")]/following-sibling::span').text()
	     #print rayon
	  except IndexError:
	       plosh_kuh = ''
	     
	  try:
	       plosh_com = grab.doc.select(u'//label[contains(text(),"Комнаты:")]/following-sibling::p/br/following-sibling::text()').text()
	  except IndexError:
	       plosh_com = ''
	       
	  try:
	       et = grab.doc.select(u'//div[contains(text(),"Этаж")]/following-sibling::div').text().split(' ')[0]
	    #print price + u' руб'	    
	  except IndexError:
	       et = '' 
	      
	  try:
	       etagn = re.sub('[^0-9]','',grab.doc.select(u'//div[contains(text(),"Этаж")]/following-sibling::div').text().split(' в ')[1])
	    #print price + u' руб'	    
	  except IndexError:
	       etagn = ''
		
	  try:
	       mat = grab.doc.select(u'//div[contains(text(),"Тип дома")]/following-sibling::div').text()
	    #print rayon
	  except IndexError:
	       mat = '' 
	      
	  try:
	       god = grab.doc.select(u'//td[contains(text(),"Год постройки")]/following-sibling::td').text().replace(u'не указано','')
	  except IndexError:
	       god = ''
		
	  try:
	       balkon = grab.doc.select(u'//span[contains(text(),"Количество балконов")]/following-sibling::span').text().replace(u'нет','')
	    #print rayon
	  except IndexError:
	       balkon = ''
	      
	  try:
	       lodg = grab.doc.select(u'//span[contains(text(),"Состояние")]/following-sibling::span').text().replace(u'не указано','')
	    #print rayon
	  except IndexError:
	       lodg = ''
	      
	  try:
	       sanuzel = grab.doc.select(u'//span[contains(text(),"Санузел")]/following-sibling::span').text().replace(u'не указано','')
	  except IndexError:
	       sanuzel = ''
		
		
	  try:
	       okna = grab.doc.select(u'//div[contains(text(),"Сторона окон")]/following-sibling::div').text()
	  except IndexError:
	       okna = ''
	      
	  try:
	       potolki = grab.doc.select(u'//div[contains(text(),"Адрес")]/following-sibling::div').text().replace(u'Подробности о доме →','')
	  except IndexError:
	       potolki = ''
	      
	  try:
	       lift = grab.doc.select(u'//td[contains(text(),"Лифт")]/following-sibling::td').text().replace(u'не указано','')
	  except IndexError:
	       lift = ''
	     
	  try:
	       rinok = grab.doc.select(u'//span[contains(text(),"Тип дома")]/following-sibling::span').text().replace(u'не указано','')
	  except IndexError:
	       rinok = ''
	      
	  try:
	       kons = re.sub(u'^.*(?=консьерж)','', grab.doc.select(u'//*[contains(text(), "консьерж")]').text())[:8].replace(u'консьерж',u'есть')
	  except IndexError:
	       kons = ''
		
	  try:
	       opis = grab.doc.select(u'//h3[contains(text(),"Состояние и особенности квартиры")]/following-sibling::div[1]').text() 
	  except IndexError:
	       opis = ''
	   
	  try:
	       ob = re.sub('[^\d]','',grab.doc.rex_text(u'>№(.+?)</b>'))
	       url_ph='http://www.farpost.ru/bulletin/'+ob+'/ajax_contacts?ajax=1'
	       headers ={'Accept': '*/*',
			 'Accept-Encoding': 'gzip,deflate',
			 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			 'Cookie': 'ring='+ob, 
			 'Host': 'www.farpost.ru',
			 'Referer': task.url,
			 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			 'X-Requested-With' : 'XMLHttpRequest'}
	       r= requests.get(url_ph,headers=headers,verify=True,timeout=100)
	       #g2 = grab.clone(timeout=2000, connect_timeout=2000)
	       #g2.go(url_ph)
	       ph =re.findall('class="phone">(.*?)</span>',r.content)#re.sub('[^\d]','',g2.doc.select(u'//span[@class="phone"]').text())
	       phone=re.sub('[^\d\,\+]','',','.join(ph))
	      
	  #print phone
	  except IndexError:
	       phone = ''
	      
	  try:
	       lico = grab.doc.select(u'//div[@class="offer-card-contacts__person _name _context"]').text()
	  except IndexError:
	       lico = ''
	       
	  try:
	       comp = grab.doc.select(u'//div[@class="offer-card-contacts__person _agency"]').text()
	    #print rayon
	  except IndexError:
	       comp = ''
	       
	  try:
	       con = [ ('сегодня', (datetime.today().strftime('%d.%m.%Y'))),
                    ('вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
                    (' июля', '.07.2016'),(' июня', '.06.2016'),(' мая', '.05.2016'),(u' октября',u'.10.2016')] 
	       dt1= grab.doc.select(u'//div[@class="label"][contains(text(),"Актуально")]/following-sibling::div/div').text().split(u' ещё ')[0].split(', ')[1]
	       data = reduce(lambda dt1, r1: dt1.replace(r1[0], r1[1]), con, dt1)#.replace(' ','')#.replace(u'более3-хмесяце', u'07.2015')
	  except IndexError:
	       data = ''
	       
	  
	       
	  try:
	       co = [ ('сегодня', (datetime.today().strftime('%d.%m.%Y'))),
                    ('вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
                    (u' августа',u'.08.2016'), (u' июля',u'.07.2016'),
	            (u' мая',u'.05.2016'),(u' июня',u'.06.2016'),
	            (u' марта',u'.03.2016'),(u' апреля',u'.04.2016'),
	            (u' января',u'.01.2016'),(u' декабря',u'.12.'),
	            (u' сентября',u'.09.2016'),(u' ноября',u'.11.2016'),
	            (u' февраля',u'.02.2016'),(u' октября',u'.10.2016')]
	       dt2= grab.doc.select(u'//div[@class="label"][contains(text(),"Добавлено")]/following-sibling::div/span').text().split(', ')[1]
	       tip_pr = reduce(lambda dt2, r1: dt2.replace(r1[0], r1[1]), co, dt2)
	    #print rayon
	  except IndexError:
	       tip_pr = ''
	      
	      
	  
	      
	 
      
	  projects = {'sub': sub,
                      'rayon': ray,
                      'punkt': punkt,
                      'teritor': ter,
                      'ulica': uliza,
                      'dom': dom,
                      'orentir': orentir,
                      'metro': metro,
                      'potolki': potolki,
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
                      'god_postr': god,
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
                      'tip_prod':tip_pr
                      
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
	  print  task.project['orentir']
	  print  task.project['metro']
	  print  task.project['potolki']
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
	  print  task.project['god_postr']
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
	  print  task.project['tip_prod']
    
	  self.ws.write(self.result, 0,task.project['sub'])
	  self.ws.write(self.result, 1,task.project['rayon'])
	  self.ws.write(self.result, 2,task.project['punkt'])
	  self.ws.write(self.result, 3,task.project['teritor'])
	  self.ws.write(self.result, 4,task.project['ulica'])
	  self.ws.write(self.result, 5,task.project['dom'])
	  self.ws.write(self.result, 6,task.project['orentir'])
	  self.ws.write(self.result, 11,task.project['metro'])
	  self.ws.write(self.result, 42,task.project['potolki'])
	  self.ws.write(self.result, 9,task.project['tran'])
	  self.ws.write(self.result, 10,task.project['object'])
	  #self.ws.write(self.result, 11,oper)
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
	  self.ws.write(self.result, 22, task.project['god_postr'])
	  self.ws.write(self.result, 24, task.project['balkon'])
	  self.ws.write(self.result, 28, task.project['logia'])
	  self.ws.write(self.result, 26, task.project['uzel'])
	  self.ws.write(self.result, 27, task.project['okna'])
	  self.ws.write(self.result, 30, task.project['lift'])
	  self.ws.write(self.result, 31, task.project['rinok'])
	  self.ws.write(self.result, 32, task.project['kons'])
	  self.ws.write(self.result, 33, task.project['opis'])
	  self.ws.write(self.result, 34, u'FARPOST.RU')
	  self.ws.write_string(self.result, 35, task.project['url'])
	  self.ws.write(self.result, 36, task.project['phone'])
	  self.ws.write(self.result, 37, task.project['lico'])
	  self.ws.write(self.result, 38, task.project['company'])
	  self.ws.write(self.result, 40, task.project['data'])
	  self.ws.write(self.result, 41, datetime.today().strftime('%d.%m.%Y'))
	  self.ws.write(self.result, 39, task.project['tip_prod'])
	  
	  print('*'*50)
	 
	 
	  print 'Ready - '+str(self.result)
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '***',i+1,'/',dc,'***'
	  #print oper
	  print('*'*50)
	      
	  self.result+= 1
	  
	  
	  
	  
	  #if self.result > 100:
	       #self.stop()


bot = Upn_Kv(thread_number=2,network_try_limit=2000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
bot.run()
print('Спим 2 сек...')
time.sleep(2)
print('Сохранение...')
bot.workbook.close()
print('Done!')


     
     
