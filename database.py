from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
