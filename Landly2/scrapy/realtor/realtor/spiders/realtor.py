#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ..items import RealtorItem
from ..items import ItemMessageFilter
import logging 
import re
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.getLogger('scrapy.core.scraper').addFilter(ItemMessageFilter())

#base = 'Nashville'

class RealtorSpider(scrapy.Spider):
    name = 'realtor'
    allowed_domains = ['realtor.com']
    #client = MongoClient('mongodb://127.0.0.1:27017')
    #db = client['OpenAddress']
    #records = db[base]
    #row = 1
    #tobase = set([])
    #for data in records.find():
        #tobase.add(data['CITYZIP'])        
    #start_urls = ['https://www.realtor.com/realestateandhomes-search/'+re.sub(u'[^\d]','',m)[:5] for m in tobase]
    start_urls = ['https://www.realtor.com/realestateandhomes-search/'+links for links in open('/home/oleg/pars/zipcodes.txt').read().splitlines()]
    def parse(self, response): 
        for l in response.xpath('//li[@data-similar-home-id="similar-home-card"]/@data-url').extract():
            url = response.urljoin(l)
            #self.log(url)
            yield scrapy.Request(url, callback=self.parse_product,dont_filter=True)
        next_page_url = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url) 
            yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)

    def parse_product(self, response): 
        #self.log('********* '+str(self.row)+'/'+str(len(self.tobase))+' ****** '+str(base))
        items = []
        item = RealtorItem()
        item = {}
    
        temp = {'atAGlanceFacts':[]} 
    
        try:
            built = re.sub(u'[^\d]','',response.xpath('//div[contains(text(),"Built")]/following-sibling::div/text()').extract_first())
        except (IndexError,AttributeError,TypeError):
            built = ''

        remo = ''
        
        try:
            heat = response.xpath('//li[contains(text(),"Heating")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            heat = ''
        try:
            cool = response.xpath('//li[contains(text(),"Cooling")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            cool = ''
        try:
            park = response.xpath('//li[contains(text(),"Parking")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            park = ''
        try:
            try:
                lotsize = response.xpath('//li[contains(text(),"Lot Size Square Feet:")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
            except (IndexError,AttributeError,TypeError):
                lotsize = response.xpath('//li[@data-label="property-meta-lotsize"]/span/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            lotsize = ''
        try:
            prsq = response.xpath('//div[contains(text(),"Price/Sq Ft")]/following-sibling::div/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            prsq = ''
    
        temp['atAGlanceFacts'].append({'factLabel': 'Year built','factValue': built})
        temp['atAGlanceFacts'].append({'factLabel': 'Remodeled year','factValue': re.sub(u'[^\d]','',remo)})
        temp['atAGlanceFacts'].append({'factLabel': 'Heating','factValue': heat})
        temp['atAGlanceFacts'].append({'factLabel': 'Cooling','factValue': cool})
        temp['atAGlanceFacts'].append({'factLabel': 'Parking','factValue': park})
        temp['atAGlanceFacts'].append({'factLabel': 'lotsize','factValue': lotsize})
        temp['atAGlanceFacts'].append({'factLabel': 'Price/sqft','factValue': prsq})        
    
        try:
            item['price'] = response.xpath('//span[@itemprop="price"]/text()').extract_first().strip()
        except (IndexError,AttributeError):
            item['price'] = ''
    

        item['zestimate'] = ''
    
        try:
            item['similarhouses'] = response.xpath('//a[@sh-type="similar_homes"]/text()').getall()
        except (IndexError,AttributeError):
            item['similarhouses'] = ''        
    
        try:
            item['homeFacts'] = temp
        except (IndexError,AttributeError):
            item['homeFacts'] = ''            
    
        try:
            item['flooring'] = response.xpath('//li[contains(text(),"Flooring")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['flooring'] = ''
        try:
            item['fireplace'] = response.xpath('//li[contains(text(),"Fireplace")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['fireplace'] = ''
        try:
            item['stories'] = response.xpath('//li[contains(text(),"Stories")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['stories'] = ''
            
        item['PrivatePool'] = ''
    
        try:
            item['ExteriorFeatures'] = response.xpath('//h4[contains(text(),"Interior Features")]/following-sibling::div[1]/div[1]/ul/li/text()').extract_first()
        except (IndexError,AttributeError):
            item['ExteriorFeatures'] = ''    
        try:
            item['timeonrealtor'] = response.xpath('//div[@class="key-fact-data ellipsis"][contains(text(),"days")]/text()').extract_first()
        except (IndexError,AttributeError):
            item['timeonrealtor'] = '' 
    
        try:
            item['neighborhood'] = response.xpath(u'//li[contains(text(),"Source Neighborhood:")]/text()').extract_first().split(': ')[1].title()
        except (IndexError,AttributeError):
            item['neighborhood'] = ''
    
        try:
            item['rent'] = response.xpath(u'//p[@id="rent_per_month"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['rent'] = ''
    
        try:
            item['status'] = response.xpath('//div[contains(text(),"Status")]/following-sibling::div/text()').extract_first().strip()
        except (IndexError,AttributeError):
            item['status'] = ''    
    
        try:
            item['propertyType'] = response.xpath('//div[contains(text(),"Type")]/following-sibling::div/text()').extract_first()
        except (IndexError,AttributeError):
            item['propertyType'] = ''        
        try:
            try:
                item['sqft'] = response.xpath(u'//meta[@itemprop="floorSize"]/@content').extract_first()
            except (IndexError,AttributeError):
                item['sqft'] = response.xpath(u'//li[@data-label="property-meta-sqft"]/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['sqft'] = ''
    
        item['oneyearforecast'] = ''
        
        item['pricehistory'] = [{'Date': response.xpath('//h3[contains(text(),"Property Price")]/following-sibling::div/div/table/tbody/tr/td[1]/text()').getall(),'Price': response.xpath('//h3[contains(text(),"Property Price")]/following-sibling::div/div/table/tbody/tr/td[3]/text()').getall(),'Event': response.xpath('//h3[contains(text(),"Property Price")]/following-sibling::div/div/table/tbody/tr/td[2]/text()').getall()}]
        
    
        try:
            try:
                item['baths'] = response.xpath(u'//li[@data-label="property-meta-bath"]/span/text()').extract()[0]
            except (IndexError,AttributeError):
                item['baths'] = response.xpath(u'//li[contains(text(),"Total Bathrooms")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['baths'] = ''
    
        try:
            try:
                item['beds'] = response.xpath(u'//li[@data-label="property-meta-beds"]/span/text()').extract()[0]
            except (IndexError,AttributeError):
                item['beds'] = response.xpath(u'//li[contains(text(),"Bedrooms")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['beds'] = ''        
        try:
            item['description'] = response.xpath(u'//p[@id="ldp-detail-romance"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['description'] = ''        
    
        try:
            item['lat'] = response.xpath('//meta[@itemprop="latitude"]/@content').extract_first()
        except (IndexError,AttributeError):
            item['lat'] = ''
    
        try:
            item['lon'] = response.xpath('//meta[@itemprop="longitude"]/@content').extract_first()
        except (IndexError,AttributeError):
            item['lon'] = ''
    
        try:
            item['MlsId'] = response.xpath('//td[@itemprop="productID"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['MlsId'] = ''
        try:
            item['city'] = response.xpath('//span[@itemprop="addressLocality"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['city'] = ''
    
        try:
            item['state'] = response.xpath('//span[@itemprop="addressRegion"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['state'] = ''
    
        try:
            item['zipcode'] = response.xpath('//span[@itemprop="postalCode"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['zipcode'] = ''
    
        item['country'] = 'USA'    
    
        try:
            item['totalinteriorlivablearea'] = response.xpath('//li[contains(text(),"Lot Size Square Feet:")]/text()').extract_first().split(': ')[1].replace('No Data','').replace('None','')
        except (IndexError,AttributeError):
            item['totalinteriorlivablearea'] = ''    
    
        try:
            item['schools'] = [{'data': {'Grades': response.xpath(u'//div[@id="load-more-schools"]/table/tbody/tr/td[3][contains(text(),"–")]/text()').getall(),'Distance': response.xpath(u'//div[@id="load-more-schools"]/table/tbody/tr/td[4][contains(text(),"mi")]/text()').getall()},'name': response.xpath(u'//div[@id="load-more-schools"]/table/tbody/tr/td/a/text()').getall(),'rating': response.xpath(u'//div[@id="load-more-schools"]/table/tbody/tr/td/span[@class="school-rating"]/text()').getall()}]
        except (IndexError,AttributeError):
            item['schools'] = []
    
        try:
            item['images'] = response.xpath('//img[@class="owl-lazy ldp-carousel-img"]/@data-src').getall()
        except (IndexError,AttributeError):
            item['images'] = []
    
        try:
            item['street'] = response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first().replace(',','')
        except (IndexError,AttributeError):
            item['street'] = ''    
        try:
            try:
                item['rpid'] = 'R'+re.sub(u'[^\d]','',response.xpath(u'//div[@class="pull-right js-tracking padding-top sticky-nav-save-btn"]/@data-propertyid').extract_first())
            except (IndexError,AttributeError):
                item['rpid'] = 'R'+re.sub(u'[^\d]','',response.url.split('_M')[1][10:])
        except (IndexError,AttributeError):
            item['rpid'] = ''        
        
        item['url'] = response.url
        try:
            item['appliances'] = response.xpath('//h4[contains(text(),"Interior Features")]/following-sibling::div[1]/div[1]/ul/li/text()').extract_first().split(',')
        except (IndexError,AttributeError):
            item['appliances'] = ''
            
        #self.row+=1
        
        items.append(item)
        return items        

   