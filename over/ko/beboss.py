#!/usr/bin/env python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
from datetime import datetime
import logging
from grab import Grab
import time
import xlsxwriter
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

i = 0

l= ['http://www.beboss.ru/kn/ru/office/rent',
    'http://www.beboss.ru/kn/ru/retail/rent',
    'http://www.beboss.ru/kn/ru/stock/rent',
    'http://www.beboss.ru/kn/ru/spec/rent',
    'http://www.beboss.ru/kn/ru/industry/rent',
    'http://www.beboss.ru/kn/ru/land/rent',
    'http://www.beboss.ru/kn/ru/office/sell',
    'http://www.beboss.ru/kn/ru/retail/sell',
    'http://www.beboss.ru/kn/ru/stock/sell',
    'http://www.beboss.ru/kn/ru/spec/sell',
    'http://www.beboss.ru/kn/ru/industry/sell',
    'http://www.beboss.ru/kn/ru/land/sell']

page = l[i]


while True:
     print '********************************************',i+1,'/',len(l),'*******************************************'

     class Beboss(Spider): 
	  def prepare(self):
	       self.f = page
	       while True:
		    try:
			 time.sleep(1)
			 g = Grab(timeout=20, connect_timeout=20)
			 g.proxylist.load_file(path='../../tipa.txt',proxy_type='http')
			 g.go(self.f)
			 self.num = re.sub('[^\d]','',g.doc.select(u'//span[@class="js-count-obj"]').text())
			 self.pag = int(math.ceil(float(int(self.num))/float(20)))
			 print self.pag,self.num
			 del g
			 break
		    except(GrabTimeoutError,GrabNetworkError,DataNotFound,GrabConnectionError):
			 print g.config['proxy'],'Change proxy'
			 g.change_proxy()
			 del g
			 continue
	       self.workbook = xlsxwriter.Workbook(u'beboss/Beboss_Объекты_'+str(i+1)+'.xlsx')
	       self.workbook1 = xlsxwriter.Workbook(u'beboss/Beboss_Предложения_'+str(i+1)+'.xlsx')
	       self.ws = self.workbook.add_worksheet(u'Объекты')
	       self.ws1 = self.workbook1.add_worksheet(u'Предложения')
	       self.ws.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН)")
	       self.ws.write(0, 2, u"ПОСЕЛЕНИЕ")
	       self.ws.write(0, 3, u"ОРИЕНТИР")
	       self.ws.write(0, 4, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws.write(0, 5, u"ВНУТРИГОРОДСКАЯ_ТЕРРИТОРИЯ")
	       self.ws.write(0, 6, u"АДРЕС")
	       self.ws.write(0, 7, u"СТАНЦИЯ_МЕТРО")
	       self.ws.write(0, 8, u"ДО_МЕТРО_МИНУТ")
	       self.ws.write(0, 9, u"ПЕШКОМ_ТРАНСПОРТОМ")
	       self.ws.write(0, 10, u"МАСШТАБ")
	       self.ws.write(0, 11, u"ТИП ПОСТРОЙКИ")
	       self.ws.write(0, 12, u"НАИМЕНОВАНИЕ ОБЪЕКТА")
	       self.ws.write(0, 13, u"КЛАСС ОБЪЕКТА")
	       self.ws.write(0, 14, u"ОБЩАЯ ПЛОЩАДЬ ОБЪЕКТА")
	       self.ws.write(0, 15, u"КОЛИЧЕСТВО ЭТАЖЕЙ")
	       self.ws.write(0, 16, u"НДС")
	       self.ws.write(0, 17, u"КУ")
	       self.ws.write(0, 18, u"ЭКСПЛУАТАЦИОННЫЕ РАСХОДЫ")
	       self.ws.write(0, 19, u"ГОД ПОСТРОЙКИ")
	       self.ws.write(0, 20, u"ПАРКОВКА")
	       self.ws.write(0, 21, u"ОХРАНА")
	       self.ws.write(0, 22, u"ЯКОРНЫЕ АРЕНДАТОРЫ")
	       self.ws.write(0, 23, u"ДЕВЕЛОПЕР")
	       self.ws.write(0, 24, u"ОПИСАНИЕ")
	       self.ws.write(0, 25, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 26, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws.write(0, 27, u"КОНТАКТЫ")
	       self.ws.write(0, 28, u"ДАТА_РАЗМЕЩЕНИЯ")
	       self.ws.write(0, 29, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws.write(0, 30, u"ДАТА_ПАРСИНГА")
	       #****************************************
	       self.ws1.write(0, 0, u"СУБЪЕКТ_РОССИЙСКОЙ_ФЕДЕРАЦИИ")
	       self.ws1.write(0, 1, u"МУНИЦИПАЛЬНОЕ_ОБРАЗОВАНИЕ_(РАЙОН")
	       self.ws1.write(0, 2, u"ОРИЕНТИР")
	       self.ws1.write(0, 3, u"НАСЕЛЕННЫЙ_ПУНКТ")
	       self.ws1.write(0, 4, u"НАИМЕНОВАНИЕ ОБЪЕКТА")
	       self.ws1.write(0, 5, u"ОПЕРАЦИЯ")
	       self.ws1.write(0, 6, u"НАЗНАЧЕНИЕ ОБЪЕКТА")
	       self.ws1.write(0, 7, u"ЭТАЖ")
	       self.ws1.write(0, 8, u"ПЛОЩАДЬ ПОМЕЩЕНИЯ")
	       self.ws1.write(0, 9, u"ЦЕНА ПРОДАЖИ")
	       self.ws1.write(0, 10, u"АРЕНДНАЯ СТАВКА")
	       self.ws1.write(0, 11, u"ЦЕНА КВ.М.")
	       self.ws1.write(0, 12, u"ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws1.write(0, 13, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
	       self.ws1.write(0, 14, u"ДАТА_РАЗМЕЩЕНИЯ")            
	       self.ws1.write(0, 15, u"ДАТА_ОБНОВЛЕНИЯ")
	       self.ws1.write(0, 16, u"ДАТА_ПАРСИНГА")
	       self.result= 1
	       self.result1= 1
	  def task_generator(self):
	       for x in range(1,self.pag+1):
                    yield Task ('post',url=self.f+'?page=%d'%x,refresh_cache=True,network_try_count=100)
		    
	  def task_post(self,grab,task):
	       for elem in grab.doc.select(u'//a[contains(text(),"Подробнее")]'):
		    ur = grab.make_url_absolute(elem.attr('href'))
		    #print ur
		    yield Task('item',url=ur,refresh_cache=True,network_try_count=100)
		    
	  def task_item(self, grab, task): 
	       try:
		    conv = [(u'Александров',u'Владимирская область'),
			    (u'Анапа',u'Краснодарский край'),
			    (u'Арзамас',u'Нижегородская область'),
			    (u'Архангельск',u'Архангельская область'),
			    (u'Астрахань',u'Астраханская область'),
			    (u'Балаково',u'Саратовская область'),
			    (u'Барнаул',u'Алтайский край'),
			    (u'Белгород',u'Белгородская область'),
			    (u'Благовещенск',u'Амурская область'),
			    (u'Братск',u'Иркутская область'),
			    (u'Брянск',u'Брянская область'),
			    (u'Великий Новгород',u'Новгородская область'),
			    (u'Владивосток',u'Приморский край'),
			    (u'Владикавказ',u'Республика Северная Осетия-Алания'),
			    (u'Владимир',u'Владимирская область'),
			    (u'Волгоград',u'Волгоградская область'),
			    (u'Волжский',u'Волгоградская область'),
			    (u'Вологда',u'Вологодская область'),
			    (u'Воронеж',u'Воронежская область'),
			    (u'Грозный',u'Чеченская Республика'),
			    (u'Домодедово',u'Московская область'),
			    (u'Екатеринбург',u'Свердловская область'),
			    (u'Ессентуки',u'Ставропольский край'),
			    (u'Зеленоград',u'Москва'),
			    (u'Златоуст',u'Челябинская область'),
			    (u'Иваново',u'Ивановская область'),
			    (u'Ижевск',u'Удмуртская республика'),
			    (u'Иркутск',u'Иркутская область'),
			    (u'Йошкар-Ола',u'Республика Марий Эл'),
			    (u'Казань',u'Республика Татарстан'),
			    (u'Калининград',u'Калининградская область'),
			    (u'Калуга',u'Калужская область'),
			    (u'Кемерово',u'Кемеровская область'),
			    (u'Киров',u'Кировская область'),
			    (u'Коломна',u'Московская область'),
			    (u'Комсомольск-на-Амуре',u'Хабаровский край'),
			    (u'Кострома',u'Костромская область'),
			    (u'Котлас',u'Архангельская область'),
			    (u'Краснодар',u'Краснодарский край'),
			    (u'Красноярск',u'Красноярский край'),
			    (u'Кузнецк',u'Пензенская область'),
			    (u'Курган',u'Курганская область'),
			    (u'Курск',u'Курская область'),
			    (u'Липецк',u'Липецкая область'),
			    (u'Магнитогорск',u'Челябинская область'),
			    (u'Махачкала',u'Республика Дагестан'),
			    (u'Минеральные воды',u'Ставропольский край'),
			    (u'Мурманск',u'Мурманская область'),
			    (u'Муром',u'Владимирская область'),
			    (u'Набережные Челны',u'Республика Татарстан'),
			    (u'Находка',u'Приморский край'),
			    (u'Нефтеюганск',u'Ханты-Мансийский автономный округ—Югра'),
			    (u'Нижневартовск',u'Ханты-Мансийский автономный округ—Югра'),
			    (u'Нижнекамск',u'Республика Татарстан'),
			    (u'Нижний Новгород',u'Нижегородская область'),
			    (u'Нижний Тагил',u'Свердловская область'),
			    (u'Новокузнецк',u'Кемеровская область'),
			    (u'Новороссийск',u'Краснодарский край'),
			    (u'Новосибирск',u'Новосибирская область'),
			    (u'Обнинск',u'Калужская область'),
			    (u'Омск',u'Омская область'),
			    (u'Орел',u'Орловская область'),
			    (u'Оренбург',u'Оренбургская область'),
			    (u'Орск',u'Оренбургская область'),
			    (u'Пенза',u'Пензенская область'),
			    (u'Пермь',u'Пермский край'),
			    (u'Петрозаводск',u'Республика Карелия'),
			    (u'Подольск',u'Московская область'),
			    (u'Прокопьевск',u'Кемеровская область'),
			    (u'Псков',u'Псковская область'),
			    (u'Пятигорск',u'Ставропольский край'),
			    (u'Ростов-на-Дону',u'Ростовская область'),
			    (u'Рязань',u'Рязанская область'),
			    (u'Салават',u'Республика Башкортостан'),
			    (u'Самара',u'Самарская область'),
			    (u'Саранск',u'Республика Мордовия'),
			    (u'Саратов',u'Саратовская область'),
			    (u'Саров',u'Нижегородская область'),
			    (u'Северск',u'Томская область'),
			    (u'Симферополь',u'Крым'),
			    (u'Смоленск',u'Смоленская область'),
			    (u'Сочи',u'Краснодарский край'),
			    (u'Ставрополь',u'Ставропольский край'),
			    (u'Старый Оскол',u'Белгородская область'),
			    (u'Стерлитамак',u'Республика Башкортостан'),
			    (u'Сургут',u'Ханты-Мансийский автономный округ—Югра'),
			    (u'Сызрань',u'Самарская область'),
			    (u'Сыктывкар',u'Республика Коми'),
			    (u'Таганрог',u'Ростовская область'),
			    (u'Тамбов',u'Тамбовская область'),
			    (u'Тверь',u'Тверская область'),
			    (u'Тобольск',u'Тюменская область'),
			    (u'Тольятти',u'Самарская область'),
			    (u'Томск',u'Томская область'),
			    (u'Туапсе',u'Краснодарский край'),
			    (u'Тула',u'Тульская область'),
			    (u'Тюмень',u'Тюменская область'),
			    (u'Улан-Удэ',u'Республика Бурятия'),
			    (u'Ульяновск',u'Ульяновская область'),
			    (u'Уфа',u'Республика Башкортастан'),
			    (u'Ухта',u'Республика Коми'),
			    (u'Феодосия',u'Крым'),
			    (u'Богородск',u'Нижегородская область'),
			    (u'Хабаровск',u'Хабаровский край'),
			    (u'Чебоксары',u'Чувашская Республика'),
			    (u'Челябинск',u'Челябинская область'),
			    (u'Череповец',u'Вологодская область'),
			    (u'Черкесск',u'Карачаево-Черкесская Республика'),
			    (u'Чита',u'Забайкальскй край'),
			    (u'Ярославль',u'Ярославская область'),
			    (u'Энгельс',u'Саратовская область'),
			    (u'Югорск',u'Ханты-Мансийский автономный округ—Югра'),
			    (u'Южно-Сахалинск',u'Свердловская область'),
			    (u'Ялта',u'Крым')] 
		    t= grab.doc.select(u'//p[@class="object-addresses"]').text()
		    i=0
		    for w in t.split(','):
			 i+=1
			 if w.find(u'Россия')>=0:
			      dt = t.split(', ')[i-2]
			      #break
			 elif w.find(u'область')>=0:
			      dt = t.split(', ')[i-1]
			      #break
			 else:
			      dt =''
		    #if w.find(u'Россия')<0:
			 #dt = ''
		    sub = reduce(lambda dt, r: dt.replace(r[0], r[1]), conv, dt)
	       except IndexError: 
		    sub=''
	       try:
		    ray =  grab.doc.select(u'//dt[contains(text(),"Район")]/following-sibling::dd[1]').text() 
	       except IndexError:
		    ray = ''
	       try:
		    pun = grab.doc.select(u'//p[@class="object-addresses"]').text()
		    p=0
		    for w in pun.split(','):
			 p+=1
			 if w.find(u'Россия')>=0:
			      punkt = pun.split(', ')[p-2]
			      #break
			 elif w.find(u'область')>=0:
			      punkt = pun.split(', ')[p-2]
			      #break
			 else:
			      punkt=''
		    #if w.find(u'Россия')<0:
			 #punkt = ''
	       except IndexError:
		    punkt = ''
	       try:
		    ter =  grab.doc.select(u'//dt[contains(text(),"Административный округ")]/following-sibling::dd[1]').text() 
	       except IndexError:
		    ter = ''		    
	       try:
		    adress = grab.doc.select(u'//p[@class="object-addresses"]').text()
	       except IndexError:
		    adress = ''
	       try:
		    t = grab.doc.select(u'//title').text()
		    if t.find(',')>=0:
			 tip = t.split(', ')[0].replace(u'Аренда ','').replace(u'Продажа ','')
		    else:
			 tip = t.split(' ')[0]
	       except IndexError:
		    tip = ''
	       try:
		    metro = grab.doc.select(u'//p[@class="object-addresses"][2]').text().split('(')[0]
	       except IndexError:
		    metro = ''
	       try:
		    metro_min = re.sub('[^\d]','',grab.doc.select(u'//p[@class="object-addresses"][2]').text().split('(')[1])
	       except IndexError:
		    metro_min = ''
	       try:
		    if grab.doc.select(u'//h1[@class="franchise-header__h1"]').text().find(u',')==-1:
			 name = grab.doc.select(u'//h1[@class="franchise-header__h1"]').text()
		    else:
			 name =''
	       except IndexError:
		    name = ''
	       try:
		    klass = grab.doc.select(u'//dt[contains(text(),"Класс здания")]/following-sibling::dd[1]').text()
	       except IndexError:
		    klass = ''
	       try:
		    plosh_ob = grab.doc.select(u'//div[@class="b-franchise-layout__left-content"]/p[contains(text(),"лощадь:")]').text().split(': ')[1]
	       except IndexError:
		    plosh_ob = ''
	       try:
		    et = grab.doc.select(u'//dt[contains(text(),"Этажность объекта")]/following-sibling::dd[1]').text()
	       except IndexError:
		    et = ''
	       try:
		    if grab.doc.select(u'//dt[contains(text(),"В стоимость аренды входит")]/following-sibling::dd[1]').text().find(u'НДС')>=0:
			 nds = u'есть'
		    else:
			 nds =''
	       except IndexError:
		    nds = ''
	       try:
		    if grab.doc.select(u'//dt[contains(text(),"В стоимость аренды входит")]/following-sibling::dd[1]').text().find(u'коммунальные платежи')>=0:
			 ku = u'есть'
		    else:
			 ku=''
	       except IndexError:
		    ku = ''
	       try:
		    if grab.doc.select(u'//dt[contains(text(),"В стоимость аренды входит")]/following-sibling::dd[1]').text().find(u'эксплуатационные расходы')>=0:
			 rashodi =u'есть'
		    else:
			 rashodi=''
	       except IndexError:
		    rashodi = ''
	       try:
		    god = grab.doc.select(u'//dt[contains(text(),"Введено в эксплуатацию в")]/following-sibling::dd[1]').number()
	       except IndexError:
		    god = ''
	       try:
		    park = grab.doc.select(u'//div[@class="l w2 grey"][contains(text(),"Парковка:")]/following-sibling::div').text()
	       except IndexError:
		    park = ''
	       try:
		    ohrana = grab.doc.select(u'//dt[contains(text(),"Безопасность")]/following-sibling::dd[1]').text()
	       except IndexError:
		    ohrana = ''
	       try:
		    yakor = grab.doc.select(u'//h4[contains(text(),"Арендаторы")]/following-sibling::p[1]').text()
	       except IndexError:
		    yakor = ''
	       try:
		    opis = grab.doc.select(u'//h4[contains(text(),"Описание объекта")]/following-sibling::p[1]').text() 
	       except IndexError:
		    opis = ''
	       try:
		    lico = grab.doc.select(u'//p[@class="franchise-person__name"]').text()
	       except IndexError:
		    lico = ''
	       try:
		    data = re.sub('[^\d\.]','',grab.doc.select(u'//span[@class="kn-type-object__date"][contains(text(),"Обновлено")]').text().split(',')[0])
	       except IndexError:
		    data = ''
	       try:
		    try:
			 oper = grab.doc.select(u'//span[@class="kn-type-new"]').text()
		    except IndexError:
			 oper = grab.doc.select(u'//span[@class="kn-type-new kn-type-new_orange"]').text()
	       except IndexError:
		    oper =''
	       try:
		    try:
			 cena = grab.doc.select(u'//p[@class="kn-obj-info b-franchise-hide-mobile"]').text().split(u'Цена продажи: ')[1]
		    except IndexError:
			 cena = grab.doc.select(u'//p[@class="kn-obj-info b-franchise-hide-mobile"]').text().split(u'Цена: ')[1]
	       except IndexError:
		    cena =''
	       try:
		    cena_a = re.findall(u'Арендная ставка: (.*?)/',grab.doc.select(u'//p[@class="kn-obj-info b-franchise-hide-mobile"]').text())[0]
	       except IndexError:
		    cena_a=''
		    
     
	       projects = {'sub':sub,
		         'rayon': ray,
		         'punkt': punkt,
		         'teritory':ter,
		         'adress': adress,
		         'tip':tip.replace(u'Отдельно',u'Отдельно стоящее здание'),
		         'url': task.url,
		         'metro': metro,
		         'metro_min': metro_min,
		         'name': name,
		         'klass': klass,
		         'nds': nds,
		         'ku': ku,
		         'god':god,
		         'park': park,
		         'ohrana':ohrana,
		         'rashodi': rashodi,
		         'opis': opis,
		         'kont': lico,
		         'arendt': yakor,
		         'et': et,
		         'plosh': plosh_ob,
		         'dataraz': data,
		         'oper': oper,
		         'cena_pr': cena.replace(u' Цена: ',','),
		         'cena_ar': cena_a         
		         }
	       yield Task('write',project=projects,grab=grab)
	       
	  def task_write(self,grab,task):
	       print('*'*100)
	       print  task.project['sub']
	       print  task.project['rayon']
	       print  task.project['teritory']
	       print  task.project['punkt']
	       print  task.project['adress']
	       print  task.project['tip']
	       print  task.project['et']
	       print  task.project['metro']
	       print  task.project['metro_min']
	       print  task.project['name']
	       print  task.project['klass']
	       print  task.project['nds']
	       print  task.project['ku']             
	       print  task.project['god']
	       print  task.project['park']             
	       print  task.project['ohrana']
	       print  task.project['rashodi']
	       print  task.project['opis']
	       print  task.project['kont']
	       print  task.project['arendt']
	       print  task.project['plosh']
	       print  task.project['url']
	       print  task.project['dataraz']
	       print  task.project['oper']
	       print  task.project['cena_pr']
	       print  task.project['cena_ar']
	       
	       self.ws.write(self.result,0, task.project['sub'])
	       self.ws.write(self.result,1, task.project['rayon']) 
	       self.ws.write(self.result,4, task.project['punkt'])
	       self.ws.write(self.result,5, task.project['teritory'])
	       self.ws.write(self.result,6, task.project['adress'])
	       self.ws.write(self.result,7, task.project['metro'])
	       self.ws.write(self.result,8, task.project['metro_min'])
	       self.ws.write(self.result,11, task.project['tip'])
	       self.ws.write(self.result,12, task.project['name'])
	       self.ws.write(self.result,13, task.project['klass'])	       
	       self.ws.write(self.result,14, task.project['plosh'])
	       self.ws.write(self.result,15, task.project['et'])
	       self.ws.write(self.result,16, task.project['nds'])
	       self.ws.write(self.result,17, task.project['ku'])             
	       self.ws.write(self.result,18, task.project['rashodi'])                  
	       self.ws.write(self.result,19, task.project['god'])
	       self.ws.write(self.result,20, task.project['park'])
	       self.ws.write(self.result,21, task.project['ohrana'])
	       self.ws.write(self.result,22, task.project['arendt'])
	       self.ws.write(self.result,24, task.project['opis'])
	       self.ws.write(self.result,25, u'БИБОСС')
	       self.ws.write_string(self.result,26, task.project['url'])
	       self.ws.write(self.result,27, task.project['kont'])
	       self.ws.write(self.result,29, task.project['dataraz'])
	       self.ws.write(self.result,30, datetime.today().strftime('%d.%m.%Y'))
	       #***************************************************************
	       self.ws1.write(self.result1,0, task.project['sub'])
	       self.ws1.write(self.result1,1, task.project['rayon'])
	       self.ws1.write(self.result1,3, task.project['punkt'])
	       self.ws1.write(self.result1,4, task.project['name'])
	       self.ws1.write(self.result1,5, task.project['oper'])
	       self.ws1.write(self.result1,6, task.project['tip'])
	       self.ws1.write(self.result1,7, task.project['et'])
	       self.ws1.write(self.result1,8, task.project['plosh'])
	       self.ws1.write(self.result1,11, task.project['cena_pr'])
	       self.ws1.write(self.result1,10, task.project['cena_ar'])
	       self.ws1.write(self.result1,12, u'БИБОСС')
	       self.ws1.write_string(self.result1,13, task.project['url'])
	       self.ws1.write(self.result1,15, task.project['dataraz'])
	       self.ws1.write(self.result1,16, datetime.today().strftime('%d.%m.%Y'))	       
	       
	       print('*'*100)
	       print 'Ready - '+str(self.result)+'/'+self.num
	       logger.debug('Tasks - %s' % self.task_queue.size()) 
               print '***',i+1,'/',len(l),'***'
	       print('*'*100)
	       self.result+= 1
	       self.result1+= 1
	       
	       #if self.result >50:
		    #self.stop()
		    
     
	       
	
     
     bot = Beboss(thread_number=5,network_try_limit=1000)
     bot.load_proxylist('../../tipa.txt','text_file')
     bot.create_grab_instance(timeout=50, connect_timeout=50)
     bot.run()
     bot.workbook.close()
     bot.workbook1.close()
     print('Done!')
     i=i+1
     try:
          page = l[i]
     except IndexError:
          break     
	 