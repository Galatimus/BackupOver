#!/usr/bin/env python
# -*- coding: utf-8 -*-



from woocommerce import API
import xlrd
import time
import re
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
 #http://192.168.1.4/tokoo/wp-json/wc/v1/products?consumer_key=ck_872318adc912a4f1a10bbf45803bcf5d5eb9ceef&consumer_secret=cs_764cf540f44967138bb182bb659c1c28497d744f



logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

wcapi = API(
    url='http://192.168.1.4/tokoo/',
    consumer_key='ck_a7b3719ecaf208cac3ee5f7b3edf45587b29999d',
    consumer_secret='cs_6957d786b8716f3a853bf323592de51b08eb97b8',    
    wp_api=True,
    version="wc/v3",
    #verify_ssl = False,
    query_string_auth=True,
    timeout=100
)


rb = xlrd.open_workbook('Bornpretty.xlsx',on_demand=True)
sheet = rb.sheet_by_index(0)
for ak in range(1,sheet.nrows):
    time.sleep(1)
    data = {}
    parent = sheet.cell_value(ak,2).split(' > ')[0].replace(' ','-').strip()
    try:
        child = sheet.cell_value(ak,2).split(' > ')[1].replace(' ','-').strip()
    except IndexError:
        child = ''
    parent_categories = [x for x in wcapi.get("products/categories", params={"per_page": 100}).json() if x['name'] == parent]
    parent_id = None
    if not parent_categories:        
        try:
            response = wcapi.post("products/categories", {'name': parent}).json()
            parent_id = response['id']
            print 'Create new parent category...is', parent_id,'Name is ',parent
        except KeyError:
            print response['message']

            
        
    else:
        parent_id = parent_categories[0]['id']    
        print 'A parent Category is exit ',parent_id,' - ',parent 

    child_categories = [z for z in wcapi.get("products/categories", params={"per_page": 100}).json() if z['name'] == child]
    child_id = None
    #try:
    if not child_categories:#[0]['parent']:        
        try:
            resp = wcapi.post('products/categories/', {'name': child,'parent': parent_id}).json()
            child_id = resp['id']
            print 'Create new child category...is', child_id,'Name is ',child
        except KeyError:
            print resp['message']
            child_id = parent_id
        
    else:
        child_id = child_categories[0]['id']
        #print child_categories[0]['name']
        #print child_categories[0]['parent']
        print 'A child Category is exit',child_id,' - ',child  
    #except IndexError:
        #child_id = parent_id
        
    
    images = sheet.cell_value(ak,3).split('|')
    data = {
        "name": sheet.cell_value(ak,0),
        "type": "simple",
        "regular_price": sheet.cell_value(ak,4),
        "description": sheet.cell_value(ak,1),
        "sku": sheet.cell_value(ak,5),
        "categories": [{"id": child_id}],
        #"weight": '50',
        #"length": size.split('-')[0],
        #"width": size.split('-')[0],
        #"height": size.split('-')[0],
        "images": [{"src": images[i]} for i in range(len(images))],
        'attributes' : [
                            {'name': 'Цвет','position' : 0,'visible' : True,'variation' : True,'options' : sheet.cell_value(ak,6)},
                            {'name': 'Объем','position' : 0,'visible' : True,'variation' : True,'options' : sheet.cell_value(ak,7)},
                            {'name': 'Количество','position' : 0,'visible' : True,'variation' : True,'options' : sheet.cell_value(ak,8)},
                            {'name': 'Тип товара','position' : 0,'visible' : True,'variation' : True,'options' : sheet.cell_value(ak,9)},
                        ],               
    }
    r = wcapi.post("products",data).json()
    print('*'*20)
    print 'Ready - '+str(ak)+'/'+str(sheet.nrows)
    try:
        print 'Status is : '+r['message']+' '+r['code']
    except KeyError:
        print 'Status is : '+r['status']
        print r['id']
    print('*'*20)
    
    #print(wcapi.post("products", data).json())
    
      
    

# Add some attributes

#print('Get attributes')
#attributes = {x['name']: x for x in wcapi.get("products/attributes").json()}

#print('Create attributes if needed')
#for attr in ['Color', 'Size']:
    #if attr not in attributes:
        #r = wcapi.post('products/attributes', {'name': attr})
        #assert r.ok, 'Response not ok for {} attribute'.format(attr)
        #print(r.json())
        #attributes[attr] = r.json()

## Get the color names
#color_names = ['Orange', 'Brown', 'Black', 'White']

#print('Add Color terms if needed')
#color_attr_url = "products/attributes/{}/terms".format(attributes['Color']['id'])
#color_terms = {x['name']: x for x in wcapi.get(color_attr_url).json()}

#for color in color_names:
    #if color in color_terms:
        #continue

    #data = {'name': color}
    #print(wcapi.post(color_attr_url, data).json())

#print('Add Size terms if needed')
#size_attr_url = "products/attributes/{}/terms".format(attributes['Size']['id'])
#size_terms = {x['name']: x for x in wcapi.get(size_attr_url).json()}

#for val in ['Small', 'Medium', 'Large', 'X-Large', 'XX-Large']:
    #if val in size_terms:
        #continue

    #data = {'name': val}
    #print(wcapi.post(size_attr_url, data).json())

## Add some cats

#dimensions = {
    #"Small": {
        #"length": "27",
        #"width": "18"
    #},
    #"Medium": {
        #"length": "28",
        #"width": "20"
    #},
    #"Large": {
        #"length": "29",
        #"width": "22"
    #},
    #"X-Large": {
        #"length": "30",
        #"width": "24"
    #},
    #"XX-Large": {
        #"length": "31",
        #"width": "26"
    #}
#}

## Get attributes
#attributes = {x['name']: x for x in wcapi.get("products/attributes").json()}

## Get attribute terms
#attribute_data = []
#colors = []
#sizes = []
#color_attribute_id = size_attribute_id = print_color_attr_id = None
#for key in ['Color', 'Size']:
    #terms = wcapi.get("products/attributes/{}/terms".format(attributes[key]['id'])).json()
    #terms = [x['name'] for x in terms]
    #attribute_data.append({
        #"id": attributes[key]['id'],
        #"variation": True,
        #"options": terms
    #})
    #if key == 'Color':
        #colors = terms
        #color_attribute_id = attributes[key]['id']
    #elif key == 'Size':
        #sizes = terms
        #size_attribute_id = attributes[key]['id']

## Get the cat categories from WP
#categories = wcapi.get("products/categories?per_page=75").json()
#categories = {x['name']: x for x in categories}
#parent_id = categories['Cat']['id']

#cats = {}
#for key in categories.keys():
    #if categories[key]['parent'] == parent_id:
        #cats[key] = categories[key]

#base_image_url = 'https://placekitten.com/g/'

#resolutions = {
    #'Orange': 525,
    #'Brown': 550,
    #'Black': 575,
    #'White': 600
#}

## Create variations
#variation_data = []
#for color in colors:
    #for size in sizes:
        #variation_data.append({
            #"regular_price": '20.00',
            #"visible": True,
            #"dimensions": dimensions[size],
            #"images": [
                #{
                    #"src": '{}/{}/{}'.format(base_image_url, resolutions[color], resolutions[color]),
                    #"position": 0,
                    #"name": size + ' - ' + color
                #}
            #],
            #"attributes": [
                #{
                    #"id": color_attribute_id,
                    #"option": color
                #},
                #{
                    #"id": size_attribute_id,
                    #"option": size
                #}
            #]
        #})

## Create image data
#image_data = []
#for i in range(len(colors)):
    #image_data.append(
        #{
            #"src": '{}/{}/{}'.format(base_image_url, resolutions[colors[i]], resolutions[colors[i]]),
            #"position": i,
            #"name": size + ' - ' + colors[i]
        #})

#data = {
    #"name": " Cat",
    #"type": "variable",
    #"description": "This is a cat",
    #"short_description": "Cat",
    #"categories": [{"id": cats['Fluffy']['id']}],
    #"attributes": attribute_data,
    #"images": [image_data[0], image_data[1], image_data[2]],
    #"variations": [variation_data[1]]
#}

#r = wcapi.post("products", data)
#response = r.json()

#req = r.request

#print('Main Product Image Id: ', response['images'][0]['id'])
#print('Variant Image Id: ', response['variations'][0]['image'][0]['id'])
#print('These are the same image for some reason.')
#print('Try updating the variant image:')

#var_id = response['variations'][0]['id']
#prod_id = response['id']
#image_id = response['images'][2]['id']

#var_data = {
    #"variations": [
        #{
            #"id": var_id,
            #"images": [image_data[2]]
        #}
    #]
#}

#r = wcapi.put("products/" + str(prod_id), var_data)
#print('Main Product Image Id: ', r.json()['images'][0]['id'])
#print('Variant Image Id: ', r.json()['variations'][0]['image'][0]['id'])
#print('Note that they\'re still the same')

# Uncomment to cleanup and allow for quick reiteration
# print(wcapi.delete('products/{}?force=true'.format(prod_id)).json())

#data = {
    #"name": "Premium Quality",
    #"type": "simple",
    #"regular_price": "21.99",
    #"description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.",
    #"short_description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
    #"categories": [{"name": 'electronics'}],
 
    #"images": [
        #{
            #"src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_front.jpg"
        #},
        #{
            #"src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_back.jpg"
        #}
    #]
#}

#print(wcapi.post("products", data).json())



