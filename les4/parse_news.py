import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from datetime import date, timedelta

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/87.0.4280.88 Safari/537.36'}
client = MongoClient('127.0.0.1', 27017)
db = client['db_news']
db_news = db.db_news

# Функция для получения текста для xpath
def load_text(url, path):
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    news_text = dom.xpath(path)
    return news_text

# Собираем новости из блока главных новостей в правой части сайта
def parse_lenta():
    url = 'https://lenta.ru/'
    path = "//div[contains(@class, 'b-yellow-box__wrap')]/div[@class='item']"
    news = load_text(url, path)
    items = []
    for news_item in news:
        item0 = dict()
        item0['source'] = 'lenta.ru'
        item0['link'] = url + news_item.xpath("./a/@href")[0]
        item0['name'] = news_item.xpath("./a/text()")[0].replace(u'\xa0', ' ')
        news_date = load_text(item0['link'], "//time[@class='g-date']/@datetime")
        item0['date'] = str(news_date[0][:10])
        items.append(item0)
    save_to_bd(items)

# Собираем 5 основных новостей с картинками-подложками
def parse_mail():
    url = 'https://news.mail.ru/'
    items = []

    #  Получаем главную новость
    path = "//td[@class='daynews__main']"
    main_news = load_text(url, path)
    item0 = dict()
    item0['link'] = main_news[0].xpath(".//a/@href")[0]
    item0['name'] = main_news[0].xpath(".//span[contains(@class, 'js-topnews__notification')]/text()")[0].replace(u'\xa0', ' ')
    main_news_info = load_text(item0['link'], "//div[contains(@class, 'breadcrumbs_article')]")
    item0['source'] = main_news_info[0].xpath(".//span[@class='link__text']/text()")[0]
    main_news_date = main_news_info[0].xpath("//span[contains(@class, 'js-ago')]/@datetime")
    item0['date'] = str(main_news_date[0][:10])
    items.append(item0)


    # Получаем еще четыре новости с картинками-подложками
    path = "//div[@class='daynews__item']"
    news = load_text(url, path)
    for news_item in news:
        item0 = dict()
        item0['link'] = news_item.xpath(".//a/@href")[0]
        item0['name'] = news_item.xpath(".//span[contains(@class, 'photo__title_new_hidden')]/text()")[0].replace(u'\xa0', ' ')
        main_news_info = load_text(item0['link'], "//div[contains(@class, 'breadcrumbs_article')]")
        item0['source'] = main_news_info[0].xpath(".//span[@class='link__text']/text()")[0]
        main_news_date = main_news_info[0].xpath("//span[contains(@class, 'js-ago')]/@datetime")
        item0['date'] = str(main_news_date[0][:10])
        items.append(item0)
    save_to_bd(items)


# Собираем 5 основных новостей с картинками
def parse_yandex():
    url = 'https://yandex.ru/news/'
    items = []

    #  Получаем главную новость (с крупной картинкой)
    path = "//div[@class='mg-card__inner']"
    main_news = load_text(url, path)
    item0 = dict()
    item0['link'] = main_news[0].xpath(".//a/@href")[0]
    item0['name'] = main_news[0].xpath(".//h2[@class='mg-card__title']/text()")[0].replace(u'\xa0', ' ')
    item0['source'] = main_news[0].xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
    item0_time = main_news[0].xpath(".//span[@class='mg-card-source__time']/text()")[0]
    if item0_time.find('вчера') == -1:
        item0['date'] = str(date.today())
    else:
        item0['date'] = str(date.today() - timedelta(days=1))
    items.append(item0)

    # Получаем еще четыре новости с картинками-подложками
    path = "//div[@class='mg-grid__col mg-grid__col_xs_4']"
    news = load_text(url, path)
    for news_item in news[:4]:
        item0 = dict()
        item0['link'] = news_item[0].xpath(".//a/@href")[0]
        item0['name'] = news_item[0].xpath(".//h2[@class='mg-card__title']/text()")[0].replace(u'\xa0', ' ')
        item0['source'] = news_item[0].xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
        news_date = news_item[0].xpath(".//span[@class='mg-card-source__time']/text()")
        news_date = str(news_date[0][:10])
        if news_date.find('вчера') == -1:
            item0['date'] = str(date.today())
        else:
            item0['date'] = str(date.today() - timedelta(days=1))
        items.append(item0)
    save_to_bd(items)

def save_to_bd(items):
    db_news.insert_many(items)


parse_lenta()
parse_mail()
parse_yandex()




