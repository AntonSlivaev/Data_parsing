from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd
#import webbrowser
#from fake_useragent import UserAgent


def request_hh(main_link, params):
    response = requests.get(main_link, params=params, headers=headers)
    soup = bs(response.text, 'lxml')
    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    next_page = soup.find('a', {'data-qa': 'pager-next'})
    return vacancies_block, next_page

def salary_parsing(salary):
    salary_currency = re.findall('\D*', salary)[-2][1:]
    if 'договор' in salary:
        salary_min, salary_max, salary_currency = None, None, None
    elif '-' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('-')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('-')[1])))
    elif '-' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('-')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('-')[1])))
    elif 'от'  in salary:
        salary_min = int(''.join(re.findall('\d', salary)))
        salary_max = None
    elif 'до' in salary:
        salary_min = None
        salary_max = int(''.join(re.findall('\d', salary)))
    else:
        salary_min, salary_max, salary_currency = None, None, None
    return salary_min, salary_max, salary_currency

def hh_scraping(vacancies_block):
    vacancies_list = vacancies_block.findChildren(recursive=False)

    for vacancy in vacancies_list:
        vacancy_data = {}

        title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        if title:
            vacancy_data['title'] = title.getText()
        else:
            continue

        link = title['href']
        vacancy_data['link'] = link[:link.index('?')]

        employer = vacancy.find('a', {'data-qa' : 'vacancy-serp__vacancy-employer' })
        if employer:
            employer = employer.getText()
            if employer[0] == ' ':
                employer = employer[1:]
            vacancy_data['employer'] = employer

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary:
            salary = salary.getText()
            salary_min, salary_max, salary_currency = salary_parsing(salary)
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
        else:
            vacancy_data['salary_min'], vacancy_data['salary_max'], vacancy_data['salary_currency'] = None, None, None
        vacancy_data['site'] = 'hh.ru'

        vacancies.append(vacancy_data)
    return vacancies

def execute (vacancy, pages ):
    global vacancies

    i = 0
    next_page = True
    while next_page and i + 1 <=pages:
        params = {'text': vacancy, 'page': i}
        vacancies_block, next_page = request_hh(main_link, params)
        vacancies = hh_scraping(vacancies_block)
        i += 1
    return vacancies

headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit /' \
                          '537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
#params = {'page' : '0'}
main_link = 'https://hh.ru/search/vacancy/'
#params = {'text':vacancy}
#UserAgent().chrome
vacancies = []


if __name__ == '__main__':
    vacancy = input('Введите интересующую Вас вакансию: ')
    pages = int(input('Введите количество страниц с вакансиями (для показа всех страниц введите 0): '))
    if pages == 0:
        pages = 100

    execute(vacancy, pages)
    pprint(vacancies)
    print('Найдено вакансий: ', len(vacancies))

