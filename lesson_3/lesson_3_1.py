import main as vacdata
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies']
vacancies_db = db.vacancies

def fill_db(vacancies):
    for vacancy in vacancies:
        if vacancy['site'] == 'hh.ru':
            vacancies_db.insert_one(vacancy)

vacancy = input('Введите интересующую Вас вакансию: ')
pages = int(input('Введите количество страниц с вакансиями (для показа всех страниц введите 0): '))
if pages == 0:
    pages = 100

vacancies = vacdata.execute(vacancy,pages)
vacancies_db.drop()
fill_db(vacancies)

print('Найдены вакансии: ',len(vacancies))

