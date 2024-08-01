import requests
import html
import re
from deep_translator import GoogleTranslator

# URL для запроса
url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/2024/20240711en.html#en57208"

# Отправка HTTP-запроса
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Запись полного HTML-кода в строку
    html_content = response.text
    print("HTML-код страницы успешно получен!\n")
    # получаю элементы с отчетом, в начале каждого отчета идет <div class="border">, поэтому делаю первый сплит
    # сразу же убираю первый элемент сплита, потому что он не содержит отчет
    content1 = html_content.split('<div class="event-summary number text-center">')[1].split('<a href="#')[1:]
    content1_1 = content1[-1].split('</div>')[:1]
    content1[-1] = content1_1[0]
    ids = list()
    for elem in content1:
        ids.append(elem[:7])
    print(ids)

    content2 = html_content.split('<div class="border">')[1:]
    # через цикл отделяю отчет от мусора, через сплит, потому что каждый отчет заканчивается на </div>
    reports_eng = list()

    for elem in content2:
        reports_eng.append(re.sub(r'<[^>]+>', '', html.unescape(elem.split('</div>')[0])))

    reports_rus = list()
    for report in reports_eng:
        translated_report = GoogleTranslator(source='en', target='ru').translate(report)
        reports_rus.append(translated_report)

    id_report_dict = dict(zip(ids, reports_rus))
    print(id_report_dict)
    for val in id_report_dict.values():
        print(val)
else:
    print(f"Ошибка при загрузке страницы: {response.status_code}")

