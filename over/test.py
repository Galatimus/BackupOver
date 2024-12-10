#!/usr/bin/python
# -*- coding: utf-8 -*-



from grab.spider import Spider,Task
import logging
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError 
import re
import math
#import imgkit
import random
from datetime import datetime,timedelta
import xlsxwriter
from cStringIO import StringIO
import pytesseract
from PIL import Image 
import os
import time
import base64
from grab import Grab
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)


#places = []
#with open('faprost_com.txt', 'r') as filehandle:  
    #filecontents = filehandle.readlines()
    #for line in filecontents:
        #current_place = line[:-1]
        #for x in range(3):
            #places.append(current_place)
    #os.remove('/home/oleg/pars/over/faprost_com.txt')
    #print 'Удаляем: '
#print len(places)
#time.sleep(2)
#links = open('faprost_com.txt', 'w')
#for item in places:
    #links.write("%s\n" % item)
#links.close()

g = Grab(timeout=20, connect_timeout=50)
g.proxylist.load_file(path='../tipa.txt',proxy_type='http')

my_link = 'https://youla.ru/ulyanovsk/nedvijimost/kommercheskaya-nedvijimost/arienda-ofisnoie-pomieshchieniie-10-m2-5c37d341eef1415cc1629532'

#agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

##box = 'https://www.site-shot.com/screenshot/?width=1024&height=0&zoom=100&scaled_width=1024&full_size=1&format=PNG&user_agent='+agent+'&url='+my_link

##box = 'https://api.site-shot.com/?width=1024&height=0&zoom=100&scaled_width=1024&full_size=1&format=PNG&user_agent='+agent+'&response_type=json&url='+my_link
g.go(my_link)

print grab.doc.select(u'//h1[contains(text(),"Объявление неактивно")]').exists()

#nums = re.sub('[^\d]', u'',g.doc.select('//span[@class="long-label"]').text())
#print nums
##lin = []
#for el in g.doc.select(u'//a[@class="location"]'):
    #urr = g.make_url_absolute(el.attr('href'))  
    #print urr
    #lin.append(urr)
#links = open('Torgi_Zem.txt', 'w')
#for item in lin:
    #links.write("%s\n" % item)
#links.close()

#i = 0
#l= open('Torgi_Zem.txt').read().splitlines()
#lin = []
#while True:
    #try:
        #g = Grab(timeout=20, connect_timeout=50)
        #g.proxylist.load_file(path='../tipa.txt',proxy_type='http')
        #try:
            #g.go(l[i])
        #except IndexError:
            #break
        #my = g.make_url_absolute(g.doc.select(u'//li[@class="buy animate-block"]/a').attr('href'))
        #print my
        #lin.append(my)
        #i=i+1
    #except(GrabTimeoutError,GrabNetworkError,DataNotFound, GrabConnectionError):
        #print g.config['proxy'],'Change proxy'
        #g.change_proxy()
        #del g
        #i=i-1
        #continue
#lin = list(set(lin))
#links = open('Torgi_Zem1.txt', 'a')
#for item in lin:
    #links.write("%s\n" % item)
#links.close()
#html_string = g.doc.body

#print html_string
#print g.doc.select(u'//h1').text()
##g.doc.save(path)

#options = {'quiet': '','xvfb': '','format': 'png','quality': 1,'encoding': 'UTF-8'}
##toc = {'xsl-style-sheet': 'toc.xsl'}

#config = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')


#imgkit.from_string(html_string, 'images/Avito_.jpg',options=options)




#num = '2589'
##data_image64 = g.doc.json['image64'].replace('data:image/png;base64,','') 
#data_image64 = g.doc.json['image'].split(',')[1] 
#imgdata = base64.b64decode(data_image64)
#im = Image.open(StringIO(imgdata))
##im = Image.open(StringIO(g.doc.body))
#path = 'img/%s.jpg' % num
#im.save(path)
#del im


#in_file = open("tmob_notcleaned.csv", "rb")
#reader = csv.reader(in_file)
#next(reader, None)  # skip the headers
#out_file = open("tmob_cleaned.csv", "wb")
#writer = csv.writer(out_file)
#row = 1
#for row in reader:
    #row[13] = handle_color(row[10])[1].replace(" - ","").strip()
    #row[10] = handle_color(row[10])[0].replace("-","").replace("(","").replace(")","").strip()
    #row[14] = handle_gb(row[10])[1].replace("-","").replace(" ","").replace("GB","").strip()
    #row[10] = handle_gb(row[10])[0].strip()
    #row[9] = handle_oem(row[10])[1].replace("Blackberry","RIM").replace("TMobile","T-Mobile").strip()
    #row[15] = handle_addon(row[10])[1].strip()
    #row[10] = handle_addon(row[10])[0].replace(" by","").replace("FREE","").strip()
    #writer.writerow(row)
#in_file.close()    
#out_file.close()

#dryscrape.start_xvfb()
#sess = dryscrape.Session()
#sess.visit('https://www.avito.ru/dzerzhinskiy/kommercheskaya_nedvizhimost/torgovlya_uslugi_i_dr_1052989728')
#sess.render('screenshot.jpeg')
#source = sess.body()
##print source
#tree = html.fromstring(source)
#opis = tree.xpath('//div[@class="extended-body"]')[0].text_content()
#clearText = re.sub(u"[^а-яА-Я0-9.,\-\s]", "", opis)
#clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText)
#print clearText

#sess = dryscrape.Session()
#url = 'https://bcinform.moscow/arenda-ofisa/id640188/'
#print 'Get Phone...'
#sess.visit(url)
#time.sleep(1)
#punkt = sess.at_xpath('//div[@class="row"]/div[contains(text(),"Данные ")]').text().replace(u'Данные обновлены ','')
#print punkt
#time.sleep(2)
#print sess.url()
#lin = []
#for link in sess.xpath('//p[@class="block-user__show-telephone_number"]/a'):
    #ph = link.text()
    #lin.append(ph)
#lin = list(set(lin))
#phone = ', '.join(lin)
#print phone
#sess.reset()
#print 'Status: ', session.status_code()
#print session.xpath('//div[@class="extended-body"]').text()
#for div in session.xpath("//div[@class='quote']"):
    #print "Quote: ", div.at_xpath(".//span").text()
    #print "Author: ", div.at_xpath(".//small").text()

#if 'linux' in sys.platform:
    ## start xvfb in case no X is running. Make sure xvfb 
    ## is installed, otherwise this won't work!
    #dryscrape.start_xvfb()

#search_term = 'dryscrape'

## set up a web scraping session
#sess = dryscrape.Session(base_url = 'http://bcinform.ru/yaroslavl/office/15_metrov/id30462/')

## we don't need images
##sess.set_attribute('auto_load_images', False)

## visit homepage and search for a term
#sess.visit('/')
#q = sess.at_xpath('//div[@class="extended-body"]')
#print q
##q.set(search_term)
##q.form().submit()

## extract all links
##for link in sess.xpath('//a[@href]'):
    ##print(link['href'])


    
    
    
   