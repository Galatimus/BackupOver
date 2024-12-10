#!/usr/bin/python
# -*- coding: utf-8 -*-


import dryscrape
import time
import os
import sys
import webkit_server
reload(sys)
sys.setdefaultencoding('utf-8')


i = 0
l= open('old/comm.txt').read().splitlines()
page ='arenda-pomesheniya/'

dryscrape.start_xvfb()
server = webkit_server.Server()
server_conn = webkit_server.ServerConnection(server=server)
driver = dryscrape.driver.webkit.Driver(connection=server_conn)
sess = dryscrape.Session(driver=driver)
while True:
    try:
        sess.set_header('user-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
        sess.visit(l[i]+page)
    except IndexError:
        if page =='arenda-pomesheniya/':
            i = 0
            l= open('old/comm.txt').read().splitlines()
            page ='prodazha-pomesheniya/'
            time.sleep(2)
            continue
        else:
            print'DONE_ALL'
            time.sleep(5)
            #os.system("/home/oleg/pars/bcinfo/comm.py")
            break
    time.sleep(1)
    lin = []
    baze_url = 'https://'+l[i].split('/')[2]   
    print 'Baze Url : ',baze_url
    while True:
        try:
            time.sleep(2)   
            for link in sess.xpath('//div[@class="row page-link"]/a'):
                url = baze_url+link['href']
                print url
                lin.append(url)
            print '***',len(lin),'**********',i+1,'/',len(l),'********'
            time.sleep(1)   
            print "Next Page is ..."  
            nextpage = sess.at_xpath(u'//i[@class="material-icons"][contains(text(),"chevron_right")]/ancestor::a')['data-page']            
            url_next = l[i]+page+'page-'+nextpage+'/'
            print url_next
            print '*********************************'
            sess.visit(url_next)
            time.sleep(2)             
        except :
            links = open('bc_com.txt', 'a')
            for item in lin:
                links.write("%s\n" % item)
            links.close()            
            time.sleep(1)            
            print'NEXT'            
            break
        
    #sess.reset()
    i=i+1 
    
    




