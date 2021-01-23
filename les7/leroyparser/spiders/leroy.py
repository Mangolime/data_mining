import scrapy
from scrapy.http import HtmlResponse
from les7.leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        super(LeroySpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{search}/']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@slot='name']")
        for ads in ads_links:
            print(ads)
            yield response.follow(ads, callback=self.parse_ads)

        next_page = response.xpath("//a[contains(@class, 'next-paginator-button')]/@href").extract_first()
        if next_page:
            print('NEW PAGE!!:', next_page)
            yield response.follow(next_page, callback=self.parse)


    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('photos', "//picture[@slot='pictures']//@src")
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('terms', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('definitions', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        yield loader.load_item()

