#!/usr/bin/python
# -*- coding: utf-8 -*-



import logging
import time
from selenium import webdriver
from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import xlsxwriter
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


proxy = random.choice(list(open('../tipa.txt')))
print proxy

#profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/n1ddsdpx.default/') #Gui2
##profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/3missjz0.default/')#Gui1
#profile.set_preference("network.proxy.type", 1)
#profile.set_preference("network.proxy.http", proxy)
#profile.set_preference("network.proxy.http_port", port)
#profile.set_preference("network.proxy.ssl", proxy)
#profile.set_preference("network.proxy.ssl_port", port)
#profile.update_preferences()
#profile.native_events_enabled = False
#driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)


ua = dict(DesiredCapabilities.PHANTOMJS)
ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
service_args = ['--proxy='+proxy,'--proxy-type=http',]
driver = webdriver.PhantomJS(service_args=service_args)
driver.set_window_position(0,0)
driver.set_window_size(900,600)

#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
driver.get("http://lg29.ru/estates#/table/%22action%22:%22sell%22,%22section%22:3/")





time.sleep(5)



#driver.find_element_by_xpath(u'//div[contains(text(),"Коммерческая недвижимость")]').click()


#select=Select(driver.find_element_by_name('common:country')).select_by_visible_text(u"РОССИЯ")
lin = []

time.sleep(5)

v = 1

while True:
    for link in driver.find_elements_by_xpath(u'//tr[@class="ng-scope"]/td[2]/a'):
        url = link.get_attribute('href')   
        print url
        lin.append(url)
    print '********************',len(lin),'**********************'
    try:
        driver.find_element_by_xpath(u'//li[@class="pagination-next ng-scope"]/a').click()
    except NoSuchElementException:
        break
        
    time.sleep(2)
    v=+1
    
driver.close()
print('Done!') 

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

workbook = xlsxwriter.Workbook(u'0001-0008_29_У_001-0015_LG29.xlsx')
        
class lg29_Com(Spider):
    def prepare(self):
        #self.f = page
        self.ws = workbook.add_worksheet()
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
        self.ws.write(0, 29, u"ДАТА_ПАРСИНГА")
        self.ws.write(0, 30, u"МЕСТОПОЛОЖЕНИЕ")

        self.result= 1



    def task_generator(self):
        for line in lin:
            yield Task ('item',url=line.strip(),refresh_cache=True,network_try_count=100)

    def task_item(self, grab, task):
        try:
            sub = u'Архангельская область'
        except DataNotFound:
            sub = ''
        try:
            ray = grab.doc.select(u'//span[@id="address"]').text()
            #print ray 
        except DataNotFound:
            ray = ''          
        try:
            #if  grab.doc.select(u'//em/a[2][contains(text(),"р-н")]').exists()==True:
            punkt= grab.doc.select(u'//span[@id="address"]').text().split(', ')[0]
        except IndexError:
            punkt = ''

        try:
            ter=  re.split(r'(\W+)',grab.doc.select(u'//span[@id="address"]').text().split(', ')[1])[1]
        except IndexError:
            ter =''

        #try:
            ##if grab.doc.select(u'').exists()==False:
            #uliza = grab.doc.select(u'//span[@id="address"]').text().split(', ')[1].split(' ')[0]
            ##else:
                ##uliza = ''
        #except IndexError:
        uliza = ''
        try:
            dom =  re.split(r'\W+',grab.doc.select(u'//span[@id="address"]').text().split(', ')[1],1)[1]
        except IndexError:
            dom = ''       
        try:
            trassa = grab.doc.select(u'//td[contains(text(),"Объект:")]/following-sibling::td').text()
                #print rayon
        except DataNotFound:
            trassa = ''       
        try:
            udal = grab.doc.select(u'//td[contains(text(),"Класс:")]/following-sibling::td').text()
        except DataNotFound:
            udal = ''

        try:
            price = grab.doc.select(u'//label[contains(text(),"Стоимость:")]/following-sibling::text()').text()+u' р.'
        except DataNotFound:
            price = ''   
        try:
            plosh = grab.doc.select(u'//div[contains(text(),"Общая площадь:")]').text().split(': ')[1]
        except DataNotFound:
            plosh = ''
        try:
            vid = ''#grab.doc.select(u'//td[contains(text(),"Тип:")]/following-sibling::td').text()
        except DataNotFound:
            vid = '' 
        try:
            et = re.sub('[^\d\/]', u'',grab.doc.select(u'//div[contains(text(),"Этаж")]').text()).split('/')[0]
        except IndexError:
            et = ''
        try:
            et2 = re.sub('[^\d\/]', u'',grab.doc.select(u'//div[contains(text(),"Этаж")]').text()).split('/')[1]
        except IndexError:
            et2 = ''

        try:
            mat = grab.doc.select(u'//div[contains(text(),"Высота потолков")]/span').text()
        except IndexError:
            mat = ''
        try:
            godp = grab.doc.select(u'//div[contains(text(),"Состояние ремонта")]/span').text()
        except IndexError:
            godp = ''	       


        try:
            ohrana =re.sub(u'^.*(?=храна)','', grab.doc.select(u'//*[contains(text(), "храна")]').text())[:5].replace(u'храна',u'есть')
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
            teplo = re.sub(u'^.*(?=топление)','', grab.doc.select(u'//*[contains(text(), "топление")]').text())[:5].replace(u'топле',u'есть')
        except IndexError:
            teplo =''

        try:
            oper = u'Продажа'#grab.doc.select(u'//div[contains(text(),"Тип сделки:")]/span').text().replace(u'Сдам',u'Аренда').replace(u'Спрос',u'Аренда').replace(u'Продам',u'Продажа')  
        except IndexError:
            oper = ''               


        try:
            opis = grab.doc.select(u'//h2[contains(text(),"Описание")]/following-sibling::div').text()#.replace(u'Описание','')  
        except IndexError:
            opis = ''

        try:
            phone = re.sub('[^\d]', u'',grab.doc.select(u'//div[@class="staff__phone"]').text())
        except IndexError:
            phone = ''

        try:
            lico = grab.doc.select(u'//div[@class="staff__info"]/h4/a').text()
        except IndexError:
            lico = ''

        try:
            comp = u'Любимый город'#grab.doc.select(u'//td[contains(text(),"Фирма продавец:")]/following-sibling::td').text().split(' :: ')[0]
        except IndexError:
            comp = ''

        try:
            data= grab.doc.select(u'//td[contains(text(),"Изменено:")]/following-sibling::td').text().split(' ')[0]
        except IndexError:
            data = ''




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
                    'et': et,
                    'ets': et2,
                    'mat': mat,
                    'god':godp,
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
                    'data':data,
                    'oper':oper
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
        print  task.project['ets']
        print  task.project['mat']
        print  task.project['god']
        print  task.project['vid']
        print  task.project['ohrana']
        print  task.project['gaz']
        print  task.project['voda']
        print  task.project['kanaliz']
        print  task.project['electr']
        print  task.project['teplo']
        print  task.project['opis']
        print task.project['url']
        print  task.project['phone']
        print  task.project['lico']
        print  task.project['company']
        print  task.project['data']
        print  task.project['oper']

        #global result
        self.ws.write(self.result, 0, task.project['sub'])
        self.ws.write(self.result, 30, task.project['rayon'])
        self.ws.write(self.result, 2, task.project['punkt'])
        self.ws.write(self.result, 3, task.project['teritor'])
        self.ws.write(self.result, 4, task.project['ulica'])
        self.ws.write(self.result, 5, task.project['dom'])
        #self.ws.write(self.result, 9, task.project['trassa'])
        #self.ws.write(self.result, 10, task.project['udal'])
        self.ws.write(self.result, 9, task.project['oper'])
        self.ws.write(self.result, 10, task.project['cena'])
        self.ws.write(self.result, 12, task.project['plosh'])
        #self.ws.write(self.result, 13, task.project['et'])
        #self.ws.write(self.result, 14, task.project['ets'])
        self.ws.write(self.result, 18, task.project['god'])
        self.ws.write(self.result, 17, task.project['mat'])	  
        self.ws.write(self.result, 8, task.project['vid'])
        #self.ws.write(self.result, 20, task.project['gaz'])
        #self.ws.write(self.result, 21, task.project['voda'])
        self.ws.write(self.result, 22, task.project['kanaliz'])
        self.ws.write(self.result, 23, task.project['electr'])
        #self.ws.write(self.result, 24, task.project['teplo'])
        self.ws.write(self.result, 19, task.project['ohrana'])	       
        self.ws.write(self.result, 22, task.project['opis'])
        self.ws.write(self.result, 23, u'АН "Любимый Город"')
        self.ws.write_string(self.result, 24, task.project['url'])
        self.ws.write(self.result, 25, task.project['phone'])
        self.ws.write(self.result, 26, task.project['lico'])
        self.ws.write(self.result, 27, task.project['company'])
        self.ws.write(self.result, 28, task.project['data'])
        self.ws.write(self.result, 29, datetime.today().strftime('%d.%m.%Y'))
        print('*'*50)
        #print task.sub

        print 'Ready - '+str(self.result)#+'/'+task.project['koll']
        logger.debug('Tasks - %s' % self.task_queue.size())
        #print '*',i+1,'/',dc,'*'
        #print oper
        print('*'*50)	       
        self.result+= 1

        #if self.result >= 30:
            #self.stop()	       	       



bot = lg29_Com(thread_number=3,network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5, connect_timeout=5)
bot.run()
workbook.close()
print('Done!') 

    
    
    
    
    
    
    
    
   