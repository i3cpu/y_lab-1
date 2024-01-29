from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)


@pytest.fixture
def get_menu_id():
    response = client.get(
        f"/api/v1/menus",
    )
    menu_id = response.json()[0]["id"]
    return menu_id

@pytest.fixture
def get_submenu_id(get_menu_id):
    menu_id = get_menu_id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus"
    )
    print(response.json(), "-----------")
    submenu_id = response.json()[0]["id"]
    return submenu_id

@pytest.fixture
def get_dish_id(get_menu_id, get_submenu_id):
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
    )
    dish_id = response.json()[0]["id"]
    return dish_id


#  - - CREATE - -

def test_create_menu():
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
    assert response.status_code == 201
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }


def test_create_submenu(get_menu_id):
    menu_id= get_menu_id
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
    assert response.status_code == 201
    assert response.json() == {
            "id":submenu_id,
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 0
        }

def test_create_dish(get_submenu_id, get_menu_id):
    menu_id= get_menu_id
    submenu_id= get_submenu_id
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        },
    )  
    assert response.status_code == 201
    dish_id = response.json()["id"]
    assert response.json() == {
        "id": dish_id,
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.5"
    }



# - - GET - - 
    
def test_get_menu_by_id(get_menu_id):
    menu_id = get_menu_id
    response = client.get(
        f"/api/v1/menus/{menu_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 1,
        "dishes_count": 1
    }


def test_get_submenu_by_id(get_menu_id, get_submenu_id ):
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
            "id":submenu_id,
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 1
        }
    
def test_get_dish_by_id(get_dish_id, get_menu_id,get_submenu_id):
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    dish_id = get_dish_id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": dish_id,
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.5"
    }

    
#  - - UPDATE - -
    
def test_update_menu(get_menu_id):
    menu_id = get_menu_id
    response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "id": menu_id,
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
            "submenus_count": 0,
            "dishes_count": 0
        }
    )
    assert response.status_code == 200

def test_update_submenu(get_menu_id,get_submenu_id):
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
            "dishes_count": 0
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": submenu_id,
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
        "dishes_count": 0
        }

def test_update_dish(get_dish_id, get_submenu_id,get_menu_id):
    dish_id = get_dish_id
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json={
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.5"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
            "id":dish_id, 
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.5"
        }


#  - - DELETE - - 
    
def test_delete_dish(get_menu_id, get_submenu_id, get_dish_id):
    dish_id = get_dish_id
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": 'true',
        "message": "The dish has been deleted"
    }


def test_delete_submenu(get_menu_id, get_submenu_id):
    menu_id = get_menu_id
    submenu_id = get_submenu_id
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": 'true',
        "message": "The submenu has been deleted"
    }

def test_delete_menu(get_menu_id):
    menu_id = get_menu_id
    response = client.delete(
        f"/api/v1/menus/{menu_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": 'true',
        "message": "The menu has been deleted"
    }


#  - - NOT FOUND - -
    
def test_menu_not_found():
    menu_id = "a2eb416c-2245-4526-bb4b-6343d5c5016f",
    response = client.get(
        f"/api/v1/menus/{menu_id}",
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "menu not found"
    }

def test_submenu_not_found():
    menu_id = "a2eb416c-2245-4526-bb4b-6343d5c5016f"
    submenu_id = "bc19488a-cc0e-4eaa-8d21-4d486a45392f"
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}"
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "submenu not found"
    }

def test_dish_not_found():
    menu_id = "a2eb416c-2245-4526-bb4b-6343d5c5016f"
    submenu_id = "bc19488a-cc0e-4eaa-8d21-4d486a45392f"
    dish_id = "602033b3-0462-4de1-a2f8-d8494795e0c0"
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "dish not found"
    }