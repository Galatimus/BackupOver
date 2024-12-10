#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import join as joinpath
import sys
reload(sys)
sys.setdefaultencoding('cp866')

b = 1
basedir = u"temp"

for line in listdir(basedir):
       print line.replace(u'.xlsx','')
       b += 1
       
       
#a= u'НГС.НЕДВИЖИМОСТЬ'
#print a.lower().strip()