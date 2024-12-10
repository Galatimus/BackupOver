#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from lxml import html
import logging
import math
from lxml.etree import ParserError
from lxml.etree import XMLSyntaxError
import time
import re
import subprocess
reload(sys)
sys.setdefaultencoding('utf-8')






i = 0
l= open('old/comm.txt').read().splitlines()

page ='arenda-pomesheniya/'
   
logging.basicConfig(level=logging.DEBUG)



while True:
    try:
        print i+1,'/',len(l),'>>>>',l[i]+page
        command = "phantomjs --ignore-ssl-errors=true --ssl-protocol=any --load-images=false fetchh.js %s" % l[i]+page
        proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE).communicate()
        try:
            parsed_body = html.fromstring(proc[0].decode('utf-8').strip())
        except (ParserError,XMLSyntaxError):
            del proc
            continue        
    except IndexError:
        if page =='arenda-pomesheniya/':
            i = 0
            l= open('links/urls.txt').read().splitlines()
            page ='prodazha-pomesheniya/'
            time.sleep(2)
            continue
        else:
            print'DONE_ALL'
            time.sleep(2)
            break
    time.sleep(2)    
    nums = parsed_body.xpath('//span[@class="color-red ss"]/text()')[0]
    pag = int(math.ceil(float(int(nums))/float(16)))
    print 'Total...',nums,' Pages...',pag
    if pag == 0:
        del proc
        i=i+1
        continue
    del proc
    lin = []
    for x in range(1,pag+1):
        url_next = l[i]+page+'?page=%s' % str(x)
        print('*'*10)
        print ">>>>>..." ,url_next,' / ',str(pag)
        print('*'*10)
        comma = "phantomjs --ignore-ssl-errors=true --ssl-protocol=any --load-images=false fetchh.js %s" % url_next
        p = subprocess.Popen(comma, shell=True,stdout=subprocess.PIPE).communicate()
        try:
            bod = html.fromstring(p[0].decode('utf-8').strip())
        except (ParserError,XMLSyntaxError):
            continue        
        time.sleep(2)        
        linkss = bod.xpath('//a[@itemprop="url"]/@href')
        my_urls = '\n'.join(linkss)
        print my_urls
        lin.append(my_urls)
        del p
    print ('*'*20)
    time.sleep(2)
    links = open('mlsn_com.txt', 'a')
    for item in lin:
        links.write("%s\n" % item)
    links.close()            
    time.sleep(2)            
    ll= open('mlsn_com.txt').read().splitlines()
    print'Ready...',len(ll)
    print('*'*10)
    time.sleep(2)
    i=i+1 
    





