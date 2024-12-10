#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
import math
import random
from datetime import datetime,timedelta
import xlsxwriter
from cStringIO import StringIO
import pytesseract
from PIL import Image 
import os
import time
import base64
from grab import Grab
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



logging.basicConfig(level=logging.DEBUG)


i = 0
l= open('comp.txt').read().splitlines()
page = l[i]
oper = u'Продажа'





while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'	   

     class Metr(Spider):
	  def prepare(self):
	       self.f = page
	       self.workbook = xlsxwriter.Workbook(u'com/Kvmeter_'+oper+str(i+1) + '.xlsx')
	       self.ws = self.workbook.add_worksheet()
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
	       self.result= 1
		
     
     
	  def task_generator(self):
	       #for x in range(1,500):
                    #yield Task ('post',url=self.f+'?PAGEN_1=%d'%x,refresh_cache=True,network_try_count=1000)
	       yield Task ('post',url=self.f,refresh_cache=True,network_try_count=100)		    
		    
		    
	  def task_post(self,grab,task):
	       for elem in grab.doc.select(u'//a[contains(@href,"objects")]'):
		    ur = grab.make_url_absolute(elem.attr('href'))  
		    #print ur	      
		    yield Task('item',url=ur,refresh_cache=True,network_try_count=100)
	       yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
		    
	  def task_page(self,grab,task):
	       try:
		    pg = grab.doc.select(u'//li[@class="active"]/following-sibling::li/a[contains(text(),"Следующая")]')
		    u = grab.make_url_absolute(pg.attr('href'))
		    yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	       except IndexError:
		    print('*'*100)
		    print '!!!','NO PAGE NEXT','!!!'
		    print('*'*100)
			 
	       
		  
	  def task_item(self, grab, task):
	       
	       try:
		    mesto = grab.doc.select(u'//meta[@itemprop="addressRegion"]').attr('content').replace('город ','')
	       except IndexError:
		    mesto = ''
	  
	       try:
		    ray =  grab.doc.select(u'//div[contains(text(), "Адрес")]/following-sibling::div/a[contains(@title,"район")]').text()
	       except IndexError:
		    ray = ''
	       try:
		    if mesto == u'Москва':
			 punkt= u'город Москва'
		    elif mesto == u'Санкт-Петербург':
			 punkt= u'Санкт-Петербург'
		    elif mesto == u'Севастополь':
			 punkt= u'Севастополь'
		    else:	       
			 punkt = grab.doc.select(u'//div[contains(text(), "Адрес")]/following-sibling::div/a[contains(text(),"город")]').text()
	       except IndexError:
		    punkt = ''
	       try:
		    uliza = grab.doc.select(u'//div[contains(text(), "Адрес")]/following-sibling::div/a[contains(@href,"street")]').text()
		    #uliza = re.split('(\W+)',ul)[1]
	       except IndexError:
		    uliza = ''
	       try:
		    dom = grab.doc.select(u'//div[contains(text(), "Адрес")]/following-sibling::div/a[contains(@href,"street")]/following-sibling::text()').text().replace(', ','')
		    #dom =re.split('\W+', d,1)[1]
	       except IndexError:
		    dom = ''
	       
	       try:
		    tip = grab.doc.select(u'//div[contains(text(), "Шоссе")]/following-sibling::div/a').text()
	       except IndexError:
		    tip = ''
	       try:
		    naz = grab.doc.select(u'//div[@id="b-object_detail"]/meta').attr('content')
	       except IndexError:
		    naz = ''
	       try:
		    klass = grab.doc.select(u'//div[contains(text(), "Тип дома")]/following-sibling::div').text()
	       except IndexError:
		    klass = ''
	       try:
		    price = grab.doc.select(u'//table[@class="block_cost"]').text().split('≈')[0]
	       except IndexError:
		    price = ''
	       try:
		    et = grab.doc.select(u'//div[contains(text(), "Адрес")]/following-sibling::div').text()
	       except IndexError:
		    et = ''
	  
	       try:
		    et2 = grab.doc.select(u'//div[contains(text(), "Станция метро")]/following-sibling::div').text().split(' – ')[0]
	       except IndexError:
		    et2 = ''
		    
	       try:
		    god = grab.doc.select(u'//div[contains(text(), "Год постройки")]/following-sibling::div').number()
	       except IndexError:
		    god = ''
	       
	       try:
		    mat = grab.doc.select(u'//div[contains(text(), "Станция метро")]/following-sibling::div').text().split(' – ')[1].split('(')[0]
	       except IndexError:
		    mat = ''
     
	            
	       try:
		    sos = grab.doc.select(u'//span[@class="item-map-metro"]').text().split(u' (')[0]
	       except IndexError:
		    sos = ''
		    
	       try:
		    plosh = grab.doc.select(u'//div[contains(text(), "Площадь")]/following-sibling::div').text()
	       except IndexError:
		    plosh = ''
	       
	       try:
		    gaz = grab.doc.select(u'//span[@class="item-map-metro"]').text().split(' (')[1].replace(')','')
	       except IndexError:
		    gaz =''
	       try:
		    voda = grab.doc.select(u'//title').text()
	       except IndexError:
		    voda =''
	       try:
		    kanal = grab.doc.rex_text(u"maps:'(.*?)',").split(',')[0]
	       except IndexError:
		    kanal =''
	       try:
		    elekt = grab.doc.rex_text(u"maps:'(.*?)',").split(',')[1]
	       except IndexError:
		    elekt =''
	       try:
		    teplo = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"отопление")]').text().replace(u'есть отопление',u'есть').replace(u'нет отопления','')
	       except IndexError:
		    teplo =''
	       try:
		    ohrana = grab.doc.select(u'//ul[@id="infra_data"]/li[contains(text(),"охрана")]').text().replace(u'есть охрана',u'есть').replace(u'нет охраны','')
	       except IndexError:
		    ohrana =''
	       try:
		    opis = grab.doc.select(u'//div[@itemprop="description"]').text() 
	       except IndexError:
		    opis = ''
	       try:
		    try:
			 try:
			      lico = grab.doc.select(u'//p[@class="lead"]/following-sibling::p[1]').text()
			 except IndexError:
			      lico = grab.doc.select(u'//p[@class="lead"]').text()
		    except IndexError:
			 lico = grab.doc.select(u'//div[contains(text(),"Контактное лицо")]/following-sibling::div').text()
	       except IndexError:
		    lico = ''
	       
	       try:
		    com = grab.doc.select(u'//a[@class="company"]').text()
	       except IndexError:
		    com = ''
		    
	       try:
		    ad_id= grab.doc.select(u'//img[contains(@src,"data:image/png;base64")]').attr('src').replace('data:image/png;base64,','')
		    imgdata = base64.b64decode(ad_id)
		    im = Image.open(StringIO(imgdata))
		    x,y = im.size
		    phone = pytesseract.image_to_string(im.convert("RGB").resize((int(x*2), int(y*3)),Image.BICUBIC))
		    del im	       
	       except IndexError:
		    phone = ''
		    
		    
	       try:
		    conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
			 (u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
			 (u'июня', '.06.'),(u' Июль ', '.07.'),(u'августа', '.08.'),(u' Январь ', '.01.'),(u' Февраль ', '.02.'),
			 (u' Март ', '.03.'),(u' Апрель ', '.04.'),(u'мая', '.05.2017'),
			 (u'ноября', '.11.'),(u'сентября', '.09.'),(u'октября', '.10.'),(u'декабря', '.12.')]
		    dt= grab.doc.select(u'//div[contains(text(), "Обновлено")]/following-sibling::div').text()
		    data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	       except IndexError:
		    data = ''		    
	       
	       
	       
	       
	       
	       
	       projects = {'url': task.url,
		         'rayon': ray,
		         'punkt': punkt,
		         'ulica': uliza,
		         'dom': dom,
		         'naz': naz,
		         'tip': tip,
		         'price': price,
		         'klass': klass,
		         'ploshad': plosh,
		         'et': et,
		         'ets': et2,
		         'god': god,
		         'mat': mat,
		         'potolok': oper,
		         'sost': sos,
		         'gaz': gaz,
		         'voda':voda,
		         'phone': re.sub('[^\d\,\+]','',phone),
		         'kanal': kanal,
		         'elekt': elekt,
		         'teplo': teplo,
		         'ohrana': ohrana,
		         'opis': opis,
		         'mesto':mesto,
		         'lico':lico,
		         'company':com,
		         'data': data }
	     
	       
	       yield Task('write',project=projects,grab=grab)
	       
	       
	       
	       
	       
	  def task_write(self,grab,task):
	       if task.project['mesto'] <>'':
		    print('*'*100)
		    print  task.project['mesto']
		    print  task.project['rayon']
		    print  task.project['punkt']
		    print  task.project['ulica']
		    print  task.project['dom']
		    print  task.project['naz']
		    print  task.project['tip']
		    print  task.project['price']
		    print  task.project['klass']
		    print  task.project['ploshad']
		    print  task.project['et']
		    print  task.project['ets']
		    print  task.project['god']
		    print  task.project['mat']	  
		    print  task.project['voda']
		    print  task.project['kanal']
		    print  task.project['elekt']
		    #print  task.project['teplo']
		    print  task.project['phone']
		    print  task.project['opis']
		    print  task.project['url']
		    print  task.project['lico']
		    print  task.project['company']
		    print  task.project['data']
		    
	       
		    self.ws.write(self.result,0, task.project['mesto'])
		    self.ws.write(self.result,1, task.project['rayon'])
		    self.ws.write(self.result,2, task.project['punkt'])
		    self.ws.write(self.result,4, task.project['ulica'])
		    self.ws.write(self.result,5, task.project['dom'])
		    self.ws.write(self.result,9, task.project['naz'])
		    self.ws.write(self.result,6, task.project['tip'])
		    self.ws.write(self.result,11, task.project['price'])
		    self.ws.write(self.result,8, task.project['klass'])
		    self.ws.write(self.result,14, task.project['ploshad'])
		    self.ws.write(self.result,24, task.project['et'])
		    self.ws.write(self.result,26, task.project['ets'])
		    self.ws.write(self.result,17, task.project['god'])
		    self.ws.write(self.result,27, task.project['mat'])
		    self.ws.write(self.result,28, task.project['potolok'])
		    #self.ws.write(self.result,26, task.project['sost'])
		    #self.ws.write(self.result,27, task.project['gaz'])
		    self.ws.write(self.result,33, task.project['voda'])
		    self.ws.write(self.result,34, task.project['kanal'])
		    self.ws.write(self.result,35, task.project['elekt'])
		    self.ws.write(self.result,18, task.project['opis'])
		    self.ws.write(self.result,19, u'Метр Квадратный')
		    self.ws.write_string(self.result,20, task.project['url'])
		    self.ws.write(self.result,22, task.project['lico'])
		    self.ws.write(self.result,23, task.project['company'])
		    self.ws.write(self.result,30, task.project['data'])
		    self.ws.write(self.result,31, datetime.today().strftime('%d.%m.%Y'))
		    self.ws.write(self.result,21, task.project['phone'])
		    
		   
		    
		    print('*'*50)	       
		    print 'Ready - '+str(self.result)
		    print 'Tasks - %s' % self.task_queue.size()
		    print  task.project['potolok']
		    print '***',i+1,'/',len(l),'***'
		    print('*'*50)
		   
		    self.result+= 1
		    
		    if self.result > 50:
			 self.stop()
			 
		   
     
     bot = Metr(thread_number=5, network_try_limit=1000)
     bot.load_proxylist('../../tipa.txt','text_file',proxy_type='http')
     bot.create_grab_instance(timeout=50, connect_timeout=50)
     try:
	  bot.run()
     except KeyboardInterrupt:
	  pass
     print('Wait 2 sec...')
     time.sleep(1)
     print('Save it...')    
     command = 'mount -a'
     p = os.system('echo %s|sudo -S %s' % ('1122', command))
     print p
     time.sleep(2)
     bot.workbook.close()
     print('Done!')
     i=i+1
     try:
          page = l[i]
     except IndexError: 
	  break