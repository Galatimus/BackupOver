#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab import Grab
import logging
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


g = Grab()
g.go('https://raui.ru/kupit-office-sklad')
print g.response.code
lin = []
for elem in g.doc.select(u'//h2[contains(text(),"Регионы России:")]/following-sibling::table/tbody/tr/td/a'):
    ur = g.make_url_absolute(elem.attr('href'))
    print ur
    lin.append(ur)
links = open('raui_com.txt', 'a')
for item in lin:
    links.write("%s\n" % item)
links.close()