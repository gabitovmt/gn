from tkinter import Tk, Button, Frame, Entry, StringVar, Text

def main():
    root = Tk()
    root.geometry("640x480")

    top_panel = Frame(root)
    top_panel.pack(side='top', fill='x')

    open_btn = Button(top_panel, text='open')
    open_btn.pack(side='left')
    save_btn = Button(top_panel, text='save')
    save_btn.pack(side='left')

    note_key = StringVar()
    not_key_entry = Entry(top_panel, textvariable=note_key)
    not_key_entry.pack(side='left')

    text = Text(
        root,
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

    root.mainloop()


if __name__ == '__main__':
    main()
