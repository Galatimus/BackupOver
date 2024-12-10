#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import math
import re
import os
import time
from datetime import datetime,timedelta
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)



workbook = xlsxwriter.Workbook(u'0001-0062_00_Б_005-0002_CIAN.xlsx')



class Cian_Com(Spider):
    def prepare(self):
        self.ws = workbook.add_worksheet(u'Cian')
        self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
        self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
        self.ws.write(0, 2, u"НАСЕЛЕННЫЙ_ПУНКТ")
        self.ws.write(0, 3, u"УЛИЦА")
        self.ws.write(0, 4, u"ДОМ")
        self.ws.write(0, 5, u"МЕТРО")
        self.ws.write(0, 6, u"СФЕРА БИЗНЕСА")
        self.ws.write(0, 7, u"СЕГМЕНТ_ГОТОВОГО_БИЗНЕСА")
        self.ws.write(0, 8, u"ОПЕРАЦИЯ")
        self.ws.write(0, 9, u"ЦЕНА_ПРОДАЖИ")
        self.ws.write(0, 10, u"ОПИСАНИЕ")
        self.ws.write(0, 11, u"ИСТОЧНИК_ИНФОРМАЦИИ")
        self.ws.write(0, 12, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
        self.ws.write(0, 13, u"КОНТАКТЫ")
        self.ws.write(0, 14, u"ДАТА_РАЗМЕЩЕНИЯ")
        self.ws.write(0, 15, u"ДАТА_ПАРСИНГА")
        self.ws.write(0, 16, u"АДРЕС")
        self.ws.write(0, 17, u"ЗАГОЛОВОК")    
        self.result= 1
        #self.count = 2






    def task_generator(self):
        l= open('cian_biz.txt').read().splitlines()
        self.dc = len(l)
        print self.dc
        for line in l:
            yield Task ('item',url=line,refresh_cache=True,network_try_count=100)

    def task_item(self, grab, task):
        #time.sleep(1)

        try:
            sub = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]').text().split(', ')[0]
        except IndexError:
            sub = ''	
            
        try:
            ray = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"р-н ")]').text()
        except IndexError:
            ray ='' 
            
        try:
            usl = grab.doc.select(u'//div[@class="specialty--39OLY"]').text().split(': ')[1]
        except IndexError:
            usl = ''	

        try:
            if sub == u'Москва':
                punkt= u'Москва'
            elif sub == u'Санкт-Петербург':
                punkt= u'Санкт-Петербург'
            elif sub == u'Севастополь':
                punkt= u'Севастополь'
            else:
                if  grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[2][contains(text(),"р-н ")]').exists()==True:
                    punkt= grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[3]').text()
                elif grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[3][contains(text(),"р-н ")]').exists()==True:
                    punkt= grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[2]').text()
                else:
                    punkt=grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[2]').text()
        except IndexError:
            punkt = ''

        try:
            try:
                try:
                    try:
                        try:
                            try:
                                try:
                                    try:
                                        uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"ул.")]').text()
                                    except IndexError:
                                        uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"пер.")]').text()
                                except IndexError:
                                    uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"просп.")]').text()
                            except IndexError:
                                uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"ш.")]').text()
                        except IndexError:
                            uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"бул.")]').text()
                    except IndexError:
                        uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"проезд")]').text()
                except IndexError:
                    uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"наб.")]').text()
            except IndexError:
                uliza = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(text(),"пл.")]').text()
        except IndexError:
            uliza =''

        try:
            if uliza == '':
                dom =''
            else:
                dom = grab.doc.select(u'//address[@class="a10a3f92e9--address--140Ec"]/a[contains(@href,"house")]').text()
        except IndexError:
            dom = ''

        try:
            seg = grab.doc.select(u'//a[contains(@href,"metro")]/span').text()
            #print oren
        except DataNotFound:
            seg = '' 

        try:
            naz = grab.doc.select(u'//title').text()
            #print naz
        except IndexError:
            naz = '' 

        try:
            price = grab.doc.select(u'//span[@itemprop="price"]').text()
            #print price
        except IndexError:
            price = ''

 

        try:
            opis = grab.doc.select(u'//p[@itemprop="description"]').text()
            #print opis
        except IndexError:
            opis = ''

        try:
            try:
                phone = re.sub(u'[^\d\+]','',grab.doc.select(u'//div[@class="cf_offer_show_phone-number"]/a').text())
            except IndexError:
                phone = re.sub(u'[^\d\+]','',grab.doc.rex_text(u'offerPhone(.*?),'))
        except IndexError:
            phone = '' 


        try:
            data = re.sub(u'[^\d\-]','',grab.doc.rex_text(u'editDate(.*?)T')).replace('-','.')
        except IndexError:
            data = ''



        try:
            vent = grab.doc.select(u'//div[@class="a10a3f92e9--address--2T-DP"]').text()
        except IndexError:
            vent =''		

      

        try:
            if 'sale' in task.url:
                oper = u'Продажа' 
            elif 'rent' in task.url:
                oper = u'Аренда'     
        except IndexError:
            oper = ''

        projects = {'url': task.url,
                    'sub': sub,       
                    'ray': ray,
                    'punkt': punkt,                   
                    'uliza': uliza,
                    'dom': dom,
                    'seg': seg,
                    'naznachenie': naz,
                    'uslovi': usl,                   
                    'cena': price,
                    'opisanie': opis,
                    'phone':phone.replace(u'79311111111',''),                  
                    'internet':vent,
                    'data':data,
                    'oper':oper

                    }
        yield Task('write',project=projects,grab=grab)

    def task_write(self,grab,task):
        if task.project['sub'] <> '':    
            print('*'*50)
            print  task.project['sub']
            print  task.project['ray']
            print  task.project['punkt']            
            print  task.project['uliza']
            print  task.project['dom']
            print  task.project['seg']
            print  task.project['naznachenie']
            print  task.project['uslovi'] 
            print  task.project['cena']         
            print  task.project['opisanie']
            print  task.project['url']
            print  task.project['phone']           
            print  task.project['data']




            self.ws.write(self.result, 0, task.project['sub'])
            self.ws.write(self.result, 1, task.project['ray'])
            self.ws.write(self.result, 2, task.project['punkt'])            
            self.ws.write(self.result, 3, task.project['uliza'])
            self.ws.write(self.result, 4, task.project['dom'])
            self.ws.write(self.result, 16, task.project['internet'])
            self.ws.write(self.result, 5, task.project['seg'])          
            self.ws.write(self.result, 17, task.project['naznachenie'])
            self.ws.write(self.result, 9, task.project['cena'])         
            self.ws.write(self.result, 6, task.project['uslovi'])            
            self.ws.write_string(self.result, 12, task.project['url'])
            self.ws.write(self.result, 13, task.project['phone'])          
            self.ws.write(self.result, 14, task.project['data'])
            self.ws.write(self.result, 10, task.project['opisanie'])
            self.ws.write(self.result, 11, u'ЦИАН')
            self.ws.write(self.result, 15, datetime.today().strftime('%d.%m.%Y'))
            self.ws.write(self.result, 8, task.project['oper'])


            print('*'*50)
            print 'Ready - '+str(self.result)+'/'+str(self.dc)
            print 'Tasks - %s' % self.task_queue.size()
            print  task.project['oper']
            print('*'*50)

            self.result+= 1



            #if self.result > 10:
                #self.stop()	



bot = Cian_Com(thread_number=5,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=50, connect_timeout=50)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')
command = 'mount -a'
os.system('echo %s|sudo -S %s' % ('1122', command))
time.sleep(3)
workbook.close()
print('Done')


