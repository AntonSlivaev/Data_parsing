import main as vacdata
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies']
vacancies_db = db.vacancies

vac_quantity = len(list(vacancies_db.find()))
#print(vac_quantity)

def fill_new(vacancies):
    i = 0
    for vacancy in vacancies:
        if vacancy['site'] == 'hh.ru' and not vacancies_db.find_one ({'id': vacancy['id']}):
            vacancies_db.insert_one(vacancy)
            i += 1
    return i

vacancy = input('Введите интересующую Вас вакансию: ')
pages = int(input('Введите количество страниц с вакансиями (для показа всех страниц введите 0): '))
if pages == 0:
    pages = 100

vacancies = vacdata.execute(vacancy,pages)
i = fill_new(vacancies)

print('Найдены новые вакансии: ',len(list(vacancies_db.find()))  - vac_quantity)

