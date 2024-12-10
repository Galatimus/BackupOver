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
import os
import re
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')







profile =  webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/n1ddsdpx.default/') #Gui2
#profile = webdriver.FirefoxProfile('/home/oleg/.mozilla/firefox/1yvcvhni.default/')#Gui1
#profile = webdriver.FirefoxProfile()
profile.native_events_enabled = False
driver  = webdriver.Firefox(firefox_profile=profile,executable_path=r'/usr/local/bin/geckodriver',timeout=40)


time.sleep(1)




driver.set_window_position(0,0)
driver.set_window_size(950,720)



time.sleep(5)



driver.get("https://www.gisip.ru/#!ru/parks/")



lin = []

time.sleep(15)



for link in driver.find_elements_by_xpath(u'//a[@class="list-item"]'):
        url = link.get_attribute('href')   
        print url
        lin.append(url)
print '***',len(lin),'***'

    
#driver.close()
print('Done!') 



workbook = xlsxwriter.Workbook(u'Gisip_Система_Индустриальных_Парков.xlsx')
        
ws = workbook.add_worksheet(u'gisip')
ws.write(0, 0,u"Субъект РФ")
ws.write(0, 1, u"Название парка")
ws.write(0, 2, u"Тип площадки")
ws.write(0, 3, u"Тип парка")
ws.write(0, 4, u"Адрес парка")
ws.write(0, 5, u"Наименование управляющей компании парка")
ws.write(0, 6, u"Форма собственности Управляющей компании")
ws.write(0, 7, u"Форма собственности активов недвижимого имущества (не принадлежащих резидентам парка) и внутренней инфраструктуры")
ws.write(0, 8, u"Тип парка по форме собственности")
ws.write(0, 9, u"Название сайта парка")
ws.write(0, 10, u"Наличие концепции развития парка")
ws.write(0, 11, u"Контактное лицо от парка")
ws.write(0, 12, u"Телефон")
ws.write(0, 13, u"Мобильный телефон")
ws.write(0, 14, u"E-mail")
ws.write(0, 15, u"Специализация парка")
ws.write(0, 16, u"Статус")
ws.write(0, 17, u"Продажа земельного участка")
ws.write(0, 18, u"Сдача в аренду земельного участка")
ws.write(0, 19, u"Сдача в аренду готовых производственных помещений")
ws.write(0, 20, u"Строительство готовых производственных зданий под ключ (услуга built-to-suit)")
ws.write(0, 21, u"Предоставление специализированного оборудования")
ws.write(0, 22, u"Логистические услуги")
ws.write(0, 23, u"Подбор персонала")
ws.write(0, 24, u"Содержание и эксплуатация объектов общего пользования")
ws.write(0, 25, u"Охранные услуги")
ws.write(0, 26, u"Юридические услуги")
ws.write(0, 27, u"Консалтинговые услуги")
ws.write(0, 28, u"Уборка территории, вывоз мусора")
ws.write(0, 29, u"Расстояние до ближайшего города, км")
ws.write(0, 30, u"Расстояние до регионального центра, км")
ws.write(0, 31, u"Расстояние до Москвы, км")
ws.write(0, 32, u"Расстояние до ближайшей федеральной трассы, км")
ws.write(0, 33, u"Ближайшая автомобильная дорога, название")
ws.write(0, 34, u"Ближайшая автомобильная дорога, расстояние, км")
ws.write(0, 35, u"Протяженность дорожной сети на территории парка, км")
ws.write(0, 36, u"Наличие присоединения к ж/д путям")
ws.write(0, 37, u"Наличие ж/д путей на территории парка")
ws.write(0, 38, u"Название ближайшего терминала разгрузки")
ws.write(0, 39, u"Расстояние до ближайшего терминала разгрузки ж/д транспорта, км")
ws.write(0, 40, u"Расстояние до ближайшего Международного аэропорта, км")
ws.write(0, 41, u"Общий размер территории, га")
ws.write(0, 42, u"Размер свободной территории, га")
ws.write(0, 43, u"Допустимый класс опасности для размещаемых предприятий, сооружений и иных объектов")
ws.write(0, 44, u"Средняя стоимость продажи земельного участка на территории парка, руб. за Га")
ws.write(0, 45, u"Существующие производственные помещения, предназначенные для размещения резидентов, кв.м")
ws.write(0, 46, u"Свободная площадь производственной недвижимости, кв.м")
ws.write(0, 47, u"Максимальная высота потолков производственных помещений (до ферм перекрытий), м")
ws.write(0, 48, u"Средняя стоимость аренды производственных помещений, руб. за кв.м. в год")
ws.write(0, 49, u"Общая площадь офисной недвижимости, предназначенной для размещения резидентов, кв.м")
ws.write(0, 50, u"Наличие электроснабжения")
ws.write(0, 51, u"Электрическая мощность, МВт")
ws.write(0, 52, u"Свободная электрическая мощность, МВт")
ws.write(0, 53, u"Наличие газообеспечения")
ws.write(0, 54, u"Мощность по газу, м3/ч")
ws.write(0, 55, u"Наличие теплоснабжения")
ws.write(0, 56, u"Мощность тепловой энергии, Гкал/ч")
ws.write(0, 57, u"Свободная мощность тепловой энергии, Гкал/ч")
ws.write(0, 58, u"Источник тепловой энергии")
ws.write(0, 59, u"Теплоноситель")
ws.write(0, 60, u"Наличие водообеспечения")
ws.write(0, 61, u"Мощность водообеспечения, кбм/ч")
ws.write(0, 62, u"Свободная мощность водообеспечения, кбм/ч")
ws.write(0, 63, u"Источник водообеспечения")
ws.write(0, 64, u"Наличие канализационных очистных сооружений")
ws.write(0, 65, u"Наличие ливневых очистных сооружений")
ws.write(0, 66, u"Каналы связи")
ws.write(0, 67, u"Наличие транспортного сообщения от населенных пунктов до парка")
ws.write(0, 68, u"Суммарный объем государственных вложений в инфраструктуру парка, руб")
ws.write(0, 69, u"Общее число резидентов на территории парка, ед")
ws.write(0, 70, u"Число резидентов, начавших производство на территории парка, ед.")
ws.write(0, 71, u"Количество созданных рабочих мест на территории парка, ед")
ws.write(0, 72, u"Является участником федеральных государственных программ")
ws.write(0, 73, u"Является участником региональных государственных программ")
ws.write(0, 74, u"Сертификат Ассоциации индустриальных парков")
ws.write(0, 75, u"Налог на прибыль")
ws.write(0, 76, u"Налог на транспорт")
ws.write(0, 77, u"Налог на имущество юридических лиц")
ws.write(0, 78, u"Налог на землю")
ws.write(0, 79, u"НДС")
ws.write(0, 80, u"Сертификат национального стандарта")
ws.write(0, 81, u"Суммарный объем частных вложений в инфраструктуру парка, руб")
ws.write(0, 82, u"Суммарный объем вложений резидентов на территории парка, руб")
ws.write(0, 83, u"ИСТОЧНИК_ИНФОРМАЦИИ")
ws.write(0, 84, u"ССЫЛКА_НА_ИСТОЧНИК_ИНФОРМАЦИИ")
row = 1




v = 1
for line in lin:
        print v,'/',len(lin)
        #try:
        driver.get(line)
        time.sleep(3)                
                #WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'//div[@id="over"][contains(@style,"none")]')))
        #except TimeoutException:
                #driver.execute_script("window.stop();")
        
        try:
                try:
                        sub = driver.find_element_by_xpath(u'//td[contains(text(),"Субъект РФ")]/following-sibling::td').text
                        print sub
                        ws.write(row, 0, sub)
                except (NoSuchElementException,IndexError):
                        sub = driver.find_element_by_xpath(u'//td[contains(text(),"Местонахождение промышленного технопарка, субъект РФ")]/following-sibling::td').text
                        print sub
                        ws.write(row, 0, sub)                        
        except (NoSuchElementException,IndexError):
                sub=''
                
        try:
                try:
                        naz = driver.find_element_by_xpath(u'//td[contains(text(),"Название парка")]/following-sibling::td').text
                        print naz
                        ws.write(row, 1, naz)
                except (NoSuchElementException,IndexError):
                        naz = driver.find_element_by_xpath(u'//td[contains(text(),"Наименование промышленного технопарка")]/following-sibling::td').text
                        print naz
                        ws.write(row, 1, naz)                        
        except (NoSuchElementException,IndexError):
                naz=''
        try:
                tip_pl = driver.find_element_by_xpath(u'//td[contains(text(),"Тип площадки")]/following-sibling::td').text
                print tip_pl
                ws.write(row, 2, tip_pl)
        except (NoSuchElementException,IndexError):
                tip_pl=''                
                
        try:
                punkt= driver.find_element_by_xpath(u'//td[contains(text(),"Тип парка")]/following-sibling::td').text
                print punkt
                ws.write(row, 3, punkt)
        except (NoSuchElementException,IndexError):
                punkt=''
                
        try:
                try:
                        adres= driver.find_element_by_xpath(u'//td[contains(text(),"Адрес парка")]/following-sibling::td').text
                        print adres
                        ws.write(row, 4, adres)
                except (NoSuchElementException,IndexError):
                        adres= driver.find_element_by_xpath(u'//td[contains(text(),"Почтовый адрес технопарка")]/following-sibling::td').text
                        print adres
                        ws.write(row, 4, adres)                        
        except (NoSuchElementException,IndexError):
                adres='' 
        try:
                try:
                        compania= driver.find_element_by_xpath(u'//td[contains(text(),"Наименование управляющей компании парка")]/following-sibling::td').text
                        print compania
                        ws.write(row, 5, compania)
                except (NoSuchElementException,IndexError):
                        compania= driver.find_element_by_xpath(u'//td[contains(text(),"Наименование управляющей компании промышленного технопарка")]/following-sibling::td').text
                        print compania
                        ws.write(row, 5, compania)                        
        except (NoSuchElementException,IndexError):
                compania=''
                
        try:
                try:
                        forma_sob= driver.find_element_by_xpath(u'//td[contains(text(),"Форма собственности Управляющей компании")]/following-sibling::td').text
                        print forma_sob
                        ws.write(row, 6, forma_sob)
                except (NoSuchElementException,IndexError):
                        forma_sob= driver.find_element_by_xpath(u'//td[contains(text(),"Форма собственности управляющей компании промышленного технопарка")]/following-sibling::td').text
                        print forma_sob
                        ws.write(row, 6, forma_sob)                        
        except (NoSuchElementException,IndexError):
                forma_sob=''                 
                
        try:
                metro= driver.find_element_by_xpath(u'//td[contains(text(),"Форма собственности активов недвижимого имущества (не принадлежащих резидентам парка) и внутренней инфраструктуры")]/following-sibling::td').text
                print metro
                ws.write(row, 7, metro)
        except (NoSuchElementException,IndexError):
                metro=''
                
        try:
                tip_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Тип парка по форме собственности")]/following-sibling::td').text
                print tip_parka
                ws.write(row, 8, tip_parka)
        except (NoSuchElementException,IndexError):
                tip_parka=''
                
        try:
                try:
                        side= driver.find_element_by_xpath(u'//td[contains(text(),"Название сайта парка")]/following-sibling::td').text
                        print side
                        ws.write_string(row, 9, side)
                except (NoSuchElementException,IndexError):
                        side= driver.find_element_by_xpath(u'//td[contains(text(),"Адрес сайта промышленного технопарка в сети интернет")]/following-sibling::td').text
                        print side
                        ws.write_string(row, 9, side)                        
        except (NoSuchElementException,IndexError):
                side=''                
                
        try:
                try:
                        sfera= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие концепции развития парка")]/following-sibling::td').text
                        print sfera
                        ws.write(row, 10, sfera)
                except (NoSuchElementException,IndexError):
                        sfera= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие концепции развития промышленного технопарка")]/following-sibling::td').text
                        print sfera
                        ws.write(row, 10, sfera)                        
        except (NoSuchElementException,IndexError):
                sfera=''
                
        try:
                try:
                        lico_parka= driver.find_element_by_xpath(u'//td[contains(text(),"ФИО")]/following-sibling::td').text
                        print lico_parka
                        ws.write(row, 11, lico_parka)
                except (NoSuchElementException,IndexError):
                        lico_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Ф.И.О. контактного лица")]/following-sibling::td').text
                        print lico_parka
                        ws.write(row, 11, lico_parka)                        
        except (NoSuchElementException,IndexError):
                lico_parka=''
                
        try:
                phone_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Телефон")]/following-sibling::td').text
                print phone_parka
                ws.write(row, 12, phone_parka)
        except (NoSuchElementException,IndexError):
                phone_parka=''                
                
        try:
                cena= driver.find_element_by_xpath(u'//td[contains(text(),"Мобильный телефон")]/following-sibling::td').text
                print cena
                ws.write(row, 13, cena)
        except (NoSuchElementException,IndexError):
                cena=''
                
        try:
                mail_parka= driver.find_element_by_xpath(u'//td[contains(text(),"E-mail")]/following-sibling::td').text
                print mail_parka
                ws.write_string(row, 14, mail_parka)
        except (NoSuchElementException,IndexError):
                mail_parka=''
                
        try:
                try:
                        spec_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Специализация парка")]/following-sibling::td').text
                        print spec_parka
                        ws.write(row, 15, spec_parka)
                except (NoSuchElementException,IndexError):
                        spec_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Специализация промышленного технопарка")]/following-sibling::td').text
                        print spec_parka
                        ws.write(row, 15, spec_parka)                        
        except (NoSuchElementException,IndexError):
                spec_parka=''        
        try:
                dolya= driver.find_element_by_xpath(u'//td[contains(text(),"Статус")]/following-sibling::td').text
                print dolya
                ws.write(row, 16, dolya)
        except (NoSuchElementException,IndexError):
                dolya=''
        try:
                mes= driver.find_element_by_xpath(u'//td[contains(text(),"Продажа земельного участка")]/following-sibling::td').text
                print mes
                ws.write(row, 17, mes)
        except (NoSuchElementException,IndexError):
                mes=''
        try:
                prib= driver.find_element_by_xpath(u'//td[contains(text(),"Сдача в аренду земельного участка")]/following-sibling::td').text
                print prib
                ws.write(row, 18, prib)
        except (NoSuchElementException,IndexError):
                prib=''
        try:
                sotr= driver.find_element_by_xpath(u'//td[contains(text(),"Сдача в аренду готовых производственных помещений")]/following-sibling::td').text
                print sotr
                ws.write(row, 19, sotr)
        except (NoSuchElementException,IndexError):
                sotr=''
                
        try:
                stroitel= driver.find_element_by_xpath(u'//td[contains(text(),"Строительство готовых производственных зданий под ключ (услуга built-to-suit)")]/following-sibling::td').text
                print stroitel
                ws.write(row, 20, stroitel)
        except (NoSuchElementException,IndexError):
                stroitel=''
                
        try:
                obor_parka= driver.find_element_by_xpath(u'//td[contains(text(),"Предоставление специализированного оборудования")]/following-sibling::td').text
                print obor_parka
                ws.write(row, 21, obor_parka)
        except (NoSuchElementException,IndexError):
                obor_parka=''        
        try:
                vozr= driver.find_element_by_xpath(u'//td[contains(text(),"Логистические услуги")]/following-sibling::td').text
                print vozr
                ws.write(row, 22, vozr)
        except (NoSuchElementException,IndexError):
                vozr=''
        try:
                sred= driver.find_element_by_xpath(u'//td[contains(text(),"Подбор персонала")]/following-sibling::td').text
                print sred
                ws.write(row, 23, sred)
        except (NoSuchElementException,IndexError):
                sred=''
        try:
                prich= driver.find_element_by_xpath(u'//td[contains(text(),"Содержание и эксплуатация объектов общего пользования")]/following-sibling::td').text
                print prich
                ws.write(row, 24, prich)
        except (NoSuchElementException,IndexError):
                prich=''
        try:
                opis= driver.find_element_by_xpath(u'//td[contains(text(),"Охранные услуги")]/following-sibling::td').text
                print opis
                ws.write(row, 25, opis)
        except (NoSuchElementException,IndexError):
                opis=''
                
        try:
                ur_uslugi= driver.find_element_by_xpath(u'//td[contains(text(),"Юридические услуги")]/following-sibling::td').text
                print ur_uslugi
                ws.write(row, 26, ur_uslugi)
        except (NoSuchElementException,IndexError):
                ur_uslugi='' 
                
        try:
                colsat= driver.find_element_by_xpath(u'//td[contains(text(),"Консалтинговые услуги")]/following-sibling::td').text
                print colsat
                ws.write(row, 27, colsat)
        except (NoSuchElementException,IndexError):
                colsat=''                
        try:
                musor= driver.find_element_by_xpath(u'//td[contains(text(),"Уборка территории, вывоз мусора")]/following-sibling::td').text
                print musor
                ws.write(row, 28, musor)
        except (NoSuchElementException,IndexError):
                musor=''
                
        try:
                try:
                        data= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до ближайшего города, км")]/following-sibling::td').text
                        print data
                        ws.write(row, 29, data)
                except (NoSuchElementException,IndexError):
                        data= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до центра города, км")]/following-sibling::td').text
                        print data
                        ws.write(row, 29, data)                        
        except (NoSuchElementException,IndexError):
                data=''
                
        try:
                region= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до регионального центра, км")]/following-sibling::td').text
                print region
                ws.write(row, 30, region)
        except (NoSuchElementException,IndexError):
                region=''                
        try:
                zag = driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до Москвы, км")]/following-sibling::td').text
                print zag
                ws.write(row, 31, zag)
        except (NoSuchElementException,IndexError):
                zag =''                
        try:
                web= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до ближайшей федеральной трассы, км")]/following-sibling::td').text#.split(': ')[1]
                print web
                ws.write(row, 32, web)
        except (NoSuchElementException,IndexError):
                web=''
                
        try:
                adr = driver.find_element_by_xpath(u'//td[contains(text(),"Ближайшая автомобильная дорога, название")]/following-sibling::td').text
                print adr
                ws.write(row, 33, adr)
        except (NoSuchElementException,IndexError):
                adr =''
                
        try:
                tov = driver.find_element_by_xpath(u'//td[contains(text(),"Ближайшая автомобильная дорога, расстояние, км")]/following-sibling::td').text
                print tov
                ws.write(row, 34, tov)
        except (NoSuchElementException,IndexError):
                tov =''  
                
        ##########################################################################################
        
        
        try:
                dor_set = driver.find_element_by_xpath(u'//td[contains(text(),"Протяженность дорожной сети на территории парка, км")]/following-sibling::td').text
                print dor_set
                ws.write(row, 35, dor_set)
        except (NoSuchElementException,IndexError):
                dor_set=''

        try:
                pris = driver.find_element_by_xpath(u'//td[contains(text(),"Наличие присоединения к ж/д путям")]/following-sibling::td').text
                print pris
                ws.write(row, 36, naz)
        except (NoSuchElementException,IndexError):
                pris=''
        try:
                gdputi = driver.find_element_by_xpath(u'//td[contains(text(),"Наличие ж/д путей на территории парка")]/following-sibling::td').text
                print gdputi
                ws.write(row, 37, gdputi)
        except (NoSuchElementException,IndexError):
                gdputi=''                

        try:
                terminal= driver.find_element_by_xpath(u'//td[contains(text(),"Название ближайшего терминала разгрузки")]/following-sibling::td').text
                print terminal
                ws.write(row, 38, terminal)
        except (NoSuchElementException,IndexError):
                terminal=''

        try:
                rassto= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до ближайшего терминала разгрузки ж/д транспорта, км")]/following-sibling::td').text
                print rassto
                ws.write(row, 39, rassto)
        except (NoSuchElementException,IndexError):
                rassto='' 
        try:
                aero= driver.find_element_by_xpath(u'//td[contains(text(),"Расстояние до ближайшего Международного аэропорта, км")]/following-sibling::td').text
                print aero
                ws.write(row, 40, aero)
        except (NoSuchElementException,IndexError):
                aero=''

        try:
                razmer= driver.find_element_by_xpath(u'//td[contains(text(),"Общий размер территории, га")]/following-sibling::td').text
                print razmer
                ws.write(row, 41, razmer)
        except (NoSuchElementException,IndexError):
                razmer=''                 

        try:
                svobod= driver.find_element_by_xpath(u'//td[contains(text(),"Размер свободной территории, га")]/following-sibling::td').text
                print svobod
                ws.write(row, 42, svobod)
        except (NoSuchElementException,IndexError):
                svobod=''

        try:
                klass= driver.find_element_by_xpath(u'//td[contains(text(),"Допустимый класс опасности для размещаемых предприятий, сооружений и иных объектов")]/following-sibling::td').text
                print klass
                ws.write(row, 43, klass)
        except (NoSuchElementException,IndexError):
                klass=''

        try:
                zem_uch= driver.find_element_by_xpath(u'//td[contains(text(),"Средняя стоимость продажи земельного участка на территории парка, руб. за Га")]/following-sibling::td').text
                print zem_uch
                ws.write_string(row, 44, zem_uch)
        except (NoSuchElementException,IndexError):
                zem_uch=''                

        try:
                pomech= driver.find_element_by_xpath(u'//td[contains(text(),"Существующие производственные помещения, предназначенные для размещения резидентов, кв.м")]/following-sibling::td').text
                print pomech
                ws.write(row, 45, pomech)
        except (NoSuchElementException,IndexError):
                pomech=''

        try:
                rpoiz= driver.find_element_by_xpath(u'//td[contains(text(),"Свободная площадь производственной недвижимости, кв.м")]/following-sibling::td').text
                print rpoiz
                ws.write(row, 46, rpoiz)
        except (NoSuchElementException,IndexError):
                rpoiz=''

        try:
                potolki= driver.find_element_by_xpath(u'//td[contains(text(),"Максимальная высота потолков производственных помещений (до ферм перекрытий), м")]/following-sibling::td').text
                print potolki
                ws.write(row, 47, potolki)
        except (NoSuchElementException,IndexError):
                potolki=''                

        try:
                arenda= driver.find_element_by_xpath(u'//td[contains(text(),"Средняя стоимость аренды производственных помещений, руб. за кв.м. в год")]/following-sibling::td').text
                print arenda
                ws.write(row, 48, arenda)
        except (NoSuchElementException,IndexError):
                arenda=''

        try:
                ofis_nedv= driver.find_element_by_xpath(u'//td[contains(text(),"Общая площадь офисной недвижимости, предназначенной для размещения резидентов, кв.м")]/following-sibling::td').text
                print ofis_nedv
                ws.write_string(row, 49, ofis_nedv)
        except (NoSuchElementException,IndexError):
                ofis_nedv=''

        try:
                elektro= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие электроснабжения")]/following-sibling::td').text
                print elektro
                ws.write(row, 50, elektro)
        except (NoSuchElementException,IndexError):
                elektro=''        
        try:
                mosh= driver.find_element_by_xpath(u'//td[contains(text(),"Электрическая мощность, МВт")]/following-sibling::td').text
                print mosh
                ws.write(row, 51, mosh)
        except (NoSuchElementException,IndexError):
                mosh=''
        try:
                svobod_mosh= driver.find_element_by_xpath(u'//td[contains(text(),"Свободная электрическая мощность, МВт")]/following-sibling::td').text
                print svobod_mosh
                ws.write(row, 52, svobod_mosh)
        except (NoSuchElementException,IndexError):
                svobod_mosh=''
        try:
                gazoob= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие газообеспечения")]/following-sibling::td').text
                print gazoob
                ws.write(row, 53, gazoob)
        except (NoSuchElementException,IndexError):
                gazoob=''
        try:
                mosh_gaz= driver.find_element_by_xpath(u'//td[contains(text(),"Мощность по газу, м3/ч")]/following-sibling::td').text
                print mosh_gaz
                ws.write(row, 54, mosh_gaz)
        except (NoSuchElementException,IndexError):
                mosh_gaz=''

        try:
                teplo= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие теплоснабжения")]/following-sibling::td').text
                print teplo
                ws.write(row, 55, teplo)
        except (NoSuchElementException,IndexError):
                teplo=''

        try:
                teplo_mosh= driver.find_element_by_xpath(u'//td[contains(text(),"Мощность тепловой энергии, Гкал/ч")]/following-sibling::td').text
                print teplo_mosh
                ws.write(row, 56, teplo_mosh)
        except (NoSuchElementException,IndexError):
                teplo_mosh=''        
        try:
                svo_teplo= driver.find_element_by_xpath(u'//td[contains(text(),"Свободная мощность тепловой энергии, Гкал/ч")]/following-sibling::td').text
                print svo_teplo
                ws.write(row, 57, svo_teplo)
        except (NoSuchElementException,IndexError):
                svo_teplo=''
        try:
                istoch_teplo= driver.find_element_by_xpath(u'//td[contains(text(),"Источник тепловой энергии")]/following-sibling::td').text
                print istoch_teplo
                ws.write(row, 58, istoch_teplo)
        except (NoSuchElementException,IndexError):
                istoch_teplo=''
        try:
                teplonos= driver.find_element_by_xpath(u'//td[contains(text(),"Теплоноситель")]/following-sibling::td').text
                print teplonos
                ws.write(row, 59, teplonos)
        except (NoSuchElementException,IndexError):
                teplonos=''
        try:
                voda= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие водообеспечения")]/following-sibling::td').text
                print voda
                ws.write(row, 60, voda)
        except (NoSuchElementException,IndexError):
                voda=''

        try:
                voda_mosh= driver.find_element_by_xpath(u'//td[contains(text(),"Мощность водообеспечения, кбм/ч")]/following-sibling::td').text
                print voda_mosh
                ws.write(row, 61, voda_mosh)
        except (NoSuchElementException,IndexError):
                voda_mosh='' 

        try:
                voda_svobod= driver.find_element_by_xpath(u'//td[contains(text(),"Свободная мощность водообеспечения, кбм/ч")]/following-sibling::td').text
                print voda_svobod
                ws.write(row, 62, voda_svobod)
        except (NoSuchElementException,IndexError):
                voda_svobod=''                
        try:
                voda_istoch= driver.find_element_by_xpath(u'//td[contains(text(),"Источник водообеспечения")]/following-sibling::td').text
                print voda_istoch
                ws.write(row, 63, voda_istoch)
        except (NoSuchElementException,IndexError):
                voda_istoch=''
        try:
                kanaliz= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие канализационных очистных сооружений")]/following-sibling::td').text
                print kanaliz
                ws.write(row, 64, kanaliz)
        except (NoSuchElementException,IndexError):
                kanaliz=''

        try:
                liven= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие ливневых очистных сооружений")]/following-sibling::td').text
                print liven
                ws.write(row, 65, liven)
        except (NoSuchElementException,IndexError):
                liven=''                
        try:
                svyaz = driver.find_element_by_xpath(u'//td[contains(text(),"Каналы связи")]/following-sibling::td').text
                print svyaz
                ws.write(row, 66, svyaz)
        except (NoSuchElementException,IndexError):
                svyaz =''                
        try:
                soob= driver.find_element_by_xpath(u'//td[contains(text(),"Наличие транспортного сообщения от населенных пунктов до парка")]/following-sibling::td').text
                print soob
                ws.write(row, 67, soob)
        except (NoSuchElementException,IndexError):
                soob=''

        try:
                obem = driver.find_element_by_xpath(u'//h3[contains(text(),"Суммарный объем государственных вложений в инфраструктуру парка, руб")]/following-sibling::div/table/tbody/tr/td[2]').text
                print obem
                ws.write(row, 68, obem)
        except (NoSuchElementException,IndexError):
                obem =''

        try:
                chislo = driver.find_element_by_xpath(u'//td[contains(text(),"Общее число резидентов на территории парка, ед")]/following-sibling::td').text
                print chislo
                ws.write(row, 69, chislo)
        except (NoSuchElementException,IndexError):
                chislo =''        
        ############################################################################
        
        try:
                reziden = driver.find_element_by_xpath(u'//td[contains(text(),"Число резидентов, начавших производство на территории парка, ед.")]/following-sibling::td').text
                print reziden
                ws.write(row, 70, reziden)
        except (NoSuchElementException,IndexError):
                reziden=''

        try:
                mesta = driver.find_element_by_xpath(u'//td[contains(text(),"Количество созданных рабочих мест на территории парка, ед")]/following-sibling::td').text
                print mesta
                ws.write(row, 71, mesta)
        except (NoSuchElementException,IndexError):
                mesta=''
        try:
                fed_prog = driver.find_element_by_xpath(u'//td[contains(text(),"Является участником федеральных государственных программ")]/following-sibling::td').text
                print fed_prog
                ws.write(row, 72, fed_prog)
        except (NoSuchElementException,IndexError):
                fed_prog=''                

        try:
                region_prog= driver.find_element_by_xpath(u'//td[contains(text(),"Является участником региональных государственных программ")]/following-sibling::td').text
                print region_prog
                ws.write(row, 73, region_prog)
        except (NoSuchElementException,IndexError):
                region_prog=''

        try:
                nalog= driver.find_element_by_xpath(u'//td[contains(text(),"Сертификат Ассоциации индустриальных парков")]/following-sibling::td').text
                print nalog
                ws.write(row, 74, nalog)
        except (NoSuchElementException,IndexError):
                nalog='' 
        try:
                nalog_prib= driver.find_element_by_xpath(u'//td[contains(text(),"Налог на прибыль")]/following-sibling::td[1]').text
                print nalog_prib
                ws.write(row, 75, nalog_prib)
        except (NoSuchElementException,IndexError):
                nalog_prib=''

        try:
                nalog_tran= driver.find_element_by_xpath(u'//td[contains(text(),"Налог на транспорт")]/following-sibling::td[1]').text
                print nalog_tran
                ws.write(row, 76, nalog_tran)
        except (NoSuchElementException,IndexError):
                nalog_tran=''                 

        try:
                nalog_urlic= driver.find_element_by_xpath(u'//td[contains(text(),"Налог на имущество юридических лиц")]/following-sibling::td[1]').text
                print nalog_urlic
                ws.write(row, 77, nalog_urlic)
        except (NoSuchElementException,IndexError):
                nalog_urlic=''

        try:
                nalog_zem= driver.find_element_by_xpath(u'//td[contains(text(),"Налог на землю")]/following-sibling::td[1]').text
                print nalog_zem
                ws.write(row, 78, nalog_zem)
        except (NoSuchElementException,IndexError):
                nalog_zem=''

        try:
                nds_nalog= driver.find_element_by_xpath(u'//td[@class="tax_name"][contains(text(),"НДС")]/following-sibling::td[1]').text
                print nds_nalog
                ws.write_string(row, 79, nds_nalog)
        except (NoSuchElementException,IndexError):
                nds_nalog=''
                
        try:
                standard= driver.find_element_by_xpath(u'//td[contains(text(),"Сертификат национального стандарта")]/following-sibling::td').text
                print standard
                ws.write_string(row, 80, standard)
        except (NoSuchElementException,IndexError):
                standard='' 
                
        try:
                obem_sum= driver.find_element_by_xpath(u'//h3[contains(text(),"Суммарный объем частных вложений в инфраструктуру парка, руб")]/following-sibling::div/table/tbody/tr/td[2]').text
                print obem_sum
                ws.write_string(row, 81, obem_sum)
        except (NoSuchElementException,IndexError):
                obem_sum=''
                
        try:
                sum_rezident= driver.find_element_by_xpath(u'//h3[contains(text(),"Суммарный объем вложений резидентов на территории парка, руб")]/following-sibling::div/table/tbody/tr/td[2]').text
                print sum_rezident
                ws.write_string(row, 82, sum_rezident)
        except (NoSuchElementException,IndexError):
                sum_rezident=''                

        
        
        
        ws.write(row, 83, 'Геоинформационная система индустриальных парков, технопарков и кластеров Российской Федерации')
        ws.write_string(row, 84, line)
      
        
        
        
        
        
        
        
        
        v+=1
        row+=1
        print('*'*5)
        time.sleep(2)
        
        #if v > 10:
             #break          
        
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
command = 'mount -a'
##command = 'apt autoremove'
p = os.system('echo %s|sudo -S %s' % ('1122', command))
print p
time.sleep(1)
workbook.close()
time.sleep(1)
driver.close()
print('Done!')

    
    
    
    
    
    
    
    
   