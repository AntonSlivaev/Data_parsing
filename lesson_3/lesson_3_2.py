from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies']
vacancies_db = db.vacancies

def great_salary(salary):
    i= True
    vacancies_list = vacancies_db.find({'$or': [{'salary_min': {'$gte': salary}, 'salary_max': {'$gte': salary}}]},
                              {'title': 1, 'employer': 1, 'salary_min': 1, 'salary_max': 1, 'salary_currency': 1,
                               'link': 1, '_id': 0}).sort('salary_min')

    print('Подходящие вакансии: ')
    for vacancy in vacancies_list:
        pprint(vacancy)
        i = False
    if i:
        print('запрашиваемых вакансий к сожалению нет ')

salary = int(input('Введите минимальную зарплату:  '))
great_salary(salary)