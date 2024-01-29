import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Глобальная переменная для хранения ID
created_menu_id = None
created_submenu_id = None
created_dish_id_1 = None
created_dish_id_2 = None


def test_create_menu():
    global created_menu_id
    response = client.post(
        "/api/v1/menus",
        json={
            "title": "My menu 1",
            "description": "My menu description 1",
            "submenus_count": 0,
            "dishes_count": 0
        },
    )  
    menu_id = response.json()["id"]
    created_menu_id = menu_id
    assert response.status_code == 201
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }


def test_create_submenu():
    global created_menu_id
    global created_submenu_id
    menu_id= created_menu_id
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 0,
            "menu_id":menu_id
        },
    )  
    submenu_id = response.json()["id"]
    created_submenu_id=submenu_id
    assert response.status_code == 201
    assert response.json() == {
            "id":submenu_id,
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 0
        }


def test_create_dish_1():
    global created_menu_id
    global created_submenu_id
    global created_dish_id_1
    menu_id = created_menu_id
    submenu_id = created_submenu_id

    # Создаем первое блюдо
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        },
    )
    dish_id_1 = response.json()["id"]
    created_dish_id_1 = dish_id_1

    assert response.status_code == 201
    assert response.json() == {
        "id": dish_id_1,
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.5"
    }

def test_create_dish_2():
    global created_menu_id
    global created_submenu_id
    global created_dish_id_2
    menu_id = created_menu_id
    submenu_id = created_submenu_id

    # Создаем второе блюдо
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": 15.75
        },
    )
    dish_id_2 = response.json()["id"]
    created_dish_id_2 = dish_id_2
    assert response.status_code == 201
    assert response.json() == {
        "id": dish_id_2,
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "15.75"
    }


def test_get_menu_by_id_1():
    global created_menu_id

    menu_id = created_menu_id
    print(created_menu_id)
    response = client.get(
        f"/api/v1/menus/{menu_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 1,
        "dishes_count": 2
    }

def test_get_submenu_by_id():
    global created_menu_id
    global created_submenu_id
    menu_id = created_menu_id
    submenu_id = created_submenu_id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
            "id":submenu_id,
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 2
        }
    
def test_delete_submenu():
    global created_menu_id
    global created_submenu_id
    menu_id = created_menu_id
    submenu_id = created_submenu_id
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": 'true',
        "message": "The submenu has been deleted"
    }

def test_get_submenus():
    global created_menu_id
    global created_submenu_id
    menu_id = created_menu_id
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert not response.json()


def test_get_dishes():
    global created_dish_id_1
    global created_dish_id_2
    global created_menu_id
    global created_submenu_id
    menu_id = created_menu_id
    submenu_id = created_submenu_id
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    # print(response.json(), )
    assert response.status_code == 200
    assert not response.json()


def test_get_menu_by_id_2():
    global created_menu_id
    menu_id = created_menu_id
    print(created_menu_id)
    response = client.get(
        f"/api/v1/menus/{menu_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }


def test_delete_menu():
    global created_menu_id
    menu_id = created_menu_id
    response = client.delete(
        f"/api/v1/menus/{menu_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": 'true',
        "message": "The menu has been deleted"
    }


def test_get_menus():
    response = client.get(
        "/api/v1/menus"
    )
    assert response.status_code == 200
    assert not response.json()