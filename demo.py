import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import webbrowser as wb


class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        menu_canvas = tk.Canvas(self, width=330, height=185, bg='#4B0082')
        monitoring_but = menu_canvas.create_text((10, 22), anchor='nw',
                                                 text=f'Мониторинг',
                                                 font='Consolas 14',
                                                 fill='#E0FFFF',
                                                 activefill='#00BFFF')
        menu_canvas.tag_bind(monitoring_but, "<Button-1>", lambda win='ws': goto(event=None, win='ws'))

        panel = menu_canvas.create_image((120, 10), anchor='nw', image=panel_img)
        menu_canvas.tag_bind(panel, "<Button-1>", lambda win='ws': goto(event=None, win='ws'))

        docx_reports_compile_but = menu_canvas.create_text((10, 80), anchor='nw',
                                                           text=f'Составление отчетов .docx',
                                                           font='Consolas 14',
                                                           fill='#E0FFFF',
                                                           activefill='#00BFFF')
        menu_canvas.tag_bind(docx_reports_compile_but, "<Button-1>", lambda win='cr': goto(event=None, win='cr'))

        report = menu_canvas.create_image((270, 67), anchor='nw', image=report_img)
        menu_canvas.tag_bind(report, "<Button-1>", lambda win='ws': goto(event=None, win='cr'))

        translate_tables_but = menu_canvas.create_text((10, 145), anchor='nw',
                                                       text=f'Перевод таблиц БД МАГАТЭ',
                                                       font='Consolas 14',
                                                       fill='#E0FFFF',
                                                       activefill='#00BFFF')
        menu_canvas.tag_bind(translate_tables_but, "<Button-1>", lambda win='tt': goto(event=None, win='tt'))

        table = menu_canvas.create_image((257, 130), anchor='nw', image=table_img)
        menu_canvas.tag_bind(table, "<Button-1>", lambda win='ws': goto(event=None, win='tt'))

        settings_but = menu_canvas.create_image((200, 15), anchor='nw', image=param_img)
        menu_canvas.tag_bind(settings_but, "<Button-1>", self.open_settings_window)

        menu_canvas.pack()
        self.pack()

    def open_settings_window(self, event):
        self.sw = tk.Toplevel(self, width=300, height=150)
        self.sw.resizable(False, False)
        self.sw_canvas = tk.Canvas(self.sw, width=300, height=150, bg='#4B0082')

        self.select_setting_lab = self.sw_canvas.create_text((10, 10),
                                                        anchor='nw',
                                                        text='Выберите пункт для настройки',
                                                        fill='#E0FFFF',
                                                        font='Consolas 10')
        settings = ['Браузер', 'Путь сохранения файлов']
        self.select_setting = ttk.Combobox(self.sw,
                                           values=settings,
                                           state='readonly',
                                           width=25
                                           )
        self.select_setting.place(x=10, y=30)
        ############################################
        # сделать обработку выбора пункта настроек #
        # потому что при выборе браузера и другого #
        # из selected1                             #
        ############################################
        self.select_setting.bind('<<ComboboxSelected>>', self.selected1)

        self.sw_canvas.pack()

    def selected1(self, event):
        if self.select_setting.get() == 'Браузер':
            try:
                self.sw_canvas.coords((-100, -100), 'get_path_but')
            except:
                pass
            browsers = ['Opera', 'Chrome', 'Chromium', 'FireFox']
            self.select_browser = ttk.Combobox(self.sw,
                                               values=browsers,
                                               state='readonly',
                                               )
            self.select_browser.place(x=10, y=70)
            self.select_browser.bind('<<ComboboxSelected>>', self.selected_browser)
        elif self.select_setting.get() == 'Путь сохранения файлов':
            try:
                self.select_browser.place(x=-100, y=-100)
            except:
                pass
            self.sw_canvas.create_text((10, 100),
                                       anchor='nw',
                                       text='Обзор...',
                                       fill='lightblue',
                                       activefill='white',
                                       font='Consolas 10',
                                       tags='get_path_but')
            self.sw_canvas.tag_bind('get_path_but', '<Button-1>', self.select_directory)

    def selected_browser(self):
        pass

    def select_directory(self, event):
        self.directory = filedialog.askdirectory()
        self.sw.lift()


class WebSourcesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.ws_canvas = tk.Canvas(self, width=800, height=600, bg='#6A5ACD')
        back_but = self.ws_canvas.create_image((10, 10), anchor='nw', image=back_img)
        self.ws_canvas.tag_bind(back_but, '<Button-1>', lambda win='menu': goto(event=None, win='menu'))

        # размещение ссылок на canvas и добавление их в список
        link_items = []
        for i, link in enumerate(smi_list):
            if i <= 19:
                coords = (100, (i * 30) + 20)  # x и y координаты для каждой ссылки
            elif i > 19:
                i -= 20
                coords = (360, (i * 30) + 20)

            short_link = link[8:-1]
            if short_link == 'www.nrc.gov/reading-rm/doc-collections/event-status/event/2024': short_link = 'nrc.gov'

            item = self.ws_canvas.create_text(*coords, text=short_link,
                                              fill="#E0FFFF",
                                              activefill='#00BFFF',
                                              anchor="w",
                                              font='Consolas 12',
                                              tags="link")
            link_items.append((item, link))

        # Обработчик клика
        def on_click(event):
            clicked_item = self.ws_canvas.find_withtag("current")
            if clicked_item:
                for item, link in link_items:
                    if item == clicked_item[0]:
                        wb.open_new_tab(link)
                        break

        # Связывание события клика с обработчиком
        self.ws_canvas.tag_bind("link", "<Button-1>", on_click)

        # добавление русских флагов первой колонки
        for i in range(0, 20):
            flag_x = 70
            flag_y = (i * 30) + 10
            if (i >= 17) and (i <= 19):
                self.insert_country_flag(coords=(flag_x, flag_y), country='eu')
            else:
                self.insert_country_flag(coords=(flag_x, flag_y), country='ru')

        # добавление флагов второй колонки 330 10
        for i in range(0, 20):
            flag_x = 330
            flag_y = (i * 30) + 10
            if i >= 17:
                self.insert_country_flag(coords=(flag_x, flag_y), country='uk')
            elif (i >= 14) and (i <= 16):
                self.insert_country_flag(coords=(flag_x, flag_y), country='fr')
            elif (i >= 11) and (i <= 13):
                self.insert_country_flag(coords=(flag_x, flag_y), country='ge')
            else:
                self.insert_country_flag(coords=(flag_x, flag_y), country='us')

        self.ws_canvas.pack()
        self.pack()

    def insert_country_flag(self, coords: tuple, country: str):
        """
        добавление флагов стран для ссылок на СМИ

        :param coords: (x, y)
        :param country: 'ru', 'uk', 'us', 'eu', 'fr', 'ge'
        :return:
        """
        if country == 'ru':
            self.ws_canvas.create_image(coords, anchor='nw', image=ru_flag)
        elif country == 'uk':
            self.ws_canvas.create_image(coords, anchor='nw', image=uk_flag)
        elif country == 'us':
            self.ws_canvas.create_image(coords, anchor='nw', image=us_flag)
        elif country == 'fr':
            self.ws_canvas.create_image(coords, anchor='nw', image=fr_flag)
        elif country == 'ge':
            self.ws_canvas.create_image(coords, anchor='nw', image=ge_flag)
        elif country == 'eu':
            self.ws_canvas.create_image(coords, anchor='nw', image=eu_flag)


class CompileReportsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        cr_canvas = tk.Canvas(self, width=800, height=600, bg='#6A5ACD')
        cr_canvas.create_text((10, 10), anchor='nw',
                              text=f'Автоматизированное составление отчетов',
                              font='Consolas 14', fill='white')
        cr_canvas.pack()
        self.pack()


class TranslateTablesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tt_canvas = tk.Canvas(self, width=800, height=600, bg='#6A5ACD')
        tt_canvas.create_text((10, 10), anchor='nw',
                              text=f'Перевод таблиц .pdf',
                              font='Consolas 14', fill='white')
        tt_canvas.pack()
        self.pack()


class MainWin:
    def __init__(self, master):
        global index, frameList
        global panel_img, report_img, table_img, back_img, param_img, info_img
        global ru_flag, uk_flag, us_flag, fr_flag, ge_flag, eu_flag

        panel_img = tk.PhotoImage(file='images/panel48.png')
        report_img = tk.PhotoImage(file='images/report48.png')
        table_img = tk.PhotoImage(file='images/table48.png')
        back_img = tk.PhotoImage(file='images/back48.png')
        param_img = tk.PhotoImage(file='images/param.png')
        info_img = tk.PhotoImage(file='images/info.png')

        ru_flag = tk.PhotoImage(file='images/rus.png')
        uk_flag = tk.PhotoImage(file='images/uk.png')
        us_flag = tk.PhotoImage(file='images/us.png')
        fr_flag = tk.PhotoImage(file='images/fr.png')
        ge_flag = tk.PhotoImage(file='images/ge.png')
        eu_flag = tk.PhotoImage(file='images/eu.png')

        combobox_style = ttk.Style()
        combobox_style.theme_create('combobox_style', parent='alt',
                                    settings={'TCombobox':
                                                  {'configure':
                                                       {'selectbackground': '#6A5ACD',
                                                        'fieldbackground': '#6A5ACD',
                                                        'background': '#6A5ACD'
                                                        }}}
                                    )
        combobox_style.theme_use('combobox_style')

        mainframe = tk.Frame(master)
        mainframe.pack()

        index = 0
        frameList = [MenuFrame(mainframe), WebSourcesFrame(mainframe), CompileReportsFrame(mainframe),
                     TranslateTablesFrame(mainframe)]
        for frame in frameList[1:]:
            frame.forget()


def open_web_source(event, tag):
    tag = int(tag[5:])
    wb.open_new_tab(smi_list[tag])


def goto(event, win):
    global index
    frameList[index].forget()
    if win == 'menu':
        index = 0
    elif win == 'ws':
        index = 1
    elif win == 'cr':
        index = 2
    elif win == 'tt':
        index = 3
    frameList[index].tkraise()
    frameList[index].pack()


def set_config():
    global browser, browser_path
    # изначально все = default
    with open('config.txt', 'r') as file:
        config = [line.strip() for line in file.readlines()]

    for elem in config:
        if elem[:10] == 'browser = ':
            browser = elem[10:].strip().lower()
        elif elem[:15] == 'browser_path = ':
            browser_path = config[1][15:].strip()

    print(browser_path, browser)


with open('smi.txt', 'r') as file:
    # чтобы убрать \n в конце строк использую стрип
    smi_list = [line.strip() for line in file.readlines()]
root = tk.Tk()
root.resizable(False, False)
obj = MainWin(root)
root.mainloop()
