import sqlite3
from typing import Annotated, Any
from cryptography.fernet import Fernet
from fastapi import FastAPI, Response, HTTPException, File
from fastapi.responses import FileResponse
import json

# Запуск сервера uvicorn main:app --reload
app = FastAPI()


@app.get('/')
def read_root():
    return FileResponse('public/index.html')


@app.get('/favicon.ico')
def read_favicon_ico():
    return FileResponse('public/favicon.ico')


@app.get('/favicon-16x16.png')
def read_favicon_ico():
    return FileResponse('public/favicon-16x16.png')


@app.get('/favicon-32x32.png')
def read_favicon_ico():
    return FileResponse('public/favicon-32x32.png')


@app.post('/request')
def run(file: Annotated[bytes, File()], response: Response):
    if file is None:
        raise HTTPException(status_code=400, detail='no request body')

    try:
        data = crypto_service.decrypt(file)
    except BaseException:
        raise HTTPException(status_code=400, detail='no valid data')

    print(data)

    response.status_code = 202
    return crypto_service.encrypt(data)


class NoteRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.__con = connection

        self.__cursor.execute('''
                              CREATE TABLE IF NOT EXISTS notes
                              (
                                  id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                  name TEXT    NOT NULL,
                                  ord  INTEGER NOT NULL,
                                  text TEXT    NOT NULL
                              )
                              ''')

    @property
    def __cursor(self) -> sqlite3.Cursor:
        return self.__con.cursor()

    def __commit(self):
        self.__con.commit()

    def get_one(self, uid: int) -> dict[str, Any]:
        sql = 'SELECT id, name, ord, text FROM notes WHERE id = ?'
        result = self.__cursor.execute(sql, (uid,)).fetchone()

        return NoteRepository.__map(result)

    def get_all(self) -> list[dict[str, Any]]:
        sql = 'SELECT id, name, ord, text FROM notes'
        result = self.__cursor.execute(sql).fetchall()

        return [NoteRepository.__map(record) for record in result]

    def save(self, note: dict[str, Any]) -> int:
        if 'id' in note:
            sql = 'UPDATE notes SET name = :name, ord = :ord, text = :text WHERE id = :id'
            self.__cursor.execute(sql, note)
            self.__commit()

            return note['id']
        else:
            sql = 'INSERT INTO notes(name, ord, text) VALUES (:name, :ord, :text)'
            cursor = self.__cursor
            cursor.execute(sql, note)
            last_id = cursor.lastrowid
            self.__commit()

            return last_id

    def delete(self, uid: int) -> None:
        sql = 'DELETE FROM notes WHERE id = ?'
        self.__cursor.execute(sql, (uid,))
        self.__commit()

    @staticmethod
    def __map(record: tuple[Any, ...]) -> dict[str, Any]:
        return {
            'id': record[0],
            'name': record[1],
            'ord': record[2],
            'text': record[3]
        }


class CryptoService:

    def __init__(self, key_filename: str):
        with open(key_filename) as f:
            key = f.read().rstrip()
            self.__cipher_suite = Fernet(key)

    def decrypt(self, data):
        return json.loads(self.__cipher_suite.decrypt(data).decode('utf-8'))

    def encrypt(self, data):
        return self.__cipher_suite.encrypt(json.dumps(data).encode('utf-8'))


connect = sqlite3.connect('gnote.db')
note_repository = NoteRepository(connect)
crypto_service = CryptoService('key.txt')
