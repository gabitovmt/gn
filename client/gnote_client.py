import json
import sys
from tkinter import Tk, Entry, StringVar
from typing import Any

import requests
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


class NoteClient:

    def __init__(self, server_url: str, crypto_service: CryptoService):
        self.__server_url = server_url + '/request'
        self.__crypto_service = crypto_service

    def get_one(self, uid: int) -> dict[str, Any]:
        pass

    def get_all(self) -> list[dict[str, Any]]:
        return self.__post('get_all')

    def post(self, note: dict[str, Any]) -> int:
        pass

    def put(self, note: dict[str, Any]) -> None:
        pass

    def delete(self, uid: int) -> None:
        pass

    def __post(self, action: str):
        request = {
            'object': 'note',
            'action': action,
        }
        encrypted_request = self.__crypto_service.encrypt(request)
        response = requests.post(self.__server_url, data=encrypted_request)
        print(response)


def main():
    props = load_properties()

    if 'key' not in props:
        key = enter_password()
        if not key:
            sys.exit(1)
        props['key'] = key

    crypto_service = CryptoService(props['key'])
    note_client = NoteClient(props['server_url'], crypto_service)

    print(note_client.get_all())


if __name__ == '__main__':
    main()
