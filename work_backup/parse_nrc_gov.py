import requests
import html
import re
from bs4 import BeautifulSoup

# URL для запроса
url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/2024/20240711en.html#en57208"


def get_reports_list(url):
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Запись полного HTML-кода в строку
        html_content = response.text
        # получаю элементы с отчетом, в начале каждого отчета идет <div class="border">, поэтому делаю первый сплит
        # сразу же убираю первый элемент сплита, потому что он не содержит отчет
        content2 = html_content.split('<div class="border">')[1:]
        # через цикл отделяю отчет от мусора, через сплит, потому что каждый отчет заканчивается на </div>
        reports = list()

        for elem in content2:
            reports.append(re.sub(r'<[^>]+>', '', html.unescape(elem.split('</div>')[0])))

        return reports
    else:
        print('error')


def get_reports_info(url):
    # Отправка GET-запроса
    response = requests.get(url)
    response.raise_for_status()  # Проверка на успешность запроса

    # Парсинг содержимого страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Словарь для хранения городов происшествий
    incident_cities = {}

    # Находим все элементы с отчетами
    reports = soup.find_all(id=lambda x: x and x.startswith('en57'))

    for report in reports:
        # Ищем элемент с классом 'grid border', где указаны город и штат
        location_element = report.find_previous(class_='grid border')
        if location_element:
            # Извлекаем текст и разбиваем по строкам
            location_text = location_element.get_text(strip=True)
            # Предполагаем, что город указан в первой строке
            city = location_text.splitlines()[0]

            # Добавляем в словарь
            incident_cities[report['id']] = city

    result = []

    for event_id, details in incident_cities.items():
        # Извлекаем город
        city_start = details.find('City:') + len('City:')
        city_end = details.find('State:')
        city = details[city_start:city_end].strip()

        # Извлекаем штат
        state_start = details.find('State:') + len('State:')
        state_end = details.find('County:') if 'County:' in details else details.find(
            'Unit:')  # учитываем случаи с отсутствием County
        state = details[state_start:state_end].strip()

        # Извлекаем дату уведомления
        notif_date_start = details.find('Notification Date:') + len('Notification Date:')
        notif_date_end = details.find('Notification Time:')
        notif_date = details[notif_date_start:notif_date_end].strip()

        # Обрабатываем случаи недостающих значений
        if len(city) > 20:
            city = ''
        if len(state) > 20:
            state = ''

        # Создаем словарь и добавляем в результат
        result.append({
            'id': event_id,
            'city': city,
            'state': state,
            'notif date': notif_date
        })

    # Выводим результат
    return result


print(get_reports_list(url))
print(get_reports_info(url))
