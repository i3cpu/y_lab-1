from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine
import uuid

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String(255))
    description = Column(String(255))
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)
    submenus = relationship("Submenu", backref="menu", cascade="all, delete-orphan")


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String(255))
    description = Column(String(255))
    dishes_count = Column(Integer, default=0)
    menu_id = Column(String, ForeignKey('menu.id'))
    dishes = relationship("Dish", backref="submenu", cascade="all, delete-orphan")


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String(255))
    description = Column(String(255))
    price = Column(Float)
    submenu_id = Column(String, ForeignKey('submenu.id'))


# # очистка бд

Base.metadata.drop_all(engine)
# создание таблиц в бд
Base.metadata.create_all(engine)
