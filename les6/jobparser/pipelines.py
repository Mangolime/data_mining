# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_2212


    def process_item(self, item, spider):

        # item['new_field'] = 0         # не получится так добавить новое поле, идем в items.py
        # del item['new_field']         # Удаляем ненужное поле в item
        # item['salary_min'] = self.process_salary(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        pass
