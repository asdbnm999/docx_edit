import pprint
from deep_translator import GoogleTranslator
import PyPDF2
import re


def get_txt(pdf):
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

    text = text.split('\n')
    return text


def get_docx_info(pdf):
    def detect_radioactive_elements_in_string(s):
        pattern = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d.*\d)(?=.*(?:Bq|Sv))(?<! )([^-\s]*[-][^-\s]*\d{2})')

        if pattern.search(s):
            return True
        return False

    def extract_radioactive_elements(s):
        pattern = r'([A-Z][a-z]-\d{2,3})(?=\s|$)'
        matches = re.findall(pattern, s)
        return matches

    def string_delete_trash(input_string):
        try:
            elements = input_string.splitlines()
            cleaned_elements = [element for element in elements if len(element) > 1]
            output_string = '\n'.join(cleaned_elements)
            return output_string
        except:
            return input_string

    def search_keys(input_string):
        pattern = r'\d{4}-\d{2}-\d{3}[A-Z]{3}-\d{2}-\d{3}'
        return bool(re.search(pattern, input_string))

    itdbKey = str()
    webInfKey = str()                       # keys_checked_flag
    incidentGroup = str()
    incidentDate = str()

    incidentCountry_ru = str()
    incidentCountry_en = str()

    incidentLocation_ru = str()
    incidentLocation_en = str()

    incidentDetectSummary = str()
    incidentMaterial = str()
    incidentMaterial_list = list()
    incidentType = str()
    incidentDangerCategories = str()       # idc_flag
    incidentText = str()

    keys_checked_flag = False
    idc_flag = False
    material_flag = False

    # 2024-01-001.pdf
    source_text = get_txt('tables/' + pdf)
    pprint.pprint(source_text)
    for i in range(len(source_text)):
        try:
            if 'WebINF Key' in source_text[i]:
                if '2024' in source_text[i] and not keys_checked_flag:
                    if search_keys(source_text[i].split('WebINF Key: ')[1].strip()):
                        itdbKey = source_text[i].split('WebINF Key: ')[1].strip()[:11]
                        webInfKey = f"({source_text[i].split('WebINF Key: ')[1].strip()[11:]})"
                    else:
                        itdbKey = source_text[i].split('WebINF Key: ')[1].strip()
                        webInfKey = f'({source_text[i+1].strip()})'
                    keys_checked_flag = True
                elif '2024' not in source_text[i] and not keys_checked_flag:
                    itdbKey = source_text[i+1].strip()
                    webInfKey = f'({source_text[i+2].strip()})'
                    keys_checked_flag = True

            elif 'WebINF' in source_text[i] and 'Key:' in source_text[i+1]:
                itdbKey = source_text[i+1].split('Key: ')[1].strip()
                webInfKey = f'({source_text[i+2].strip()})'
                keys_checked_flag = True

            elif 'Incident Group' in source_text[i]:
                incidentGroup = source_text[i].split('Incident Group: ')[1].split('Location Details:')[0][6:].strip()
                webInfKey += f'\nИнцидент\n{incidentGroup} группы'

            elif 'Incident Date' in source_text[i] and 'Country' in source_text[i]:
                united_list = source_text[i].split('Incident Date: ')[1].split('Country:')
                incidentDate = GoogleTranslator(source='en', target='ru').translate(united_list[0].strip())
                if incidentDate[-2:] != 'г.':
                    incidentDate += ' г.'
                incidentCountry_en = united_list[1].strip()
                incidentCountry_ru = GoogleTranslator(source='en', target='ru').translate(incidentCountry_en)
                incidentCountry_en = '(' + incidentCountry_en + ')'

            elif 'Incident Type' in source_text[i]:
                united_list = source_text[i].split('Incident Type: ')[1].split('Location: ')
                incidentType = GoogleTranslator(source='en', target='ru').translate(united_list[0].strip())
                incidentLocation_en = united_list[1].strip()
                incidentLocation_ru = GoogleTranslator(source='en', target='ru').translate(incidentLocation_en)
                incidentLocation_en = '(' + incidentLocation_en + ')'

            elif source_text[i].strip()[-2].isalpha() and source_text[i].strip()[-1].isdigit():
                if idc_flag:
                    incidentDangerCategories += ';'
                else:
                    idc_flag = True

                incidentDangerCategories += f'\nКатегория опасности\n(RS-G-1.9)-{source_text[i][-1]}'

            elif 'ADDITIONAL' in source_text[i] and 'COMMENTS' in source_text[i]:
                for n in range(1, 100):
                    if 'MATERIAL' not in source_text[i+n]:
                        incidentDetectSummary += GoogleTranslator(source='en', target='ru').translate(source_text[i+n])
                    else:
                        break

            elif detect_radioactive_elements_in_string(source_text[i]):
                if extract_radioactive_elements(source_text[i])[0] not in incidentMaterial or source_text[i] in incidentMaterial_list:
                    if material_flag:
                        incidentMaterial += '; '
                    incidentMaterial_list.append(source_text[i])
                    incidentMaterial += extract_radioactive_elements(source_text[i])[0]
                if not material_flag:
                    material_flag = True

            elif source_text[i] == 'Am-':
                if material_flag:
                    incidentMaterial += '; '
                incidentMaterial += 'Am-241/Be'
                if not material_flag:
                    material_flag = True

            elif 'Provide a brief summary' in source_text[i]:
                for n in range(1, 100):
                    if 'CHARACTERISTICS' not in source_text[i+n]:
                        incidentText += GoogleTranslator(source='en', target='ru').translate(source_text[i+n]) + '\n'
                    else:
                        incidentText = incidentText.strip()
                        break

        except IndexError:
            pass
    if incidentDetectSummary != '':
        incidentDetectSummary += '\n(' + string_delete_trash(incidentMaterial.strip()) + ')'
    else:
        incidentDetectSummary += '\n' + string_delete_trash(incidentMaterial.strip())

    return [itdbKey.strip(), incidentDate.strip(), incidentCountry_ru.strip(), incidentLocation_ru.strip(),
            incidentDetectSummary.strip(), incidentType.strip(), incidentText.strip(), webInfKey.strip(),
            incidentCountry_en.strip(), incidentLocation_en.strip(), incidentDangerCategories.strip()]


docx_list = get_docx_info('2024-05-002.pdf')
for elem in docx_list:
    print(elem)
