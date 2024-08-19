"""
есть все данные кроме последней строчки отчета,
ее можно сделать через нейросеть или добавить ручной ввод
"""
import requests
from bs4 import BeautifulSoup
import json
import article_parsing as ap


def save_json(data):
    with open('rbk_data.json', "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_soup(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Проверка на ошибки HTTP
        return BeautifulSoup(r.text, 'lxml')
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


link = 'https://www.rbc.ru/rbcfreenews/66bc16519a79474665ba5fed'
news_data = {}
article_soup = get_soup(link)

if article_soup is None:
    print(f"Не удалось получить данные статьи по ссылке: {link}")

# Переходим на страницу для дальнейшего парсинга
article = article_soup.find('div', class_='article')
if article is None:
    print(f"Статья не найдена по ссылке: {link}")

date = article.find('time', class_='article__header__date')
title = article.find('div', class_='article__header__title')
article_paragraphs = ap.get_article_arr(link)
article_text = '\n'.join(paragraph.strip() for paragraph in article_paragraphs)

# Заполняем полученными данными news_data
source = link.split('://')[1]
if source[:4] == 'www.':
    source = source[4:]
news_data['source'] = source.split('/')[0]
news_data['link'] = link
date = date['content'].split('T')[0]
news_data['date'] = '%s.%s.%s'%(date[-2:], date[5:7], date[:4])
news_data['text'] = article_text.replace('\xa0', '').strip()
if not title:
    title = article.find('div', class_='article__header__note')
news_data['title'] = title.text.strip() if title else 'Без заголовка'

save_json(news_data)
