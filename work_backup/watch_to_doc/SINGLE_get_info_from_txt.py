from deep_translator import GoogleTranslator

itdbKey = str()
webInfKey = str()                       # keys_checked_flag
incidentGroup = str()
incidentDate = str()

incidentCountry_ru = str()
incidentCountry_en = str()

incidentLocation_ru = str()
incidentLocation_en = str()

incidentDetectSummary = str()
incidentType = str()
incidentDangerCategories = list()       # idc_flag
incidentText = str()

keys_checked_flag = False
idc_flag = False

with open('extracted_text.txt', 'r', encoding='utf-8') as text_file:
    source_text = text_file.readlines()

print(source_text)

for i in range(len(source_text)):
    try:
        if 'WebINF Key' in source_text[i]:
            if '2024' in source_text[i] and not keys_checked_flag:
                itdbKey = source_text[i].split('WebINF Key: ')[1].strip()
                webInfKey = f'({source_text[i+1].strip()})'
                keys_checked_flag = True
            elif '2024' not in source_text[i] and not keys_checked_flag:
                # print('\n\n\n\n\n\n\n')
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
                incidentType += ';'
            else:
                idc_flag = True

            incidentType += f'\nКатегория опасности\n(RS-G-1.9)-{source_text[i][-2]}'

        elif 'ADDITIONAL' in source_text[i] and 'COMMENTS' in source_text[i]:
            for n in range(1, 100):
                if 'MATERIAL' not in source_text[i+n]:
                    incidentDetectSummary += GoogleTranslator(source='en', target='ru').translate(source_text[i+n])
                else:
                    break

    except IndexError:
        pass


print(itdbKey + '\n')
print(webInfKey + '\n')
print(incidentDate + '\n')
print(incidentCountry_ru)
print(incidentCountry_en + '\n')
print(incidentLocation_ru)
print(incidentLocation_en + '\n')
print(incidentDetectSummary + '\n')
print(incidentType + '\n')

# ADDITIONAL COMMENTS ABOUT THE MATERIAL
# ADDITIONAL COMMENTS ABOUT THE MATERIAL
