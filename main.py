import cryptography # 이 라이브러리가 없으면 오류 발생

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from admin import *
from menu import *

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(admin)
app.include_router(menus)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request":request})
