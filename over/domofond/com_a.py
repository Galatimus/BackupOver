#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
from head import agents
import re
import time
import math
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)


g = Grab(timeout=20, connect_timeout=20)
g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')



i = 82
l= open('Links/Com_Arenda.txt').read().splitlines()
page = l[i]
oper = u'Аренда'




while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'	       
     class Domofond_Com(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	      
               while True:
                    try:
                         time.sleep(2)
                         g.go(self.f)
                         self.sub = g.doc.select(u'//span[@class="e-crumb m-active-crumb"]').text()
                         self.num =  re.sub('[^\d]','', g.doc.select('//h4[@class="g-no-margins"]').text())
                         self.pag = int(math.ceil(float(int(self.num))/float(20)))
                         print self.sub,self.num,self.pag
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
               self.workbook = xlsxwriter.Workbook(u'com/Domofond_%s' % bot.sub + u'_Коммерческая_'+oper+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Domofond_Коммерческая')
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
	       self.ws.write(0, 32, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 33, u"ДАТА_ПАРСИНГА")
	       self.ws.write(0, 34, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 35, u"ЦЕНА_ЗА_М2")
	       self.ws.write(0, 36, u"МЕСТОПОЛОЖЕНИЕ")
	       self.result= 1
	       self.g = 0
                
                
                
                
	  def task_generator(self):
	       for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'?Page=%d'% x,refresh_cache=True,network_try_count=100)
		   
		    
	  def task_post(self,grab,task):
	       for elem in grab.doc.select('//a[@itemprop="sameAs"]'):
		    ur1 = grab.make_url_absolute(elem.attr('href')) 
		    yield Task('item', url=ur1,refresh_cache=True, network_try_count=100)
		
        
	  def task_item(self, grab, task):
	       try:
		    r = grab.doc.select(u'//span[@itemprop="address"]').text()
		    t1=0
		    for w in r.split(','):
			 t1+=1
			 if w.find(u'район')>=0:
			      ray = r.split(',')[t1-1]
			      break
			 elif w.find(u'р-н')>=0:
			      ray = r.split(',')[t1-1]
			      break
			 else:
			      ray =''
	       except IndexError:
	            ray = ''
	       try:    
	            if self.sub == u'Москва':
		         punkt= u'Москва'
	            elif self.sub == u'Санкт-Петербург':
	                 punkt= u'Санкт-Петербург'
	            elif self.sub == u'Севастополь':
	                 punkt= u'Севастополь'
	            else:
		         if grab.doc.select(u'//div[@class="b-breadcrumb hidden-print"]/span[3]/a[contains(text(),"шоссе")]').exists()== False:
                              punkt = grab.doc.select('//div[@class="b-breadcrumb hidden-print"]/span[3]/a').text()
                         else:
	                      r1= grab.doc.select('//span[@itemprop="address"]').text()
	                      t2=0
	                      for w1 in r1.split(','):
	                           t2+=1
	                           if w1.find(u'село')>=0:
		                        punkt = r1.split(',')[t2-1]
		                        break
	                           elif w1.find(u'деревня')>=0:
		                        punkt = r1.split(',')[t2-1]
		                        break
	                           elif w1.find(u'поселок')>=0:
		                        punkt = r1.split(',')[t2-1]
		                        break  
	                           else:
		                        punkt ='' 
               except IndexError:
		    punkt =''

               try:
                    if grab.doc.select(u'//div[@class="b-breadcrumb hidden-print"]/span[4]/a[contains(text(),"шоссе")]').exists()== False:
                         ter= grab.doc.select(u'//div[@class="b-breadcrumb hidden-print"]/span[4]/a').text()
                    else:
	                 ter =''
               except IndexError:
                    ter =''
               try:
		    uliza = grab.doc.select(u'//span[@itemprop="address"]').text().split(',')[0].replace(punkt,'').replace(self.sub,'').replace(ter,'').replace(ray,'')
		  
	       except IndexError:
	            uliza = ''
               try:
                    try:                    
                         page1=re.sub('[\s]','',grab.doc.select(u'//span[@itemprop="address"]').text())
		         dom = [int(s) for s in page1.split(',') if s.isdigit()][0]
		    except IndexError:
			 dom = re.compile(r'[0-9]+$',re.S).search(uliza).group(0)
               except AttributeError:
                    dom = ''
		    
               try:
                    tip = grab.doc.select(u'//strong[contains(text(),"Тип объекта:")]/following-sibling::text()').text()
               except IndexError:
                    tip = ''
               try:
                    naz = grab.doc.select(u'//strong[contains(text(),"Тип:")]/following-sibling::text()').text()
               except IndexError:
                    naz =''
               try:
                    klass =  grab.doc.select(u'//strong[contains(text(),"Готовый бизнес:")]/following-sibling::text()').text()
               except IndexError:
                    klass = ''
               try:
                    price = grab.doc.select(u'//strong[contains(text(),"Цена:")]/following-sibling::text()').text()
               except IndexError:
                    price =''
               try: 
                    plosh = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::text()').text()
               except IndexError:
                    plosh=''
               try:
                    ohrana = grab.doc.select(u'//strong[contains(text(),"Цена за м²:")]/following-sibling::text()').text()
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
                    teplo = grab.doc.select(u'//span[@itemprop="address"]').text()
               except DataNotFound:
                    teplo =''
               #time.sleep(1)
	       try:
		    opis = grab.doc.select(u'//p[@class="m-listing-description"]').text() 
	       except IndexError:
		    opis = ''
               try:
                    lico = grab.doc.select(u'//*[contains(text(),"Частное лицо:")]/following::h6[1]').text()
               except DataNotFound:
                    lico = ''
               try:
                    comp = grab.doc.select(u'//*[contains(text(),"Компания:")]/following::h6[1]').text()
               except DataNotFound:
                    comp = ''
               try:
                    data = grab.doc.select(u'//strong[contains(text(),"Дата публикации объявления:")]/following-sibling::text()').text().replace('/','.')  
               except DataNotFound:   
                    data = ''
               try: 
                    data1 = grab.doc.select(u'//strong[contains(text(),"Дата обновления объявления:")]/following-sibling::text()').text().replace('/','.')
               except DataNotFound:
		    data1=''
	       
	      
		    
               projects = {'sub': self.sub,
	                  'adress': ray,
	                   'terit':ter, 
	                   'punkt':punkt,
	                   'ulica': re.sub('\d+$', '',uliza),
	                   'dom':dom,
	                   'tip':tip,
	                   'naz':naz,
	                   'klass': klass,
	                   'cena': price,
	                   'plosh': plosh,
	                   'ohrana':ohrana,
	                   'gaz': gaz,
	                   'voda': voda,
	                   'kanaliz': kanal,
	                   'electr': elek,
	                   'teplo': teplo,
	                   'opis': opis,
	                   'url': task.url,
	                   'lico':lico,
	                   'company': comp,
	                   'data':data,
	                   'data1':data1}
	       
	       try:
		    ad_id= re.sub(u'[^\d]','',task.url)
		    link = grab.make_url_absolute(grab.doc.select(u'//a[@class="b-btn m-green g-size-lg"][contains(@data-url,"Token")]').attr('data-url'))
		    ad_phone=link.split(u'Token=')[1].replace(u'%3d',u'=')
		    headers ={'Accept': '*/*',
			      'Accept-Encoding': 'gzip,deflate',
			      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			      'Cookie': 'optimizelyEndUserId='+ad_id+'.'+ad_phone,
			      'Host': 'www.domofond.ru',
			      'Referer': task.url,
			      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			      'X-Requested-With': 'XMLHttpRequest'}
	       
		    gr = Grab()
		    gr.setup(post='{ ListingId %s, Token %s}' % (ad_id, ad_phone),url=link,headers=headers)
	            yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
	       except IndexError:
	            yield Task('phone',grab=grab,project=projects)
		    
		    
          def task_phone(self, grab, task):
	       try:
		    try:
	                 phone = grab.doc.rex_text('#(.*?)#')[:11]
		    except IndexError:
		         phone = re.findall(u'#(.*?)#',grab.response.body)[0][:11]
	       except IndexError:
	            phone=''
		    
	       
	       
	       
	  
	  
	       yield Task('write',project=task.project,phone=phone,grab=grab)
	       
	   
	  
	  
	  
	  def task_write(self,grab,task):
	       if task.project['teplo']<>'':
		    print('*'*50)	       
		    print  task.project['sub']
		    print  task.project['punkt']
		    print  task.project['adress']
		    print  task.project['terit']
		    print  task.project['ulica']
		    print  task.project['dom']
		    print  task.project['tip']
		    print  task.project['naz']
		    print  task.project['klass']
		    print  task.project['cena']
		    print  task.project['plosh']
		    print  task.project['gaz']
		    print  task.project['voda']
		    print  task.project['kanaliz']
		    print  task.project['electr']
		    print  task.project['ohrana']
		    print  task.project['opis']
		    print  task.project['url']
		    print  task.phone
		    print  task.project['lico']
		    print  task.project['company']
		    print  task.project['data']
		    print  task.project['data1']
		    print  task.project['teplo']
	            
	            #if task.project['ulica']<>'':
			 #self.ws.write(self.result, 5,task.project['dom'])
	            #else:
			 #self.ws.write(self.result, 5,'')
	       
     
		    self.ws.write(self.result, 0, task.project['sub'])
		    self.ws.write(self.result, 1, task.project['adress'])
		    self.ws.write(self.result, 3, task.project['terit'])
		    self.ws.write(self.result, 2, task.project['punkt'])
		    self.ws.write(self.result, 4, task.project['ulica'])
		    self.ws.write(self.result, 5, task.project['dom'])
		    self.ws.write(self.result, 8, task.project['tip'])
		    self.ws.write(self.result, 9, task.project['naz'])
		    self.ws.write(self.result, 10, task.project['klass'])
		    self.ws.write(self.result, 11, task.project['cena'])
		    self.ws.write(self.result, 12, task.project['plosh'])
		    self.ws.write(self.result, 35, task.project['ohrana'])
		    self.ws.write(self.result, 20, task.project['gaz'])
		    self.ws.write(self.result, 21, task.project['voda'])
		    self.ws.write(self.result, 22, task.project['kanaliz'])
		    self.ws.write(self.result, 23, task.project['electr'])
		    self.ws.write(self.result, 36, task.project['teplo'])
		    self.ws.write(self.result, 25, task.project['opis'])
		    self.ws.write(self.result, 26, u'DOMOFOND.RU')
		    self.ws.write_string(self.result, 27, task.project['url'])
		    self.ws.write(self.result, 28, task.phone)
		    self.ws.write(self.result, 29, task.project['lico'])
		    self.ws.write(self.result, 30, task.project['company'])
		    self.ws.write(self.result, 31, task.project['data'])
		    self.ws.write(self.result, 32, task.project['data1'])
		    self.ws.write(self.result, 33, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result, 34, oper)
		    print('*'*50)
		    #print self.sub
		    print 'Ready - '+str(self.result)+'/'+str(self.num)
		    print 'Tasks - %s' % self.task_queue.size() 
		    print '***',i+1,'/',len(l),'***'
		    print oper
		    print('*'*50)
		    self.result+= 1
	       
	      
	       
	       
	       
		    #if self.result > 10:
			 #self.stop()	       


     bot = Domofond_Com(thread_number=5, network_try_limit=2000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=5000, connect_timeout=5000)
     #bot.setup_queue(backend='mongo',database ='oleg')
     bot.run()
     print bot.sub
     print('Спим 2 сек...')
     time.sleep(2)
     print('Сохранение...')
     bot.workbook.close()
     print('Done!')
     time.sleep(1) 
    
     i=i+1
     try:
          page = l[i]
     except IndexError:
          break
       
     
     
     