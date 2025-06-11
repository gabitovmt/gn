import json
import sqlite3
from typing import Annotated, Any

from cryptography.fernet import Fernet
from fastapi import FastAPI, Response, HTTPException, File
from fastapi.responses import FileResponse

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
        req = crypto_service.decrypt(file)
    except BaseException:
        raise HTTPException(status_code=400, detail='invalid request')

    if 'object' not in req and 'action' not in req:
        raise HTTPException(status_code=400, detail='invalid request')

    resp = None
    if req['object'] == 'note':
        if req['action'] == 'get_all':
            resp = note_service.get_all()
        elif req['action'] == 'get_one':
            resp = note_service.get_one(req['args']['id'])
        elif req['action'] == 'post':
            resp = note_service.post(req['args'])
            response.status_code = 201
        elif req['action'] == 'put':
            note_service.put(req['args'])
            response.status_code = 202
        elif req['action'] == 'delete':
            note_service.delete(req['args']['id'])
            response.status_code = 204
        else:
            raise HTTPException(status_code=400, detail='invalid request')
    else:
        raise HTTPException(status_code=400, detail='invalid request')

    if resp is None:
        return None

    return crypto_service.encrypt(resp)


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


class NoteService:

    def __init__(self, note_repo: NoteRepository):
        self.__note_repo = note_repo

    def get_one(self, uid: int) -> dict[str, Any]:
        return self.__note_repo.get_one(uid)

    def get_all(self) -> list[dict[str, Any]]:
        return self.__note_repo.get_all()

    def post(self, note: dict[str, Any]) -> int:
        return self.__note_repo.save(note)

    def put(self, note: dict[str, Any]) -> None:
        self.__note_repo.save(note)

    def delete(self, uid: int) -> None:
        self.__note_repo.delete(uid)


connect = sqlite3.connect('gnote.db')
note_repository = NoteRepository(connect)
note_service = NoteService(note_repository)
crypto_service = CryptoService('key.txt')
