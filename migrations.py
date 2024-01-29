from database import engine
from database import Base

# Очистка базы данных
# Base.metadata.drop_all(engine)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)
