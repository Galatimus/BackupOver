#! /usr/bin/env python
# -*- coding: utf-8 -*-




from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time



profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/ymoy2ffu.default/')#Gui1
#profile = webdriver.FirefoxProfile()
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)
driver.set_window_position(0,0)
driver.set_window_size(900,700)

driver.get(url='https://www.google.com/recaptcha/api2/demo')
captchaResponse = '03AJIzXZ4bCapZpoF4RAS9-Bz4WZaursOnkp9qRSBX6f-Jph9lvhL6oMhyZB8tuAgmQZT0jnuQ0fq1GdcJIZkwqlbbHQQsfDMsrl2awbt9y1joIwLqIv_ZwV37xoQGVD2sUJfNv576ugmnxBHWrHzjHQuigwgq88TACv-WOnO2Q6BSTrLzY_JS4Tnyb05uTAlFPUlpabJ1jRlzBVXQIUB2UINhCCYt5y-kQ1xRNaxphCHgh1q4COVt7UgPj9IKSoHurOiqCzX4LjxoWWi4B4Oi2V6hfFE7mD3RQdAuk0UwJjJBnjfILRmkEIsaVS0gz8NJ0yc02joM-WiLRfozmPNDeiIJX_Lf2dQRtKTed2aGvo485SBlIg1vZysGm3OCw3fE037_3ouRawTMXcr__P4CxTkI3AiOJPDnIjuiTeFL1KH32k7X2ihd3Jj9dV9EIMCpGqxugx0BlKBt'
## find iframe
captcha_iframe = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'iframe')))
time.sleep(2)
ActionChains(driver).move_to_element(captcha_iframe).click().perform()
time.sleep(2)
## click im not robot
captcha_box = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'g-recaptcha-response')))
time.sleep(2)
driver.execute_script("arguments[0].click()", captcha_box)
time.sleep(2)

driver.execute_script("document.getElementById('g-recaptcha-response').setAttribute('style', 'block')")

time.sleep(5)

driver.find_element_by_id('g-recaptcha-response').send_keys(captchaResponse)

time.sleep(1)

driver.find_element_by_id('recaptcha-demo-submit').click()

print('Done!') 

     

	  #self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	  #self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
	  #self.ws.write(0, 3, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	  #self.ws.write(0, 4, u"УЛИЦА")
	  #self.ws.write(0, 5, u"ДОМ")
	  #self.ws.write(0, 6, u"ОРИЕНТИР")
	  #self.ws.write(0, 7, u"ТРАССА")
	  #self.ws.write(0, 8, u"УДАЛЕННОСТЬ")
	  #self.ws.write(0, 9, u"КАДАСТРОВЫЙ_НОМЕР_ЗЕМЕЛЬНОГО_УЧАСТКА")
	  #self.ws.write(0, 10, u"ТИП_ОБЪЕКТА")
	  #self.ws.write(0, 11, u"ОПЕРАЦИЯ")
	  #self.ws.write(0, 12, u"СТОИМОСТЬ")
	  #self.ws.write(0, 13, u"ЦЕНА_М2")
	  #self.ws.write(0, 14, u"ПЛОЩАДЬ_ОБЩАЯ")
	  #self.ws.write(0, 15, u"КОЛИЧЕСТВО_КОМНАТ")
	  #self.ws.write(0, 16, u"ЭТАЖНОСТЬ")
	  #self.ws.write(0, 17, u"МАТЕРИАЛ_СТЕН")
	  #self.ws.write(0, 18, u"ГОД_ПОСТРОЙКИ")
	  #self.ws.write(0, 19, u"ПЛОЩАДЬ_УЧАСТКА")
	  #self.ws.write(0, 20, u"ДОПОЛНИТЕЛЬНЫЕ_ПОСТРОЙКИ")
	  #self.ws.write(0, 21, u"ГАЗОСНАБЖЕНИЕ")
	  #self.ws.write(0, 22, u"ВОДОСНАБЖЕНИЕ")
	  #self.ws.write(0, 23, u"КАНАЛИЗАЦИЯ")
	  #self.ws.write(0, 24, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  #self.ws.write(0, 25, u"ТЕПЛОСНАБЖЕНИЕ")
	  #self.ws.write(0, 26, u"ЛЕС")
	  #self.ws.write(0, 27, u"ВОДОЕМ")
	  #self.ws.write(0, 28, u"БЕЗОПАСНОСТЬ")
	  #self.ws.write(0, 29, u"ОПИСАНИЕ")
	  #self.ws.write(0, 30, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 31, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 32, u"ТЕЛЕФОН")
	  #self.ws.write(0, 33, u"КОНТАКТНОЕ_ЛИЦО")
	  #self.ws.write(0, 34, u"КОМПАНИЯ")
	  #self.ws.write(0, 35, u"ДАТА_РАЗМЕЩЕНИЯ")
	  #self.ws.write(0, 36, u"ДАТА_ПАРСИНГА")
	  #self.ws.write(0, 37, u"ВИД_РАЗРЕШЕННОГО_ИСПОЛЬЗОВАНИЯ")
	  #self.ws.write(0, 38, u"МЕСТОПОЛОЖЕНИЕ")
	       
	       
	  #self.result= 1
	
	       
    
     #def task_generator(self):
	  #for line in open('Links/Zag.txt').read().splitlines():
	       #yield Task ('post',url=line.strip(),refresh_cache=True,network_try_count=100)
          ##yield Task ('post',url='http://www.cian.ru/cat.php?deal_type=rent&engine_version=2&object_type[0]=1&object_type[1]=2&object_type[2]=4&offer_type=suburban&region=4593',refresh_cache=True,network_try_count=100)  
            
     #def task_page(self,grab,task):
	  #try:         
	       #pg = grab.doc.select(u'//div[@class="pager_pages"]/span/following-sibling::a[1]')
	       #u = grab.make_url_absolute(pg.attr('href'))
	       #yield Task ('post',url= u,refresh_cache=True,network_try_count=100)
	  #except DataNotFound:
	       #print('*'*50)
	       #print '!!!!','NO PAGE NEXT','!!!'
	       #print('*'*50)
	       #logger.debug('%s taskq size' % self.task_queue.size())             
        
        
            
            
     #def task_post(self,grab,task): 
	  #for elem in grab.doc.select(u'//a[@class="serp-item__card-link link"]'):
	       #ur = grab.make_url_absolute(elem.attr('href'))  
	       ##print ur
	       #yield Task('item', url=ur,refresh_cache=True,network_try_count=100,use_proxylist=False)
	  #yield Task("page", grab=grab,refresh_cache=True,network_try_count=100,use_proxylist=False)
        
        
     #def task_item(self, grab, task):
	  #try:
	       #sub = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[1]').text()#.split(', ')[0]
	  #except DataNotFound:
	       #sub = ''
	  #try:
	       #ray = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"район")]').text()
	  #except DataNotFound:
	       #ray = ''          
	  #try:
	       #if sub == u'Москва':
		    #punkt= u'Москва'
	       #elif sub == u'Санкт-Петербург':
		    #punkt= u'Санкт-Петербург'
	       #elif sub == u'Севастополь':
		    #punkt= u'Севастополь'
	       #else:
		    #if  grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2][contains(text(),"район")]').exists()==True:
			 #punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]/a[3]').text()
		    #elif grab.doc.select(u'//h1[@class="object_descr_addr"]/a[3][contains(text(),"район")]').exists()==True:
			 #punkt= grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2]').text()
		    #else:
			 #punkt=grab.doc.select(u'//h1[@class="object_descr_addr"]/a[2]').text()
	  #except IndexError:
	       #punkt = ''
	       
	  #try:
	       #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  #except IndexError:
	       #ter =''
	       
	  #try:
	       #try:
		    #try:
			 #try:
			      #try:
				   #try:
					#try:
					     #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ул.")]').text()
					#except IndexError:
					     #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"пер.")]').text()
				   #except IndexError:
					#uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"просп.")]').text()
			      #except IndexError:
				   #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"ш.")]').text()
			 #except IndexError:
			      #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"бул.")]').text()
		    #except IndexError:
			 #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"проезд")]').text()
	       #except IndexError:
		    #uliza = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(text(),"наб.")]').text()
	  #except IndexError:
	       #uliza =''
	       
	  #try:
               #dom = grab.doc.select(u'//h1[@class="object_descr_addr"]/a[contains(@href,"house")]').text()
          #except IndexError:
	       #dom = '' 
	       
	  #try:
	       #trassa = grab.doc.select(u'//div[@class="object_descr_metro"]/a[contains(text(),"шоссе")]').text()
		##print rayon
	  #except DataNotFound:
	       #trassa = ''
	       
	  #try:
	       #udal = grab.doc.select(u'//span[@class="objects_item_metro_comment"]/span[contains(text(),"км.")]').text()
	  #except DataNotFound:
	       #udal = ''
          #try:
	       #if grab.doc.select(u'//div[@class="object_descr_title"]').text().find(u'дом') <> -1:
                    #tip_ob = u'Дом'
               #else:
		    #tip_ob = u'Таунхаус '
          #except IndexError:
               #tip_ob = ''	       
	       
	  #try:
	       #price = grab.doc.select(u'//div[@class="object_descr_price"]').text()
	  #except DataNotFound:
	       #price = ''
	       
	  
	       
	  #try:
	       #plosh = re.sub(u'[^\d\,\м\ ]','',grab.doc.select(u'//div[@class="object_descr_title"]').text()).split(u'м ')[1]
	  #except IndexError:
	       #plosh = ''
	       
          #try:
               #etash = re.sub(u'[^\d\,\м\ ]','',grab.doc.select(u'//div[@class="object_descr_title"]').text()).split(u'м ')[0][:1]
          #except IndexError:
               #etash = ''
	       
          #try:
               #plosh_uch = grab.doc.select(u'//th[contains(text(),"Площадь участка:")]/following-sibling::td').text()
          #except DataNotFound:
               #plosh_uch = ''
	  
	  
	       
	  #try:
	       #vid = grab.doc.select(u'//th[contains(text(),"Тип земли:")]/following-sibling::td').text()
	  #except DataNotFound:
	       #vid = '' 
	       
	       
	  #try:
	       #ohrana = grab.doc.select(u'//h1').text()
	  #except DataNotFound:
	       #ohrana =''
	  #try:
	       #gaz = re.sub(u'^.*(?=газ)','', grab.doc.select(u'//*[contains(text(), "газ")]').text())[:3].replace(u'газ',u'есть')
	  #except DataNotFound:
	       #gaz =''
	  #try:
	       #voda = re.sub(u'^.*(?=вод)','', grab.doc.select(u'//*[contains(text(), "вод")]').text())[:3].replace(u'вод',u'есть')
	  #except DataNotFound:
	       #voda =''
	  #try:
	       #kanal = re.sub(u'^.*(?=санузел)','', grab.doc.select(u'//*[contains(text(), "санузел")]').text())[:7].replace(u'санузел',u'есть')
	  #except DataNotFound:
	       #kanal =''
	  #try:
	       #elek = re.sub(u'^.*(?=лектричество)','', grab.doc.select(u'//*[contains(text(), "лектричество")]').text())[:12].replace(u'лектричество',u'есть')
	  #except DataNotFound:
	       #elek =''
	  #try:
	       #teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
	  #except DataNotFound:
	       #teplo =''
	  #try:
	       #les = grab.doc.select(u'//th[contains(text(),"Количество спален:")]/following-sibling::td').text()
	  ##gazz = gaz.replace('True',u'есть')
	  #except DataNotFound:
	       #les =''
	    
	  #try:
	       #vodoem = grab.doc.select(u'//th[contains(text(),"Материал дома:")]/following-sibling::td').text()
	  ##gazz = gaz.replace('True',u'есть')
	  #except DataNotFound:
	       #vodoem =''	  
	       
	  #try:
	       #oper = grab.doc.select(u'//div[@class="breadcrumbs breadcrumbs_override"]/a[2]').text() 
	  #except DataNotFound:
	       #oper = ''               
	      
		    
	  #try:
	       #opis = grab.doc.select(u'//div[@class="object_descr_text"]/text()').text() 
	  #except DataNotFound:
	       #opis = ''
	       
	  #try:
	       #phone = grab.doc.rex_text(u'tel:(.*?)">')
	  #except DataNotFound:
	       #phone = ''
	       
	  #try:
	       #try:
	            #lico = grab.doc.select(u'//h3[@class="realtor-card__title"][contains(text(),"Представитель: ")]').text().replace(u'Представитель: ','')
	       #except IndexError:
	            #lico = grab.doc.select(u'//h3[@class="realtor-card__title"]/a[contains(@href,"agents")]').text() 
	  #except IndexError:
	       #lico = ''
	       
	  #try:
	       #try:
		    #comp = grab.doc.select(u'//h3[@class="realtor-card__title"]/a[contains(@href,"company")]').text()
	       #except IndexError:
		    #comp = grab.doc.select(u'//h4[@class="realtor-card__subtitle"]').text()
	  #except IndexError:
	       #comp = '' 
	       
	  #try:
	       #conv = [ (u'сегодня', (datetime.today().strftime('%d.%m.%Y'))),
		        #(u'вчера','{:%d.%m.%Y}'.format(datetime.today() - timedelta(days=1))),
		        #(u'Окт', '.10.2016'),(u'окт', '.10.2016'),
		        #(u'Сен', '.09.2016'),(u'сен', '.09.2016'),
		        #(u'Авг', '.08.2016'),(u'авг', '.08.2016'),
		        #(u'Июл', '.07.2016'),(u'июл', '.07.2016'),
		        #(u'Июн', '.06.2016'),(u'июн', '.06.2016'),
		        #(u'Май', '.05.2016'),(u'май', '.05.2016'),
		        #(u'Янв', '.05.2016'),(u'янв', '.05.2016'),
		        #(u'Фев', '.05.2016'),(u'фев', '.05.2016'),
		        #(u'Мар', '.05.2016'),(u'мар', '.05.2016'),
		        #(u'Апр', '.04.2016'),(u'апр', '.04.2016'), 
		        #(u'Апр', '.04.2016'),(u'апр', '.04.2016'),
		        #(u'Май', '.05.2016'),(u'май', '.05.2016')]
	       #dt= grab.doc.select(u'//ul[@class="offerStatuses"]/following-sibling::span[@class="object_descr_dt_added"]').text().split(', ')[0]
	       #data = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt).replace(' ','')
	  
	  #except IndexError:
	       #data = ''
		    
	  
	   
	       
	  #projects = {'url': task.url,
                      #'sub': sub,
                      #'rayon': ray,
                      #'punkt': punkt.replace(u' городской округ',''),
                      #'teritor': ter,
                      #'ulica': uliza,
	               #'dom': dom,
                      #'trassa': trassa,
                      #'udal': udal,
	              #'object': tip_ob,
                      #'cena': price,
                      #'plosh':plosh,
	              #'etach': etash,
	              #'plouh': plosh_uch,
                      #'vid': vid,
                      #'ohrana':ohrana,
                      #'gaz': gaz,
                      #'voda': voda,
                      #'kanaliz': kanal,
                      #'electr': elek,
                      #'teplo': teplo,
	              #'les': les,
                      #'vodoem':vodoem,
                      #'opis':opis,
                      #'phone':phone,
                      #'lico':lico,
                      #'company':comp,
                      #'data':data,
                      #'oper':oper
                      #}
          
	  #yield Task('write',project=projects,grab=grab,refresh_cache=True)
            
     #def task_write(self,grab,task):
	  #print('*'*50)
	  #print  task.project['sub']
	  #print  task.project['rayon']
	  #print  task.project['punkt']
	  #print  task.project['teritor']
	  #print  task.project['ulica']
	  #print  task.project['dom']
	  #print  task.project['trassa']
	  #print  task.project['udal']
	  #print  task.project['object']
	  #print  task.project['cena']
	  #print  task.project['plosh']
	  #print  task.project['etach']
	  #print  task.project['plouh']
	  #print  task.project['vid']
	  #print  task.project['ohrana']
	  #print  task.project['gaz']
	  #print  task.project['voda']
	  #print  task.project['kanaliz']
	  #print  task.project['electr']
	  #print  task.project['teplo']
	  #print  task.project['les']
	  #print  task.project['vodoem']	  
	  #print  task.project['opis']
	  #print task.project['url']
	  #print  task.project['phone']
	  #print  task.project['lico']
	  #print  task.project['company']
	  #print  task.project['data']
	  
	  
	  ##global result
	  #self.ws.write(self.result, 0, task.project['sub'])
	  #self.ws.write(self.result, 1, task.project['rayon'])
	  #self.ws.write(self.result, 2, task.project['punkt'])
	  #self.ws.write(self.result, 3, task.project['teritor'])
	  #self.ws.write(self.result, 4, task.project['ulica'])
	  #self.ws.write(self.result, 7, task.project['trassa'])
	  #self.ws.write(self.result, 8, task.project['udal'])
	  #self.ws.write(self.result, 11, task.project['oper'])
	  #self.ws.write(self.result, 10, task.project['object'])
	  #self.ws.write(self.result, 12, task.project['cena'])
	  #self.ws.write(self.result, 14, task.project['plosh'])
	  #self.ws.write(self.result, 21, task.project['gaz'])
	  #self.ws.write(self.result, 16, task.project['etach'])
	  #self.ws.write(self.result, 23, task.project['kanaliz'])
	  #self.ws.write(self.result, 24, task.project['electr'])
	  #self.ws.write(self.result, 19, task.project['plouh'])
	  #self.ws.write(self.result, 38, task.project['ohrana'])
	  #self.ws.write(self.result, 22, task.project['voda'])	  
	  #self.ws.write(self.result, 25, task.project['teplo'])
          #self.ws.write(self.result, 15, task.project['les'])
          #self.ws.write(self.result, 17, task.project['vodoem'])
	  #self.ws.write(self.result, 29, task.project['opis'])
          #self.ws.write(self.result, 37, task.project['vid'])
	  #self.ws.write(self.result, 30, u'ЦИАН')
	  #self.ws.write_string(self.result, 31, task.project['url'])
	  #self.ws.write(self.result, 32, task.project['phone'])
	  #self.ws.write(self.result, 33, task.project['lico'])
	  #self.ws.write(self.result, 34, task.project['company'])
	  #self.ws.write(self.result, 35, task.project['data'])
	  #self.ws.write(self.result, 36, datetime.today().strftime('%d.%m.%Y'))
	  #print('*'*50)
	  ##print task.sub
	  
	  #print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  #logger.debug('Tasks - %s' % self.task_queue.size())
	  ##print '*',i+1,'/',dc,'*'
	  #print  task.project['oper']
	  #print('*'*50)	       
	  #self.result+= 1
	       
	       
	       
	  ##if self.result > 50:
	       ##self.stop()

     
#bot = Cian_Zag(thread_number=3,network_try_limit=1000)
#bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
#bot.create_grab_instance(timeout=500, connect_timeout=5000)
#bot.run()
#workbook.close()
#print('Done!') 
 






