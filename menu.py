import cryptography # 이 라이브러리가 없으면 오류 발생

from fastapi import APIRouter, Depends, status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import *
from models import *

from sqlalchemy.orm import Session

import os

templates = Jinja2Templates(directory="templates")

menus = APIRouter(prefix='/menu')
menus.mount("/static", StaticFiles(directory="static"), name="static")
engine = engineconn()

cart: List[Cart_list] = []

def get_db():
    session = engine.session_maker()
    try:
        yield session
    finally:
        session.close()
    
@menus.get("/", response_model=List[Cart_list], tags=['menus'])
async def menu(request: Request, db: Session = Depends(get_db)):

    path="./static/img/"
    img_list = os.listdir(path)

    img_nm_list = []

    for i in img_list:
        img_nm_list.append(i.split(".")[0])

    dt_coffee = db.query(Menu).filter(Menu.category == "커피").order_by(Menu.menu_id)
    dt_tea = db.query(Menu).filter(Menu.category == "티").order_by(Menu.menu_id)
    dt_drink = db.query(Menu).filter(Menu.category == "음료").order_by(Menu.menu_id)
    dt_dessert = db.query(Menu).filter(Menu.category == "디저트").order_by(Menu.menu_id)

    return templates.TemplateResponse("menu.html", {"request":request, "dt_coffee": dt_coffee, "dt_tea": dt_tea, "dt_drink": dt_drink, "dt_dessert": dt_dessert, "cart_list": cart, "img_nm_list": img_nm_list})

@menus.get("/info/{menu_id}", response_model=List[Cart_list], tags=['menus'])
async def notice(request: Request, menu_id: int, db: Session = Depends(get_db)):

    path="./static/img/"
    img_list = os.listdir(path)

    img_nm_list = []

    for i in img_list:
        img_nm_list.append(i.split(".")[0])

    crn_info = db.query(Menu).filter(Menu.menu_id == menu_id).first() # current_information
    dt_info = db.query(Menu).order_by(Menu.menu_id)
    return templates.TemplateResponse("notice.html", {"request": request, "dt_info": dt_info, "crn_info": crn_info, "img_nm_list":img_nm_list})

@menus.get("/cart/add/{menu_nm}", tags=['menus'])
async def add_cart(request: Request, menu_nm: str):
    cart.append(menu_nm)
    return RedirectResponse(url=menus.url_path_for("menu"), status_code=status.HTTP_303_SEE_OTHER)

@menus.delete("/cart/delete/")
async def remove_cart():
    cart.clear()
    return {"msg": "Cart Cleared"}