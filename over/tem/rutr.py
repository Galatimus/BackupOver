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


workbook = xlsxwriter.Workbook(u'tem/Rutracker_Видео,DVD Video,HD Video(Джаз и блюз).xlsx')

    

class Cian_Zem(Spider):
     def prepare(self):
	  #self.f = page
	  self.ws = workbook.add_worksheet()
	  self.ws.write(0, 0, u"Исполнитель")
	  self.ws.write(0, 1, u"Название концерта")
	  self.ws.write(0, 2, u"Жанр")
	  self.ws.write(0, 3, u"Год выпуска")
	  self.ws.write(0, 4, u"Описание")
	  self.ws.write(0, 5, u"Качество")
	  self.ws.write(0, 6, u"Формат")
	  self.ws.write(0, 7, u"Страна")
	  self.ws.write(0, 8, u"Картинка(Url)")
	  self.ws.write(0, 9, u"Размер раздачи")
	  self.ws.write(0, 10, u"Аудио")
	  self.ws.write(0, 11, u"Видео")

	  self.result= 1
	
	       
    
     def task_generator(self):
	  yield Task ('post',url= 'https://rutracker.org/forum/viewforum.php?f=2271',refresh_cache=True,network_try_count=100)
	  
            
     def task_post(self,grab,task):
	  for elem in grab.doc.select(u'//h4[@class="forumlink"]/a'):
	       ur = grab.make_url_absolute(elem.attr('href'))  
	       #print ur
	       yield Task('next', url=ur,refresh_cache=True,network_try_count=100)
	 
     def task_next(self,grab,task):
	  for el in grab.doc.select(u'//span[@class="topictitle"]/img/following-sibling::a'):
	       urr = grab.make_url_absolute(el.attr('href'))  
	       #print urr
	       yield Task('item', url=urr,refresh_cache=True,network_try_count=100)
	  for el1 in grab.doc.select(u'//div[@class="torTopic"]/span/following-sibling::a'):
	       urr1 = grab.make_url_absolute(el1.attr('href'))  
	       #print urr1
	       yield Task('item', url=urr1,refresh_cache=True,network_try_count=100)
          yield Task("page", grab=grab,refresh_cache=True,network_try_count=100)
	       
     def task_page(self,grab,task):
	  try:
	       pg = grab.doc.select(u'//a[@class="pg"][contains(text(),"След.")]')
	       u = grab.make_url_absolute(pg.attr('href'))
	       yield Task ('next',url= u,refresh_cache=True,network_try_count=100)
	  except DataNotFound:
	       print('*'*100)
	       print '!!'
	       print('*'*100)
	            
        
     def task_item(self, grab, task):
	  try:
	       sub = grab.doc.select(u'//h1/a').text().split(' - ')[0]
	  except IndexError:
	       sub = ''
	  try:
	       ray = grab.doc.select(u'//span[contains(text(),"Жанр")]/following-sibling::text()[1]').text().replace(': ','')
	     #print ray 
	  except IndexError:
	       ray = ''          
	  try:
	       punkt= grab.doc.select(u'//span[contains(text(),"Год выпуска")]/following-sibling::text()[1]').text().replace(': ','')
	  except IndexError:
	       punkt = ''
	       
	  try:
	       lin = []
               for eem in grab.doc.select(u'//span[@class="post-br"][2]/following-sibling::text()'):
                    op = eem.text()
                    #print urr
                    lin.append(op)
               ter = "".join(lin)
	  except IndexError:
	       ter =''
	       
	  try:
	       #if grab.doc.select(u'').exists()==False:
	       uliza = grab.doc.select(u'//span[contains(text(),"Качество")]/following-sibling::text()[1]').text().replace(': ','')
	       #else:
		    #uliza = ''
	  except IndexError:
	       uliza = ''
	  try:
	       dom = grab.doc.select(u'//span[contains(text(),"Формат")]/following-sibling::text()[1]').text().replace(': ','')
	  except IndexError:
	       dom = ''       
	  try:
	       trassa = grab.doc.select(u'//span[contains(text(),"Страна")]/following-sibling::text()[1]').text().replace(': ','')
		#print rayon
	  except IndexError:
	       trassa = ''       
	  try:
	       udal = grab.doc.select(u'//span[@class="post-br"]/following-sibling::var').attr('title')
	  except IndexError:
	       udal = ''
	       
	  try:
	       price = re.sub(u'[^\d\.\A-Z]','',grab.doc.select(u'//div[@class="attach_link guest"]').text())
	  except IndexError:
	       price = ''   
	  try:
	       plosh = grab.doc.select(u'//span[contains(text(),"Аудио")]/following-sibling::text()[1]').text().replace(': ','')
	  except IndexError:
	       plosh = ''
	  try:
	       vid = grab.doc.select(u'//span[contains(text(),"Видео")]/following-sibling::text()[1]').text().replace(': ','')
	  except DataNotFound:
	       vid = '' 
	  try:
	       et = grab.doc.select(u'//h1/a').text().split(' - ')[1]
	  except IndexError:
	       et = ''
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
                      'teritor': ter.replace(': ',''),
                      'ulica': uliza,
	              'dom': dom,
                      'trassa': trassa,
                      'udal': udal,
                      'cena': price,
                      'plosh':plosh,
	              'et': et,
	              #'ets': et2,
	              #'mat': mat,
	              #'god':godp,
                      'vid': vid,
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
	  print  task.project['et']
	  #print  task.project['ets']
	  #print  task.project['mat']
	  #print  task.project['god']
	  print  task.project['vid']
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
	  self.ws.write(self.result, 1, task.project['et'])
	  self.ws.write(self.result, 2, task.project['rayon'])
	  self.ws.write(self.result, 3, task.project['punkt'])
	  self.ws.write(self.result, 4, task.project['teritor'])
	  self.ws.write(self.result, 5, task.project['ulica'])
	  self.ws.write(self.result, 6, task.project['dom'])
	  self.ws.write(self.result, 7, task.project['trassa'])
	  self.ws.write_string(self.result, 8, task.project['udal'])
	  self.ws.write(self.result, 11, task.project['vid'])
	  self.ws.write(self.result, 9, task.project['cena'])
	  self.ws.write(self.result, 10, task.project['plosh'])
	  
	
	  print('*'*50)
	  #print task.sub
	  
	  print 'Ready - '+str(self.result)#+'/'+task.project['koll']
	  logger.debug('Tasks - %s' % self.task_queue.size())
	  #print '*',i+1,'/',dc,'*'
	  #print oper
	  print('*'*50)	       
	  self.result+= 1
	       
	  #if self.result > 100:
	       #self.stop()	 

     
bot = Cian_Zem(thread_number=2,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
workbook.close()
print('Done!') 







