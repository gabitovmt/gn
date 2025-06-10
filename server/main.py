from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse("public/index.html")

@app.get("/favicon.ico")
def read_favicon_ico():
    return FileResponse("public/favicon.ico")

@app.get("/favicon-16x16.png")
def read_favicon_ico():
    return FileResponse("public/favicon-16x16.png")

@app.get("/favicon-32x32.png")
def read_favicon_ico():
    return FileResponse("public/favicon-32x32.png")