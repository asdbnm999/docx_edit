import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog
import webbrowser as wb


class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #############################
        # поменять названия на теги #
        #############################
        menu_canvas = tk.Canvas(self, width=330, height=185, bg='#4B0082')
        monitoring_but = menu_canvas.create_text((10, 22), anchor='nw',
                                                 text=f'Мониторинг',
                                                 font='Consolas 14',
                                                 fill='#E0FFFF',
                                                 activefill='#00BFFF')
        menu_canvas.tag_bind(monitoring_but, "<Button-1>", lambda win='ws': goto(event=None, win='ws'))

        panel = menu_canvas.create_image((120, 22), anchor='nw', image=panel_img)
        menu_canvas.tag_bind(panel, "<Button-1>", lambda win='ws': goto(event=None, win='ws'))

        docx_reports_compile_but = menu_canvas.create_text((10, 80), anchor='nw',
                                                           text=f'Составление отчетов .docx',
                                                           font='Consolas 14',
                                                           fill='#E0FFFF',
                                                           activefill='#00BFFF')
        menu_canvas.tag_bind(docx_reports_compile_but, "<Button-1>", lambda win='cr': goto(event=None, win='cr'))

        report = menu_canvas.create_image((267, 79), anchor='nw', image=report_img)
        menu_canvas.tag_bind(report, "<Button-1>", lambda win='ws': goto(event=None, win='cr'))

        translate_tables_but = menu_canvas.create_text((10, 145), anchor='nw',
                                                       text=f'Перевод таблиц БД МАГАТЭ',
                                                       font='Consolas 14',
                                                       fill='#E0FFFF',
                                                       activefill='#00BFFF')
        menu_canvas.tag_bind(translate_tables_but, "<Button-1>", lambda win='tt': goto(event=None, win='tt'))

        table = menu_canvas.create_image((257, 144), anchor='nw', image=table_img)
        menu_canvas.tag_bind(table, "<Button-1>", lambda win='ws': goto(event=None, win='tt'))

        settings_but = menu_canvas.create_image((306, 5), anchor='nw', image=param_img)
        menu_canvas.tag_bind(settings_but, "<Button-1>", self.open_settings_window)

        info_but = menu_canvas.create_image((280, 5), anchor='nw', image=info_img)
        menu_canvas.tag_bind(info_but, '<Button-1>', self.show_info)

        menu_canvas.pack()
        self.pack()

    def show_info(self):
        pass

    def open_settings_window(self, event):
        self.sw = tk.Toplevel(self, width=300, height=150)

        self.sw.resizable(False, False)
        self.sw_canvas = tk.Canvas(self.sw, width=300, height=150, bg='#4B0082')

        self.select_setting_lab = self.sw_canvas.create_text((10, 10),
                                                             anchor='nw',
                                                             text='Выберите пункт для настройки',
                                                             fill='#E0FFFF',
                                                             font='Consolas 10',
                                                             )
        settings = ['Браузер', 'Путь сохранения файлов']
        self.select_setting = ttk.Combobox(self.sw,
                                           values=settings,
                                           state='readonly',
                                           width=25,
                                           justify=tk.CENTER,
                                           )
        self.select_setting.place(x=10, y=30)
        self.select_setting.bind('<<ComboboxSelected>>', self.selected1)

        self.sw_canvas.pack()

    def selected1(self, event):
        self.set_choice = self.select_setting.get()
        self.sw_canvas.create_text((10, 53),
                                   anchor='nw',
                                   text='',
                                   fill='#E0FFFF',
                                   tags='second_annotation',
                                   font='Consolas 10')
        if self.set_choice == 'Браузер':
            try:
                self.sw_canvas.coords('get_path_but', (-100, -100))
                self.sw_canvas.coords('confirm_but', (-100, -100))
                self.sw_canvas.coords('dismiss_but', (-100, -100))
            except Exception as e:
                print(e)

            self.sw_canvas.itemconfig('second_annotation', text='Выберите браузер')

            browsers = ['Opera', 'Chrome', 'Chromium', 'FireFox']
            self.select_browser = ttk.Combobox(self.sw,
                                               values=browsers,
                                               state='readonly',
                                               width=25,
                                               justify=tk.CENTER
                                               )
            self.select_browser.place(x=10, y=70)
            self.select_browser.bind('<<ComboboxSelected>>', self.selected_browser)

        elif self.set_choice == 'Путь сохранения файлов':
            try:
                self.select_browser.place(x=-100, y=-100)
                self.sw_canvas.coords('get_BPath_but', (-100, -100))
                self.sw_canvas.coords('confirm_but', (-100, -100))
                self.sw_canvas.coords('dismiss_but', (-100, -100))
            except Exception as e:
                print(e)

            self.sw_canvas.itemconfig('second_annotation', text='Выберите директорию')

            try:
                self.hand_ent_path.place(x=-100, y=-100)
            except:
                pass

            self.hand_ent_path = tk.Entry(self.sw, width=27, bg='#6A5ACD', fg='#E0FFFF')
            self.hand_ent_path.place(x=10, y=70)

            self.sw_canvas.create_text((180, 72),
                                       anchor='nw',
                                       text='Обзор...',
                                       fill='lightblue',
                                       activefill='white',
                                       font='Consolas 10',
                                       tags='get_path_but')
            self.sw_canvas.tag_bind('get_path_but', '<Button-1>',
                                    lambda t='f_path': self.select_directory(event=None, type=t))

            self.sw_canvas.create_image((245, 125), anchor='nw', image=confirm_img, tags='confirm_but')
            self.sw_canvas.tag_bind('confirm_but', '<Button-1>', self.confirm_changes)

            self.sw_canvas.create_image((275, 125), anchor='nw', image=dismiss_img, tags='dismiss_but')
            self.sw_canvas.tag_bind('dismiss_but', '<Button-1>', self.dismiss_changes)

    def selected_browser(self, event):
        self.browser_name = self.select_browser.get().lower()
        print(self.browser_name)

        try:
            self.hand_ent_path.place(x=-100, y=-100)
        except:
            pass

        self.hand_ent_path = tk.Entry(self.sw, width=27, bg='#6A5ACD', fg='#E0FFFF')
        self.hand_ent_path.place(x=10, y=110)

        self.sw_canvas.create_text((180, 112),
                                   anchor='nw',
                                   text='Обзор...',
                                   fill='lightblue',
                                   activefill='white',
                                   font='Consolas 10',
                                   tags='get_BPath_but')
        self.sw_canvas.tag_bind('get_BPath_but', '<Button-1>',
                                lambda t='b_path': self.select_directory(event=None, type=t))

        self.sw_canvas.create_image((245, 125), anchor='nw', image=confirm_img, tags='confirm_but')
        self.sw_canvas.tag_bind('confirm_but', '<Button-1>', self.confirm_changes)

        self.sw_canvas.create_image((275, 125), anchor='nw', image=dismiss_img, tags='dismiss_but')
        self.sw_canvas.tag_bind('dismiss_but', '<Button-1>', self.dismiss_changes)

    def select_directory(self, event, type):
        self.directory = filedialog.askdirectory()
        self.hand_ent_path.insert(0, self.directory)
        self.sw.lift()

    def confirm_changes(self, event):
        """
        browser = default
        browser_path = default
        download_path = default
        C:/Users/vboxuser/AppData/Local/Programs/Opera/launcher.exe
        """
        global browser, browser_path, download_path
        print(browser, browser_path, download_path)
        if self.set_choice == 'Браузер':
            try:
                browser = self.browser_name
                browser_path = self.hand_ent_path.get()
                if '\\' not in browser_path and ':/' in browser_path:
                    wb.register(self.browser_name,
                                None,
                                wb.BackgroundBrowser(browser_path))

                    with open('config.txt', 'w') as file:
                        file.write('browser = ' + browser + '\nbrowser_path = ' +
                                   browser_path + '\ndownload_path = ' + download_path)

                    mb.showinfo(title='Отчет.',
                                message=f'Параметры применены успешно!\nБраузер успешно сменен на {browser}')
                else:
                    mb.showwarning(title='Ошибка настройки.', message='Новые параметры не применены!\n'
                                                                      'Проверьте путь скачивания, в нем не должно быть'
                                                                      ' символов "\\"')
            except Exception as e:
                print(e)
                mb.showwarning(title='Ошибка настройки.', message='Новые параметры не применены!')

        elif self.set_choice == 'Путь сохранения файлов':
            try:
                download_path = self.hand_ent_path.get()
                if '\\' not in browser_path and ':/' in browser_path:

                    with open('config.txt', 'w') as file:
                        file.write('browser = ' + browser + '\nbrowser_path = ' +
                                   browser_path + '\ndownload_path = ' + download_path)

                    mb.showinfo(title='Отчет.', message='Параметры применены успешно!\nПуть для скачивания файлов:\n'
                    f'{download_path}')
                else:
                    mb.showwarning(title='Ошибка настройки.', message='Новые параметры не применены!\n'
                                                                      'Проверьте путь скачивания, в нем не должно быть'
                                                                      ' символов "\\"')
            except Exception as e:
                print(e)
                mb.showwarning(title='Ошибка настройки.', message='Новые параметры не применены!')

        else:
            mb.showwarning(title='Ошибка настройки.', message='Новые параметры не применены!')

    def dismiss_changes(self, event):
        pass


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
        global panel_img, report_img, table_img, back_img, param_img, info_img, confirm_img, dismiss_img
        global ru_flag, uk_flag, us_flag, fr_flag, ge_flag, eu_flag

        panel_img = tk.PhotoImage(file='images/panel.png')
        report_img = tk.PhotoImage(file='images/report.png')
        table_img = tk.PhotoImage(file='images/translate.png')
        back_img = tk.PhotoImage(file='images/back48.png')
        param_img = tk.PhotoImage(file='images/param.png')
        info_img = tk.PhotoImage(file='images/info.png')
        confirm_img = tk.PhotoImage(file='images/confirm24.png')
        dismiss_img = tk.PhotoImage(file='images/dismiss24.png')

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
                                                        'background': '#6A5ACD',
                                                        'foreground': '#6A5ACD'
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
    global browser, browser_path, download_path
    # изначально все = default
    with open('config.txt', 'r') as file:
        config = [line.strip() for line in file.readlines()]

    for elem in config:
        if elem[:10] == 'browser = ':
            browser = elem[10:].strip().lower()
        elif elem[:15] == 'browser_path = ':
            browser_path = elem[15:].strip()
        elif elem[:16] == 'download_path = ':
            download_path = elem[16:].strip()

    if download_path != 'default' and download_path[-1] != '/':
        download_path.join('/')

    print(browser_path, browser)


with open('smi.txt', 'r') as file:
    # чтобы убрать \n в конце строк использую стрип
    smi_list = [line.strip() for line in file.readlines()]
set_config()
root = tk.Tk()
root.resizable(False, False)
obj = MainWin(root)
root.mainloop()
