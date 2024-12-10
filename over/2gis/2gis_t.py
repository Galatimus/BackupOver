#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
from grab.error import GrabTimeoutError, GrabNetworkError,GrabConnectionError 
import re
import time
from grab import Grab
import logging
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
g = Grab(timeout=2000, connect_timeout=2000)

#g.proxylist.load_file(path='/home/oleg/Proxy/tipa.txt',proxy_type='http')

workbook = xlsxwriter.Workbook(u'ready.xlsx')
ws = workbook.add_worksheet()
ws.write(0,5, u"Тип постройки")
row = 1

rb = xlrd.open_workbook(u'Типы_КОМ_0616.xlsx')
sheet = rb.sheet_by_index(0)
#print sheet.cell_value(1,3)
#print sheet.nrows
#print sheet.ncols
#lin = []
page = 'https://2gis.ru/countries/global/'
g.go(page)
v = 1
g2 = g.clone(timeout=2000, connect_timeout=2000)
for ul in range(1,sheet.nrows):
    punkt= sheet.cell_value(ul,3)#.replace(', ',',')
    uliza= sheet.cell_value(ul,5)#.replace(', ',',')
    dom= str(sheet.cell_value(ul,6)).replace('.0','')
    #print('*'*50)
    print v+1,'/',sheet.nrows
    #print punkt
    #print uliza
    #print dom
    try:
        url_gis= g.doc.select(u'//header[@class="world__sectionHeader"]/following-sibling::ul/li/h2/a[contains(text(),"'+punkt+'")]').attr('href')
        print url_gis
        
        g2.go(url_gis+'/search/'+uliza+' '+dom)
        tip_zd= g2.doc.select(u'//div[@class="miniCard__desc"]/following-sibling::div[@class="miniCard__additional"]').text()
        #name= g2.doc.select(u'//div[@class="miniCard__desc"]/following-sibling::div[@class="miniCard__additional"]/preceding::header[1]').text()
        #print name
        print punkt
        print uliza
        print tip_zd        
        ws.write(row, 5, tip_zd)
    except IndexError:
        pass
    v+=1
    print('*'*50)
    time.sleep(1)
    row+=1
    #lin.append(punkt)
#print '\n'.join(lin)


#v = 1
#for line in lin:
    #print v,'/',len(lin)
    #g.go(page)
    #try:
        #tip_zd= g.doc.select(u'//header[@class="world__sectionHeader"]/following-sibling::ul/li/h2/a[contains(text(),"'+line+'")]').attr('href')
        #print tip_zd
        ##ws.write(row, 5, tip_zd)
    #except IndexError:
        #pass
    #v+=1
    
    ##time.sleep(1)
    
    
workbook.close()
print('Done!')    