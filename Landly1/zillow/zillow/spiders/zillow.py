#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ..items import ZillowItem
import logging 
import re
import json,codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com']
    start_urls = ['https://www.zillow.com/'+links.split(',')[0]+'-'+links.split(',')[1].lower()+'/' for links in open('city.txt').read().splitlines()] #self.link = 'https://www.zillow.com/'+page.split(',')[0]+'-'+page.split(',')[1].lower()+'/'
    #start_urls = [links for links in open('city_new.txt').read().splitlines()]
    def parse(self, response): 
        for l in response.xpath('//a[@class="list-card-link list-card-info"]/@href').extract():
            url = response.urljoin(l)
            yield scrapy.Request(url, callback=self.parse_product,dont_filter=True)
        next_page_url = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
        if next_page_url:
            next_page_url =  response.urljoin(next_page_url) 
            yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)

    def parse_product(self, response): 
        items = []
        item = ZillowItem()
        item = {}
        
        temp = {'atAGlanceFacts':[]} 
        
        
        
        
        temp['atAGlanceFacts'].append({'factLabel': 'Year built','factValue': response.xpath('//span[contains(text(),"Year built:")]/following-sibling::span/text()').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'Remodeled year','factValue': response.xpath('//span[contains(text(),"Major remodel year:")]/text()[2]').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'Heating','factValue': response.xpath('//span[contains(text(),"Heating:")]/following-sibling::span/text()').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'Cooling','factValue': response.xpath('//span[contains(text(),"Cooling:")]/following-sibling::span/text()').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'Parking','factValue': response.xpath('//span[contains(text(),"Parking:")]/following-sibling::span/text()').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'lotsize','factValue': response.xpath('//span[contains(text(),"Lot:")]/following-sibling::span/text()').extract_first()})
        temp['atAGlanceFacts'].append({'factLabel': 'Price/sqft','factValue': response.xpath('//span[contains(text(),"Price/sqft:")]/following-sibling::span/text()').extract_first()})        
        
        try:
            item['price'] = response.xpath('//span[@class="ds-value"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['price'] = ''
            
        try:
            item['zestimate'] = response.xpath('//span[@class="ds-estimate-value"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['zestimate'] = ''
            
        try:
            item['similarhouses'] = response.xpath('//h6[contains(text(),"Similar homes")]/following::div[1]/div/a/@href').getall()
        except (IndexError,AttributeError):
            item['similarhouses'] = ''        

        try:
            item['homeFacts'] = temp
        except (IndexError,AttributeError):
            item['homeFacts'] = ''            
            
        try:
            item['flooring'] = response.xpath('//span[contains(text(),"Flooring:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['flooring'] = ''
        try:
            item['fireplace'] = response.xpath('//span[contains(text(),"Fireplace:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['fireplace'] = ''
        try:
            item['stories'] = response.xpath('//span[contains(text(),"Stories:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['stories'] = ''    
        try:
            item['PrivatePool'] = response.xpath('//span[contains(text(),"Private pool:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['PrivatePool'] = ''
        try:
            item['ExteriorFeatures'] = response.xpath('//span[contains(text(),"Exterior features:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['ExteriorFeatures'] = ''    
        try:
            item['timeonzillow'] = response.xpath('//div[contains(text(),"Time on Zillow")]/following-sibling::div/text()').extract_first()
        except (IndexError,AttributeError):
            item['timeonzillow'] = '' 
            
        try:
            try:
                item['neighborhood'] = response.xpath(u'//h4[contains(text(),"Neighborhood:")]/text()').extract_first().split(': ')[1]
            except (IndexError,AttributeError):
                item['neighborhood'] = response.xpath(u'//h4[contains(text(),"Neighborhood:")]/text()').re('Neighborhood:(.*?)<')[0]
        except (IndexError,AttributeError):
            item['neighborhood'] = ''
            
        try:
            try:
                item['rent'] = response.xpath(u'//div[@class="ds-chip"]/div/div[@class="ds-mortgage-row"]/div/span[2]/text()').extract()[0]
            except (IndexError,AttributeError):
                item['rent'] = response.xpath(u'//span[contains(text(),"Estimated monthly cost")]/preceding-sibling::h4/text()').extract()[0]
        except (IndexError,AttributeError):
            item['rent'] = ''
            
        try:
            item['status'] = response.xpath('//span[@class="ds-status-details"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['status'] = ''    
            
        try:
            item['propertyType'] = response.xpath('//span[contains(text(),"Type:")]/following-sibling::span/text()').extract_first()
        except (IndexError,AttributeError):
            item['propertyType'] = ''        
        try:
            try:
                item['sqft'] = response.xpath(u'//h3[@class="ds-bed-bath-living-area-container"]/span[4]/span/text()').extract()[0]
            except (IndexError,AttributeError):
                item['sqft'] = response.xpath(u'//span[contains(text(),"Total interior livable area:")]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['sqft'] = ''
            
        try:
            try:
                item['oneyearforecast'] = response.xpath(u'//script[@data-zrr-shared-data-key="mobileSearchPageStore"]/text()').re('regionForecastRate":"(.*?)"}')[0]
            except (IndexError,AttributeError):
                item['oneyearforecast'] = response.xpath(u'//div[contains(text(),"One Year Forecast")]/following-sibling::div/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['oneyearforecast'] = ''    
        try:
            try:
                item['baths'] = response.xpath(u'//span[contains(text(),"Bathrooms:")]/text()').extract()[1]
            except (IndexError,AttributeError):
                item['baths'] = response.xpath(u'//h3[@class="ds-bed-bath-living-area-container"]/button/span/span[1]/text()').extract()[1]
        except (IndexError,AttributeError):
            item['baths'] = ''
                
        try:
            try:
                item['beds'] = response.xpath(u'//span[contains(text(),"Bedrooms:")]/text()').extract()[1]
            except (IndexError,AttributeError):
                item['beds'] = response.xpath(u'//h3[@class="ds-bed-bath-living-area-container"]/span[1]/span/text()').extract()[1]
        except (IndexError,AttributeError):
            item['beds'] = ''        
        try:
            try:
                item['description'] = response.xpath(u'//div[@class="ds-overview-section"][2]/div/text()').extract_first()
            except (IndexError,AttributeError):
                item['description'] = response.xpath(u'//meta[@name="description"]/@content').extract_first()
        except (IndexError,AttributeError):
            item['description'] = ''        
        
        try:
            item['lat'] = response.xpath('//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').re('latitude":(.*?),')[0]
        except (IndexError,AttributeError):
            item['lat'] = ''
                
        try:
            item['lon'] = response.xpath('//div[@class="ds-data-col ds-white-bg ds-data-col-data-forward"]/script[1]').re('longitude":(.*?)}')[0]
        except (IndexError,AttributeError):
            item['lon'] = ''
            
        try:
            item['MlsId'] = response.xpath('//title/text()').extract()[0].split('#')[1].split(' |')[0]
        except (IndexError,AttributeError):
            item['MlsId'] = ''
        try:
            item['city'] = response.xpath('//h1[@class="ds-address-container"]/span[2]/text()').extract()[1].split(', ')[0]
        except (IndexError,AttributeError):
            item['city'] = ''
            
        try:
            item['state'] = response.xpath('//h1[@class="ds-address-container"]/span[2]/text()').extract()[1].split(', ')[1].split(' ')[0]
        except (IndexError,AttributeError):
            item['state'] = ''
            
        try:
            item['zipcode'] = response.xpath('//h1[@class="ds-address-container"]/span[2]/text()').extract()[1].split(', ')[1].split(' ')[1]
        except (IndexError,AttributeError):
            item['zipcode'] = ''
            
        item['country'] = 'USA'
      
        item['totalinteriorlivablearea'] = item['sqft']
        
        
        item['schools'] = [{'data': {'Grades': response.xpath('//ul[@class="ds-school-info-section"]/li[1]/span[2]/text()').getall(),'Distance': response.xpath('//ul[@class="ds-school-info-section"]/li[2]/span[2]/text()').getall()},'name': response.xpath('//div[@class="ds-nearby-schools-info-section"]/a/text()').getall(),'rating': ','.join(response.xpath('//div[@class="ds-school-rating"]/div/span/text()').getall()).replace(',/','/').split(',')}]
        
        item['images'] = response.xpath('//img[@alt="Property"][contains(@src,"zillow")]/@src').getall()
        item['street'] = response.xpath('//h1[@class="ds-address-container"]/span[1]/text()').extract_first().replace(',','')
        item['zpid'] = 'Z'+re.sub(u'[^\d]','',response.url.split('/')[5])
        item['url'] = response.url
        try:
            item['appliances'] = response.xpath('//span[contains(text(),"Appliances included in sale:")]/text()[2]').extract_first().split(', ')
        except (IndexError,AttributeError):
            item['appliances'] = ''        
        items.append(item)
        #self.log('ALL RESULT IS : %s' % items)
        return items
        #with open('Zillow1.json', 'a') as f:
            #json.dump(items, f,codecs.getwriter('utf-8')(f),sort_keys=True, indent = 4, ensure_ascii=False)
            #f.write(',\n')        

   