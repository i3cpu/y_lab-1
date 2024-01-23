import uuid
from fastapi import FastAPI, HTTPException
from database import Session
from sqlalchemy import func


from models import Menu, Dish, Submenu
from pydantic_models import MenuCreate,SubmenuCreate, DishCreate


app = FastAPI()

@app.get("/api/v1/menus")
def get_menus():
    session = Session()
    menus = session.query(Menu).all()
    return menus

@app.post("/api/v1/menus", status_code=201)
def create_menu(menu: MenuCreate):
    session = Session()
    menu = Menu(id=str(uuid.uuid4()) ,title=menu.title, description=menu.description, submenus_count=menu.submenus_count, dishes_count=menu.dishes_count)
    session.add(menu)
    session.commit()
    return {
        "id": menu.id,
        "title": menu.title,
        "description": menu.description,
        "submenus_count": menu.submenus_count,
        "dishes_count": menu.dishes_count
    }
 
@app.get("/api/v1/menus/{api_test_menu_id}")
def get_menu_by_id(api_test_menu_id: str):
    session = Session()
    menu = session.query(Menu).filter_by(id=api_test_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    submenus_count = session.query(func.count(Submenu.id)).filter(Submenu.menu_id == api_test_menu_id).scalar()
    dishes_count = session.query(func.count(Dish.id)).join(Submenu).filter(Submenu.menu_id == api_test_menu_id).scalar()

    return {
        "id": menu.id,
        "title": menu.title,
        "description": menu.description,
        "submenus_count": submenus_count,
        "dishes_count": dishes_count
    }


@app.delete("/api/v1/menus/{api_test_menu_id}")
def delete_menu(api_test_menu_id: str):
    session = Session()
    print(api_test_menu_id,"--------------")
    menu = session.query(Menu).filter_by(id=api_test_menu_id).first()
    session.delete(menu)
    session.commit()

    return {
        "status": 'true',
        "message": "The menu has been deleted"
    }

@app.patch("/api/v1/menus/{api_test_menu_id}")
def update_menu(api_test_menu_id: str, menu: MenuCreate):
    session = Session()
    menu_to_update = session.query(Menu).filter_by(id=api_test_menu_id).first()

    if menu_to_update:
        menu_to_update.title = menu.title
        menu_to_update.description = menu.description
        menu_to_update.submenus_count = menu.submenus_count
        menu_to_update.dishes_count = menu.dishes_count
        session.commit()
        return {
            "id": menu_to_update.id,
            "title": menu_to_update.title,
            "description": menu_to_update.description,
            "submenus_count": menu_to_update.submenus_count,
            "dishes_count": menu_to_update.dishes_count
        }
    else:
        raise HTTPException(status_code=404, detail="menu not found")

    


@app.get("/api/v1/menus/{api_test_menu_id}/submenus")
def get_submenus(api_test_menu_id: str):
    session = Session()
    submenu = session.query(Submenu).filter(Submenu.menu_id == api_test_menu_id).all()
    return submenu

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def get_submenu_by_id(api_test_menu_id: str, api_test_submenu_id: str):
    session = Session()
    submenu = session.query(Submenu).filter_by(id=api_test_submenu_id, menu_id=api_test_menu_id).first()
    
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    dishes_count = session.query(func.count(Dish.id)).filter(Dish.submenu_id == api_test_submenu_id).scalar()

    return {
        "id": submenu.id,
        "title": submenu.title,
        "description": submenu.description,
        "dishes_count": dishes_count
    }

@app.post("/api/v1/menus/{api_test_menu_id}/submenus", status_code=201)
def create_submenu(submenu: SubmenuCreate, api_test_menu_id: str):
    session = Session()
    submenu = Submenu(id=str(uuid.uuid4()), title=submenu.title, description=submenu.description, dishes_count=submenu.dishes_count, menu_id=api_test_menu_id)
    session.add(submenu)
    session.commit()
    return {
        "id": submenu.id,
        "title": submenu.title,
        "description": submenu.description,
        "dishes_count": submenu.dishes_count
    }


@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def update_submenu(api_test_menu_id: str, api_test_submenu_id:str, submenu: SubmenuCreate):
    session = Session()
    submenu_to_update = session.query(Submenu).filter_by(id=api_test_submenu_id, menu_id=api_test_menu_id).first()

    if submenu_to_update:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        submenu_to_update.dishes_count = submenu.dishes_count
        session.commit()
        return {
            "id": submenu_to_update.id,
            "title": submenu_to_update.title,
            "description": submenu_to_update.description,
            "dishes_count": submenu_to_update.dishes_count
        }
    else:
        raise HTTPException(status_code=404, detail="menu not found")
    
@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def delete_submenu(api_test_menu_id: str, api_test_submenu_id:str):
    session = Session()
    submenu = session.query(Submenu).filter_by(id=api_test_submenu_id, menu_id=api_test_menu_id).first()
    session.delete(submenu)
    session.commit()
    return {
        "status": "true",
        "message": "The submenu has been deleted"
        }



@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes")
def get_dishes(api_test_menu_id: str, api_test_submenu_id: str ):
    session = Session()
    dish = session.query(Dish).filter(Dish.submenu_id == api_test_submenu_id, Submenu.menu_id==api_test_menu_id).all()
    return dish

@app.post("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes", status_code=201)
def create_dish(dish: DishCreate, api_test_menu_id: str, api_test_submenu_id: str):
    session = Session()
    dish = Dish(id=str(uuid.uuid4()) ,title=dish.title, description=dish.description, price=dish.price, submenu_id=api_test_submenu_id)
    session.add(dish)
    session.commit()
    return {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": str(dish.price)
        }

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def get_dish_by_id(api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str):
    session = Session()
    dish = session.query(Dish).filter_by(id=api_test_dish_id, submenu_id=api_test_submenu_id).first()

    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": str(dish.price)
        }

@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def update_dish(api_test_dish_id: str, api_test_submenu_id:str, dish: DishCreate):
    session = Session()
    dish_to_update = session.query(Dish).filter_by(id=api_test_dish_id, submenu_id=api_test_submenu_id).first()

    if dish_to_update:
        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = dish.price
        session.commit()
        return {
            "id": dish_to_update.id,
            "title": dish_to_update.title,
            "description": dish_to_update.description,
            "price": str(dish_to_update.price)
        }
    else:
        raise HTTPException(status_code=404, detail="dish not found")

@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def delete_dish(api_test_dish_id: str, api_test_submenu_id: str):
    session = Session()
    dish = session.query(Dish).filter_by(id=api_test_dish_id, submenu_id=api_test_submenu_id).first()
    session.delete(dish)
    session.commit()

    return {
        "status": "true",
        "message": "The dish has been deleted"
        }
