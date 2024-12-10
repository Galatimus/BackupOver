#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import xlrd
from os import listdir
import time
from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['OpenAddress']
basedir = "/home/oleg/pars/ready/"
b=1
st= open('city.txt').read().splitlines()
for line in listdir(basedir):
    patch = basedir+line
    mongo = line.replace(u'.xlsx','').replace(u'_new','')
    print mongo+' *** '+str(b)+'/'+str(len(listdir(basedir)))+' ***'
    records = db[mongo.replace(' ','_')]    
    rb = xlrd.open_workbook(patch,on_demand=True)
    sheet = rb.sheet_by_index(0)
    row = 1
    id_seen = set()
    for data in records.find():
        id_seen.add(data['NUMBER']+data['STREET'].replace('+','')+data['CITY'].replace('+','')+data['CITYZIP']+data['STATE'])
    print "<<<<<<<items in base is:>>>>>>>>>>>> %s" % str(len(id_seen))        
    for ak in range(1,sheet.nrows):
        data = {}
        print '********* '+str(row)+'/'+str(sheet.nrows)+' ********** '+mongo+' *** '+str(b)+'/'+str(len(listdir(basedir)))
        number = sheet.cell_value(ak,0)
        street = sheet.cell_value(ak,1).replace(' ','+').replace('++','+')
        zipcode = sheet.cell_value(ak,3)
        city = sheet.cell_value(ak,2).replace(' ','+')
        if street == '':
            continue
        if zipcode == '':
            zipcode = city
        else:
            zipcode = zipcode
        data['NUMBER'] = number
        data['STREET']  = street
        data['CITY'] = city
        data['CITYZIP'] = zipcode
        try:
            data['STATE'] = st[[i for i,x in enumerate(st) if data['CITY'].replace('+',' ') in x][0]].split(',')[1]
        except IndexError:
            data['STATE'] = ''
            
        good = data['NUMBER']+data['STREET'].replace('+','')+data['CITY'].replace('+','')+data['CITYZIP']+data['STATE']
        if good in id_seen:
            print "<<<<<<< error Duplicate: %s " % good+'>>>>>>>'
        else:
            id_seen.add(good)
            records.insert(data)
            print "+++++ "+good+" ADDED TO MONGODB, TOTAL IS: "+str(len(id_seen))+' +++++'
        row+= 1
    b+=1
client.close()
 


    
    
    
   