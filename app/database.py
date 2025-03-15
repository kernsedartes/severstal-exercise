from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://fastapi:1234@localhost:5432/metal_rolls"

# Создаем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()