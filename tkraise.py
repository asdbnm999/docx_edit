import tkinter as tk


class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        menu_canvas = tk.Canvas(self, width=800, height=600, bg='#BBBBBB')
        monitoring = menu_canvas.create_text((10, 10), anchor='nw',
                                text=f'Мониторинг',
                                font='Consolas 14', fill='#212121')
        menu_canvas.tag_bind(monitoring, "<Button-1>", self.switchWins)
        menu_canvas.pack()
        self.pack()


class WebSourcesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ws_canvas = tk.Canvas(self, width=800, height=600, bg='#BBBBBB')
        ws_canvas.create_text((10, 10), anchor='nw',
                              text=f'Сообщение для Claude 3:',
                              font='Consolas 14', fill='#212121')
        ws_canvas.pack()
        self.pack()


class MainWin:
    def __init__(self, master):
        mainframe = tk.Frame(master)
        mainframe.pack()
        self.index = 0

        self.frameList = [MenuFrame(mainframe), WebSourcesFrame(mainframe),]
        self.frameList[1].forget()

        bottomframe = tk.Frame(master)
        bottomframe.pack(padx=10, pady=10)

        switch = tk.Button(bottomframe, text='switch', command=self.switchWins)
        switch.pack(padx=10, pady=10)

    def switchWins(self):
        self.frameList[self.index].forget()
        self.index = (self.index + 1) % len(self.frameList)
        self.frameList[self.index].tkraise()
        self.frameList[self.index].pack()


root = tk.Tk()
obj = MainWin(root)
root.mainloop()
