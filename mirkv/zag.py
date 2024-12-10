#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
from grab import Grab
import re
import time
import xlsxwriter
import os
import math
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)






i = 0
l= open('links/Zag_Prod.txt').read().splitlines()#.decode('cp1251').splitlines()
dc = len(l)
page = l[i]
oper = u'Продажа'

while True:
     print '********************************************',i+1,'/',dc,'*******************************************'
     class MK_Zag(Spider):
	  def prepare(self):
	       self.f = page
	       self.link =l[i]
	       while True:
		    try:
			 time.sleep(5)
			 g = Grab(timeout=20, connect_timeout=20)
			 g.go(self.f)
			 self.sub = g.doc.select(u'//span[@class="current"]').text()
			 try:
			      self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="b-all-offers"]').text())
			      self.pag = int(math.ceil(float(int(self.num))/float(20)))
			 except IndexError:
			      self.pag=0
			      self.num=0			      
			 print self.sub,self.num,self.pag
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
		         print g.config['proxy'],'Change proxy'
		         g.change_proxy()
		         continue	       
	       
	       self.workbook = xlsxwriter.Workbook(u'zag/Mirkvartir_%s' % bot.sub + u'_Загород_'+oper+str(i+1)+ '.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Mirkvartir_Загород')
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
	       self.ws.write(0, 37, u"МЕСТОПОЛОЖЕНИЕ")
	       
		    
		    
	       self.result= 1
	     
		    
	 
	  def task_generator(self):
	       for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'?p=%d'%x,network_try_count=100)
	
		 
	  def task_post(self,grab,task):
	       if grab.doc.select(u'//h2[@class="nearby-header"]').exists()==True:
		    links = grab.doc.select(u'//h2[@class="nearby-header"]/preceding::div[@class="item"]/a')
	       else:
		    links = grab.doc.select(u'//div[@class="item"]/a')     
	       for elem in links:
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur
		    yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	       #yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	     
	     
	  def task_item(self, grab, task):
	      
	       try:
		    ray = grab.doc.select(u'//a[@class="js-popup-select popup-select Province-popup"]/following::span[1]').text()
	       except DataNotFound:
		    ray = ''          
	       try:
		    punkt= grab.doc.select(u'//a[@class="js-popup-select popup-select City-popup"]/following::span[1]').text()
	       except IndexError:
		    punkt = ''
		    
	       try:
		    ter= grab.doc.select(u'//a[@class="js-popup-select popup-select InhabitedPoint-popup"]/following::span[1]').text()
		    
	       except IndexError:
		    ter =''
		    
	       try:
		   
		    uliza = grab.doc.select(u'//a[@class="js-popup-select popup-select Street-popup"]/following::span[1]').text()
		 
	       except IndexError:
		    uliza = ''
		    
	       try:
		    dom = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p/a[contains(@href,"houseId")]').text()
	       except DataNotFound:
		    dom = ''
		    
	       try:
		    trassa = grab.doc.select(u'//label[contains(text(),"Шоссе:")]/following-sibling::p').text().split(', ')[0]
	       except IndexError:
		    trassa = ''
		    
	       try:
		    udal = grab.doc.select(u'//label[contains(text(),"Шоссе:")]/following-sibling::p').text().split(', ')[1]
	       except IndexError:
		    udal = ''
	       try:
		    conv = [(u'дома',u'Дом'),(u'коттеджа',u'Коттедж'),
			    (u'таунхауса',u'Таунхаус'),(u'дачи',u'Дача')]
		    tip=  grab.doc.select(u'//h1[@class="offer-title"]/small').text().split(' ')[1].replace(',','')
		    tip_ob = reduce(lambda tip, r: tip.replace(r[0], r[1]), conv, tip)
	       except IndexError:
		    tip_ob = ''	       
		    
	       try:
		    price = grab.doc.select(u'//p[@class="price"]/strong').text()+u' р.'
	       except DataNotFound:
		    price = ''
		    
	       
		    
	       try:
		    plosh = grab.doc.select(u'//label[contains(text(),"Площадь:")]/following-sibling::p').text().split(u'м²')[0]+ u'м2'
	       except IndexError:
		    plosh = ''
		    
	       try:
		    kom = grab.doc.select(u'//label[contains(text(),"Всего комнат:")]/following-sibling::p').number()
	       except DataNotFound:
		    kom = ''	       
		    
	       try:
		    etash = grab.doc.select(u'//label[contains(text(),"Этажность:")]/following-sibling::p').number()
	       except IndexError:
		    etash = ''
		    
	       try:
		    mat = grab.doc.select(u'//label[contains(text(),"Дом:")]/following-sibling::p').text().split(', ')[0]
	       except IndexError:
		    mat = ''
	       try:
		    god = grab.doc.select(u'//label[contains(text(),"Дом:")]/following-sibling::p').text().split(', ')[1]
	       except IndexError:
		    god = ''	       
		    
	       try:
		    plosh_uch = grab.doc.select(u'//label[contains(text(),"Площадь:")]/following-sibling::p').text().split(u'участок ')[1]
	       except IndexError:
		    plosh_uch = ''
	       
		 
	       try:
		    ohrana = grab.doc.select(u'//small[contains(text(),"м²")]/ancestor::p').text()
	       except DataNotFound:
		    ohrana =''
	       try:
		    z =  grab.doc.select(u'//label[contains(text(),"Коммуникации:")]/following-sibling::p').text()
		    if z.find(u'газ')>=0:
			 gaz='есть'
		    else:
			 gaz=''
	       except DataNotFound:
		    gaz =''
	       try:
		    v =  grab.doc.select(u'//label[contains(text(),"Коммуникации:")]/following-sibling::p').text()
		    if v.find(u'вода')>=0:
			 voda='есть'
		    else:
			 voda=''
	       except DataNotFound:
	            voda =''
	       try:
		    k =  grab.doc.select(u'//label[contains(text(),"Коммуникации:")]/following-sibling::p').text()
		    if k.find(u'канализация')>=0:
			 kanal='есть'
		    else:
			 kanal=''
	       except DataNotFound:
			 kanal =''
	       try:
			 lk =  grab.doc.select(u'//label[contains(text(),"Коммуникации:")]/following-sibling::p').text()
			 if lk.find(u'электричество')>=0:
			      elek='есть'
			 else:
			      elek=''
	       except DataNotFound:
			 elek =''
	       try:
		    teplo = grab.doc.select(u'//label[contains(text(),"Адрес:")]/following-sibling::p').text()
	       except DataNotFound:
		    teplo =''
	       try:
		    les = re.sub(u'^.*(?=лес)','', grab.doc.select(u'//*[contains(text(), "лес")]').text())[:3].replace(u'лес',u'есть')
	       #gazz = gaz.replace('True',u'есть')
	       except DataNotFound:
		    les =''
		 
	       try:
		    vodoem = re.sub(u'^.*(?=озер)','', grab.doc.select(u'//*[contains(text(), "озер")]').text())[:4].replace(u'озер',u'есть')
	       #gazz = gaz.replace('True',u'есть')
	       except DataNotFound:
		    vodoem =''	  
		    
	                     
		   
			 
	       try:
		    opis = grab.doc.select(u'//div[@class="clear"]/following-sibling::p').text() 
	       except DataNotFound:
		    opis = ''

	       try:
		    lico = grab.doc.select(u'//span[@class="phones"]/following-sibling::text()').text()
	       except IndexError:
		    lico = ''
		    
	       try:
		    comp = grab.doc.select(u'//a[@rel="nofollow"]').text().replace(u'Показать телефон','')
	       except DataNotFound:
		    comp = ''
		    
	       try:

		    conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		         (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		         (u'августа', '.08.2017'),(u'мая', '.05.2017'),(u'ноября', '.11.2016'),
		         (u'марта', '.03.2017'),(u'сентября', '.09.2017'),(u'октября', '.10.2017'),(u'января', '.01.2017'),(u'февраля', '.02.2017'),(u'апреля', '.04.2017'),
		         (u'июля', '.07.2017'),(u'июня', '.06.2017'),(u'декабря', '.12.2016')]
		    dt= grab.doc.rex_text(u'Опубликовано: (.*?)в ').replace(' (','')
		    data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','').replace(u'более3-хмесяце','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=92)))
		    #print data
	       except IndexError:
	            data = ''
			 
	       
							
		    
	       projects = {'url': task.url,
		           'sub': self.sub,
		           'rayon': ray,
		           'punkt': punkt,
		           'teritor': ter,
		           'ulica': uliza,
		            'dom': dom,
		           'trassa': trassa,
		           'udal': udal,
		           'object': tip_ob,
		           'cena': price,
		           'plosh':plosh,
		           'kom':kom,
		           'etach': etash,
		           'material': mat,
		           'god_postr': god,
		           'plouh': plosh_uch,
		           'ohrana':ohrana,
		           'gaz': gaz,
		           'voda': voda,
		           'kanaliz': kanal,
		           'electr': elek,
		           'teplo': teplo,
		           'les': les,
		           'vodoem':vodoem,	              
		           'opis':opis,
		           'lico':lico,
		           'company':comp,
		           'data':data }
	       
	       try:
		         #ad_id= re.sub(u'[^\d]','',task.url[-9:])
		    ad_id= re.sub(u'[^\d]','',task.url)
		    ad_phone = grab.doc.select(u'//span[@class="phone"]/a').attr('key')
		    link = grab.make_url_absolute('/EstateOffers/DecryptPhone?offerId='+ad_id+'&encryptedPhone='+ad_phone)
		    headers ={'Accept': '*/*',
			      'Accept-Encoding': 'gzip,deflate',
			      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			      'Cookie': 'sessid='+ad_id+'.'+ad_phone,
			      'Host': 'mirkvartir.ru',
			      'Referer': task.url,
			      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0', 
			      'X-Requested-With' : 'XMLHttpRequest'}
		    gr = Grab()
		    gr.setup(url=link)
		    yield Task('phone',grab=gr,project=projects,refresh_cache=True,network_try_count=100)
	       except IndexError:
	            yield Task('phone',grab=grab,project=projects)	       
	       
	  def task_phone(self, grab, task):
	       try:
		    phone = grab.doc.rex_text(u'normalizedPhone":"(.*?)"')
	       except (IndexError,ValueError,GrabNetworkError,GrabTimeoutError,IOError):
		    phone = ''	  
	       
	       
	       yield Task('write',project=task.project,phone=phone,grab=grab)
		 
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
	       print  task.project['object']
	       print  task.project['cena']
	       print  task.project['plosh']
	       print  task.project['kom']
	       print  task.project['etach']
	       print  task.project['material']
	       print  task.project['god_postr']
	       print  task.project['plouh']
	       print  task.project['ohrana']
	       print  task.project['gaz']
	       print  task.project['voda']
	       print  task.project['kanaliz']
	       print  task.project['electr']
	       print  task.project['teplo']
	       print  task.project['les']
	       print  task.project['vodoem']	  
	       print  task.project['opis']
	       print task.project['url']
	       print  task.phone
	       print  task.project['lico']
	       print  task.project['company']
	       print  task.project['data']
	       
	       
	       #global result
	       self.ws.write(self.result, 0, task.project['sub'])
	       self.ws.write(self.result, 1, task.project['rayon'])
	       self.ws.write(self.result, 2, task.project['punkt'])
	       self.ws.write(self.result, 3, task.project['teritor'])
	       self.ws.write(self.result, 4, task.project['ulica'])
	       self.ws.write(self.result, 5, task.project['dom'])
	       self.ws.write(self.result, 7, task.project['trassa'])
	       self.ws.write(self.result, 8, task.project['udal'])
	       self.ws.write(self.result, 11, oper)
	       self.ws.write(self.result, 10, task.project['object'])
	       self.ws.write(self.result, 12, task.project['cena'])
	       self.ws.write(self.result, 14, task.project['plosh'])
	       self.ws.write(self.result, 15, task.project['kom'])
	       self.ws.write(self.result, 21, task.project['gaz'])
	       self.ws.write(self.result, 16, task.project['etach'])
	       self.ws.write(self.result, 17, task.project['material'])
	       self.ws.write(self.result, 18, task.project['god_postr'])
	       self.ws.write(self.result, 23, task.project['kanaliz'])
	       self.ws.write(self.result, 24, task.project['electr'])
	       self.ws.write(self.result, 19, task.project['plouh'])
	       self.ws.write(self.result, 13, task.project['ohrana'])
	       self.ws.write(self.result, 22, task.project['voda'])	  
	       self.ws.write(self.result, 37, task.project['teplo'])
	       self.ws.write(self.result, 26, task.project['les'])
	       self.ws.write(self.result, 27, task.project['vodoem'])
	       self.ws.write(self.result, 29, task.project['opis'])
	       self.ws.write(self.result, 30, u'MIRKVARTIR.RU')
	       self.ws.write_string(self.result, 31, task.project['url'])
	       self.ws.write(self.result, 32, task.phone)
	       self.ws.write(self.result, 33, task.project['lico'])
	       self.ws.write(self.result, 34, task.project['company'])
	       self.ws.write(self.result, 35, task.project['data'])
	       self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	       print('*'*50)
	       #print task.sub
	       
	       print 'Ready - '+str(self.result)+'/'+str(self.num)
	       logger.debug('Tasks - %s' % self.task_queue.size())
	       print '*',i+1,'/',dc,'*'
	       print oper
	       print('*'*50)	       
	       self.result+= 1
		    
		    
		    
	       #if self.result > 30:
		    #self.stop()
               if str(self.result) == str(self.num):
	            self.stop()		    
     
	  
     bot = MK_Zag(thread_number=3,network_try_limit=1000)
     bot.load_proxylist('../tipa.txt','text_file')
     bot.create_grab_instance(timeout=5, connect_timeout=10)
     bot.run()
     print('Wait 2 sec...')
     time.sleep(2)
     print('Save it...')
     try:
	  command = 'mount -t cifs //192.168.1.6/d /home/oleg/pars -o _netdev,sec=ntlm,auto,username=oleg,password=1122,file_mode=0777,dir_mode=0777'
	  os.system('echo %s|sudo -S %s' % ('1122', command))
	  time.sleep(3)
	  bot.workbook.close()
	  print('Done')
     except IOError:
	  time.sleep(30)
	  os.system('echo %s|sudo -S %s' % ('1122', 'mount -a'))
	  time.sleep(10)
	  bot.workbook.close()
	  print('Done!')
     i=i+1
     try:
	  page = l[i]
     except IndexError:
	  if oper == u'Продажа':
	       i = 0
	       l= open('links/Zag_Arenda.txt').read().splitlines()
	       dc = len(l)
	       page = l[i]
	       oper = u'Аренда'
	  else:
	       break    
       






