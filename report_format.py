from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches


def set_cell_border(cell, **kwargs):
    """
    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))


document = Document()

document.add_paragraph()
sdl_table = document.add_table(rows=3, cols=2)
items = [
    ("Источник информации: ", "info"),
    ("Дата публикации: ", "info"),
    ("Ссылка на источник: ", "info")
]


sdl_table.cell(row_idx=0, col_idx=0).text = "Источник информации:"
sdl_table.cell(row_idx=1, col_idx=0).text = "Дата публикации:"
sdl_table.cell(row_idx=2, col_idx=0).text = "Ссылка на источник:"
sdl_table.cell(row_idx=0, col_idx=1).text = "Источник информации:"
sdl_table.cell(row_idx=1, col_idx=1).text = "Дата публикации:"
sdl_table.cell(row_idx=2, col_idx=1).text = "Ссылка на источник:"

# обнуление обводки, смена шрифта, размера шрифта + bold
# костыль с счетчиком, чтобы выровнять четные ячейки
counter = 0
for row in sdl_table.rows:
    for cell in row.cells:
        if counter > 0:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
            counter = 0
        else:
            counter += 1
        cell.paragraphs[0].add_run('')
        rc = cell.paragraphs[0].runs[0]
        rc.font.size = Pt(14)
        rc.font.name = 'TimesNewRoman'
        rc.font.bold = True
        set_cell_border(
            cell,
            top={"sz": 0},
            bottom={"sz": 0},
            start={"sz": 0},
            end={"sz": 0},
        )

document.add_paragraph('\n')
art_header = document.add_paragraph('')
art_header.paragraph_format.first_line_indent = Inches(0.5)
art_header.add_run('asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd')
art_header.runs[0].font.name = 'TimesNewRoman'
art_header.runs[0].font.size = Pt(14)
art_header.runs[0].font.bold = True

article = document.add_paragraph('')
article.paragraph_format.first_line_indent = Inches(0.5)
article.add_run('asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd')
article.runs[0].font.name = 'TimesNewRoman'
article.runs[0].font.size = Pt(14)

document.save('demo.docx')
