import scrapy
from scrapy.http import HtmlResponse
from les6.jobparser.items import JobparserItem


def parse_salary(salary):
    salary = [x.replace(' ', '') for x in salary]
    salary = [x.replace('\xa0', '') for x in salary]
    try:
        n_from = salary.index('от')
        salary_min = int(salary[n_from + 1])
    except ValueError:
        salary_min = None
    try:
        n_to = salary.index('до')
        salary_max = int(salary[n_to + 1])
    except ValueError:
        salary_max = None
    return salary_min, salary_max


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python','https://izhevsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&L_save_area=true&area=1&from=cluster_area&showClusters=true']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='vacancy-serp-item__info']//a/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//span/text()").extract()
        salary_min, salary_max = parse_salary(salary)
        link = response.url
        site = 'hh.ru'
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link, site=site)

