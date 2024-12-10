#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
import re
import time

#client = MongoClient('mongodb://oleg:walter2005@cluster0-shard-00-00-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-01-cfwsy.gcp.mongodb.net:27017,cluster0-shard-00-02-cfwsy.gcp.mongodb.net:27017/landly?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['OpenAddress']
lin = []
for coll in db.list_collection_names():
      print coll
      lin.append(coll)
      #records = db[coll] 
      #tobase = set([])
      #for data in records.find():
            #print data['CITYZIP']
            #print data['NUMBER']
            #print data['STREET']
            #tobase.add(data['CITYZIP'])
      #for m in tobase:  
            #zp = re.sub(u'[^\d]','',m)[:5]
            #print zp
            #lin.append(zp)
links = open('collnames.txt', 'w')
for item in lin:
      links.write("%s\n" % item)
links.close()
time.sleep(1) 
print 'All Done'
client.close()

    
    
    
   