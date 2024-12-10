# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import logging 
import re


class TruliaItem(scrapy.Item):
    schools = scrapy.Field()
    MlsId = scrapy.Field()
    images= scrapy.Field()
    street= scrapy.Field()
    zpid = scrapy.Field()
    url = scrapy.Field()
    appliances = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    description = scrapy.Field()
    baths = scrapy.Field()
    beds = scrapy.Field()    
    sqft = scrapy.Field()
    oneyearforecast = scrapy.Field()
    propertyType = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    neighborhood = scrapy.Field()
    totalinteriorlivablearea = scrapy.Field()
    zestimate = scrapy.Field()
    timeontrulia = scrapy.Field()
    homeFacts = scrapy.Field()
    similarhouses = scrapy.Field()
    rent = scrapy.Field()
    flooring = scrapy.Field()
    fireplace = scrapy.Field()
    stories = scrapy.Field()
    PrivatePool = scrapy.Field()
    ExteriorFeatures = scrapy.Field()
    pricehistory = scrapy.Field()
    
class ItemMessageFilter(logging.Filter):
    def filter(self, record):
        # The message that logs the item actually has raw % operators in it,
        # which Scrapy presumably formats later on
        match = re.search(r'(Scraped from %\(src\)s)\n%\(item\)s', record.msg)
        if match:
            # Make the message everything but the item itself
            record.msg = match.group(1)
        # Don't actually want to filter out this record, so always return 1
        return ""

#logging.getLogger('scrapy.core.scraper').addFilter(ItemMessageFilter())

