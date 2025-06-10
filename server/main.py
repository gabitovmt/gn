from typing import Annotated

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
        data = decrypt(file)
    except BaseException:
        raise HTTPException(status_code=400, detail='no valid data')

    print(data)

    response.status_code = 202
    return encrypt(data)


def decrypt(data):
    return json.loads(cipher_suite.decrypt(data).decode('utf-8'))


def encrypt(data):
    return cipher_suite.encrypt(json.dumps(data).encode('utf-8'))


with open('key.txt') as f:
    key = f.read().rstrip()
    cipher_suite = Fernet(key)
