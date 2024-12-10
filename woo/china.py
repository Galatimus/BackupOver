#!/usr/bin/env python
# -*- coding: utf-8 -*-



from woocommerce import API
import pymongo
from pymongo import MongoClient
#from googletrans import Translator
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

wcapi = API(
    url='http://192.168.1.4/newshop/',
    consumer_key='ck_4fd391a4c8535daa2bd075a14e4d675ed87cb596',
    consumer_secret='cs_48323cf094535d46ecfe0c5f23b662f974b806e6',
    #wp_api=True,
    version="wc/v3",
    #query_string_auth=True,
    timeout=300
)
client = MongoClient('mongodb://127.0.0.1:27017', document_class=dict, tz_aware=False, connect=True)
db = client['MyShop']
records = db['Chinavasion']
#trans= Translator(service_urls=['translate.google.com', 'translate.google.co.kr'], user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0', proxies=None, timeout=300)



row = 1
for rec in records.find(no_cursor_timeout=True).batch_size(5):
    time.sleep(1)
    data = {}
    atr = []
    shot = []
    size = len(rec['category'].split(' » '))
    #print rec['category']
    prod = rec['category'].split(' » ')[size-1]
    category =  rec['category'].split(' » ')[size-2]
    if 'Others' in category:
        category =  rec['category'].split(' » ')[size-3]
    else:
        category = category
    clearText = re.sub(u"[^a-zA-Z0-9.,\-\s]", "", category)
    clearText = re.sub(u"[.,\-\s]{3,}", " ", clearText).replace('  ','-').replace(' ','-').lower()        
    print clearText
    categories = wcapi.get("products/categories").json()
    cat_categories = [x for x in categories if x['name'] == clearText]
    #print cat_categories
    parent_id = None
    if not cat_categories:        
        try:
            response = wcapi.post("products/categories", {'name': clearText})
            parent_id = response.json()['id']
        except KeyError:
            row+=1
            continue
        print 'Create new category...is', parent_id
    else:
        parent_id = cat_categories[0]['id']    
        print 'Category...is',parent_id    
    for s in range(len(rec['description_new'])):
        shot.append(rec['description_new'][s])
    shot.append(rec['name'])
    mesto = '. '.join(shot)
    #print mesto
    
    for i in range(len(rec['option'])):
        try:
            name = rec['option'][i].split(':')[0]
        except IndexError:
            name = ''
        try:
            options = rec['option'][i].split(':')[1]
        except IndexError:
            options = ''
        atr.append({'name' : name ,'position' : 0,'visible' : True,'variation' : True,'options': options})
    atr.append({'name' : 'Артикул' ,'position' : 0,'visible' : True,'variation' : True,'options': rec['category_id']})
    newprice = str(round(float(rec['price']),2)*150)
    data = {
        "name": prod,
        "type": "simple",
        "regular_price": newprice,
        "description": mesto,
        "short_description": rec['description'],
        "categories": [{"id": parent_id}],
        #"weight": '50',
        #"length": size.split('-')[0],
        #"width": size.split('-')[0],
        #"height": size.split('-')[0],
        "images": [{"src": rec['images'][i]} for i in range(len(rec['images']))],
        'attributes' : atr,

    }    
    
    time.sleep(1)
    #print(wcapi.post("products", data).json())
    r = wcapi.post("products",data)
    r.json()
    print '********* '+str(row)+'/'+str(records.count())+' ****** '+'Status is : '+str(r.status_code)
    row+=1
client.close()
  




