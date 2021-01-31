# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    photo_url = scrapy.Field()
    username = scrapy.Field()
    _id = scrapy.Field()
    f_type = scrapy.Field()
    follow_url = scrapy.Field()


