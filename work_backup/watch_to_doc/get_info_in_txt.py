import PyPDF2

# Укажите путь к вашему PDF-файлу
pdf_path = '2024-01-002.pdf'

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

# Печать извлеченного текста
print(text)

# Дополнительно: сохранение текста в файл
with open('extracted_text.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(text)

