#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

db_connect = MongoClient('mongodb://landly:3hIWQti2@mongo-nyc3-01.z.landly.ai:27017/landly')
database_name = 'landly'
database = db_connect[database_name]
collection = database.collection_names(include_system_collections=False)
for collect in collection:
    print collect
    
db = db_connect.pars_records
for document in db.get_collection('pars_records').find():
    print(document)
#with open('Zillow_new.json') as f:
    #data = json.load(f)
#client = MongoClient('mongodb://landly:3hIWQti2@mongo-nyc3-01.z.landly.ai:27017/landly')
#dbname = input("parsing")
#mydb = client[dbname]
#for coll in mydb.list_collection_names():
    #print(coll)
#db = client.get_database('landly')
#records = db.pars_records
#records.insert(data)
#for post in records.find():
    #pprint(post) 


    
    
    
   