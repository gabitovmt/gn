import sys
from tkinter import Tk, Entry, StringVar
import json

from cryptography.fernet import Fernet


class CryptoService:

    def __init__(self, key: str):
        self.__cipher_suite = Fernet(key)

    def decrypt(self, data):
        return json.loads(self.__cipher_suite.decrypt(data).decode('utf-8'))

    def encrypt(self, data):
        return self.__cipher_suite.encrypt(json.dumps(data).encode('utf-8'))


def load_properties() -> dict[str, str]:
    d = {}
    with open('application.properties') as f:
        for line in f:
            if '=' not in line:
                continue
            key, value = line.rstrip().split('=', maxsplit=1)
            d[key] = value

    return d

def enter_password() -> str:
    tk = Tk()

    tk.title('Gnote')
    tk.geometry('300x32')
    tk.resizable(False, False)
    tk.iconbitmap(default='favicon.ico')

    value = StringVar()
    entry = Entry(tk, textvariable=value)
    entry.pack(fill='x', padx=8, pady=8)
    entry.focus()
    entry.bind('<Return>', lambda e: tk.destroy())

    tk.mainloop()

    return value.get()


def main():
    props = load_properties()

    if 'key' not in props:
        key = enter_password()
        if not key:
            sys.exit(1)
        props['key'] = key

    crypto_service = CryptoService(props['key'])

    print(props)


if __name__ == '__main__':
    main()
