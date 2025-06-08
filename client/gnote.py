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
        self.__is_modified = False

        self.geometry("640x480")

        self.__top_panel = Frame(self)
        self.__top_panel.pack(side='top', fill='x')

        self.__open_btn = Button(self.__top_panel, text='open', command=self.__on_open_btn)
        self.__open_btn.pack(side='left')
        self.__save_btn = Button(self.__top_panel, text='save', command=self.__on_save_btn, state='disabled')
        self.__save_btn.pack(side='left')

        self.__key_entry = Entry(self.__top_panel, textvariable=self.__key_var)
        self.__key_entry.pack(side='left', padx=8, pady=8)

        self.__editor = Text(
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
            spacing3=4,
            state='disabled'
        )
        self.__editor.pack(fill='both', expand=True)
        self.__editor.bind('<<Modified>>', lambda e: self.__on_modified())

        self.mainloop()

    def __on_open_btn(self):
        self.__editor.config(state='normal')
        self.__editor_text = open_text()
        self.__on_not_modified()

    def __on_save_btn(self):
        save_text(self.__editor_text)

    def __on_not_modified(self):
        self.__is_modified = False
        self.__save_btn.config(state='disabled')

    def __on_modified(self):
        if self.__is_modified:
            return
        self.__is_modified = True
        self.__save_btn.config(state='normal')

    @property
    def __editor_text(self):
        return self.__editor.get('1.0', 'end').rstrip()

    @__editor_text.setter
    def __editor_text(self, text):
        self.__editor.delete('1.0', 'end')
        self.__editor.insert('1.0', text)


if __name__ == '__main__':
    MainWindow()
