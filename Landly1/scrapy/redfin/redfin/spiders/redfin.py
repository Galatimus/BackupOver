#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ..items import RedfinItem
from ..items import ItemMessageFilter
import logging 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.getLogger('scrapy.core.scraper').addFilter(ItemMessageFilter())



class RedfinSpider(scrapy.Spider):
    name = 'redfin'
    allowed_domains = ['redfin.com']
    start_urls = ['https://www.redfin.com/zipcode/'+links for links in open('/home/oleg/pars/zipcodes.txt').read().splitlines()] 
    #start_urls = ['https://www.redfin.com/zipcode/46237']
    def parse(self, response): 
        for l in response.xpath('//div[@class="homecardv2"]/following-sibling::a/@href').extract():
            url = response.urljoin(l)
            #self.log(url)
            yield scrapy.Request(url, callback=self.parse_product,dont_filter=True)
        next_page_url = response.xpath('//a[@class="selected goToPage"]/following-sibling::a[1]/@href').extract_first()
        if next_page_url:
            next_page_url =  response.urljoin(next_page_url) 
            yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)

    def parse_product(self, response): 
        items = []
        item = RedfinItem()
        item = {}
        
        temp = {'atAGlanceFacts':[]} 
        
        try:
            built = re.sub(u'[^\d]','',response.xpath('//span[contains(text(),"Built")]/following-sibling::span/text()').extract_first())
        except (IndexError,AttributeError,TypeError):
            built = ''
        try:
            remo = response.xpath('//span[contains(text(),"Year Renovated")]/following-sibling::div/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            remo = ''
        try:
            heat = response.xpath('//h3[contains(text(),"Heating & Cooling")]/following-sibling::li[2]/span/span/text()').extract_first().replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            heat = ''
        try:
            cool = response.xpath('//h3[contains(text(),"Heating & Cooling")]/following-sibling::li[1]/span/span/text()').extract_first().replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            cool = ''
        try:
            park = response.xpath('//h3[contains(text(),"Garage & Parking")]/following-sibling::li/span/text()').extract_first().replace('No Data','').replace('None','')
        except (IndexError,AttributeError,TypeError):
            park = ''
        try:
            try:
                lotsize = response.xpath('//span[contains(text(),"Lot Size")]/following-sibling::div/text()').extract_first()
            except (IndexError,AttributeError,TypeError):
                lotsize = response.xpath('//span[contains(text(),"Lot Size")]/following-sibling::span/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            lotsize = ''
        try:
            prsq = response.xpath('//div[@data-rf-test-id="abp-priceperft"]/text()').extract_first()
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
            item['price'] = response.xpath('//div[@class="info-block price"]/div/div/span[2]/text()').extract_first()
        except (IndexError,AttributeError):
            item['price'] = ''
            
        #try:
            #item['zestimate'] = response.xpath('//span[@class="ds-estimate-value"]/text()').extract_first()
        #except (IndexError,AttributeError):
        item['zestimate'] = ''
            
        try:
            item['similarhouses'] = response.xpath('//div[@class="similars"]/div/div/div/a/@title').getall()
        except (IndexError,AttributeError):
            item['similarhouses'] = ''        

        try:
            item['homeFacts'] = temp
        except (IndexError,AttributeError):
            item['homeFacts'] = ''            
            
        try:
            item['flooring'] = response.xpath('//span[contains(text(),"Flooring")]/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['flooring'] = ''
        try:
            item['fireplace'] = response.xpath('//span[contains(text(),"Fireplace")]/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['fireplace'] = ''
        try:
            item['stories'] = response.xpath('//span[contains(text(),"Stories")]/following-sibling::span/text()').extract_first()
        except (IndexError,AttributeError):
            item['stories'] = ''    
        #try:
            #item['PrivatePool'] = response.xpath('//span[contains(text(),"Private pool:")]/text()[2]').extract_first()
        #except (IndexError,AttributeError):
        item['PrivatePool'] = ''
        
        try:
            item['ExteriorFeatures'] = response.xpath('//h3[contains(text(),"Interior Features")]/following-sibling::li[2]/span/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['ExteriorFeatures'] = ''    
        try:
            item['timeonredfin'] = response.xpath('//span[contains(text(),"On Redfin:")]/following-sibling::span[contains(text(),"days")]/text()').extract_first()
        except (IndexError,AttributeError):
            item['timeonredfin'] = '' 
            
        try:
            try:
                item['neighborhood'] = response.xpath(u'//h3[@class="h3 walkscore-header"]/text()[2]').extract_first()
            except (IndexError,AttributeError):
                item['neighborhood'] = response.xpath(u'//h3[@class="h3 walkscore-header"]/text()[2]').extract_first()
        except (IndexError,AttributeError):
            item['neighborhood'] = ''
            
            
        item['pricehistory'] = [{'Date': response.xpath('//tr[contains(@id,"propertyHistory")]/td[1]/text()').getall(),'Price': response.xpath('//tr[contains(@id,"propertyHistory")]/td[3]/text()').getall(),'Event': response.xpath('//tr[contains(@id,"propertyHistory")]/td[2]/div[1]/text()').getall()}]
      
        item['rent'] = ''
            
        try:
            item['status'] = response.xpath('//span[@class="status-container"]/span/span[2]/div/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['status'] = ''    
            
        try:
            item['propertyType'] = response.xpath('//span[contains(text(),"Style")]/following-sibling::span/text()').extract_first()
        except (IndexError,AttributeError):
            item['propertyType'] = ''        
        try:
            try:
                item['sqft'] = response.xpath(u'//div[@class="info-block sqft"]/span/span[@class="statsValue"]/text()').extract_first()
            except (IndexError,AttributeError):
                item['sqft'] = response.xpath(u'//span[contains(text(),"Total Sq. Ft.")]/following-sibling::span/text()').extract_first()
        except (IndexError,AttributeError):
            item['sqft'] = ''
            
        #try:
            #try:
                #item['oneyearforecast'] = response.xpath(u'//script[@data-zrr-shared-data-key="mobileSearchPageStore"]/text()').re('regionForecastRate":"(.*?)"}')[0]
            #except (IndexError,AttributeError):
                #item['oneyearforecast'] = response.xpath(u'//div[contains(text(),"One Year Forecast")]/following-sibling::div/span/text()').extract_first()
        #except (IndexError,AttributeError):
        item['oneyearforecast'] = ''
        
        try:
            try:
                item['baths'] = response.xpath(u'//div[@data-rf-test-id="abp-baths"]/div/text()').extract()[1]
            except (IndexError,AttributeError):
                item['baths'] = response.xpath(u'//span[contains(text(),"Baths")]/following-sibling::span/text()').extract()[1]
        except (IndexError,AttributeError):
            item['baths'] = ''
                
        try:
            try:
                item['beds'] = response.xpath(u'//div[@data-rf-test-id="abp-beds"]/div/text()').extract()[1]
            except (IndexError,AttributeError):
                item['beds'] = response.xpath(u'//span[contains(text(),"Beds")]/following-sibling::span/text()').extract()[1]
        except (IndexError,AttributeError):
            item['beds'] = ''        
        try:
            item['description'] = response.xpath(u'//div[@class="sectionContent"]/div/p/span/text()').extract_first()
        except (IndexError,AttributeError):
            item['description'] = ''        
        
        try:
            item['lat'] = response.xpath('//meta[@name="geo.position"]/@content').extract_first().split(';')[0]
        except (IndexError,AttributeError):
            item['lat'] = ''
                
        try:
            item['lon'] = response.xpath('//meta[@name="geo.position"]/@content').extract_first().split(';')[1]
        except (IndexError,AttributeError):
            item['lon'] = ''
            
        try:
            item['MlsId'] = response.xpath('//title/text()').extract_first().split('MLS# ')[1].split(' | ')[0]
        except (IndexError,AttributeError):
            item['MlsId'] = ''
        try:
            item['city'] = response.xpath('//span[@class="locality"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['city'] = ''
            
        try:
            item['state'] = response.xpath('//span[@class="region"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['state'] = ''
            
        try:
            item['zipcode'] = response.xpath('//span[@class="postal-code"]/text()').extract()[0]
        except (IndexError,AttributeError):
            item['zipcode'] = ''
            
        item['country'] = 'USA'
        
        
        try:
            item['totalinteriorlivablearea'] = response.xpath('//meta[@name="twitter:text:sqft"]/@content').extract_first()
        except (IndexError,AttributeError):
            item['totalinteriorlivablearea'] = ''        
      

        
        try:
            item['schools'] = [{'data': {'Grades': response.xpath('//div[@data-rf-test-name="school-name"]/following-sibling::div[1]/text()[3]').getall(),'Distance': response.xpath('//td[@class="distance-col"][contains(text(),"mi")]/text()').getall()},'name': response.xpath('//div[@data-rf-test-name="school-name"]/text()').getall(),'rating': response.xpath('//div[@class="rating"]/text()').getall()}]
        except (IndexError,AttributeError):
            item['schools'] = []
        
        try:
            item['images'] = response.xpath('//meta[contains(@name,"twitter:image:photo")]/@content').getall()
        except (IndexError,AttributeError):
            item['images'] = []
        
        try:
            item['street'] = response.xpath('//span[@class="street-address"]/text()').extract_first()
        except (IndexError,AttributeError):
            item['street'] = ""
            
        item['fpid'] = 'RF'+response.url.split('home/')[1]
        item['url'] = response.url
        try:
            item['appliances'] = response.xpath('//h3[contains(text(),"Interior Features")]/following-sibling::li[1]/span/span/text()').extract_first().split(', ')
        except (IndexError,AttributeError):
            item['appliances'] = ''
            
        #self.log(item['pricehistory'])
        items.append(item)
        return items
       

   