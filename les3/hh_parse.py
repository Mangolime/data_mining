# Переписала код с прошлого ДЗ в виде функций, которые можно запускать из других файлов.

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def parse_salary(sal):
    n = sal.rfind(' ')
    sal_currency = sal[n + 1:]
    sal = sal[:n].replace(' ', '')
    sal = sal.replace('\xa0', '')
    sal_list = sal.split('-')
    if len(sal_list) == 2:
        sal_min, sal_max = map(int, sal_list)
    else:
        if sal_list[0].find('от') == -1:
            sal_max = int(sal_list[0][2:])
            sal_min = None
        else:
            sal_max = None
            sal_min = int(sal_list[0][2:])
    return sal_min, sal_max, sal_currency


def load_hh_data(main_link, part_link):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    params = {'customDomain': 1}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    vacancies_df = pd.DataFrame(columns=['vacancy_id', 'name', 'company', 'salary_min', 'salary_max', 'salary_currency',
                                         'link', 'site'])
    i = 0

    while True:
        link = main_link + part_link
        response = requests.get(link, headers=headers, params=params)
        soup = bs(response.text, 'html.parser')
        if response.ok:
            vacancies_list = soup.findAll('div', {'class': 'vacancy-serp-item HH-VacancySidebarTrigger-Vacancy'})
            for vacancy in vacancies_list:
                name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
                link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                vacancy_id = int(vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['data-vacancy-id'])
                if salary is None:
                    salary_min = None
                    salary_max = None
                    salary_currency = None
                else:
                    salary_min, salary_max, salary_currency = parse_salary(salary.text)
                vacancies_df.loc[i] = {'vacancy_id': vacancy_id, 'name': name, 'company': company, 'salary_min': salary_min,
                                       'salary_max': salary_max, 'salary_currency': salary_currency, 'link': link,
                                       'site': 'hh.ru'}
                i += 1
            next_page = soup.find('a', {'data-qa': 'pager-next'})
            if next_page is None:
                break
            else:
                part_link = next_page['href']
    return vacancies_df


if __name__ == '__main__':
    main_link = 'https://hh.ru'
    part_link = '/vacancies/data-scientist'
    vacancies_df = load_hh_data(main_link, part_link)
    print(vacancies_df)



