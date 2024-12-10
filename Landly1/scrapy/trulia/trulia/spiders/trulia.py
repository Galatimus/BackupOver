#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ..items import TruliaItem
from ..items import ItemMessageFilter
import logging 
import re
import json,codecs
from geopy.distance import geodesic
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.getLogger('scrapy.core.scraper').addFilter(ItemMessageFilter())





class TruliaSpider(scrapy.Spider):
    name = 'trulia'
    allowed_domains = ['trulia.com']
    #start_urls = ['https://www.zillow.com/'+links.split(',')[0]+'-'+links.split(',')[1].lower()+'/' for links in open('city.txt').read().splitlines()] #self.link = 'https://www.zillow.com/'+page.split(',')[0]+'-'+page.split(',')[1].lower()+'/'
    start_urls = ['https://www.trulia.com/'+links.split(',')[1]+'/'+links.split(',')[0].replace(' ','_')+'/' for links in open('/home/oleg/pars/city.txt').read().splitlines()]
    def parse(self, response): 
        for l in response.xpath('//div[@data-testid="home-card-sale"]/a/@href').extract():
            url = response.urljoin(l)
            yield scrapy.Request(url, callback=self.parse_product,dont_filter=True)
        next_page_url = response.xpath('//a[@aria-label="Next Page"]/@href').extract_first()
        if next_page_url:
            next_page_url =  response.urljoin(next_page_url) 
            yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)

    def parse_product(self, response): 
        pass
        items = []
        item = TruliaItem()
        item = {}
        
        temp = {'atAGlanceFacts':[]} 
        
        try:
            built = re.sub(u'[^\d]','',response.xpath('//li[contains(text(),"Built in")]/text()').extract_first())
        except (IndexError,AttributeError,TypeError):
            built = ''
        try:
            remo = response.xpath('//li[contains(text(),"Year Updated")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError,TypeError):
            remo = ''
        try:
            heat = response.xpath('//li[contains(text(),"Heating")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError,TypeError):
            heat = ''
        try:
            cool = response.xpath('//li[contains(text(),"Cooling System")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError,TypeError):
            cool = ''
        try:
            park = response.xpath('//li[contains(text(),"Parking")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError,TypeError):
            park = ''
        try:
            lotsize = response.xpath('//li[contains(text(),"Lot Size:")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError,TypeError):
            lotsize = ''
        try:
            prsq = response.xpath('//li[contains(text(),"/sqft")]/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            prsq = ''
        
        temp['atAGlanceFacts'].append({'factLabel': 'Year built','factValue': built})
        temp['atAGlanceFacts'].append({'factLabel': 'Remodeled year','factValue': remo})
        temp['atAGlanceFacts'].append({'factLabel': 'Heating','factValue': heat})
        temp['atAGlanceFacts'].append({'factLabel': 'Cooling','factValue': cool})
        temp['atAGlanceFacts'].append({'factLabel': 'Parking','factValue': park})
        temp['atAGlanceFacts'].append({'factLabel': 'lotsize','factValue': lotsize})
        temp['atAGlanceFacts'].append({'factLabel': 'Price/sqft','factValue': prsq})        
        
        try:
            item['price'] = response.xpath('//h3[@data-testid="on-market-price-details"]/div/text()').extract_first()
        except (IndexError,AttributeError):
            item['price'] = ''
            
            
        item['zestimate'] = ''
            
        try:
            item['similarhouses'] = []
            for s in json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['similarHomes']['homes']:
                item['similarhouses'].append(s['location']['fullLocation'])
        except (IndexError,KeyError,TypeError):
            item['similarhouses'] = []        

        try:
            item['homeFacts'] = temp
        except (IndexError,AttributeError):
            item['homeFacts'] = ''
            
        item['flooring'] = ''
        
        try:
            item['fireplace'] = response.xpath('//li[contains(text(),"Fireplace")]/text()').extract_first().replace('Fireplace','yes')
        except (IndexError,AttributeError):
            item['fireplace'] = ''
            
        try:
            item['stories'] = response.xpath('//li[contains(text(),"Stories:")]/text()').extract_first().split(': ')[1]
        except (IndexError,AttributeError):
            item['stories'] = ''
            
        try:
            item['PrivatePool'] = response.xpath('//li[contains(text(),"Pool")]/text()').extract_first().replace('Pool','yes')
        except (IndexError,AttributeError):
            item['PrivatePool'] = ''
            
        try:
            item['ExteriorFeatures'] = response.xpath('//h3[contains(text(),"Interior Features")]/following-sibling::li/text()').extract_first()
        except (IndexError,AttributeError):
            item['ExteriorFeatures'] = ''
            
        try:
            item['timeontrulia'] = response.xpath('//li[contains(text(),"Days on Trulia")]/text()').extract_first().replace(' on Trulia','')
        except (IndexError,AttributeError):
            item['timeontrulia'] = ''
            
        try:
            try:
                item['neighborhood'] = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['_page']['tracking']['listingNeighborhood']
            except (IndexError,KeyError,TypeError):
                item['neighborhood'] = response.xpath('//script[@id="__NEXT_DATA__"]/text()').re('neighborhood":"(.*?)"')[0]
        except IndexError:
            item['neighborhood'] = ''    

        item['rent'] = ''
            
        try:
            item['status'] = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['_page']['tracking']['listingStatus']
        except (IndexError,KeyError,TypeError):
            item['status'] = ''    
            
        try:
            item['propertyType'] = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['_page']['tracking']['propertyType']
        except (IndexError,KeyError,TypeError):
            item['propertyType'] = ''        
        try:
            item['sqft'] = response.xpath('//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"sqft")]/text()').extract_first()
        except (IndexError,AttributeError):
            item['sqft'] = ''
            
        item['oneyearforecast'] = ''    
        try:
            item['baths'] = response.xpath(u'//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"Baths")]/text()').extract_first()
        except (IndexError,AttributeError):
            item['baths'] = ''
                
        try:
            item['beds'] = response.xpath(u'//div[@class="MediaBlock__MediaContent-ldzu2c-1 bumWFt"][contains(text(),"Beds")]/text()').extract_first()
        except (IndexError,AttributeError):
            item['beds'] = ''        
        try:
            item['description'] = response.xpath('//div[@data-testid="home-description-text-description-text"]/div/p/text()').extract_first()
        except (IndexError,AttributeError):
            item['description'] = ''        
        
        try:
            item['lat'] = str(json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['location']['coordinates']['latitude'])
        except (IndexError,KeyError,TypeError):
            item['lat'] = ''
                
        try:
            item['lon'] = str(json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['location']['coordinates']['longitude'])
        except (IndexError,KeyError,TypeError):
            item['lon'] = ''
            
        try:
            item['MlsId'] = response.xpath('//title/text()').extract_first().split('MLS# ')[1].split(' - ')[0].replace(' | Trulia','')
        except (IndexError,AttributeError):
            item['MlsId'] = ''
        try:
            item['city'] = json.loads(response.xpath('//script[@data-testid="hdp-seo-residence-schema"]/text()').extract_first())['address']['addressLocality']
        except (IndexError,KeyError,TypeError):
            item['city'] = ''
            
        try:
            item['state'] = json.loads(response.xpath('//script[@data-testid="hdp-seo-residence-schema"]/text()').extract_first())['address']['addressRegion']
        except (IndexError,KeyError,TypeError):
            item['state'] = ''
            
        try:
            item['zipcode'] = json.loads(response.xpath('//script[@data-testid="hdp-seo-residence-schema"]/text()').extract_first())['address']['postalCode']
        except (IndexError,KeyError,TypeError):
            item['zipcode'] = ''
            
        item['country'] = 'USA'
        
        item['pricehistory'] = [{'Date': response.xpath('//tbody[contains(@data-testid,"price-history-event")]/tr[1]/td[1]/span/text()').getall(),'Price': response.xpath('//tbody[contains(@data-testid,"price-history-event")]/tr[1]/td[2]/span/text()').getall(),'Event': response.xpath('//tbody[contains(@data-testid,"price-history-event")]/tr[1]/td[3]/div/div/span/text()').getall()}]
        
      
        item['totalinteriorlivablearea'] = item['sqft']
        
        try:
            name = []
            grad = []
            dis = []
            rat = []
            origin = (item['lat'], item['lon'])
            for n in json.loads(response.xpath(u'//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['assignedSchools']['schools']:
                name.append(n['name'])
            for gr in json.loads(response.xpath(u'//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['assignedSchools']['schools']:
                grad.append(gr['gradesRange'])
            for di in json.loads(response.xpath(u'//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['assignedSchools']['schools']:
                dist = (di['latitude'], di['longitude'])
                dis.append(str(round(geodesic(origin, dist).miles,2))+'mi')
            for rt in json.loads(response.xpath(u'//script[@id="__NEXT_DATA__"]/text()').extract_first())['props']['homeDetails']['assignedSchools']['schools']:   
                rat.append(str(rt['providerRating']['rating'])+'/'+str(rt['providerRating']['maxRating'])) 
        except (IndexError,KeyError,TypeError):
            name = []
            grad = []
            dis = []
            rat = []       
        
        item['schools'] = [{'data': {'Grades': grad,'Distance': dis},'name': name,'rating': rat}]
        
        item['images'] = response.xpath('//script[@id="__NEXT_DATA__"]/text()').re('largeSrc":"(.*?)"')
        
        item['street'] = response.xpath('//title/text()').extract_first().split(', ')[0]
        item['tpid'] = 'T'+re.sub(u'[^\d]','',response.xpath('//script[@id="__NEXT_DATA__"]/text()').re('listingID(.*?)maloneID')[0])
        item['url'] = response.url
        
        try:
            item['appliances'] = response.xpath('//li[contains(text(),"Floors")]/text()').extract_first().split(': ')[1].split(', ')
        except (IndexError,AttributeError):
            item['appliances'] = ''
            
        #self.log(item['pricehistory'])
        
        items.append(item)
        return items
        

   