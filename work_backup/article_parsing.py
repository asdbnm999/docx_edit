import requests
from bs4 import BeautifulSoup

URL = 'https://www.rbc.ru/finances/15/08/2024/66bc7f609a79471dd2a42e12?from=from_main_2'  # Замените на нужный URL


def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на наличие ошибок HTTP
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


def get_article_arr(url: str) -> list:
    soup = get_soup(url)

    if soup is None:
        print("Не удалось получить данные с сайта.")
        return

    # Находим статью
    article = soup.find('div', class_='article')
    if article is None:
        print("Статья не найдена.")
        return

    # Получаем все параграфы до div с классом "article__footer-share"
    article_text = []

    for elem in article.find_all(['p', 'div']):
        if elem.name == 'div' and 'article__footer-share' in elem.get('class', []):
            break
        if elem.name == 'p':
            article_text.append(elem.get_text(strip=True))

    # Выводим или обрабатываем текст статей
    return article_text

