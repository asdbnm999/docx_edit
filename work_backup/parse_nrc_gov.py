import requests
import html
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# URL для запроса
url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/2024/20240711en.html#en57208"


states = {
    'AL': 'Алабама',
    'AK': 'Аляска',
    'AZ': 'Аризона',
    'AR': 'Арканзас',
    'CA': 'Калифорния',
    'CO': 'Колорадо',
    'CT': 'Коннектикут',
    'DE': 'Делавэр',
    'FL': 'Флорида',
    'GA': 'Джорджия',
    'HI': 'Гавайи',
    'ID': 'Айдахо',
    'IL': 'Иллинойс',
    'IN': 'Индьяна',
    'IA': 'Айова',
    'KS': 'Канзас',
    'KY': 'Кентукки',
    'LA': 'Луизиана',
    'ME': 'Мэн',
    'MD': 'Мэриленд',
    'MA': 'Массачусетс',
    'MI': 'Мичиган',
    'MN': 'Миннесота',
    'MS': 'Миссисипи',
    'MO': 'Миссури',
    'MT': 'Монтана',
    'NE': 'Небраска',
    'NV': 'Невада',
    'NH': 'Нью-Гэмпшир',
    'NJ': 'Нью-Джерси',
    'NM': 'Нью-Мексико',
    'NY': 'Нью-Йорк',
    'NC': 'Северная Каролина',
    'ND': 'Северная Дакота',
    'OH': 'Огайо',
    'OK': 'Оклахома',
    'OR': 'Орегон',
    'PA': 'Пенсильвания',
    'RI': 'Род-Айленд',
    'SC': 'Южная Каролина',
    'SD': 'Южная Дакота',
    'TN': 'Теннесси',
    'TX': 'Техас',
    'UT': 'Юта',
    'VT': 'Вермонт',
    'VA': 'Виргиния',
    'WA': 'Вашингтон',
    'WV': 'Западная Виргиния',
    'WI': 'Висконсин',
    'WY': 'Вайоминг'
}


def get_reports_list(url):
    # Отправка HTTP-запроса
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Запись полного HTML-кода в строку
        html_content = response.text
        # получаю элементы с отчетом, в начале каждого отчета идет <div class="border">, поэтому делаю первый сплит
        # сразу же убираю первый элемент сплита, потому что он не содержит отчет
        content1 = html_content.split('<div class="event-summary number text-center">')[1].split('<a href="#')[1:]
        content1_1 = content1[-1].split('</div>')[:1]
        content1[-1] = content1_1[0]
        ids = list()
        for elem in content1:
            ids.append(elem[:7])

        content2 = html_content.split('<div class="border">')[1:]
        # через цикл отделяю отчет от мусора, через сплит, потому что каждый отчет заканчивается на </div>
        reports_eng = list()

        for elem in content2:
            reports_eng.append(re.sub(r'<[^>]+>', '', html.unescape(elem.split('</div>')[0])))

        reports_rus = list()
        for report in reports_eng:
            translated_report = GoogleTranslator(source='en', target='ru').translate(report)
            reports_rus.append(translated_report)

        return dict(zip(ids, reports_rus))

    else:
        print(f"Ошибка при загрузке страницы: {response.status_code}")


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
        else:
            city = GoogleTranslator(source='en', target='ru').translate(city)
        if len(state) > 20:
            state = ''
        else:
            state = states[state]

        # Создаем словарь и добавляем в результат
        result.append({
            'id': event_id,
            'city': city,
            'state': state,
            'notif date': notif_date
        })

    # Выводим результат
    return result


result_dict = {}

for item in get_reports_info(url):
    id_value = item["id"]
    if id_value in get_reports_list(url):
        result_dict[id_value] = [
            item["state"],
            item["city"],
            item["notif date"],
            get_reports_list(url)[id_value]
        ]

print(result_dict)
