import requests
import pprint
import html
import re
from deep_translator import GoogleTranslator
import g4f
import time
from create_single_rep_docx import create_single_rep_docx


def create_reports_dict(url: str) -> dict[str, list[str]] | str:

    def create_header(report: str) -> str:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o_mini,
            messages=[{'role': 'user',
                       'content': f'не отвечай ничего лишнего, дай мне краткое содержание текста можно использовать до 15 слов без слов "отчет", "текст": {report}'}]
        )
        return response

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        id = url[-5:]
        trash_reports = html_content.split('<div class="border">')[1:]

        # ids
        id_date_report = dict()
        date_block = html_content.split(f'<div class="grid border" id="en{id}">')[1].split('</div>')[3].strip()

        try:
            date = date_block.split(r'<b>Notification Date:</b> ')[1].split('<br>')[0]
            date = '%s.%s.%s' % (date[3:5], date[0:2], date[6:])
        except IndexError:
            date_block = html_content.split(f'<div class="grid border" id="en{id}">')[1].split('</div>')[5].strip()
            date = date_block.split(r'<b>Notification Date:</b> ')[1].split('<br>')[0]
            date = '%s.%s.%s' % (date[3:5], date[0:2], date[6:])

        eng_report = re.sub(r'<[^>]+>', '', html.unescape(trash_reports[0].split('</div>')[0])).strip()

        try:
            eng_report = eng_report.split('EN Revision Text: ')[1]
        except IndexError:
            pass

        rus_report = GoogleTranslator(source='en', target='ru').translate(eng_report)

        header = create_header(rus_report)
        time.sleep(1)

        id_date_report[id] = [date, header, rus_report]

        return id_date_report
    elif response.status_code == 404:
        return 'Происшествий по сегодняшней дате не найдено!'
    else:
        return 'Внутренняя ошибка'


url = f'https://www.nrc.gov/reading-rm/doc-collections/event-status/event/2024/20240719en.html#en57210'
create_single_rep_docx(url, create_reports_dict(url))
