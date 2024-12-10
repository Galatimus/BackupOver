#!/usr/bin/env python
# -*- coding: utf-8 -*-



from woocommerce import API
import xlrd
import time
from mtranslate import translate
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print translate("Bonjour","ru","auto")

wcapi = API(
    url='http://192.168.1.5/waltershop/',
    #consumer_key='ck_7b34901f108633ef879f2d681a19e6f15a8003b1',
    #consumer_secret='cs_0fe15cc3efe2f8e407d00df7ab381e5000e7cad7',
    consumer_key='ck_d78d195a3ed2e274a020f4e666cbc3a2497e944c',
    consumer_secret='cs_04feea2748eee07fa4028224a3ee85a0f2d75311',    
    #wp_api=True,
    version="wc/v3",
    #query_string_auth=True,
    timeout=300
)


# Add some categories

# Create a parent category "Cat" if doesn't exists
# Then get id
categories = wcapi.get("products/categories").json()
cat_categories = [x for x in categories if x['name'] == 'lamoda']

print cat_categories

parent_id = None
#if not cat_categories:
    #response = wcapi.post("products/categories", {'name': 'electronics'})
    #assert response.ok, "Response not ok"
    #parent_id = response.json()['id']
    #print parent_id
#else:
    #assert len(cat_categories) == 1, "More than one cat category for some reason"
parent_id = cat_categories[0]['id']
print parent_id

rb = xlrd.open_workbook('Lamoda_test.xlsx',on_demand=True)
sheet = rb.sheet_by_index(0)
row = 1
for ak in range(1,sheet.nrows):
    time.sleep(1)
    data = {}
    name = sheet.cell_value(ak,0)
    price = re.sub(u'[^\d]','',sheet.cell_value(ak,7))
    description = sheet.cell_value(ak,2)
    short_description = sheet.cell_value(ak,1)
    images = sheet.cell_value(ak,6).split(', ')
    size = sheet.cell_value(ak,13)
    art = sheet.cell_value(ak,5)
    color = sheet.cell_value(ak,9)
    sz = sheet.cell_value(ak,3).split(', ')
    sez = sheet.cell_value(ak,16)
    strana = sheet.cell_value(ak,20)
    image_data = []
    for i in range(len(images)):
        image_data.append({"src": images[i]})
        
    #print image_data
    data = {
        "name": name,
        "type": "simple",
        "regular_price": price,
        "description": description,
        "short_description": short_description,
        "categories": [{"id": parent_id}],
        #"weight": '50',
        #"length": size.split('-')[0],
        #"width": size.split('-')[0],
        #"height": size.split('-')[0],
        "images": [image_data[0],image_data[1],image_data[2]],
        'attributes' : [
                            {'name' : 'Артикул','position' : 0,'visible' : True,'variation' : True,'options' : art},
                            {'name': 'Цвет','position' : 0,'visible' : True,'variation' : True,'options' : color},
                            {'name': 'Размеры','position' : 0,'visible' : True,'variation' : True,'options' : sz},
                            {'name': 'Сезон','position' : 0,'visible' : True,'variation' : True,'options' : sez},
                            {'name': 'Страна производства','position' : 0,'visible' : True,'variation' : True,'options' : strana},
                        ],               
    }

    print(wcapi.post("products", data).json())
    
      
    

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



