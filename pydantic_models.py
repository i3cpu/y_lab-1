from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

class SubmenuCreate(BaseModel):
    title: str
    description: str
    dishes_count: int = 0

class DishCreate(BaseModel):
    title: str
    description: str
    price: float = 0