#!/usr/bin/python
# -*- coding: utf-8 -*-


import dryscrape
import webkit_server
import time
import os
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


i = 0
l= open('city_cian.txt').read().splitlines()
page ='snyat-pomeshenie-v-biznes-centre/'

dryscrape.start_xvfb()
server = webkit_server.Server()
server_conn = webkit_server.ServerConnection(server=server)
driver = dryscrape.driver.webkit.Driver(connection=server_conn)
sess = dryscrape.Session(driver=driver)

while True:
    print '**********',i+1,'/',len(l),'********'
    proxy = random.choice(list(open('../../tipa.txt').read().splitlines())).split(':')[0]
    print 'Proxy is : ',proxy     
    try:
        
        sess.set_timeout(30)
        sess.set_proxy(host = proxy, port = 4045)
        #sess.set_header('Host', 'www.cian.ru')
        sess.set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0')
        sess.set_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        sess.set_header('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3')
        #sess.set_header('Accept-Encoding', 'gzip, deflate, br')       
        sess.set_cookie('_CIAN_GK=728644fe-916e-416e-af6d-41d9bf52f7cf')
        #sess.set_proxy(host= proxy, port=8080, user='Ivan', password='tempuvefy')
        sess.visit(l[i]+page)
        print sess.status_code()
        print sess.url()
    except BaseException as e:
        print str(e)
        time.sleep(2)
        #sess.reset()
        continue
    
    if 'captcha'in sess.url() or sess.status_code() <> 200 or 'Broken' in e:    
        time.sleep(2)
        sess.reset()
        continue 
    
    #if sess.status_code() <> 200:    
        #time.sleep(2)
        #continue    
        
    time.sleep(1)
    lin = []
    baze_url = 'https://'+l[i].split('/')[2]   
    print 'Baze Url : ',baze_url
    while True:
        try:
            time.sleep(2)   
            for link in sess.xpath('//h3/a'):
                url = baze_url+link['href']
                print url
                lin.append(url)
            print '***',len(lin),'**********',i+1,'/',len(l),'********'
            time.sleep(1)   
            print "Next Page is ...",'Proxy is : ',proxy  
            nextpage = 'https://www.cian.ru'+sess.at_xpath(u'//nav[@class="cf-pagination"]/span/following-sibling::a[1]')['href']
            print nextpage
            time.sleep(2)
            #url_next = l[i]+page+'page-'+nextpage+'/'
            #print url_next
            #print '*********************************'
            sess.visit(nextpage)
            time.sleep(2)             
        except BaseException as e:
            print str(e)
            #links = open('bc_com.txt', 'a')
            #for item in lin:
                #links.write("%s\n" % item)
            #links.close()            
            #time.sleep(1)            
            print'NEXT'            
            break
        
    #sess.reset()
    i=i+1 
    
    




