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
ls= ['https://kn.ngs.ru/kupit/?gorod=all','https://kn.e1.ru/kupit/?gorod=all','https://kn.ngs.ru/snyat/?gorod=all','https://kn.e1.ru/snyat/?gorod=all']
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
                self.pag = 45
            
        def task_generator(self):
            for x in range(1,self.pag+1):
                link = self.f+'&page=%s' % str(x)
                yield Task ('post',url=link,refresh_cache=True,network_try_count=100)

        def task_post(self,grab,task):
            for elem in grab.doc.select(u'//tr[@class="lines  shown"]/td[6]/a'):
                ur = grab.make_url_absolute(elem.attr('href')).replace('?open_card_kn','').replace('?utm_source=realty_similar_listing&utm_medium=ngs','')
                print ur
                lin.append(ur)

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
    
liks = open('ngs_com.txt', 'w')
for itm in places:
    liks.write("%s\n" % itm)
liks.close()
print('Done')
time.sleep(5)
os.system("/home/oleg/pars/ngs/comm.py")
    





