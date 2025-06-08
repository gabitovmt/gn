from tkinter import Tk, Button, Frame, Entry, StringVar, Text

HOME_TEXT = 'gnote.bin'


def open_text():
    with open(HOME_TEXT, 'rb') as f:
        return f.read().decode('utf16')


def save_text(text):
    with open(HOME_TEXT, 'wb') as f:
        f.write(text.encode('utf16'))


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.__key_var = StringVar()

        self.geometry("640x480")

        top_panel = Frame(self)
        top_panel.pack(side='top', fill='x')

        open_btn = Button(top_panel, text='open', command=self.__on_open_btn)
        open_btn.pack(side='left')
        save_btn = Button(top_panel, text='save', command=self.__on_save_btn)
        save_btn.pack(side='left')

        key_entry = Entry(top_panel, textvariable=self.__key_var)
        key_entry.pack(side='left', padx=8, pady=8)

        text = Text(
            self,
            width=60,
            height=20,
            font=('Segoe UI', 14),
            bg='#f5f5f5',
            fg='#1a1a1a',
            padx=10,
            pady=10,
            wrap='word',
            spacing1=4,
            spacing2=2,
            spacing3=4
        )
        text.pack(fill='both', expand=True)

        self.mainloop()

    def __on_open_btn(self):
        pass

    def __on_save_btn(self):
        pass


if __name__ == '__main__':
    MainWindow()
