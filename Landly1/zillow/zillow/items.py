# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowItem(scrapy.Item):
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
    timeonzillow = scrapy.Field()
    homeFacts = scrapy.Field()
    similarhouses = scrapy.Field()
    rent = scrapy.Field()
    flooring = scrapy.Field()
    fireplace = scrapy.Field()
    stories = scrapy.Field()
    PrivatePool = scrapy.Field()
    ExteriorFeatures = scrapy.Field()
