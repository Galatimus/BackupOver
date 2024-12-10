# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
import pymongo
import logging

class MongoPipeline(object):

    collection_name = 'zillow_api'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.id_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        for item in self.db[self.collection_name].find():
            self.id_seen.add(item["zpid"])
        logging.debug("<<<<<<<items in base is:>>>>>>>>>>>> %s" % str(len(self.id_seen)))

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        if item['zpid'] in self.id_seen:
            logging.debug("<<<<<<< Duplicate item : %s " % item['zpid']+'>>>>>>>')
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.id_seen.add(item['zpid'])        
            self.db[self.collection_name].insert(dict(item))
            logging.debug("+++++ "+item['zpid']+" ADDED TO MONGODB, TOTAL IS: "+str(len(self.id_seen))+' +++++')
            return item
