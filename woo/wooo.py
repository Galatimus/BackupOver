#!/usr/bin/env python
# -*- coding: utf-8 -*-



from woocommerce import API
from grab.spider import Spider,Task
import time
import logging
import re
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Cian_Zem(Spider):
    def prepare(self):
        self.wcapi = API(
            url='http://192.168.1.4/nails/',
            consumer_key='ck_6a1e9fd960a3baa07e83b1ee0c45ba190217b441',
            consumer_secret='cs_9575dadda00ce0e73c83bf85d2932cc00762d21c',    
            wp_api=True,
            version="wc/v3",
            #query_string_auth=True,
            timeout=300
        )        
        self.result= 1
        self.trans= Translator(service_urls=['translate.google.com', 'translate.google.co.kr'], user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0', proxies=None, timeout=300)

    def task_generator(self):
        l= open('id.txt').read().splitlines()
        self.dc = len(l)
        for line in l:
            id_num = [x for x in self.wcapi.get("products/"+line).json()['attributes'] if x['name'] == 'Номер модели'][0]['options'][0]
            yield Task ('item',url='https://www.bornprettystore.com/show.php?keywords='+re.sub(u'[^\d]','',id_num),id_num=id_num,line=line,refresh_cache=True,network_try_count=100)

    def task_item(self, grab, task):
        try:
            sub = str(round(float(grab.doc.select(u'//span[@class="sp0"]/span/span[1]').text().replace('$','')),2)*100)
        except (IndexError,ValueError):
            sub = ''

        projects = {'price': sub,
                    'number':task.id_num, 
                    'prod_id':task.line} 

        yield Task('write',project=projects,grab=grab,refresh_cache=True)
        
    def task_write(self,grab,task):
        print('*'*50)
        print  task.project['price']
        print  task.project['number']
        print  task.project['prod_id']
       
        logger.debug('Tasks - %s' % self.task_queue.size())
        if task.project['price'] <>'':
            r = self.wcapi.put("products/"+task.project['prod_id'], {"regular_price": task.project['price']})
        else:
            r = self.wcapi.put("products/"+task.project['prod_id'], {"stock_status": 'outofstock'})
        r.json()
        print 'Ready - '+str(self.result)+'/'+str(self.dc)+' ****** '+'Status is : '+str(r.status_code)
        print('*'*50)
        self.result =self.result+1
        
    
bot = Cian_Zem(thread_number=1,network_try_limit=1000)
#bot.load_proxylist('../ivan.txt','text_file')
bot.create_grab_instance(timeout=500, connect_timeout=5000)
try:
    bot.run()
except KeyboardInterrupt:
    pass
print('Done!')




#products = wcapi.get("products/categories", params={"per_page":100,"status":"publish"})
#print products.json()[0]['_links']['self']
#with open('Nail.json', 'w') as f:
    #json.dump(wcapi.get("products/1861").json(), f,sort_keys=True, indent = 2, ensure_ascii=False)
    #f.write('\n')

#getAllProducts = wcapi.get('products/categories', params={"per_page":100,"status":"publish"})
#for product in getAllProducts.json():
    #print product['name'],product['id'],product['count']
    ##print product
    
##print(wcapi.get("products/?category=36").json())



#for prod in wcapi.get("products/?category=36",method={"per_page":100,"status":"publish"}).json():
    #print prod['name']

#print  {x[0]: x for x in wcapi.get("products").json()}

#categories = wcapi.get("products/categories").json()

#for attr in categories:
    #print attr['name']

#page=0
#while True:
    #page=page+1
    #r=("products?per_page=%d") % page
    #r=wcapi.get(r)
    #r_text=r.text
    #print r_text
    #time.sleep(2)
    #parsed = json.loads(r_text)
    #file=json.dumps(parsed, indent=4)
    #file_json = json.loads(file)
    #if file_json.len()<10:
        #break

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



