import scrapy
from scrapy.http import HtmlResponse
from les6.jobparser.items import JobparserItem


def parse_salary(salary):
    if 'от' in salary:
        n_from = salary.index('от')
        salary_min = salary[n_from + 2]
        salary_min = int(''.join([x for x in salary_min if x.isdigit()]))
    if 'до' in salary:
        n_to = salary.index('до')
        salary_max = salary[n_to + 2]
        salary_max = int(''.join([x for x in salary_max if x.isdigit()]))
    if 'от' not in salary and 'до' not in salary:
        salary = [''.join([x for x in y if x.isdigit()]) for y in salary]
        salary = [x for x in salary if x != '']
        if len(salary) == 0:
            salary_max = None
            salary_min = None
        elif len(salary) == 1:
            salary_min = int(salary[0])
            salary_max = salary_min
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])
    return salary_min, salary_max


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[contains(@class, '_6AfZ9')]/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]//span/span[contains(@class, '_2Wp8I')]/text()").extract()
        salary_min, salary_max = parse_salary(salary)
        print(salary)
        link = response.url
        site = 'superjob.ru'
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link, site=site)

