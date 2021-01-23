# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def price_to_float(price):
    try:
        return float(price.replace(' ', ''))
    except Exception as e:
        print(e)


class LeroyparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_to_float))
    link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    definitions = scrapy.Field()
    terms = scrapy.Field()

