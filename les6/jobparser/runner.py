from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from les6.jobparser.spiders.hhru import HhruSpider
from les6.jobparser.spiders.sjru import SjruSpider
from les6.jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()


