#!/usr/bin/python
# -*- coding: utf-8 -*-

from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
from grab import Grab
import logging
import time


logging.basicConfig(level=logging.DEBUG)



i = 0
ls= open('Links/com_p.txt').read().splitlines()
dc = len(ls)

g = Grab(timeout=500, connect_timeout=500)
g.proxylist.load_file(path='../ivan.txt',proxy_type='http')			 




while i < len(ls):
    print '*********'
    print i+1,'/',dc  
    time.sleep(1)           
    g.go(ls[i])    
    #print ls[i]
    time.sleep(2)
    lin = []

    while True:

        try:
            for link in g.doc.select(u'//a[contains(@href,"sale/commercial")]'):
                url = link.attr('href')   
                print url
                lin.append(url)
            for link in g.doc.select(u'//a[contains(@href,"rent/commercial")]'):
                url = link.attr('href')   
                print url
                lin.append(url)                                 
            time.sleep(1)                                 
            page = g.doc.select(u'//li[@class="list-item--2QgXB list-item--active--2-sVo"]/following-sibling::li[1]/a').text()
            print'*********************'
            print 'Next Page = '+str(page)
            print '***',len(lin),'****'
            print i+1,'/',dc
            print'*********************'
            g.go(ls[i]+'&p=%s'% page) 
            time.sleep(1) 
        except IndexError:
            lin = list(set(lin))
            print '***',len(lin),'****'
            print 'Save...' 
            links = open('cian_com1.txt', 'a')
            for item in lin:
                links.write("%s\n" % item)
            links.close()
            time.sleep(3)
            #driver.close()
            break



    i=i+1 




