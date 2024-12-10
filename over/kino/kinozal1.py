#! /usr/bin/env python
# -*- coding: utf-8 -*-


from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
#from grab import Grab
import re
#import xlwt
import time
import xlsxwriter
from datetime import datetime,timedelta

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


workbook = xlsxwriter.Workbook(u'Kinozal_Аниме_Золото.xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Название раздачи")
	  self.ws.write(0, 1, u"Оригинальное название")
	  self.ws.write(0, 2, u"Год выпуска")
	  self.ws.write(0, 3, u"Жанр")
	  self.ws.write(0, 4, u"Выпущено")
	  self.ws.write(0, 5, u"В ролях")
	  self.ws.write(0, 6, u"О фильме")
	  self.ws.write(0, 7, u"Картинка(Url)")
	  self.ws.write(0, 8, u"Размер раздачи")
	  #self.ws.write(0, 9, u"Аудио")
	  #self.ws.write(0, 10, u"ПОТРЕБИТЕЛЬСКИЙ_КЛАСС")
	  #self.ws.write(0, 11, u"СТОИМОСТЬ")
	  #self.ws.write(0, 12, u"ПЛОЩАДЬ")
	  #self.ws.write(0, 13, u"ЭТАЖ")
	  #self.ws.write(0, 14, u"ЭТАЖНОСТЬ")
	  #self.ws.write(0, 15, u"ГОД_ПОСТРОЙКИ")
	  #self.ws.write(0, 16, u"МАТЕРИАЛ_СТЕН")
	  #self.ws.write(0, 17, u"ВЫСОТА_ПОТОЛКА")
	  #self.ws.write(0, 18, u"СОСТОЯНИЕ")
	  #self.ws.write(0, 19, u"БЕЗОПАСНОСТЬ")
	  #self.ws.write(0, 20, u"ГАЗОСНАБЖЕНИЕ")
	  #self.ws.write(0, 21, u"ВОДОСНАБЖЕНИЕ")
	  #self.ws.write(0, 22, u"КАНАЛИЗАЦИЯ")
	  #self.ws.write(0, 23, u"ЭЛЕКТРОСНАБЖЕНИЕ")
	  #self.ws.write(0, 24, u"ТЕПЛОСНАБЖЕНИЕ")
	  #self.ws.write(0, 25, u"ОПИСАНИЕ")
	  #self.ws.write(0, 26, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 27, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	  #self.ws.write(0, 28, u"ТЕЛЕФОН")
	  #self.ws.write(0, 29, u"КОНТАКТНОЕ_ЛИЦО")
	  #self.ws.write(0, 30, u"КОМПАНИЯ")
	  #self.ws.write(0, 31, u"ДАТА_РАЗМЕЩЕНИЯ")
	  #self.ws.write(0, 32, u"ДАТА_ПАРСИНГА")
	  #self.ws.write(0, 33, u"ОПЕРАЦИЯ")
	  #self.ws.write(0, 34, u"ЦЕНА_М2")
	  #self.ws.write(0, 35, u"МЕСТОПОЛОЖЕНИЕ")
	  self.result= 1
	
	       
    
     def task_generator(self):
	  for x in range(33):#30
               yield Task ('post',url= 'https://kinozal-tv.appspot.com/browse.php?c=20&w=11&page=%d'%x,network_try_count=100)
          #for x1 in range(9):#18
	       #yield Task ('post',url='https://kinozal-tv.appspot.com/browse.php?c=20&w=7&page=%d'%x1,network_try_count=100)
          #for x2 in range(13):#18
	       #yield Task ('post',url='https://kinozal-tv.appspot.com/browse.php?c=20&w=8&page=%d'%x2,network_try_count=100)         
          #for x3 in range(32):#18
	       #yield Task ('post',url='https://kinozal-tv.appspot.com/browse.php?c=20&w=9&page=%d'%x3,network_try_count=100)                 
          #for x4 in range(18):#18
	       #yield Task ('post',url='https://kinozal-tv.appspot.com/browse.php?c=20&w=10&page=%d'%x4,network_try_count=100)
         
                 
        
        
            
            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//td[@class="nam"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('item', url=ur,refresh_cache=True,network_try_count=100)
	 
        
        
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h1').text()
	  except DataNotFound:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//b[contains(text(),"Оригинальное название:")]/following-sibling::text()[1]').text()
	     #print ray 
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//b[contains(text(),"Год выпуска:")]/following-sibling::text()[1]').text()
	  except IndexError:
	       punkt = ''
	       
	  try:
	       #if  grab.doc.select(u'//a[@class="hp_title1"]/a[contains(text()," район")]').exists()==True:
	       ter= grab.doc.select(u'//b[contains(text(),"Жанр:")]/following-sibling::text()[1]').text()#.split(', ')[3].replace(u'улица','')
	       #else:
		    #ter= ''#grab.doc.select(u'//h1[@class="object_descr_addr"]').text().split(', ')[2]
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//b[contains(text(),"Выпущено:")]/following-sibling::text()[1]').text()
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       r=[]
               for m in grab.doc.select(u'//b[contains(text(),"В ролях:")]/following-sibling::a'):
                    r.append(m.text())
               dom = ','.join(r)
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//b[contains(text(),"О фильме:")]/following-sibling::text()[1]').text()
		#print rayon
	  except IndexError:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//img[@class="p200"]').attr('src')
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = grab.doc.select(u'//b[contains(text(),"Размер:")]/following-sibling::text()[1]').text()
	  except IndexError:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//b[contains(text(),"Аудио:")]/following-sibling::text()[1]').text()
	  except IndexError:
	       plosh = ''
	  #try:
	       #vid = grab.doc.select(u'//span[contains(text(),"Стоимость 1 м²:")]/following-sibling::span[@class="hp_price"]').text()
	  #except DataNotFound:
	       #vid = '' 
	  #try:
	       #et = grab.doc.select(u'//span[contains(text(),"Этаж:")]/following-sibling::text()[1]').text()
	  #except IndexError:
	       #et = ''
	  #try:
	       #et2 = grab.doc.select(u'//span[contains(text(),"Количество этажей:")]/following-sibling::text()[1]').text()
	  #except IndexError:
	       #et2 = ''
	  
	  #try:
	       #mat = grab.doc.select(u'//span[contains(text(),"Тип здания:")]/following-sibling::text()[1]').text()
	  #except IndexError:
	       #mat = ''
          #try:
               #godp = grab.doc.select(u'//span[contains(text(),"Состояние:")]/following-sibling::text()[1]').text()
          #except IndexError:
               #godp = ''	       
	       
	       
	  #try:
	       #ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
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
	  #except IndexError:
	       #teplo =''
	       
	  #try:
	       #oper = grab.doc.select(u'//span[@class="pathway"]/a[5]').text().replace(u'Сдам',u'Аренда').replace(u'Продам',u'Продажа')  
	  #except IndexError:
	       #oper = ''               
	      
		    
	  #try:
	       #opis = grab.doc.select(u'//span[contains(text(),"Полное описание:")]/following-sibling::text()').text() 
	  #except IndexError:
	       #opis = ''
	       
	  #try:
	       #try:
	            #phone = re.sub('[^\d]', u'',grab.doc.select(u'//span[contains(text(),"Моб. телефон:")]/following-sibling::text()[1]').text())
	       #except IndexError:
		    #phone = re.sub('[^\d\,]', u'',grab.doc.select(u'//span[contains(text(),"Телефон:")]/following-sibling::text()[1]').text())
	  #except IndexError:
	       #phone = ''
	       
	  #try:
	       #lico = grab.doc.select(u'//a[@class="hp_caption_agentname"]').text()
	       
	  #except IndexError:
	       #lico = ''
	       
	  #try:
	       #comp = grab.doc.select(u'//span[contains(text(),"Организация:")]/following-sibling::text()[1]').text()
	  #except IndexError:
	       #comp = ''
	       
	  #try:
	       #data= grab.doc.select(u'//span[contains(text(),"Создано/Изменено:")]/following-sibling::text()[1]').text().replace('-','.').split(' ')[0]
	  #except IndexError:
	       #data = ''
		    
	  
						   
	       
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
	              #'et': et,
	              #'ets': et2,
	              #'mat': mat,
	              #'god':godp,
                      #'vid': vid,
                      #'ohrana':ohrana,
                      #'gaz': gaz,
                      #'voda': voda,
                      #'kanaliz': kanal,
                      #'electr': elek,
                      #'teplo': teplo,
                      #'opis':opis,
                      #'phone':phone,
                      #'lico':lico,
                      #'company':comp,
                      #'data':data,
                      #'oper':oper
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
	  #print  task.project['et']
	  #print  task.project['ets']
	  #print  task.project['mat']
	  #print  task.project['god']
	  #print  task.project['vid']
	  #print  task.project['ohrana']
	  #print  task.project['gaz']
	  #print  task.project['voda']
	  #print  task.project['kanaliz']
	  #print  task.project['electr']
	  #print  task.project['teplo']
	  #print  task.project['opis']
	  #print task.project['url']
	  #print  task.project['phone']
	  #print  task.project['lico']
	  #print  task.project['company']
	  #print  task.project['data']
	  #print  task.project['oper']
	  
	  #global result
	  self.ws.write(self.result, 0, task.project['sub'])
	  self.ws.write(self.result, 1, task.project['rayon'])
	  self.ws.write(self.result, 2, task.project['punkt'])
	  self.ws.write(self.result, 3, task.project['teritor'])
	  self.ws.write(self.result, 4, task.project['ulica'])
	  self.ws.write(self.result, 5, task.project['dom'])
	  self.ws.write(self.result, 6, task.project['trassa'])
	  self.ws.write_string(self.result, 7, task.project['udal'])
	  #self.ws.write(self.result, 33, task.project['oper'])
	  self.ws.write(self.result, 8, task.project['cena'])
	  #self.ws.write(self.result, 9, task.project['plosh'])
	  #self.ws.write(self.result, 13, task.project['et'])
	  #self.ws.write(self.result, 14, task.project['ets'])
	  #self.ws.write(self.result, 18, task.project['god'])
	  #self.ws.write(self.result, 16, task.project['mat'])	  
	  #self.ws.write(self.result, 34, task.project['vid'])
	  #self.ws.write(self.result, 20, task.project['gaz'])
	  #self.ws.write(self.result, 21, task.project['voda'])
	  #self.ws.write(self.result, 22, task.project['kanaliz'])
	  #self.ws.write(self.result, 23, task.project['electr'])
	  #self.ws.write(self.result, 24, task.project['teplo'])
	  #self.ws.write(self.result, 19, task.project['ohrana'])	       
	  #self.ws.write(self.result, 25, task.project['opis'])
	  #self.ws.write(self.result, 26, u'Home29.ru')
	  #self.ws.write_string(self.result, 2, task.project['url'])
	  #self.ws.write(self.result, 28, task.project['phone'])
	  #self.ws.write(self.result, 29, task.project['lico'])
	  #self.ws.write(self.result, 30, task.project['company'])
	  #self.ws.write(self.result, 31, task.project['data'])
	  #self.ws.write(self.result, 32, datetime.today().strftime('%d.%m.%Y'))
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

     
bot = Cian_Zem(thread_number=5,network_try_limit=1000)
bot.load_proxylist('/home/oleg/Proxy/tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







