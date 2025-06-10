from typing import Annotated

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

    response.status_code = 202
    return file
'''
from cryptography.fernet import Fernet

# Генерация ключа
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Шифрование данных
data = b'Hello, Python!'
encrypted_data = cipher_suite.encrypt(data)

# Дешифрование данных
decrypted_data = cipher_suite.decrypt(encrypted_data)

print(encrypted_data)
print(decrypted_data)
'''