from pymongo import MongoClient
from pprint import pprint
from hh_parse import load_hh_data


client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh = db.hh

#  1. Сохранение вакансий в MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh = db.hh
main_link = 'https://hh.ru'
part_link = '/vacancies/data-scientist'
vacancies_df = load_hh_data(main_link, part_link)
for ind, row in vacancies_df.iterrows():
    hh.insert_one(row.to_dict())




#  2. Поиск вакансий с заработной платой больше введённой суммы.
def search_vacancies(salary, no_info):
    for vacancy in hh.find({'$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]}):
        pprint(vacancy)
        print('\n')
    if no_info == 1:
        for vacancy in hh.find({'$and': [{'salary_min': None}, {'salary_max': None}]}):
            pprint(vacancy)
            print('\n')


try:
    salary = float(input("Введите желаемый размер заработной платы: "))
    no_info = int(input("Учитывать ли ваканчии без укаания зарплаты? 0 - нет, 1 - да "))
    search_vacancies(salary, no_info)
except:
    print("Некорректный ввод данных")


#  3. Сохранение новых вакансий в базу
vacancies_df = load_hh_data(main_link, part_link)
for ind, row in vacancies_df.iterrows():
    if hh.count_documents({'vacancy_id': row['vacancy_id']}) == 0:
        hh.insert_one(row.to_dict())
