#!/usr/bin/python
# -*- coding: utf-8 -*-

from grab.spider import Spider,Task
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import logging
import re
import os
import math
import time
from datetime import datetime,timedelta
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab


logging.basicConfig(level=logging.DEBUG)

#try:
    #os.remove('/home/oleg/pars/mlsn/mlsn_zem.txt')
    #print 'Удаляем: '
#except (IOError, OSError):
    #print 'Нет файла'
    
i = 0
ls= ['https://land.ngs.ru/kupit/?gorod=all','https://land.e1.ru/kupit/?gorod=all','https://land.ngs.ru/snyat/?gorod=all']
dc = len(ls)

places = []



while True:
    print '********************************************',i+1,'/',dc,'*******************************************'
    page = ls[i]
    lin = []
    class Brsn_Com(Spider):
        def prepare(self):
            self.f = page
            for p in range(1,15):
                try:
                    time.sleep(1)
                    g = Grab(timeout=50, connect_timeout=100)
                    g.proxylist.load_file(path='../tipa.txt',proxy_type='http') 
                    g.go(self.f)
                    try:
                        self.num = re.sub('[^\d]','',g.doc.select(u'//div[@id="param_search"]/strong').text())
                    except IndexError:
                        self.num =re.sub('[^\d]','',g.doc.select(u'//h2[@class="re-search-result-header-title__text"]').text())
                    self.pag = int(math.ceil(float(int(self.num))/float(50)))
                    print self.num,self.pag
                    del g
                    break
                except(GrabTimeoutError,GrabNetworkError,IndexError,KeyError,AttributeError,GrabConnectionError):
                    print g.config['proxy'],'Change proxy'
                    g.change_proxy()
                    del g
                    continue
            else:
                self.pag = 85
            
        def task_generator(self):
            for x in range(1,self.pag+1):
                link = self.f+'&page=%s' % str(x)
                yield Task ('post',url=link,refresh_cache=True,network_try_count=100)

        def task_post(self,grab,task):
            for elem in grab.doc.select(u'//a[contains(@href,"view")]'):
                ur = grab.make_url_absolute(elem.attr('href')).replace('?open_card_land','').replace('?utm_source=realty_similar_listing&utm_medium=ngs','')
                print ur
                lin.append(ur)
            #for el in grab.doc.select(u'//td[@class="re-search-result-table__body-cell re-search-result-table__body-cell_price"]/a[contains(@href,"view")]'):
                #ur1 = grab.make_url_absolute(el.attr('href'))
                #print ur1
                #lin.append(ur1)

    bot = Brsn_Com(thread_number=5,network_try_limit=1000)
    bot.load_proxylist('../tipa.txt','text_file')
    bot.create_grab_instance(timeout=500, connect_timeout=500)    
    bot.run()
    print 'Save...' 
    #lin = list(set(lin))
    print '***',len(lin),'****'
    time.sleep(2)    
    for item in lin:
        places.append(item)
    print 'Total...',len(places)
    time.sleep(1)
    try:
        i=i+1
        page = ls[i]
    except IndexError:
        break
    
liks = open('ngs_zem.txt', 'w')
for itm in places:
    liks.write("%s\n" % itm)
liks.close()
print('Done')
time.sleep(5)
os.system("/home/oleg/pars/ngs/zem.py")
    





