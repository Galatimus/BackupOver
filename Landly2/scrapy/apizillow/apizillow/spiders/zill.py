#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ..items import ApiItem
from ..items import ItemMessageFilter
import logging 
import re
import xlrd
import time
import random
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.getLogger('scrapy.core.scraper').addFilter(ItemMessageFilter())

#base = 'Murfreesboro'

class ZillowSpider(scrapy.Spider):
    name = 'apizil'
    allowed_domains = ['zillow.com']
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['OpenAddress']
    #records = db[base]
    key = open('keys.txt').read().splitlines()
    colls = open('collnames.txt').read().splitlines()
    
    #for coll in db.list_collection_names():
        #records = db[coll]
    def start_requests(self):
        for p in range(6,len(self.colls)):
            row = 1
            for data in self.db[self.colls[p]].find(): 
                self.log('********* '+str(row)+'/'+str(self.db[self.colls[p]].count())+' ****** '+str(self.colls[p])+' ** '+str(p+1)+'/'+str(len(self.colls)))
                if re.sub(u'[^\d]','',data['CITYZIP']).isdigit() == True:
                    links = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id='+random.choice(list(self.key))+'&address='+data['NUMBER']+'+'+data['STREET']+'&citystatezip='+data['CITYZIP'][:5]
                else:
                    links = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id='+random.choice(list(self.key))+'&address='+data['NUMBER']+'+'+data['STREET']+'&citystatezip='+data['CITYZIP']
                if links:
                    yield scrapy.Request(url=links, callback=self.parse_product,dont_filter=True)
                row+=1

    def parse_product(self, response):         
        items = []
        item = ApiItem()
        item = {}
       
        try:
            item['zpid'] = response.xpath(u'//result/zpid/text()').extract_first()
        except (IndexError,AttributeError,TypeError):
            item['zpid'] = 'Z00000' 
            
        
        try:
            item['address'] = {'street': response.xpath(u'//result/address/street/text()').extract_first(),
                               'zipcode': response.xpath(u'//result/address/zipcode/text()').extract_first(),
                               'city': response.xpath(u'//result/address/city/text()').extract_first(),
                               'state': response.xpath(u'//result/address/state/text()').extract_first(),
                               'country': 'USA',
                               'latitude': response.xpath(u'//result/address/latitude/text()').extract_first(),
                               'longitude': response.xpath(u'//result/address/longitude/text()').extract_first()}
        except (IndexError,AttributeError):
            item['address'] = {}
            
        try:
            item['links'] = {'homedetails': response.xpath(u'//result/links/homedetails/text()').extract_first(),
                            'graphsanddata': response.xpath(u'//result/links/graphsanddata/text()').extract_first(),
                            'mapthishome': response.xpath(u'//result/links/mapthishome/text()').extract_first(),
                            'comparables': response.xpath(u'//result/links/comparables/text()').extract_first()} 
        except (IndexError,AttributeError):
            item['links'] = {}
            
        try:
            item['FIPScounty'] = response.xpath('//result/address/following-sibling::FIPScounty/text()').extract_first()
        except (IndexError,AttributeError):
            item['FIPScounty'] = ''
            
        try:
            item['useCode'] = response.xpath('//result/address/following-sibling::useCode/text()').extract_first()
        except (IndexError,AttributeError):
            item['useCode'] = ''

        try:
            item['lastSoldDate'] = response.xpath('//result/address/following-sibling::lastSoldDate/text()').extract_first()
        except (IndexError,AttributeError):
            item['lastSoldDate'] = ''        


        try:
            item['yearBuilt'] = response.xpath('//result/address/following-sibling::yearBuilt/text()').extract_first()
        except (IndexError,AttributeError):
            item['yearBuilt'] = ''
            
        try:
            item['taxAssessmentYear'] = response.xpath('//result/address/following-sibling::taxAssessmentYear/text()').extract_first()
        except (IndexError,AttributeError):
            item['taxAssessmentYear'] = ''
            
        try:
            item['taxAssessment'] = response.xpath('//result/address/following-sibling::taxAssessment/text()').extract_first()
        except (IndexError,AttributeError):
            item['taxAssessment'] = ''
            
        try:
            item['lotSizeSqFt'] = response.xpath('//result/address/following-sibling::lotSizeSqFt/text()').extract_first()
        except (IndexError,AttributeError):
            item['lotSizeSqFt'] = ''
            
        try:
            item['finishedSqFt'] = response.xpath('//result/address/following-sibling::finishedSqFt/text()').extract_first()
        except (IndexError,AttributeError):
            item['finishedSqFt'] = ''
            
        try:
            item['bathrooms'] = response.xpath('//result/address/following-sibling::bathrooms/text()').extract_first()
        except (IndexError,AttributeError):
            item['bathrooms'] = ''
            
        try:
            item['bedrooms'] = response.xpath('//result/address/following-sibling::bedrooms/text()').extract_first()
        except (IndexError,AttributeError):
            item['bedrooms'] = ''
            
        try:
            item['totalRooms'] = response.xpath('//result/address/following-sibling::totalRooms/text()').extract_first()
        except (IndexError,AttributeError):
            item['totalRooms'] = ''
            
        try:
            item['lastSoldPrice'] = response.xpath('//result/address/following-sibling::lastSoldPrice/text()').extract_first()
        except (IndexError,AttributeError):
            item['lastSoldPrice'] = ''
            
            
        try:
            item['zestimate'] = {'amount': response.xpath(u'//result/zestimate/amount/text()').extract_first(),
                            'last-updated': response.xpath(u'//result/zestimate/last-updated/text()').extract_first(),
                            'valueChange': response.xpath(u'//result/zestimate/valueChange/text()').extract_first(),
                            'valuationRange_low': response.xpath(u'//result/zestimate/valuationRange/low/text()').extract_first(),
                            'valuationRange_high': response.xpath(u'//result/zestimate/valuationRange/high/text()').extract_first()}
        except (IndexError,AttributeError):
            item['zestimate'] = {}
            
        try:
            item['localRealEstate'] = {'region-name': response.xpath(u'//result/localRealEstate/region/@name').extract_first(),
                                'region-ID': response.xpath(u'//result/localRealEstate/region/@id').extract_first(),
                                'region-type': response.xpath(u'//result/localRealEstate/region/@type').extract_first(),
                                'links_overview': response.xpath(u'//result/localRealEstate/region/links/overview/text()').extract_first(),
                                'links_forSale': response.xpath(u'//result/localRealEstate/region/links/forSale/text()').extract_first(),
                                'links_forSaleByOwner': response.xpath(u'//result/localRealEstate/region/links/forSaleByOwner/text()').extract_first()}
        except (IndexError,AttributeError):
            item['localRealEstate'] = {}     
        items.append(item)
        return items
   