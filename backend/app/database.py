"""Configuración de la base de datos SQLite con SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Motor de SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Necesario para SQLite con FastAPI
)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


def get_db():
    """Dependency para inyectar sesión de base de datos en los endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea todas las tablas si no existen."""
    Base.metadata.create_all(bind=engine)
