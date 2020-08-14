from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
client = MongoClient('localhost', 27017)
db = client['news']

def news_lenta_ru():
    main_link = 'https://lenta.ru/'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)

    dom_lenta = dom.xpath("//a/time")

    news = []

    for item in dom_lenta:
        novelty = {}

        text = item.xpath("../text()")
        date = item.xpath("./@title")
        link = item.xpath("../@href")

        novelty['text'] = text
        novelty['date'] = date[0]
        #novelty['link'] = link
        novelty['source'] = 'lenta.ru'

        if 'https://' in link[0]:
            novelty['link'] = link[0][:link[0].index('?')]
        else:
            novelty['link'] = main_link + link[0]

        news.append(novelty)

    return news

def news_yandex_ru():
    main_link = 'https://yandex.ru'

    response = requests.get(main_link + '/news/', headers=header)
    dom = html.fromstring(response.text)

    dom_yandex = dom.xpath("//td[@class = 'stories-set__item']")
    news = []

    for item in dom_yandex:
        novelty = {}

        text = item.xpath(".//h2[@class='story__title']/a/text()")
        date = item.xpath(".//div[@class='story__date']/text()")
        link = item.xpath(".//h2[@class='story__title']/a/@href")

        novelty['text'] = text[0]
        novelty['link'] = main_link + link[0].split('?')[0]

        if 'вчера\xa0в' in date[0]:
            date = date[0].replace(' вчера\xa0в', '')
            novelty['date'] = str(datetime.date.today() - datetime.timedelta(days=1))
            novelty['source'] = date[:-6]
        else:
            novelty['date'] = str(datetime.date.today())
            novelty['source'] = date[0][:-6]

        news.append(novelty)
    return news


def fill_db(source, news):
    if source == 'lenta':
        db.lenta.insert_many(news)
    elif source == 'yandex':
        db.yandex.insert_many(news)


fill_db('lenta', news_lenta_ru())
fill_db('yandex', news_yandex_ru())

print('новости lenta.ru: ')
for novelty in db.news_lenta_ru.find({}, {'_id': 0}):
    pprint(novelty)
