import requests
from bs4 import BeautifulSoup
import json
import article_parsing as ap

URL = 'https://www.rbc.ru/'


def get_soup(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Проверка на ошибки HTTP
        return BeautifulSoup(r.text, 'lxml')
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


def save_json(data):
    with open('rbk_data.json', "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    news_data = {}
    soup = get_soup(URL)

    if soup is None:
        print("Не удалось получить данные с сайта.")
        return

    # Получаем все ссылки на новости
    main_div = soup.find('div', class_='main__list js-main-news-list')
    if main_div is not None:
        news_links = main_div.find_all('a', {'class': ['main__big__link', 'main__feed__link']})
    else:
        print("Не найден элемент с классом 'main'.")
        return

    # Для каждой ссылки получаем информацию и записываем в news_data
    for i in range(min(len(news_links), 15)):
        link = news_links[i].get('href').split('?')[0]
        name = link
        news_data[name] = {}
        article_soup = get_soup(link)

        if article_soup is None:
            print(f"Не удалось получить данные статьи по ссылке: {link}")
            continue

        # Переходим на страницу для дальнейшего парсинга
        article = article_soup.find('div', class_='article')
        if article is None:
            print(f"Статья не найдена по ссылке: {link}")
            continue

        category = article.find('a', class_='article__header__category')
        date = article.find('time', class_='article__header__date')
        title = article.find('div', class_='article__header__title')
        image = article.find('div', class_='article__main-image')
        article_paragraphs = ap.get_article_arr(link)
        article_text = '\n'.join(paragraph.strip() for paragraph in article_paragraphs)

        # Заполняем полученными данными news_data
        news_data[name]['link'] = link
        news_data[name]['date'] = date['content'].replace('T', ' ').split('+')[0] if date else 'Без даты'
        news_data[name]['text'] = article_text.replace('\xa0', '').strip()
        if not title:
            title = article.find('div', class_='article__header__note')
        news_data[name]['title'] = title.text.strip() if title else 'Без заголовка'
        if not category:
            category = article.find('div', class_='master-tags js-master-tags')
            if category:
                category = category.text.strip().split('\n')[0]
        try:
            news_data[name]['category'] = category.text.strip() if category else 'Без категории'
        except AttributeError:
            news_data[name]['category'] = category.strip()

    save_json(news_data)


if __name__ == "__main__":
    main()
