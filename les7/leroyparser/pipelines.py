# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from scrapy.utils.python import to_bytes
import hashlib


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["name"]}/{image_guid}.jpg'


class LeroyparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy
        self.collection = self.mongo_base['leroy_goods']

    def process_item(self, item, spider):
        #  Преобразуем поля terms и definitions в словарь.
        characteristics = {}
        for i in range(len(item['definitions'])):
            definition = item['definitions'][i].strip()
            characteristics[item['terms'][i]] = definition
        item._values['characteristics'] = characteristics
        item._values.__delitem__('terms')
        item._values.__delitem__('definitions')
        self.collection.insert_one(item)
        return item
