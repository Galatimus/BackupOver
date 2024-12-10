#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
import re
from head import agents
from mesto import ul,pu,ra
import time
import xlsxwriter
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab(timeout=5, connect_timeout=10)

g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')


i = 0
l= open('Links/Zem.txt').read().splitlines()
dc = len(l)
page = l[i]

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class Dmf_Zem(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	       while True:
                    try:
                         time.sleep(1)
                         g.go(self.f)
			 for elem in g.doc.select(u'//ul[@class="e-pages"]/li/a'):
                              self.last = elem.number()
                         self.sub = g.doc.select(u'//span[@class="e-crumb m-active-crumb"]').text()
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
	       self.workbook = xlsxwriter.Workbook(u'zem/Domofond_%s' % bot.sub + u'_Земля_Продажа.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Domofond_Земля')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 4, u"УЛИЦА")
	       self.ws.write(0, 5, u"ДОМ")
	       self.ws.write(0, 6, u"ОРИЕНТИР")
	       self.ws.write(0, 7, u"ТРАССА")
	       self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	       self.ws.write(0, 9, u"ОПЕРАЦИЯ")
	       self.ws.write(0, 10, u"СТОИМОСТЬ")
	       self.ws.write(0, 11, u"ЦЕНА_ЗА_СОТКУ")
	       self.ws.write(0, 12, u"ПЛОЩАДЬ")
	       self.ws.write(0, 13, u"КАТЕГОРИЯ_ЗЕМЛИ")
	       self.ws.write(0, 14, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	       self.ws.write(0, 15, u"ГАЗОСНАБЖЕНИЕ")
	       self.ws.write(0, 16, u"ВОДОСНАБЖЕНИЕ")
	       self.ws.write(0, 17, u"КАНАЛИЗАЦИЯ")
	       self.ws.write(0, 18, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	       self.ws.write(0, 19, u"ТЕПЛОСНАБЖЕНИЕ")
	       self.ws.write(0, 20, u"ОХРАНА")
	       self.ws.write(0, 21, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	       self.ws.write(0, 22, u"ОПИСАНИЕ")
	       self.ws.write(0, 23, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 24, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 25, u"ТЕЛЕФОН")
	       self.ws.write(0, 26, u"КОНТАКТНОЕ_ЛИЦО")
	       self.ws.write(0, 27, u"КОМПАНИЯ")
	       self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
               self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
               self.ws.write(0, 30, u"ДАТА_ПАРСИНГА")
               self.ws.write(0, 31, u"МЕСТОПОЛОЖЕНИЕ")
	       self.result= 1
	       self.g = 0
    
	  def task_generator(self):
	       for x in range(1,self.last+1):
		    yield Task ('post',url=self.f+'?Page=%d'%x,refresh_cache=True,network_try_count=100)
                  
        
        
            
            
	  def task_post(self,grab,task):	     
	       try:
		    self.num =  re.sub('[^\d]','', grab.doc.select('//h4[@class="g-no-margins"]').text())
	       except DataNotFound:
		    self.num = ''       
	       for elem in grab.doc.select('//a[@itemprop="sameAs"]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	     
	     
	     
	  def task_item(self, grab, task):
	       
	       try:
		    r5= grab.doc.select(u'//span[@itemprop="address"]').text()
	            t5=0
	            for w5 in r5.split(','):
	                 t5+=1
	                 for x in range(len(ra)):
		              if ra[x] in w5:
			           ray = r5.split(',')[t5-1]
			           break
	            print ray
	       except (IndexError,UnboundLocalError):
	            ray = '' 
	       try:
		    punkt = grab.doc.select(u'//title').text().split(' - ')[1].split(' : ')[0].replace(u'город ','')
	       except IndexError:
		    punkt = ''
		    
	       try:
		    r= grab.doc.select(u'//span[@itemprop="address"]').text()
                    t=0
                    for w in r.split(','):
	                 t+=1
	                 for x in range(len(pu)):
	                      if pu[x] in w:
		                   ter = r.split(',')[t-1].replace(u' д.','')
		                   break
                    print ter
	       except (IndexError,UnboundLocalError):
		    ter =''
		    
	       try:
		    r1= grab.doc.select(u'//span[@itemprop="address"]').text()
                    t2=0
                    for w1 in r1.split(','):
	                 t2+=1
	                 for x in range(len(ul)):
	                      if ul[x] in w1:
		                   uliza = r1.split(',')[t2-1].replace(u' д','')
		                   break
                    print uliza
	       except (IndexError,UnboundLocalError):
	            uliza = ''
		    
	       try:
		    try:
                         try:                    
	                      page1=re.sub('[\s]','',grab.doc.select(u'//span[@itemprop="address"]').text())
	                      dom = [int(s) for s in page1.split(',') if s.isdigit()][0]
                         except IndexError:
	                      dom = re.compile(r'[0-9]+$',re.M).search(uliza).group(0)
                    except AttributeError:
	                 dom = re.compile(r'[0-9]+$',re.M).search(ter).group(0)
	       except AttributeError:
		    dom = ''
		    
	       try:
	            oren = grab.doc.select(u'//span[@itemprop="address"]').text().split(', ')[0].replace(ray,'').replace(punkt,'').replace(self.sub,'').replace(ter,'').replace(uliza,'').replace(str(dom),'')
	       except IndexError:
	            oren ='' 
		    
	       try:
		    trassa = grab.doc.select(u'//div[@class="b-breadcrumb hidden-print"]/span/a[contains(text(),"шоссе")]').text()
		     #print rayon
	       except IndexError:
		    trassa = ''
		    
	       try:
		    udal = grab.doc.select(u'//strong[contains(text(),"Расстояние от центра:")]/following-sibling::text()').text().split(', ')[0]
	       except IndexError:
		    udal = ''
		    
	       try:
		    price = grab.doc.select(u'//strong[contains(text(),"Цена:")]/following-sibling::text()').text()
	       except DataNotFound:
		    price = ''
		    
	       
		    
	       try:
		    plosh = grab.doc.select(u'//strong[contains(text(),"Площадь:")]/following-sibling::text()').text()
	       except DataNotFound:
		    plosh = ''
		    
	       
	       
	       
		    
	       try:
		    vid = grab.doc.select(u'//strong[contains(text(),"Тип объекта:")]/following-sibling::text()').text()
	       except DataNotFound:
		    vid = '' 
		    
		    
	       try:
		    ohrana = grab.doc.select(u'//strong[contains(text(),"Цена за сотку:")]/following-sibling::text()').text()
	       except DataNotFound:
		    ohrana =''
	       try:
		    gaz = grab.doc.select(u'//span[@itemprop="address"]').text()
	       except DataNotFound:
		    gaz =''
	       try:
		    voda = grab.doc.select(u'//strong[contains(text(),"Дата обновления объявления:")]/following-sibling::text()').text().replace('/','.')
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
		    teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	       except DataNotFound:
		    teplo =''
		    
	      
	       try:
		    opis = grab.doc.select(u'//p[@class="m-listing-description"]').text() 
	       except DataNotFound:
		    opis = ''
		    
	       if grab.doc.select(u'//a[@class="b-btn m-green g-size-lg"]/@data-url').exists()==True:
                    ListingId = str(grab.doc.select(u'//strong[contains(text(),"Номер в каталоге:")]/following-sibling::text()').number())
                    Token = grab.doc.rex_text(u'Token=(.*?)">')
		    headers ={'Accept': '*/*',
			      'Accept-Encoding': 'gzip,deflate',
			      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			      'Cookie': 'sessid='+ListingId+'.'+Token,
			      'Host': 'www.domofond.ru',
			      'Referer': task.url,
			      'User-Agent': agents[self.g], 
			      'X-Requested-With': 'XMLHttpRequest'}
		    g2 = grab.clone(headers=headers,proxy_auto_change=True)
		    
		    for p in range(1,25):
			 try:
			      url1 = grab.doc.select(u'//a[@class="b-btn m-green g-size-lg"]').attr('data-url')
			      g2.request(post='{"ListingId": %s, "Token": %s}' % (ListingId, Token),url=url1)
			      phone = re.findall('#(.*?)#',g2.response.body)[0]
			      print('*'*50+'  '+'Phone-OK'+'  '+'*'*50) 
			      break
			 except (IndexError,GrabConnectionError,GrabNetworkError,GrabTimeoutError,IOError):
			      bot.change_proxy(task, grab)
			      print 'Change proxy'+' : '+str(p)+' / 25'
			      g2 = grab.clone(headers=headers,proxy_auto_change=True)
		    else:
			 phone =''
	       else:
		    phone =''
		    
		    
		    
              
     
	       try:
		    lico = grab.doc.select(u'//*[contains(text(),"Частное лицо:")]/following::h6[1]').text()
	       except IndexError:
		    lico = ''
		    
	       try:
		    comp = grab.doc.select(u'//*[contains(text(),"Компания:")]/following::h6[1]').text()
	       except IndexError:
		    comp = ''
		    
	       try:
	            data = grab.doc.select(u'//strong[contains(text(),"Дата публикации объявления:")]/following-sibling::text()').text().replace('/','.') 
	       except DataNotFound:   
	            data = ''
			 
	       if self.g == 76:
		    self.g = 0
	       else:
	            self.g+= 1	       

		    
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt.replace(trassa,''),
		           'teritor': ter.replace(uliza,'').replace(str(dom),''),
		           'ulica': re.sub('\d+$', '',uliza),
		           'dom': dom,
	                   'orentir':oren.replace(trassa,''),
		           'trassa': trassa,
		           'udal': udal,
		           'cena': price,
		           'plosh':plosh,
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
		           'data':data}
	       
	       yield Task('write',project=projects,grab=grab)
		 
	  def task_write(self,grab,task):
	       if task.project['phone']<>'':
                       
		    print('*'*50)
		    print  task.project['sub']
		    print  task.project['rayon']
		    print  task.project['punkt']
		    print  task.project['teritor']
		    print  task.project['ulica']
		    print  task.project['dom']
		    print  task.project['orentir']
		    print  task.project['trassa']
		    print  task.project['udal']
		    print  task.project['cena']
		    print  task.project['plosh']
		    print  task.project['vid']
		    print  task.project['ohrana']
		    print  task.project['kanaliz']
		    print  task.project['electr']
		    print  task.project['teplo']
		    print  task.project['opis']
		    print task.project['url']
		    print  task.project['phone']
		    print  task.project['lico']
		    print  task.project['company']
		    print  task.project['data']
		    print  task.project['voda']
		    print  task.project['gaz']
		    
		    
		    self.ws.write(self.result, 0, task.project['sub'])
		    self.ws.write(self.result, 1, task.project['rayon'])
		    self.ws.write(self.result, 2, task.project['punkt'])
		    self.ws.write(self.result, 3, task.project['teritor'])
		    self.ws.write(self.result, 4, task.project['ulica'])
		    self.ws.write(self.result, 5, task.project['dom'])
		    self.ws.write(self.result, 6, task.project['orentir'])
		    self.ws.write(self.result, 7, task.project['trassa'])
		    self.ws.write(self.result, 8, task.project['udal'])
		    self.ws.write(self.result, 9, u'Продажа')
		    self.ws.write_string(self.result, 10, task.project['cena'])
		    self.ws.write(self.result, 12, task.project['plosh'])
		    self.ws.write(self.result, 13, task.project['vid'])
		    self.ws.write(self.result, 31, task.project['gaz'])
		    self.ws.write(self.result, 29, task.project['voda'])
		    self.ws.write(self.result, 17, task.project['kanaliz'])
		    self.ws.write(self.result, 18, task.project['electr'])
		    self.ws.write(self.result, 19, task.project['teplo'])
		    self.ws.write(self.result, 11, task.project['ohrana'])
		    self.ws.write(self.result, 22, task.project['opis'])
		    self.ws.write(self.result, 23, u'DOMOFOND.RU')
		    self.ws.write_string(self.result, 24, task.project['url'])
		    self.ws.write(self.result, 25, task.project['phone'])
		    self.ws.write(self.result, 26, task.project['lico'])
		    self.ws.write(self.result, 27, task.project['company'])
		    self.ws.write(self.result, 28, task.project['data'])
		    self.ws.write(self.result, 30, datetime.today().strftime('%d.%m.%Y'))
		    print('*'*50)
		    #print task.sub
		    
		    print 'Ready - '+str(self.result)+' / '+self.num
		    logger.debug('Tasks - %s' % self.task_queue.size())
		    print '*',i+1,'/',dc,'*'
		    print agents[self.g]
		    print('*'*50) 
		    self.result+= 1
			 
			 
			 
		    #if self.result >= 50:
			 #self.stop()
     
	  
     bot = Dmf_Zem(thread_number=5,network_try_limit=1000)
     bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
     bot.create_grab_instance(timeout=50, connect_timeout=500)
     bot.run()
     print bot.sub
     print('Спим 1 сек...')
     time.sleep(1)
     print('Сохранение...')
     bot.workbook.close()
     print('Done!')
    
     i=i+1
     try:
          page = l[i]
     except IndexError:
	  break 
     






